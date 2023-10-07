import sys
from dataclasses import dataclass
import colorama

from tokenizer import tokenize

index = 0
errors = []
symbol_table = []

@dataclass
class Symbol:
    type: str
    value: str
    scope: str

class ParseError(Exception):
    def __init__(self, message, token):
        self.message = message
        self.token = token
        super().__init__(self.message, self.token)

    def __str__(self):
        return f"{self.message} at {self.token}"
    

# heavily inspired by the parse tree that we went over in class 
def parse_expression(tokens):
    global symbol_table
    global index
    global errors

    f = {"children": [], "value": None}
    f["value"] = "EXPR"

    term = parse_term(tokens)
    if term:
        f["children"].append(term)
    else:
        errors.append(ParseError("Expected term", tokens[index]))

    while index < len(tokens) and tokens[index].type == "OP" and tokens[index].value in ["+", "-"]:
        f["value"] = tokens[index].value
        index += 1

        t = parse_expression(tokens)
        if t:
            f["children"].append(t)
        else:
            errors.append(ParseError("Expected expression", tokens[index]))

    return f


# heavily inspired by the parse tree that we went over in class 
def parse_term(tokens):
    global symbol_table
    global index
    global errors

    f = {"children": [], "value": None}
    f["value"] = "TERM"

    factor = parse_factor(tokens)
    if factor:
        f["children"].append(factor)
    else:
        errors.append(ParseError("Expected factor", tokens[index]))

    while index < len(tokens) and tokens[index].type == "OP" and tokens[index].value in ["*", "/"]:
        f["value"] = tokens[index].value
        index += 1

        t = parse_term(tokens)
        if t:
            f["children"].append(t)
        else:
            errors.append(ParseError("Expected term", tokens[index]))

    return f


# heavily inspired by the parse tree that we went over in class 
def parse_factor(tokens):
    global symbol_table
    global index
    global errors

    f = {"children": [], "value": None}
    f["value"] = "FACTOR"

    if index < len(tokens) and (tokens[index].type == "ID" or tokens[index].type == "NUMBER"):
        f["value"] = tokens[index].value
        index += 1
    elif index < len(tokens) and tokens[index].type == "L_PAREN":
        index += 1
        expr = parse_expression(tokens)
        if expr:
            f["children"].append(expr)
        else:
            errors.append(ParseError("Expected expression", tokens[index]))

        if index < len(tokens) and tokens[index].type != "R_PAREN":
            errors.append(ParseError("Expected )", tokens[index]))
        else:
            index += 1
    else:
        errors.append(ParseError("Expected ID, NUMBER, or (", tokens[index - 1]))

    return f


# parse declaration will only parse int declarations and does not support assignment
def parse_declaration(tokens):
    global symbol_table
    global index
    global errors

    f = {"children": [], "value": "DECLARATION"}
    
    if index < len(tokens) and tokens[index].type == "int": # Only aceepting int declarations 
        f["children"].append({"value": tokens[index].type})
        index += 1
        
    else:
        errors.append(ParseError("Expected an int to be declared", tokens[index]))

    if index < len(tokens) and tokens[index].type == "ID":
        f["children"].append({"value": tokens[index].value})

        if Symbol(tokens[index - 1].type, tokens[index].value, "local") not in symbol_table:
            symbol_table.append(Symbol(tokens[index - 1].type, tokens[index].value, "local"))

        index += 1
    else:
        errors.append(ParseError("Expected an ID after declaring an int", tokens[index]))

    if index < len(tokens) and tokens[index].type == "SEMICOLON":
        index += 1
    else:
        errors.append(ParseError("Expected ';'", tokens[index]))

    return f 


def parse_assignment(tokens):
    global symbol_table
    global index
    global errors


    f = {"children": [], "value": None}
    f["value"] = "ASSIGNMENT"

    if index < len(tokens) and tokens[index].type == "ID":
        f["children"].append({"value": tokens[index].value})
        index += 1
    else:
        errors.append(ParseError("Expected an ID for assignment", tokens[index]))

    if index < len(tokens) and tokens[index].type == "ASSIGN":
        f["children"].append({"value": "="})
        index += 1
    else:
        errors.append(ParseError("Expected '=' for assignment", tokens[index]))

    expr = parse_expression(tokens)
    if expr:
        f["children"].append(expr)
    else:
        errors.append(ParseError("Expected expression for assignment", tokens[index]))

    return f


