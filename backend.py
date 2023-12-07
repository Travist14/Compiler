# define a class line that defines a line of x86 assembly code
class Line:
    def __init__(self, label=None, instruction=None, op1=None, op2=None):
        self.label = label
        self.instruction = instruction
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        # return f"{self.label} {self.instruction} {self.op1} {self.op2}"
        if self.label is None:
            return f"{self.instruction} {self.op1} {self.op2}"
        else:
            return f"{self.label}: {self.instruction} {self.op1} {self.op2}"

# function that gets the number of local variables in the ir
def num_local_variables(ir):
    num = 0 
    for line in ir:
        if type(line) == list:
            continue
        elif "=" in line: # reserving 4 bytes for every assignment
            num += 1 

    return num
            
# TODO: switch src dest
def setup_preamble(ir):
    stack_space = num_local_variables(ir) * 4 + 4
    output = []
    output.append("main:") 
    output.append("push rbp")
    output.append("mov rbp, rsp")
    output.append(f"sub rsp, {stack_space}") # reserve 32 bytes for local variables
    return output


def setup_postamble(ir):
    return ["pop rbp", "ret"]


def is_register(operand):
    if operand in ["eax", "ebx", "ecx", "edx", "esi", "edi", "ebp", "esp"]:
        return True
    else:
        return False


# def ir_to_asm(ir):
#     asm = []
#     temp_counter = 0
#     var_offset = 4

#     for line in ir:
#         if line[0].endswith(':'):
#             # asm.append(line[0])
#             continue
#         else:
#             tokens = line.split(' ')
#             if tokens[0] == "return":
#                 asm.append(f"mov eax, DWORD PTR [rbp-{var_offset-4}]")
#             elif tokens[1] == '=':
#                 if '+' in tokens:
#                     asm.append(f'mov eax, DWORD PTR [rbp-{var_offset}]')
#                     asm.append(f'add eax, {tokens[2]}')
#                     asm.append(f'mov DWORD PTR [rbp-{var_offset}], eax')
#                 elif '*' in tokens:
#                     asm.append(f'mov eax, DWORD PTR [rbp-{var_offset}]')
#                     asm.append(f'lea edx, [0+rax*4]')
#                     asm.append(f'mov DWORD PTR [rbp-{var_offset}], edx')
#                 elif '-' in tokens:
#                     asm.append(f'mov eax, DWORD PTR [rbp-{var_offset}]')
#                     asm.append(f'sub eax, {tokens[2]}')
#                     asm.append(f'mov DWORD PTR [rbp-{var_offset}], eax')
#                 else:
#                     asm.append(f'mov DWORD PTR [rbp-{var_offset}], {tokens[2]}')
#                 var_offset += 4
#             else:
#                 asm.append(f'mov DWORD PTR [rbp-{var_offset}], {tokens[0]}')
#                 var_offset += 4

#     return asm


# def ir_to_asm(intermediate_representation):
#     assembly_code = []
#     memory_location = -4
#     for line in intermediate_representation:
#         if '=' in line:
#             left, right = line.split('=')
#             left = left.strip()
#             right = right.strip()
#             if '+' in right:
#                 operand1, operand2 = right.split('+')
#                 operand1 = operand1.strip()
#                 operand2 = operand2.strip()
#                 if operand1.isdigit():
#                     assembly_code.append(f'mov eax, {operand1}')
#                 else:
#                     assembly_code.append(f'mov eax, DWORD PTR [rbp{memory_location}]')
#                 if operand2.isdigit():
#                     assembly_code.append(f'add eax, {operand2}')
#                 else:
#                     assembly_code.append(f'add eax, DWORD PTR [rbp{memory_location}]')
#                 memory_location -= 4
#                 assembly_code.append(f'mov DWORD PTR [rbp{memory_location}], eax')
#             elif '*' in right:
#                 operand1, operand2 = right.split('*')
#                 operand1 = operand1.strip()
#                 operand2 = operand2.strip()
#                 if operand1.isdigit():
#                     assembly_code.append(f'mov eax, {operand1}')
#                 else:
#                     assembly_code.append(f'mov eax, DWORD PTR [rbp{memory_location}]')
#                 if operand2.isdigit():
#                     assembly_code.append(f'imul eax, {operand2}')
#                 else:
#                     assembly_code.append(f'imul eax, DWORD PTR [rbp{memory_location}]')
#                 memory_location -= 4
#                 assembly_code.append(f'mov DWORD PTR [rbp{memory_location}], eax')
#             elif '-' in right:
#                 operand1, operand2 = right.split('-')
#                 operand1 = operand1.strip()
#                 operand2 = operand2.strip()
#                 if operand1.isdigit():
#                     assembly_code.append(f'mov eax, {operand1}')
#                 else:
#                     assembly_code.append(f'mov eax, DWORD PTR [rbp{memory_location}]')
#                 if operand2.isdigit():
#                     assembly_code.append(f'sub eax, {operand2}')
#                 else:
#                     assembly_code.append(f'sub eax, DWORD PTR [rbp{memory_location}]')
#                 memory_location -= 4
#                 assembly_code.append(f'mov DWORD PTR [rbp{memory_location}], eax')
#             else:
#                 assembly_code.append(f'mov DWORD PTR [rbp{memory_location}], {right}')
#         elif 'return' in line:
#             assembly_code.append(f'mov eax, DWORD PTR [rbp{memory_location}]')

