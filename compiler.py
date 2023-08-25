import argparse

from tokenizer import Tokenizer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='the file to be compiled')
    parser.add_argument('-t', '--tokenize', help='tokenize the file', action='store_true')
    args = parser.parse_args()


    # open the file and read the contents as a string
    with open(args.file, 'r') as f:
        text = f.read()
    assert type(text) == str, "text should be a string"
    
    if args.tokenize:
        tokenizer = Tokenizer(text)
        tokens = tokenizer.tokenize()

        print(tokens)

if __name__ == '__main__':
    main()
