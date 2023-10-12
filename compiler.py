import argparse

from tokenizer import tokenize, print_tokens
from my_parser import parse, print_parse_tree, print_symbol_table
from ir import convert_to_ir

def read_file(filename):
    with open(filename, 'r') as f:
        text = f.read()

    return text

def check_valid_file(filename):
    if not filename.endswith('.c'):
        raise ValueError('The input file must be a .c file')

def setup_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='the file to be compiled')
    parser.add_argument('-t', '--tokenize', help='tokenize the file', action='store_true')
    parser.add_argument("-p", "--parse", help="parse the file", action="store_true")
    parser.add_argument("-i", "--intermediate-representation", help="generate three address code", action="store_true")
    args = parser.parse_args()
    return args

def main():

    args = setup_arg_parser()
    
    check_valid_file(args.file)
    
    text = read_file(args.file)
    tokens = tokenize(text)
    if type(tokens) != list:
        raise ValueError("Tokenize function must return a list of tokens")

    if args.tokenize:
        print_tokens(tokens)

    tree, state = parse(tokens, args.file) # state is needed here for symbol table, returning the entire state object becuase might need other info later
    if args.parse:
        print_parse_tree(tree)
        print_symbol_table(state)

    if args.intermediate_representation:
        convert_to_ir(tree, state.symbol_table)
        

if __name__ == '__main__':
    main()
