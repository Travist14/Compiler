import sys
from dataclasses import dataclass
import colorama


@dataclass
class RunState:
    index: int
    errors: list
    symbol_table: list


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
def parse_expression(tokens, state):

    f = {"children": [], "value": "EXPR"}

    term = parse_term(tokens, state)
    if term:
        f["children"].append(term)
    else:
        state.errors.append(ParseError("Expected term", tokens[state.index]))

    while state.index < len(tokens) and tokens[state.index].type == "OP" and tokens[state.index].value in ["+", "-"]:
        f["value"] = tokens[state.index].value
        state.index += 1

        t = parse_expression(tokens, state)
        if t:
            f["children"].append(t)
        else:
            state.errors.append(ParseError("Expected expression", tokens[state.index]))

    return f


# heavily inspired by the parse tree that we went over in class 
def parse_term(tokens, state):

    f = {"children": [], "value": "TERM"}

    factor = parse_factor(tokens, state)
    if factor:
        f["children"].append(factor)
    else:
        state.errors.append(ParseError("Expected factor", tokens[state.index]))

    while state.index < len(tokens) and tokens[state.index].type == "OP" and tokens[state.index].value in ["*", "/"]:
        f["value"] = tokens[state.index].value
        state.index += 1

        t = parse_term(tokens, state)
        if t:
            f["children"].append(t)
        else:
            state.errors.append(ParseError("Expected term", tokens[state.index]))

    return f


# heavily inspired by the parse tree that we went over in class 
def parse_factor(tokens, state):

    f = {"children": [], "value": "FACTOR"}

    if state.index < len(tokens) and (tokens[state.index].type == "ID" or tokens[state.index].type == "NUMBER"):
        f["value"] = tokens[state.index].value
        state.index += 1
    elif state.index < len(tokens) and tokens[state.index].type == "L_PAREN":
        state.index += 1
        expr = parse_expression(tokens, state)
        if expr:
            f["children"].append(expr)
        else:
            state.errors.append(ParseError("Expected expression", tokens[state.index]))

        if state.index < len(tokens) and tokens[state.index].type != "R_PAREN":
            state.errors.append(ParseError("Expected )", tokens[state.index]))
        else:
            state.index += 1
    else:
        state.errors.append(ParseError("Expected ID, NUMBER, or (", tokens[state.index - 1]))

    return f


# parse declaration will only parse int declarations and does not support assignment
def parse_declaration(tokens, state):

    f = {"children": [], "value": "DECLARATION"}
    
    if state.index < len(tokens) and tokens[state.index].type == "int": # Only aceepting int declarations 
        f["children"].append({"value": tokens[state.index].type})
        state.index += 1
        
    else:
        state.errors.append(ParseError("Expected an int to be declared", tokens[state.index]))

    if state.index < len(tokens) and tokens[state.index].type == "ID":
        f["children"].append({"value": tokens[state.index].value})

        if Symbol(tokens[state.index - 1].type, tokens[state.index].value, "local") not in state.symbol_table:
            state.symbol_table.append(Symbol(tokens[state.index - 1].type, tokens[state.index].value, "local"))

        state.index += 1
    else:
        state.errors.append(ParseError("Expected an ID after declaring an int", tokens[state.index]))

    if state.index < len(tokens) and tokens[state.index].type == "SEMICOLON":
        state.index += 1
    else:
        state.errors.append(ParseError("Expected ';'", tokens[state.index]))

    return f 


def parse_assignment(tokens, state):

    f = {"children": [], "value": "ASSIGNMENT"}

    if state.index < len(tokens) and tokens[state.index].type == "ID":
        if tokens[state.index].value in [symbol.value for symbol in state.symbol_table]: # check if the variable has been declared
            f["children"].append({"value": tokens[state.index].value})
            state.index += 1
        else:
            state.index += 1
            state.errors.append(ParseError("Variable never declared", tokens[state.index]))
    else:
        state.errors.append(ParseError("Expected an ID for assignment", tokens[state.index]))

    if state.index < len(tokens) and tokens[state.index].type == "ASSIGN":
        f["children"].append({"value": "="})
        state.index += 1
    else:
        state.errors.append(ParseError("Expected '=' for assignment", tokens[state.index]))

    expr = parse_expression(tokens, state)
    if expr:
        f["children"].append(expr)
    else:
        state.errors.append(ParseError("Expected expression for assignment", tokens[state.index]))

    return f


