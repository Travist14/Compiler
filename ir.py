
# print the ast
def print_ast(tree, indent=0):
    indentation = " " * indent
    print(f"{indentation}{tree['value']}")
    if 'children' in tree:
        for child in tree['children']:
            print(f"{indentation}")
            print_ast(child, indent + 4)


def convert_parse_tree_to_ast(parse_tree):
    ast = {'children': [], 'value': ""}
    
    if parse_tree['value'] not in ["PROGRAM", "DECLARATION", "STATEMENT", "EXPRESSION", "FUNCTION", "PARAMETER", "ASSIGNMENT", "PARAMETERS", "FACTOR", "TERM", "EXPR"]:
        ast['value'] = parse_tree['value']

    if 'children' in parse_tree:
        for child in parse_tree['children']:
            ast['children'].append(convert_parse_tree_to_ast(child))

    return ast


def remove_empty_nodes(ast):
    if not ast:
        return None
    if ast['value'] == '' and not ast['children']:
        return None
    else:
        ast['children'] = [remove_empty_nodes(child) for child in ast['children']]
        ast['children'] = [child for child in ast['children'] if child is not None]
        return ast



def convert_to_ir(tree, symbol_table):

    ast = convert_parse_tree_to_ast(tree)
    ast = remove_empty_nodes(ast)
    print_ast(ast)
    print(ast)
    
