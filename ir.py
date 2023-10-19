# print the ast
def print_ast(tree, indent=0):
    indentation = " " * indent
    if tree['value'] not in ["PROGRAM", "DECLARATION", "STATEMENT", "EXPRESSION", "FUNCTION", "PARAMETER", "ASSIGNMENT", "PARAMETERS", "FACTOR", "TERM", "EXPR"]:
        print(f"{indentation}{tree['value']}")
    if 'children' in tree:
        for child in tree['children']:
            print(f"{indentation}")
            print_ast(child, indent + 4)


# depth first search to find the leaf nodes of the tree
def dfs(tree):
    if 'children' in tree:
        for child in tree['children']:
            dfs(child)
    else:
        print(tree['value'])
    

def convert_to_ir(tree, symbol_table):
    print(tree)

    print_ast(tree)
    dfs(tree)
    