def parse_condition(tokens, state):

    f = {"children": [], "value": "CONDITION"}

    if state.index < len(tokens) and (tokens[state.index].type == "ID" or tokens[state.index].type == "NUMBER"):
        f["children"].append({"value": tokens[state.index].value})
        state.index += 1

    if state.index < len(tokens) and tokens[state.index].type == "OP" and tokens[state.index].value in ["==", "!=", "<", ">", "<=", ">="]: # all supported comparisons 
        f["children"].append({"value": tokens[state.index].value})
        state.index += 1

    if state.index < len(tokens) and (tokens[state.index].type == "ID" or tokens[state.index].type == "NUMBER"):
        f["children"].append({"value": tokens[state.index].value})
        state.index += 1


    if state.index < len(tokens) and tokens[state.index].type == "OP" and tokens[state.index].value in ["&&", "||"]:
        state.index += 1
        pc = parse_condition(tokens, state)
        if pc:
            f["children"].append(pc) # TODO: the way that this currently works is that it creates a new child for each condition after a && or ||, maybe need to change this to create a new child on the same level as the first condition

    return f


def parse_conditional(tokens, state):

    f = {"children": [], "value": "CONDITIONAL"}

    # if state.index < len(tokens) and tokens[state.index].type == "if" and tokens[state.index].value == "if":
    if state.index < len(tokens) and tokens[state.index].type in ["if", "while"]:
        f["children"].append({"value": tokens[state.index].value})
        state.index += 1

    if state.index < len(tokens) and tokens[state.index].type == "L_PAREN":
        state.index += 1
    else:
        state.errors.append(ParseError("Expected '('", tokens[state.index]))

    pc = parse_condition(tokens, state) 
    if pc:
        f["children"].append(pc)
    else:
        state.errors.append(ParseError("Expected condition inside parentheses", tokens[state.index]))

    if state.index < len(tokens) and tokens[state.index].type == "R_PAREN":
        state.index += 1
    else:
        state.errors.append(ParseError("Expected ')'", tokens[state.index]))

    if state.index < len(tokens) and tokens[state.index].type == "LBRACE":
        state.index += 1
        
    while state.index < len(tokens) and tokens[state.index].type != "RBRACE":
        stmt = parse_statement(tokens, state)
        if stmt:
            f["children"].append(stmt)
        else:
            state.errors.append(ParseError("Expected statement", tokens[state.index]))

    if state.index < len(tokens) and tokens[state.index].type == "RBRACE":
        state.index += 1 

    return f


def parse_statement(tokens, state):

    f = {"children": [], "value": "STATEMENT"}
    
    # return
    if state.index < len(tokens) and tokens[state.index].type == "return" and tokens[state.index].value == "return":
        f["children"].append({"value": "return"})
        state.index += 1 
        
        expr = parse_expression(tokens, state)
        if expr:
            f["children"].append(expr)
        else:
            state.errors.append(ParseError("Expected expression", tokens[state.index]))

        if state.index < len(tokens) and tokens[state.index].type == "SEMICOLON":
            state.index += 1 
        else:
            state.errors.append(ParseError("Expected ';'", tokens[state.index]))
    # declaration
    elif state.index < len(tokens) and tokens[state.index].type == "int":
        declaration = parse_declaration(tokens, state)
        if declaration:
            f["children"].append(declaration)
        else:
            state.errors.append(ParseError("Expected declaration", tokens[state.index]))
    # assignment
    elif state.index < len(tokens) and tokens[state.index].type == "ID":
        assignment = parse_assignment(tokens, state)
        if assignment:
            f["children"].append(assignment)
        else :
            state.errors.append(ParseError("Expected assignment", tokens[state.index]))

        if state.index < len(tokens) and tokens[state.index].type == "SEMICOLON":
            state.index += 1
        else:
            state.errors.append(ParseError("Expected ';'", tokens[state.index]))
    # conditionals and loops
    elif state.index < len(tokens) and tokens[state.index].type in ["if", "while"]:
        conditional = parse_conditional(tokens, state)
        if conditional:
            f["children"].append(conditional)
    else:
        state.errors.append(ParseError("Expected 'return' or 'int'", tokens[state.index]))

    return f


