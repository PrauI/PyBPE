from pybpe import Tokenizer

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
    
    # Initialize the tokenizer
    tk = Tokenizer()

    # Generate tokens
    tk.generate_tokens(SOURCE_FILE, 812, TOKEN_FILE, DELIMITER)

    # after token generation the tokenizer can be initialized with the already 
    # existing list of tokens
    # tk = Tokenizer(TOKEN_FILE, DELIMITER)

    # if you want to read an existing list of tokens:
    # tokens = tk.read_tokens(TOKEN_FILE, DELIMITER)

    # encode / tokenize a string
    encoded = tk.encode(TEST_STRING)
    print(f"'{TEST_STRING}' \nmaps to: {encoded}")

    # decode a list of tokens
    decoded = tk.decode(encoded)
    print(f"{encoded} maps to:\n'{decoded}'")

    



main()
