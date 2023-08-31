from dataclasses import dataclass
import re

@dataclass
class Token():
    type: str
    value: str
    line: int
    column: int

def tokenize(code):
    tokens = []
    keywords = {'if', 'else', 'while', 'for', 'return', 'int', 'float', 'double', 'char', 'void', 'true', 'false', 'NULL'}
    token_specification = [
        ('NUMBER', r'\d+(\.\d*)?'),        # Integer or decimal number
        ('HEX_NUMBER', r'0[xX][0-9A-Fa-f]+'),  # Hexadecimal number
        ('OCT_NUMBER', r'0[oO]?[0-7]+'),    # Octal number
        ('ID', r'[A-Za-z_]\w*'),            # Identifiers
        ('STRING', r'\"([^\"\\]|\\.)*\"'),  # String literal
        ('CHAR', r'\'([^\"\']|\\.)*\''),    # Character literal
        ('OP', r'[+\-*/=<>!%&|]+'),         # Arithmetic operators
        ('INC', r'\+\+'),                   # Increment operator
        ('DEC', r'--'),                     # Decrement operator
        ('ASSIGN_OP', r'\+=|-=|\*=|/=|%=|='),  # Assignment operators
        ('LOGICAL_OP', r'&&|\|\|'),         # Logical operators
        ('BITWISE_OP', r'&|\|'),            # Bitwise operators
        ('PREPROCESSOR', r'\#.*'),          # Preprocessor directive
        ('LBRACKET', r'\['),                # Left square bracket
        ('RBRACKET', r'\]'),                # Right square bracket
        ('LPAREN', r'\('),                  # Left parenthesis
        ('RPAREN', r'\)'),                  # Right parenthesis
        ('LBRACE', r'\{'),                  # Left brace
        ('RBRACE', r'\}'),                  # Right brace
        ('SEMICOLON', r';'),                # Statement terminator
        ('COMMA', r','),                    # Comma
        ('COLON', r':'),                    # Colon
        ('DOT', r'\.'),                     # Dot
        ('NEWLINE', r'\n'),                 # Line endings
        ('SKIP', r'[ \t]+'),                # Skip over spaces and tabs
        ('MISMATCH', r'.'),                 # Any other character
    ]

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start

        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind in ['HEX_NUMBER', 'OCT_NUMBER']:
            value = int(value, 0)
        elif kind == 'ID' and value in keywords:
            kind = value
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'STRING':
            value = value[1:-1]
        elif kind == 'CHAR':
            value = value[1:-1]
        elif kind == 'OP':
            if value == '=':
                kind = 'ASSIGN'
            elif value == '!':
                kind = 'NOT'
        elif kind == 'LOGICAL_OP':
            if value == '&&':
                kind = 'AND'
            elif value == '||':
                kind = 'OR'
        elif kind == 'BITWISE_OP':
            if value == '&':
                kind = 'BITWISE_AND'
            elif value == '|':
                kind = 'BITWISE_OR'
        elif kind == 'LPAREN':
            kind = 'L_PAREN'
        elif kind == 'RPAREN':
            kind = 'R_PAREN'
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')

        tokens.append(Token(kind, value, line_num, column))

    return tokens

def print_tokens(tokens):
    print(f"Tokens in input C file:\n")
    for tok in tokens:
        print(tok)

