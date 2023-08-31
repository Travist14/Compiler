import argparse

# from tokenizer import tokenize, print_tokens
from tokenizer import tokenize, print_tokens

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='the file to be compiled')
    parser.add_argument('-t', '--tokenize', help='tokenize the file', action='store_true')
    args = parser.parse_args()

    if not args.file.endswith('.c'):
        raise ValueError('The input file must be a .c file')
    
    with open(args.file, 'r') as f:
        text = f.read()
    assert type(text) == str, "Input text from the file should be a string"
    
    if args.tokenize:
        tokens = tokenize(text)
        assert type(tokens) == list, "tokens should in the form of a list"
        print_tokens(tokens)
    
if __name__ == '__main__':
    main()
