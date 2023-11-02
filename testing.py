def generate_three_address_code(node):

    code = []
    if node['value'] == 'PROGRAM':
        for child in node['children']:
            code.extend(generate_three_address_code(child))
    
    elif node['value'] == 'FUNCTION':
        for child in node['children']:
            code.extend(generate_three_address_code(child))
    
    elif node['value'] == 'STATEMENT':
        if len(node['children']) == 1 and node['children'][0]['value'] == 'ASSIGNMENT':
            assignment = node['children'][0]
            target = assignment['children'][0]['value']
            source1 = assignment['children'][2]['children'][0]['children'][0]['value']
            source2 = assignment['children'][2]['children'][1]['children'][0]['value']
            op = assignment['children'][2]['value']
            code.append(f"{target} = {source1} {op} {source2}")
    
    return code


global temp_counter # added this line to declare the temp_counter variable
temp_counter = 0 # initialize the temp_counter to zero

def generate_three_address_code(node):

    global code

    if node['value'] == 'PROGRAM':
        for child in node['children']:
            code.extend(generate_three_address_code(child))

    elif node['value'] == 'FUNCTION':
        for child in node['children']:
            code.extend(generate_three_address_code(child))

    elif node['value'] == 'STATEMENT':
        if len(node['children']) == 1 and node['children'][0]['value'] == 'ASSIGNMENT':
            assignment = node['children'][0]
            target = assignment['children'][0]['value']
            expr = assignment['children'][2]
            code.extend(generate_expression_code(expr, target))

    return code

def generate_expression_code(node, target):
    global code

    if node['value'] == 'EXPR':
        if len(node['children']) == 1 and node['children'][0]['value'] == 'TERM':
            term = node['children'][0]
            code.extend(generate_term_code(term, target))
        else:
            left_operand = target
            op = node['children'][1]['value']
            right_operand = f"t{temp_counter}"
            temp_counter += 1
            code.extend(generate_expression_code(node['children'][0], left_operand))
            code.extend(generate_term_code(node['children'][2], right_operand))
            code.append(f"{target} = {left_operand} {op} {right_operand}")

    return code

def generate_term_code(node, target):
    global code
    if node['value'] == 'term':
        if len(node['children']) == 1 and node['children'][0]['value'] == 'factor':
            factor = node['children'][0]
            code.extend(generate_factor_code(factor, target))

    return code

def generate_factor_code(node, target):
    global code
    if node['value'] == 'factor':
        if len(node['children']) == 1 and node['children'][0]['value'] == 'int':
            int_value = node['children'][0]['value']
            code.append(f"{target} = {int_value}")
        elif len(node['children']) == 1 and node['children'][0]['value'] == 'id':
            id_name = node['children'][0]['value']
            code.append(f"{target} = {id_name}")
    return code