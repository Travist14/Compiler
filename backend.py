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

#     for line in ir:

#         if type(line) == list:
#             continue
#         elif "+" in line:
#             op1 = line.split(" ")[0]
#             op2 = line.split(" ")[2]

#             if is_register(op1):
#                 if is_register(op2):
#                     asm_lines.append(Line(instruction=f"add {op1}, {op2}"))
#                 else:
#                     asm_lines.append(Line(instruction=f"add {op1}, [rbp-{op2}]"))
#             else:
#                 if is_register(op2):
#                     asm_lines.append(Line(instruction=f"add [rbp-{op1}], {op2}"))
#                 else:
#                     asm_lines.append(Line(instruction=f"add [rbp-{op1}], [rbp-{op2}]"))
#         elif "*" in line:
#             op1 = line.split(" ")[0]
#             op2 = line.split(" ")[2]
#             if is_register(op1):
#                 asm_lines.append(Line(instruction=f"imul {op1}, [rbp-{op2}]"))
#             else:
#                 asm_lines.append(Line(instruction=f"imul [rbp-{op1}], [rbp-{op2}]"))
#         elif "=" in line:
#             op1 = line.split(" ")[0]
#             op2 = line.split(" ")[2]
#             if is_register(op2):
#                 asm_lines.append(Line(instruction=f"mov {op1}, {op2}"))
#             else:
#                 asm_lines.append(Line(instruction=f"mov {op1}, [rbp-{op2}]"))

#     return asm_lines


def ir_to_asm(ir):
    asm_lines = []

    size = 0

    for line in ir:
        if type(line) == list:
            continue
        elif "=" in line:
            parts = line.split(" ")
            dest = parts[0]
            size += 4
            expr = parts[2:]

            if "+" in expr or "-" in expr or "*" in expr or "/" in expr:
                # Arithmetic operation
                asm_lines.append(Line(instruction="mov", op1=expr[0], op2=f"[rbp-{size}]"))
                asm_lines.append(Line(instruction="add", op1=expr[2], op2=f"[rbp-{size}]"))

            else:
                # Assignment of a constant
                asm_lines.append(Line(instruction="mov", op1=expr[0], op2=f"[rbp-{size}]"))

    return asm_lines

    
def convert_to_backend(ir, symbol_table):
    
    output = []
    output.extend(setup_preamble(ir))
    output.extend(ir_to_asm(ir))
    output.extend(setup_postamble(ir))
    for line in output:
        print(line)

def print_backend(backend):
    print("\n-------------- x86 Code --------------")
    for line in backend:
        if ":" in line:
            print(line)
        else:
            print("    " + line)