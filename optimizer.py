import re

def print_ir(ir):
    for line in ir:
        if type(line) == list:
            print(line[0])
        else:
            print("    " + line)


def perform_constant_folding(ir):
    for i, line in enumerate(ir):
        if type(line) != list:
            if "=" in line:
                # use regular expression matching to see if there are two numbers on the right side of the assignment
                # if there are, then perform the operation and replace the line with the result
                var = line.split("=")[0].strip()
                match = re.search(r'(\d+) (\+|\-|\*|\/) (\d+)', line)
                if match:
                    
                    left_operand = int(match.group(1))
                    operator = match.group(2)
                    right_operand = int(match.group(3))
                    
                    if operator == "+":
                        result = left_operand + right_operand
                    elif operator == "-":
                        result = left_operand - right_operand
                    elif operator == "*":
                        result = left_operand * right_operand
                    elif operator == "/":
                        result = left_operand / right_operand
                    
                    ir[i] = f"{var} = {result}"

    return ir


# def perform_constat_propagation(ir):

#     constant_variables = {}
    
#     assignment_regex = re.compile(r'(\w+)\s*=\s*(\d+)')
    
#     variable_regex = re.compile(r'\b\w+\b')

#     for i, line in enumerate(ir):
#         if type(line) != list:
#             assignment_match = assignment_regex.match(line)
#             if assignment_match:
#                 variable, value = assignment_match.groups()
#                 constant_variables[variable] = value

# def perform_constant_propagation(ir):
#     # Dictionary to store variable-constant pairs
#     constant_variables = {}

#     # Regular expression to match lines where a variable is assigned a constant
#     assignment_regex = re.compile(r'(\w+)\s*=\s*(\d+)')

#     # Regular expression to match variables
#     variable_regex = re.compile(r'\b\w+\b')

#     # Iterate over the IR
#     for i, line in enumerate(ir):
#         if type(line) != list:
#             # If the line is a variable assignment to a constant
#             assignment_match = assignment_regex.match(line)
#             if assignment_match:
#                 variable, value = assignment_match.groups()
#                 constant_variables[variable] = value

#             # If the line contains a variable that has been assigned a constant
#             else:
#                 variables_in_line = variable_regex.findall(line)
#                 for variable in variables_in_line:
#                     if variable in constant_variables:
#                         # Replace the variable with its constant value
#                         ir[i] = line.replace(variable, constant_variables[variable])

#     return ir


# def constant_propagation(three_address_code):
#     # Regular expressions to match constants and variables.
#     CONSTANT_REGEX = re.compile(r'^[0-9]+$')
#     VARIABLE_REGEX = re.compile(r'^[a-z]+$')

#     # A dictionary to store the values of constants.
#     constant_values = {}

#     # Iterate over the three address code statements.
#     for statement in three_address_code:
#         # Split the statement into its components.
#         operator, left_operand, right_operand = statement.split()

#         # If the left operand is a variable, update its value if it is a constant.
#         if VARIABLE_REGEX.match(left_operand):
#             if CONSTANT_REGEX.match(right_operand):
#                 constant_values[left_operand] = int(right_operand)

#         # If the right operand is a variable, replace it with its value if it is known.
#         if VARIABLE_REGEX.match(right_operand) and right_operand in constant_values:
#             right_operand = str(constant_values[right_operand])

#         # Update the statement with the propagated values.
#         statement = f'{operator} {left_operand} {right_operand}'

#     # Return the updated three address code statements.
#     return three_address_code



def perform_constant_propagation(ir):
    
    # regular expression to find a constant assignment
    assignment_regex = re.compile(r'(\w+)\s*=\s*(\d+)')

    for i, line in enumerate(ir):
        if type(line) != list:
            # check if line is constant assignment
            assignment_match = assignment_regex.match(line)
            if assignment_match:
                print(f"line: {line}")
    # for i, line in enumerate(ir):
    #     if type(line) != list:
    #         # if the line is a constant assignment
    #         assignment_match = assignment_regex.match(line)
    #         if assignment_match:
                
    #             # get the variable and the value
    #             variable, value = assignment_match.groups()
    #             print(f"variable: {variable}, value: {value}")

    #             # iterate from the current line to the end of the IR
    #             for j in range(i, len(ir)):
    #                 if type(ir[j]) != list:
    #                     if variable in ir[j]:
    #                         ir[j] = ir[j].replace(variable, value)

    return ir


def run_optimizer(ir, symbol_table):
    print(ir)
    
    ir = perform_constant_folding(ir)
    print_ir(ir)

    ir = perform_constant_propagation(ir)
    print_ir(ir)