import sys
import colorama 

from tokenizer import tokenize

index = 0
errors = []

class ParseError(Exception):
    def __init__(self, message, token):
        self.message = message
        self.token = token
        super().__init__(self.message, self.token)

    def __str__(self):
        return f"{self.message} at {self.token}"
    

# heavily inspired by the parse tree that we went over in class 
def parse_expression(tokens):
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
def parse(text, filename):
    tokens = tokenize(text)
    if type(tokens) != list:
        raise ValueError("tokenize should return a list of tokens")
    
    tree = parse_expression(tokens)
    
    handle_errors(filename)
    
    return tree