def parse_statement(tokens):
    global symbol_table
    global index
    global errors

    f = {"children": [], "value": None}
    f["value"] = "STATEMENT"
    
    if index < len(tokens) and tokens[index].type == "return" and tokens[index].value == "return":
        f["children"].append({"value": "return"})
        index += 1 
        
        expr = parse_expression(tokens)
        if expr:
            f["children"].append(expr)
        else:
            errors.append(ParseError("Expected expression", tokens[index]))

        if index < len(tokens) and tokens[index].type == "SEMICOLON":
            index += 1 
        else:
            errors.append(ParseError("Expected ';'", tokens[index]))

    elif index < len(tokens) and tokens[index].type == "int":
        declaration = parse_declaration(tokens)
        if declaration:
            f["children"].append(declaration)
        else:
            errors.append(ParseError("Expected declaration", tokens[index]))
    elif index < len(tokens) and tokens[index].type == "ID":
        assignment = parse_assignment(tokens)
        if assignment:
            f["children"].append(assignment)
        else :
            errors.append(ParseError("Expected assignment", tokens[index]))

        if index < len(tokens) and tokens[index].type == "SEMICOLON":
            index += 1
        else:
            errors.append(ParseError("Expected ';'", tokens[index]))
    else:
        errors.append(ParseError("Expected 'return' or 'int'", tokens[index]))

    return f


def parse_parameter(tokens):
    global index
    global errors
    global symbol_table
    
    f = {"children": [], "value": "PARAMETER"}
    
    if tokens[index].type == "int":
        f["children"].append({"value": tokens[index].value})
        index += 1

    if tokens[index].type == "ID":
        f["children"].append({"value": tokens[index].value})
        
        symbol_table.append(Symbol(tokens[index - 1].type, tokens[index].value, "parameter"))
        
        index += 1

    return f


def parse_parameters(tokens):
    global index
    global errors
    global symbol_table

    f = {"children": [], "value": "PARAMETERS"}

    if index < len(tokens) and tokens[index].type == "L_PAREN":
        index += 1

    while tokens[index].type != "R_PAREN":
        param = parse_parameter(tokens)
        if param:
            f["children"].append(param)
        
        if tokens[index].type == "COMMA":
            index += 1

    return f


def parse_function(tokens):
    global symbol_table
    global index
    global errors

    f = {"children": [], "value": "FUNCTION"}
    if index < len(tokens) and tokens[index].type in ["int", "void"] and tokens[index].value in ["int", "void"]: # support int and void function return types
        f["children"].append({"value": tokens[index].value})
        index += 1
    else:
        errors.append(ParseError("Expected 'int'", tokens[index]))

    if index < len(tokens) and tokens[index].type == "ID": 
        f["children"].append({"value": tokens[index].value})
        index += 1
    else:
        errors.append(ParseError("Expected function name", tokens[index]))

    if index < len(tokens) and tokens[index].type == "L_PAREN":
        index += 1
    else:
        errors.append(ParseError("Expected '('", tokens[index]))

    params = parse_parameters(tokens)
    if params:
        f["children"].append(params)

    if index < len(tokens) and tokens[index].type == "R_PAREN":
        index += 1
    else:
        errors.append(ParseError("Expected ')'", tokens[index]))

    if index < len(tokens) and tokens[index].type == "LBRACE":
        index += 1
    else:
        errors.append(ParseError("Expected '{'", tokens[index]))

    while index < len(tokens) and tokens[index].type != "RBRACE": # TODO: chnage this to support conditionals and loops
        stmt = parse_statement(tokens)
        if stmt:
            f["children"].append(stmt)

    if index < len(tokens) and tokens[index].type == "RBRACE":
        index += 1
    else:
        errors.append(ParseError("Expected '}'", tokens[index]))

    return f

# main program parser 
def parse_program(tokens):
    global symbol_table
    global index
    global errors

    f = {"children": [], "value": "PROGRAM"}

    while index < len(tokens):
        func = parse_function(tokens)
        if func:
            f["children"].append(func)

    return f


# iterates over all the errors and print them out in a nice format 
def handle_errors(filename):
    if len(errors) > 0:
        locations = []
        for error in errors:
            tok = error.token
            line_number = tok.line
            col = tok.column
            message = error.message
            locations.append((line_number, col, message))

        print(f"\n\t{colorama.Fore.YELLOW}{len(errors)} errors found in {filename}{colorama.Fore.RESET}\n")
        with open(filename, "r") as f:
            lines = f.readlines()
        for line_number, col, message in locations:
            print(f"\tLine {line_number} Column {col}:")
            line = lines[line_number - 1]
            print(f"\t\t{line}")
            print(f"\t\t{' ' * (col)}{colorama.Fore.RED}^{colorama.Fore.RESET}")
            print(f"\t{colorama.Fore.RED}{message}{colorama.Fore.RESET}\n")

        sys.exit(1) 


# main parse function, need to pass in filename for printing errors
# TODO: sure there is a better way to do this but it works for right now 
def parse(tokens, filename):
    
    tree = parse_program(tokens)
    
    handle_errors(filename)
    
    return tree

# print the parse tree in a nice format
def print_parse_tree(tree, indent=0):
    indentation = " " * indent
    print(f"{indentation}{tree['value']}")
    if 'children' in tree:
        for child in tree['children']:
            print(f"{indentation}")
            print_parse_tree(child, indent + 4)


# print the associated symbol table
def print_symbol_table():
    print("\n\nSymbol Table:")
    for symbol in symbol_table:
        print(f"\ttype:{symbol.type}, value: {symbol.value}, scope: {symbol.scope}")
    print("\n")