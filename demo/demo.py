from pybpe import *

GenerateTokens("../README.md", "readmetokens", 14)
tokens = ReadTokens("readmetokens")
print(tokens)
