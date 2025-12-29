import ctypes
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))

if sys.platform == "win32":
    lib_name = "../bin/bpe.dll"
else:
    lib_name = "../bin/bpe.so"

lib_path = os.path.join(dir_path, lib_name)

try:
    _lib = ctypes.CDLL(lib_path)
except OSError:
    raise FileNotFoundError(f"Could not load the shared library at {lib_path}")

_lib.GenerateTokens.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
_lib.GenerateTokens.restype = ctypes.c_int

def GenerateTokens(input_file:str, output_file:str, max_n_tokens:int, delimiter:str = '@@') -> int:
    """Generates a list of Tokens based on input_file and saves them to output_file split by the delimitor @@"""
    return _lib.GenerateTokens(input_file.encode('utf-8'), output_file.encode('utf-8'), max_n_tokens, delimiter.encode('utf-8'))