#     return assembly_code








def ir_to_asm(intermediate_representation):
    assembly_code = []
    memory_location = -4
    temp_vars = {}
    for line in intermediate_representation:
        if '=' in line:
            left, right = line.split('=')
            left = left.strip()
            right = right.strip()
            if '+' in right:
                operand1, operand2 = right.split('+')
                operand1 = operand1.strip()
                operand2 = operand2.strip()
                if operand1.isdigit():
                    assembly_code.append(f'mov eax, {operand1}')
                else:
                    assembly_code.append(f'mov eax, DWORD PTR [rbp{temp_vars[operand1]}]')
                if operand2.isdigit():
                    assembly_code.append(f'add eax, {operand2}')
                else:
                    assembly_code.append(f'add eax, DWORD PTR [rbp{temp_vars[operand2]}]')
                memory_location -= 4
                assembly_code.append(f'mov DWORD PTR [rbp{memory_location}], eax')
            elif '*' in right:
                operand1, operand2 = right.split('*')
                operand1 = operand1.strip()
                operand2 = operand2.strip()
                if operand1.isdigit():
                    assembly_code.append(f'mov eax, {operand1}')
                else:
                    assembly_code.append(f'mov eax, DWORD PTR [rbp{temp_vars[operand1]}]')
                if operand2.isdigit():
                    assembly_code.append(f'imul eax, {operand2}')
                else:
                    assembly_code.append(f'imul eax, DWORD PTR [rbp{temp_vars[operand2]}]')
                memory_location -= 4
                assembly_code.append(f'mov DWORD PTR [rbp{memory_location}], eax')
            elif '-' in right:
                operand1, operand2 = right.split('-')
                operand1 = operand1.strip()
                operand2 = operand2.strip()
                if operand1.isdigit():
                    assembly_code.append(f'mov eax, {operand1}')
                else:
                    assembly_code.append(f'mov eax, DWORD PTR [rbp{temp_vars[operand1]}]')
                if operand2.isdigit():
                    assembly_code.append(f'sub eax, {operand2}')
                else:
                    assembly_code.append(f'sub eax, DWORD PTR [rbp{temp_vars[operand2]}]')
                memory_location -= 4
                assembly_code.append(f'mov DWORD PTR [rbp{memory_location}], eax')
            else:
                if right.isdigit():
                    assembly_code.append(f'mov DWORD PTR [rbp{memory_location}], {right}')
                else:
                    # assembly_code.append(f'mov DWORD PTR [rbp{memory_location}], DWORD PTR [rbp{temp_vars[right]}]')
                    pass
            temp_vars[left] = memory_location
        elif 'return' in line:
            assembly_code.append(f'mov eax, DWORD PTR [rbp{memory_location}]')

    return assembly_code









    
def convert_to_backend(ir, symbol_table):
    
    # print(ir)
    output = []
    output.extend(setup_preamble(ir))
    output.extend(ir_to_asm(ir))
    output.extend(setup_postamble(ir))

    print_backend(output)
    print_asm_to_file(output)


def print_backend(backend):
    print("\n-------------- x86 Code --------------")
    for line in backend:
        # print(line)
        if line == "main:":
            print(line)
        else:
            print("    ", line)


# print the output to an asm file
def print_asm_to_file(backend):
    with open('output.asm', 'w') as f:
        for line in backend:
            if line == "main:":
                f.write(line + '\n')
            else:
                f.write("    " + line + '\n')