def parse_parameter(tokens, state):
    
    f = {"children": [], "value": "PARAMETER"}
    
    if tokens[state.index].type == "int":
        f["children"].append({"value": tokens[state.index].value})
        state.index += 1

    if tokens[state.index].type == "ID":
        f["children"].append({"value": tokens[state.index].value})
        
        state.symbol_table.append(Symbol(tokens[state.index - 1].type, tokens[state.index].value, "parameter"))
        
        state.index += 1

    return f


def parse_parameters(tokens, state):

    f = {"children": [], "value": "PARAMETERS"}

    if state.index < len(tokens) and tokens[state.index].type == "L_PAREN":
        state.index += 1

    while tokens[state.index].type != "R_PAREN":
        param = parse_parameter(tokens, state)
        if param:
            f["children"].append(param)
        
        if tokens[state.index].type == "COMMA":
            state.index += 1

    return f


# used to check if a void function returns a value
def check_valid_void(tokens, state):
    i = state.index
    while i < len(tokens) and tokens[i].type != "RBRACE":
        if tokens[i].type == "return":
            return False
        i += 1

    return True


def parse_function(tokens, state):

    f = {"children": [], "value": "FUNCTION"}

    if state.index < len(tokens) and tokens[state.index].type in ["int", "void"] and tokens[state.index].value in ["int", "void"]: # support int and void function return types

        # if the function is void, then we check if "return" is in the function body
        # if it is then error
        if tokens[state.index].value == "void":
            if not check_valid_void(tokens, state):
                state.errors.append(ParseError("void function cannot return a value", tokens[state.index]))

        f["children"].append({"value": tokens[state.index].value})
        state.index += 1
    else:
        state.errors.append(ParseError("Expected 'int'", tokens[state.index]))

    if state.index < len(tokens) and tokens[state.index].type == "ID": 
        f["children"].append({"value": tokens[state.index].value})
        state.index += 1
    else:
        state.errors.append(ParseError("Expected function name", tokens[state.index]))

    if state.index < len(tokens) and tokens[state.index].type == "L_PAREN":
        state.index += 1
    else:
        state.errors.append(ParseError("Expected '('", tokens[state.index]))

    params = parse_parameters(tokens, state)
    if params:
        f["children"].append(params)

    if state.index < len(tokens) and tokens[state.index].type == "R_PAREN":
        state.index += 1
    else:
        state.errors.append(ParseError("Expected ')'", tokens[state.index]))

    if state.index < len(tokens) and tokens[state.index].type == "LBRACE":
        state.index += 1
    else:
        state.errors.append(ParseError("Expected '{'", tokens[state.index]))

    while state.index < len(tokens) and tokens[state.index].type != "RBRACE": # TODO: chnage this to support conditionals and loops
        stmt = parse_statement(tokens, state)
        if stmt:
            f["children"].append(stmt)

    if state.index < len(tokens) and tokens[state.index].type == "RBRACE":
        state.index += 1
    else:
        state.errors.append(ParseError("Expected '}'", tokens[state.index]))

    return f

# main program parser 
def parse_program(tokens, state):

    f = {"children": [], "value": "PROGRAM"}

    while state.index < len(tokens):
        func = parse_function(tokens, state)
        if func:
            f["children"].append(func)

    return f


# iterates over all the errors and print them out in a nice format 
def handle_errors(filename, errors):
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


# main parse function, need to pass in filename for printing state.errors
# TODO: sure there is a better way to do this but it works for right now 
def parse(tokens, filename):

    index = 0
    errors = []
    symbol_table = []

    # state object that keeps track of everything in the parser, and is passed around to all the function
    # tracks the index, current errors, and current symbol table
    state = RunState(index, errors, symbol_table)
    
    tree = parse_program(tokens, state)
    
    handle_errors(filename, state.errors)
    
    return tree, state # TODO: returning state here so that we can return the symbol table to the main program

# print the parse tree in a nice format
def print_parse_tree(tree, indent=0):
    indentation = " " * indent
    print(f"{indentation}{tree['value']}")
    if 'children' in tree:
        for child in tree['children']:
            print(f"{indentation}")
            print_parse_tree(child, indent + 4)


# print the associated symbol table
def print_symbol_table(state):
    print("\n\nSymbol Table:")
    for symbol in state.symbol_table:
        print(f"\ttype:{symbol.type}, value: {symbol.value}, scope: {symbol.scope}")
    print("\n")