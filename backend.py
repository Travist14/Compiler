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
#     asm_lines = []

#     size = 0

#     for line in ir:
#         if type(line) == list:
#             continue
#         elif "=" in line:
#             parts = line.split(" ")
#             dest = parts[0]
#             size += 4
#             expr = parts[2:]

#             if "+" in expr or "-" in expr or "*" in expr or "/" in expr:
#                 # Arithmetic operation
#                 asm_lines.append(Line(instruction="mov", op1=expr[0], op2=f"[rbp-{size}]"))
#                 asm_lines.append(Line(instruction="add", op1=expr[2], op2=f"[rbp-{size}]"))

#             else:
#                 # Assignment of a constant
#                 asm_lines.append(Line(instruction="mov", op1=expr[0], op2=f"[rbp-{size}]"))

#     return asm_lines

def ir_to_asm(ir):
    asm = []
    temp_counter = 0
    var_offset = 4

    for line in ir:
        if line[0].endswith(':'):
            # asm.append(line[0])
            continue
        else:
            tokens = line.split(' ')
            if tokens[1] == '=':
                if '+' in tokens:
                    asm.append(f'mov eax, DWORD PTR [rbp-{var_offset}]')
                    asm.append(f'add eax, {tokens[2]}')
                    asm.append(f'mov DWORD PTR [rbp-{var_offset}], eax')
                elif '*' in tokens:
                    asm.append(f'mov eax, DWORD PTR [rbp-{var_offset}]')
                    asm.append(f'lea edx, [0+rax*4]')
                    asm.append(f'mov DWORD PTR [rbp-{var_offset}], edx')
                elif '-' in tokens:
                    asm.append(f'mov eax, DWORD PTR [rbp-{var_offset}]')
                    asm.append(f'sub eax, {tokens[2]}')
                    asm.append(f'mov DWORD PTR [rbp-{var_offset}], eax')
                else:
                    asm.append(f'mov DWORD PTR [rbp-{var_offset}], {tokens[2]}')
                var_offset += 4
            else:
                asm.append(f'mov DWORD PTR [rbp-{var_offset}], {tokens[0]}')
                var_offset += 4

    return asm

    
def convert_to_backend(ir, symbol_table):
    
    print(ir)
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
