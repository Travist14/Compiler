import argparse

from tokenizer import tokenize, print_tokens
# from Parser import parse, print_parse_tree
from new_parser import parse, print_parse_tree

def read_file(filename):
    with open(filename, 'r') as f:
        text = f.read()

    return text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='the file to be compiled')
    parser.add_argument('-t', '--tokenize', help='tokenize the file', action='store_true')
    parser.add_argument("-p", "--parse", help="parse the file", action="store_true")
    args = parser.parse_args()

    if not args.file.endswith('.c'):
        raise ValueError('The input file must be a .c file')
    
    if args.tokenize:
        text = read_file(args.file)
        tokens = tokenize(text)
        assert type(tokens) == list, "tokens should in the form of a list"
        print_tokens(tokens)
    elif args.parse:
        text = read_file(args.file)
        tree = parse(text, args.file, DEBUG=True) # Debug here will print tokens along with parse tree
        if tree is not None:
            print("-" * 60)
            print("\n\tParse Tree:")
            print(tree)
            print("\n")

if __name__ == '__main__':
    main()
