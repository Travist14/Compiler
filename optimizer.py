import re

def print_ir(ir):
    for line in ir:
        if type(line) == list:
            print(line[0])
        else:
            print("    " + line)


def perform_dead_code_elimination(ir):
    new_ir = []
    for i, line in enumerate(ir):
        if type(line) == list:
            new_ir.append(line)
            continue
        
        variable = line.split("=")[0].strip()
        # print(f"Checking if {variable} is used again")

        # iterate through the rest of the ir to see if the variable is used again

        for j in range(i + 1, len(ir)):
            if variable in ir[j]:
                new_ir.append(line)
                break

    return new_ir

def perform_constant_folding(ir):
    for i, line in enumerate(ir):
        if type(line) != list:
            if "=" in line:
                # use regular expression matching to see if there are two numbers on the right side of the assignment
                # if there are, then perform the operation and replace the line with the result
                var = line.split("=")[0].strip()

                match = re.search(r'(\d+) (\+|\-|\*|\/) (\d+)', line)

                if match:
                    
                    # we could run into a situation where we have "a = t1 - 3" which would match the regex and be replaced with -2
                    # handle this by making sure that the previous character is a space
                    if line[match.start() - 1] != " ":
                        continue
                    
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


def perform_constant_propagation(ir):
    
    assignment_regex = re.compile(r'(\w+)\s*=\s*(\d+)')

    variable_regex = re.compile(r'\b\w+\b')

    constant_variables = {}

    for i, line in enumerate(ir):
        if type(line) != list:
            assignment_match = assignment_regex.match(line)
            
            # make sure that the legnth of the line is the same as the length of the match becuase we could encounter situation where we have "t0 = 4 + a" which would match the regex but we don't want to replace it
            if assignment_match and len(line) == len(assignment_match.group()):
                variable, value = assignment_match.groups()
                constant_variables[variable] = value

            else:
                variables_in_line = variable_regex.findall(line)

                for variable in variables_in_line:
                    if variable in constant_variables:
                        ir[i] = line.replace(variable, constant_variables[variable])
                    
    return ir



def run_optimizer(ir, symbol_table):
    

    # iterate through the IR and optimize until we can't optimize anymore
    while True:
        old_ir = ir.copy()

        ir = perform_constant_folding(ir)
        ir = perform_constant_propagation(ir)
        if ir == old_ir:
            break

    
            
    print_ir(ir)

    # ir = perform_dead_code_elimination(ir)
    # print_ir(ir)
    