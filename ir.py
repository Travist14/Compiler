
# print the ast
def print_ast(tree, indent=0):
    indentation = " " * indent
    print(f"{indentation}{tree['value']}")
    if 'children' in tree:
        for child in tree['children']:
            print(f"{indentation}")
            print_ast(child, indent + 4)


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


def generate_three_address_code(node, symbol_table):
    
    code = []

    if node['value'] == "PROGRAM":
        for child in node['children']:
            code.append(generate_three_address_code(child, symbol_table))
    elif node['value'] == "FUNCTION":
        for child in node['children']:
            code.append(generate_three_address_code(child, symbol_table))
    elif node['value'] == "STATEMENT":

        for child in node['children']:
            
            # check if its an assignment 
            code.append(generate_assignment(node, symbol_table))


    return code 

    
def generate_assingment(node, symbol_table):
    
    code = []

    
    
ast = {'children': [], 'value': 'PROGRAM'}
def convert_parse_tree_to_ast(parse_tree):
    
    for child in parse_tree['children']:
        if child['value'] in ['STATEMENT', 'EXPR', 'ASSIGNMENT', 'TERM']:
            ast['children'].append(convert_parse_tree_to_ast(grandchild for grandchild in child['children']))
        else:
            ast['children'].append(child)

    return ast


def convert_to_ir(tree, symbol_table):
    print(tree)
    ast = convert_parse_tree_to_ast(tree)
    print_ast(ast)
    print(ast)    

    # tac = generate_three_address_code(tree, symbol_table)
    # print(tac)











        # # This will always be the set up for declaration so we can look ahead 
        # if node['children'][0]['value'] == "DECLARATION":
        #     code.append(f"{node['children'][0]['children'][0]['value']} {node['children'][0]['children'][1]['value']}")
            
        # # 
        # elif node['children'][0]['value'] == "ASSIGNMENT":
        #     # var = node['children'][0]['children'][0]['value'] # get the variable
        #     # op = node['children'][0]['children'][2]['value'] # get the operator

        #     # if node['children'][0]['children'][2]['children'][0]['value'] == "TERM": # check to see if the left operand is just a term
        #     #     left_operand = generate_term(node['children'][0]['children'][2]['children'][0], symbol_table)

        #     # if node['children'][0]['children'][2]['children'][1]['value'] == "EXPR":
        #     #     right_operand = generate_expression(node['children'][0]['children'][2]['children'][1], symbol_table)
                
        #     # code.append(f"{var} = {left_operand} {op} {right_operand}")

        #     code.append(generate_assignment(node['children'][0], symbol_table))

    # return code
    
# def generate_assignment(node, symbol_table):
#     # start at the root of the assignment subtree 
#     # iterate over and handle assignment
#     # return the code

#     code = []

#     if node['value'] == "ASSIGNMENT":
#         if node['children'][0]['value'] != "EXPR": # we need to make sure that we dont start with an expression, if not then we know where each operand will be
#             var = node['children'][0]['value'] 
#             op = node['children'][2]['value'] 

#             # if the left operand is a term then we can go ahead and pull out the left operand
#             if node['children'][2]['children'][0]['value'] == "TERM": 
#                 left_operand = generate_term(node['children'][2]['children'][0], symbol_table)
                
#                 # now we check the right right of the operator
#             if node['children'][2]['children'][1]['value'] == "EXPR":
#                 # code.append(generate_expression(node['children'][2]['children'][1], symbol_table))
#                 right_operand = generate_expression(node['children'][2]['children'][1], symbol_table)

#             code.append(f"{var} = {left_operand} {op} {right_operand}")

                
#     return code
        

# temp_var = 0
# def generate_expression(node, symbol_table):
#     global temp_var
#     code = []

#     if node['value'] == "EXPR":

#         # check to see if its just a term in the expression
#         if node['children'][0]['value'] == "TERM":
#             operand = generate_term(node['children'][0], symbol_table)
#             code.append(operand)
#             return code
#         else:
#             # handle another expression
#             left_operand = generate_expression(node['children'][0], symbol_table)
#             right_operand = generate_expression(node['children'][2], symbol_table)
#             operator = node['children'][1]['value']
#             temp_var_name = f"t{temp_var}"
#             temp_var += 1
#             return temp_var_name

            
# def generate_term(node, symbol_table):
#     if node['value'] == "TERM":
#         operand = node['children'][0]['value']
#         return operand