import argparse

from tokenizer import tokenize, print_tokens

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='the file to be compiled')
    parser.add_argument('-t', '--tokenize', help='tokenize the file', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        text = f.read()
    assert type(text) == str, "text should be a string"
    
    if args.tokenize:
        tokens = tokenize(text)
        assert type(tokens) == list, "tokens should in the form of a list"
        print_tokens(tokens)
    
if __name__ == '__main__':
    main()
