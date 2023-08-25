import argparse

from tokenizer import Tokenizer

def main():
    # accept a c file as an argument as well as the -t flag that tokenizes the file
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='the file to be compiled')
    parser.add_argument('-t', '--tokenize', help='tokenize the file', action='store_true')
    args = parser.parse_args()


    # open the file and read the contents as a string
    with open(args.file, 'r') as f:
        text = f.read()
    assert type(text) == str, "text should be a string"
    
    # tokenize the file if the -t flag is passed
    if args.tokenize:
        tokenizer = Tokenizer(text)
        print(tokenizer.tokens)


if __name__ == '__main__':
    main()
