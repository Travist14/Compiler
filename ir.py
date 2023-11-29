
# print the ast
def print_ast(tree, indent=0):
    indentation = " " * indent
    print(f"{indentation}{tree['value']}")
    if 'children' in tree:
        for child in tree['children']:
            print(f"{indentation}")
            print_ast(child, indent + 4)


# This function is just for testing and is not used anywhere, keeping it for now
def generate_with_two_var(node):

    code = []
    if node['value'] == 'PROGRAM':
        for child in node['children']:
            code.extend(generate_with_two_var(child))
    
    elif node['value'] == 'FUNCTION':
        for child in node['children']:
            code.extend(generate_with_two_var(child))
    
    elif node['value'] == 'STATEMENT':
        if len(node['children']) == 1 and node['children'][0]['value'] == 'ASSIGNMENT':
            assignment = node['children'][0]
            target = assignment['children'][0]['value']
            source1 = assignment['children'][2]['children'][0]['children'][0]['value']
            source2 = assignment['children'][2]['children'][1]['children'][0]['children'][0]['value']
            op = assignment['children'][2]['value']
            code.append(f"{target} = {source1} {op} {source2}")
    
    return code


# --------------- AST stuff below here ----------------- #

# there is bug in this function that leaves a single "TERM" the tree right above leaf nodes
def convert_parse_tree_to_ast(parse_tree):
    if 'children' not in parse_tree:
        return parse_tree

    # Initialize the AST for this node
    ast_node = {'value': parse_tree['value']}
    ast_children = []

    for child in parse_tree['children']:
        if child['value'] in ['EXPR', 'STATEMENT', 'TERM', 'FACTOR']:
            # Recursively convert the children of 'EXPR' and 'TERM'
            for grandchild in child['children']:
                ast_child = convert_parse_tree_to_ast(grandchild)
                ast_children.append(ast_child)
        else:
            # Recursively convert the child node
            ast_child = convert_parse_tree_to_ast(child)
            ast_children.append(ast_child)

    ast_node['children'] = ast_children
    return ast_node

def final_convert_for_ast(tree):
    if 'children' in tree:
        for child in tree['children']:
            if child['value'] == "TERM":
                tree['children'].extend(child['children'])

                # get rid of the child node
                tree['children'].remove(child)                

            final_convert_for_ast(child)

    return tree

def get_ast(tree):
    ast = convert_parse_tree_to_ast(tree)
    ast = final_convert_for_ast(ast)
    return ast






# --------------- TAC stuff below here ----------------- #




temp_count = 0
def get_temp_var():
    global temp_count
    temp_var = f"t{temp_count}"
    temp_count += 1
    return temp_var
    

def generate_expression_code(ast, symbol_table):
    global temp_count 
    code = []

    if ast['value'] == '+':
        left_code = generate_expression_code(ast['children'][0], symbol_table)
        right_code = generate_expression_code(ast['children'][1], symbol_table)
        temp_var = get_temp_var()
        code.extend(left_code)
        code.extend(right_code)
        code.append(f"{temp_var} = {left_code[-1]} + {right_code[-1]}")
        return code + [temp_var]

    elif ast['value'] == '-':
        left_code = generate_expression_code(ast['children'][0], symbol_table)
        right_code = generate_expression_code(ast['children'][1], symbol_table)
        temp_var = get_temp_var()
        code.extend(left_code)
        code.extend(right_code)
        code.append(f"{temp_var} = {left_code[-1]} - {right_code[-1]}")
        return code + [temp_var]

    elif ast['value'] == '*':
        left_code = generate_expression_code(ast['children'][0], symbol_table)
        right_code = generate_expression_code(ast['children'][1], symbol_table)
        temp_var = get_temp_var()
        code.extend(left_code)
        code.extend(right_code)
        code.append(f"{temp_var} = {left_code[-1]} * {right_code[-1]}")
        return code + [temp_var]

    elif ast['value'] == '/':
        left_code = generate_expression_code(ast['children'][0], symbol_table)
        right_code = generate_expression_code(ast['children'][1], symbol_table)
        temp_var = get_temp_var()
        code.extend(left_code)
        code.extend(right_code)
        code.append(f"{temp_var} = {left_code[-1]} / {right_code[-1]}")
        return code + [temp_var]

    # this elif was auto generated, shouldn't be needed but I had issues when I deleted it
    # TODO: figure this out and fix it later 
    # this should be what is causing extra vars to be added to the ir, but for right now handle it by just removing them
    elif isinstance(ast['value'], int):
        return [str(ast['value'])]

    else:
        return [ast['value']]



def generate_three_address_code(ast, symbol_table):
    code = []

    if ast['value'] == "PROGRAM":
        for child in ast['children']:
            code.extend(generate_three_address_code(child, symbol_table))
    elif ast['value'] == "FUNCTION":
        code.append(["L0:"])
        for child in ast['children']:
            code.extend(generate_three_address_code(child, symbol_table))
    elif ast['value'] == "DECLARATION":
        var_type = ast['children'][0]['value']
        variable_name = ast['children'][1]['value']
        code.append(f"{var_type} {variable_name}")

    elif ast['value'] == "ASSIGNMENT":
        left_operand = ast['children'][0]['value']
        expression_code = generate_expression_code(ast['children'][2], symbol_table)
        code.extend(expression_code)
        code.append(f"{left_operand} = {expression_code[-1]}")

    return code


def transform_ir(ir):
    new_ir = []
    for line in ir:
        if isinstance(line, list):
            new_ir.append(line)
        elif len(line) > 2:
            new_ir.append(line)

    return new_ir


def print_ir(ir):
    print("\n-------------- Intermediate Representation --------------")
    for line in ir:
        if type(line) == list:
            print(line[0])
        else:
            print("    " + line)


def convert_to_ir(tree, symbol_table):
    
    # conver the parse tree into an AST
    ast = get_ast(tree)

    tac = generate_three_address_code(ast, symbol_table)
    ir = transform_ir(tac)

    return ir 

