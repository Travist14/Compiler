import colorama

# print the ast
def print_ast(tree, indent=0):
    indentation = " " * indent
    print(f"{indentation}{tree['value']}")
    if 'children' in tree:
        for child in tree['children']:
            print(f"{indentation}")
            print_ast(child, indent + 4)


def find_leaf_nodes(tree):
    leaves = []
    if 'children' in tree:
        if tree['children'] == [] and tree['value'] not in ["PARAMETERS"]:
            leaves.append(tree)
        else:
            for child in tree['children']:
                leaves.extend(find_leaf_nodes(child))

    return leaves


def convert_parse_tree_to_ast(parse_tree):
    ast = {'children': [], 'value': ""}
    
    if parse_tree['value'] not in ["PROGRAM", "DECLARATION", "STATEMENT", "EXPRESSION", "FUNCTION", "PARAMETER", "ASSIGNMENT", "PARAMETERS", "FACTOR", "TERM", "EXPR"]:
        ast['value'] = parse_tree['value']

    if 'children' in parse_tree:
        for child in parse_tree['children']:
            ast['children'].append(convert_parse_tree_to_ast(child))

    return ast


def convert_to_ir(tree, symbol_table):

    ast = convert_parse_tree_to_ast(tree)
    print_ast(ast)
    
