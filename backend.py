# define a class line that defines a line of x86 assembly code
class Line:
    pass

# function that gets the number of local variables in the ir
def num_local_variables(ir):
    # num = 0
    # for line in ir:
    #     if type(line) == list:
    #         continue
    #     elif line.startswith("int"):
    #         num += 1

    # return num
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
    output.append("")
    output.append("push rbp")
    output.append("mov rbp, rsp")
    output.append(f"sub rsp, {stack_space}") # reserve 32 bytes for local variables
    return output


def setup_postamble(ir):
    return ["pop rbp", "ret"]

def convert(ir, symbol_table):
    
    output = setup_preamble(ir)
    # print(output)

    output.extend(setup_postamble(ir))
    
    return output

def print_backend(backend):
    print("\n-------------- x86 Code --------------")
    for line in backend:
        if type(line) == list:
            print(line[0])
        else:
            print("    " + line)