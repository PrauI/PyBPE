import os
import json
import ctypes
import sys

class Tokenizer:
    def __init__(self, tokenfile:str='tokens.txt', delimiter:str='@@'):

        # load library
        dir_path = os.path.dirname(os.path.realpath(__file__))
        if sys.platform == "win32":
            lib_name = "../bin/bpe.dll"
        else:
            lib_name = "../bin/bpe.so"

        lib_path = os.path.join(dir_path, lib_name)

        try:
            self._lib = ctypes.CDLL(lib_path)
        except OSError:
            raise FileNotFoundError(f"Could not load the shared library at {lib_path}")

        self._lib.GenerateTokens.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
        self._lib.GenerateTokens.restype = ctypes.c_int
        # FreeString
        self._lib.FreeString.argtypes = [ctypes.c_void_p]
        # ReadTokens
        self._lib.ReadTokens.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self._lib.ReadTokens.restype = ctypes.c_void_p
        # encode
        self._lib.Encode.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self._lib.Encode.restype = ctypes.c_void_p
        # decode
        self._lib.Decode.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self._lib.Decode.restype = ctypes.c_void_p


        self.tokenfile = tokenfile
        self.delimiter = delimiter
        if not os.path.exists(tokenfile):
            self.tokens = []
        else:
            self.tokens = self.read_tokens(tokenfile, delimiter)

        self.jsontokens = json.dumps(self.tokens)
        
    def read_tokens(self, input_file:str, delimiter:str='@@') -> [str]:
        """Reads Tokens from a file and returns them as list of strings"""
        ptr = self._lib.ReadTokens(input_file.encode('utf-8'), delimiter.encode('utf-8'))
        if not ptr:
            return []

        try:
            cstr = ctypes.cast(ptr, ctypes.c_char_p)
            jsonstr = cstr.value.decode('utf-8')
            tokens = json.loads(jsonstr)
            return tokens
        finally:
            self._lib.FreeString(ptr)

    def generate_tokens(self, sourcefile:str, vocabsize:int, outputfile:str='tokens.txt', delimiter:str='@@'):
        self._lib.GenerateTokens(sourcefile.encode('utf-8'), outputfile.encode('utf-8'), vocabsize, delimiter.encode('utf-8'))

        self.tokens = self.read_tokens(outputfile, delimiter)
        self.tokenfile = outputfile
        self.jsontokens = json.dumps(self.tokens)

    def encode(self, src:str)->[int]:
        ptr = self._lib.Encode(src.encode('utf-8'), self.jsontokens.encode('utf-8'))
        if not ptr:
            return []
        try:
            cstr = ctypes.cast(ptr, ctypes.c_char_p)
            jsonstr = cstr.value.decode('utf-8')
            encoded = json.loads(jsonstr)
            return encoded
        finally:
            self._lib.FreeString(ptr)

    def decode(self, input_tokens:[int])->str:
        jsonencoded = json.dumps(input_tokens)
        
        ptr = self._lib.Decode(jsonencoded.encode('utf-8'), self.jsontokens.encode('utf-8'))
        if not ptr:
            return []
        try:
            cstr = ctypes.cast(ptr, ctypes.c_char_p)
            decoded = cstr.value.decode('utf-8')
            return decoded
        finally:
            self._lib.FreeString(ptr)

