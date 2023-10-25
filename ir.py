
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


def ast_to_tac(ast):
    tac = []
    tmp_var = 0
    
    def gen_tmp():
        nonlocal tmp_var 
        tmp_var += 1
        return f't{tmp_var}'
    
    def traverse(node):
        if node['value'] == '=':
            left = traverse(node['children'][0])
            right = traverse(node['children'][2])
            tmp = gen_tmp()
            tac.append(f'{tmp} = {right}') 
            tac.append(f'{left} = {tmp}')
            return left
        elif node['value'] == '+':
            left = traverse(node['children'][0])
            right = traverse(node['children'][2])
            tmp = gen_tmp()
            tac.append(f'{tmp} = {left} + {right}')
            return tmp
        else:
            return node['value']
            
    traverse(ast)
    return tac
    

def convert_to_ir(tree, symbol_table):

    ast = convert_parse_tree_to_ast(tree)
    print_ast(ast)
    print(ast)

    ir = ast_to_tac(ast)

    print(ir)