from pybpe import *

import urllib.request
import os


SOURCE_URL = "https://www.gutenberg.org/cache/epub/1727/pg1727.txt"
SOURCE_FILE = "homer.txt"
TOKEN_FILE = "tokens.txt"
VOCAB_SIZE = 812
DELIMITER = '@@'
TEST_STRING = "Hateful to me as the gates of Hades is that man who hides one thing in his heart and speaks another"

if not os.path.exists(SOURCE_FILE):
    print(f"Downloading sample text from {SOURCE_URL}...")

    try:
        with urllib.request.urlopen(SOURCE_URL) as response:
            text = response.read().decode('utf-8')
            with open(SOURCE_FILE, "w", encoding="utf-8") as f:
                    f.write(text)
        print("Download complete.")
    except Exception as e:
        print(f"Error downloading file: {e}")
        exit(1)
else:
    print(f"Using existing file: {SOURCE_FILE}")

def main():
    
    # GenerateTokens takes a text file as input and saves the tokens in 
    # a new text file.
    # Tokens are seperated by a delimiter
    GenerateTokens(SOURCE_FILE, TOKEN_FILE, VOCAB_SIZE, DELIMITER)

    # Load the tokens from the File for further usage
    tokens = ReadTokens(TOKEN_FILE, DELIMITER)
    print(f"{len(tokens)} Tokens loaded succesfully:\n...\n{tokens[600:700]}\n...\n")

    # Encode or tokenize a string, given some tokens
    encoded = Encode(TEST_STRING, tokens)
    # Encode returns a list of indices referring to the the Tokens
    # provided to the function
    print(f"'{TEST_STRING}' maps to {encoded}")
    print(f"Test string has length: {len(TEST_STRING)}\nEncoded has length: {len(encoded)}")

    # Decode a tokenized string
    decoded = Decode(encoded, tokens)
    print(f"{encoded} maps to '{decoded}'")



main()
