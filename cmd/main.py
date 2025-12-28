import ctypes
import os

# Load the shared library
lib_path = os.path.abspath("../bin/bpe.so")
lib = ctypes.CDLL(lib_path)

lib.GenerateTokens.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
lib.GenerateTokens.restype = ctypes.c_int

def generate_tokens(input_file:str, output_file:str, max_n_tokens:int) -> int:
    return lib.GenerateTokens(input_file.encode('utf-8'), output_file.encode('utf-8'), max_n_tokens)

generate_tokens("../new-tokens.txt", "newer-tokens.txt", 12)
