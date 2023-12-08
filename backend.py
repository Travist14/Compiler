import re
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Set, Collection, Dict, Optional, Tuple


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

def build_interference_graph(ir):
    graph = {}
    for line in ir:
        if '=' in line:
            left, right = line.split('=')
            left = left.strip()
            if left not in graph:
                graph[left] = set()
            for operand in right.split():
                if operand in graph:
                    graph[left].add(operand)
                    graph[operand].add(left)
    print(f"The graph is given by {graph}")
    return graph


def color_graph(graph, num_colors):
    colors = {}
    for node in graph:
        available_colors = set(range(num_colors))
        for neighbor in graph[node]:
            if neighbor in colors:
                available_colors.discard(colors[neighbor])
        if not available_colors:
            return None  # Graph is not colorable
        colors[node] = available_colors.pop()
    return colors


def allocate_registers(ir, num_registers):
    while True:
        graph = build_interference_graph(ir)
        colors = color_graph(graph, num_registers)
        if colors is not None:
            return {var: f"r{color}" for var, color in colors.items()}
        # Spill a variable to memory
        var_to_spill = min(graph, key=lambda var: len(graph[var]))
        # print(f"Spilling {var_to_spill}")
        ir = [line.replace(var_to_spill, f"[{var_to_spill}]") for line in ir]



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


def graph_coloring_ir_to_asm(intermediate_representation, num_registers):
    register_allocation = allocate_registers(intermediate_representation, num_registers)
    print(f"Register Allocation: {register_allocation}")
    
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
                    assembly_code.append(f'mov {register_allocation[left]}, {operand1}')
                else:
                    assembly_code.append(f'mov {register_allocation[left]}, {register_allocation[operand1]}')
                if operand2.isdigit():
                    assembly_code.append(f'add {register_allocation[left]}, {operand2}')
                else:
                    assembly_code.append(f'add {register_allocation[left]}, {register_allocation[operand2]}')
                memory_location -= 4
                assembly_code.append(f'mov DWORD PTR [rbp{memory_location}], {register_allocation[left]}')
            elif '*' in right:
                operand1, operand2 = right.split('*')
                operand1 = operand1.strip()
                operand2 = operand2.strip()
                if operand1.isdigit():
                    assembly_code.append(f'mov {register_allocation[left]}, {operand1}')
                else:
                    assembly_code.append(f'mov {register_allocation[left]}, {register_allocation[operand1]}')
                if operand2.isdigit():
                    assembly_code.append(f'imul {register_allocation[left]}, {operand2}')
                else:
                    assembly_code.append(f'imul {register_allocation[left]}, {register_allocation[operand2]}')
                memory_location -= 4
                assembly_code.append(f'mov DWORD PTR [rbp{memory_location}], {register_allocation[left]}')
            elif '-' in right:
                operand1, operand2 = right.split('-')
                operand1 = operand1.strip()
                operand2 = operand2.strip()
                if operand1.isdigit():
                    assembly_code.append(f'mov {register_allocation[left]}, {operand1}')
                else:
                    assembly_code.append(f'mov {register_allocation[left]}, {register_allocation[operand1]}')
                if operand2.isdigit():
                    assembly_code.append(f'sub {register_allocation[left]}, {operand2}')
                else:
                    assembly_code.append(f'sub {register_allocation[left]}, {register_allocation[operand2]}')
                memory_location -= 4
                assembly_code.append(f'mov DWORD PTR [rbp{memory_location}], {register_allocation[left]}')
            else:
                if right.isdigit():
                    assembly_code.append(f'mov DWORD PTR [rbp{memory_location}], {right}')
                else:
                    pass
            temp_vars[left] = memory_location
        elif 'return' in line:
            assembly_code.append(f'mov eax, DWORD PTR [rbp{memory_location}]')

    return assembly_code



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


from collections import defaultdict

def ir_to_asm_graph_coloring(intermediate_representation):
    assembly_code = []
    memory_location = -4

    # Build the interference graph
    interference_graph = defaultdict(list)
    for line in intermediate_representation:
        if "=" in line:
            left, right = line.split("=")
            left = left.strip()
            right = right.strip()
            for operand in right.split("+"):
                operand = operand.strip()
                if operand != left:
                    interference_graph[left].append(operand)
                    interference_graph[operand].append(left)

    # Perform graph coloring
    available_colors = list(range(4))  # Assuming 4 registers
    register_allocation = {}
    for variable in sorted(interference_graph, key=len, reverse=True):
        used_colors = set(register_allocation[neighbor]
                          for neighbor in interference_graph[variable]
                          if neighbor in register_allocation)
        for color in available_colors:
            if color not in used_colors:
                register_allocation[variable] = color
                available_colors.remove(color)
                break

    # Generate assembly code
    for line in intermediate_representation:
        if "=" in line:
            left, right = line.split("=")
            left = left.strip()
            right = right.strip()
            if "+" in right:
                operand1, operand2 = right.split("+")
                operand1 = operand1.strip()
                operand2 = operand2.strip()
                if operand1.isdigit():
                    assembly_code.append(f"mov eax, {operand1}")
                else:
                    assembly_code.append(f"mov eax, DWORD PTR [rbp{register_allocation[operand1]}]")
                if operand2.isdigit():
                    assembly_code.append(f"add eax, {operand2}")
                else:
                    assembly_code.append(f"add eax, DWORD PTR [rbp{register_allocation[operand2]}]")
                memory_location -= 4
                assembly_code.append(f"mov DWORD PTR [rbp{memory_location}], eax")
            elif "*" in right:
                operand1, operand2 = right.split("*")
                operand1 = operand1.strip()
                operand2 = operand2.strip()
                if operand1.isdigit():
                    assembly_code.append(f"mov eax, {operand1}")
                else:
                    assembly_code.append(f"mov eax, DWORD PTR [rbp{register_allocation[operand1]}]")
                if operand2.isdigit():
                    assembly_code.append(f"imul eax, {operand2}")
                else:
                    assembly_code.append(f"imul eax, DWORD PTR [rbp{register_allocation[operand2]}]")
                memory_location -= 4
                assembly_code.append(f"mov DWORD PTR [rbp{memory_location}], eax")
            elif "-" in right:
                operand1, operand2 = right.split("-")
                operand1 = operand1.strip()
                operand2 = operand2.strip()
                if operand1.isdigit():
                    assembly_code.append(f"mov eax, {operand1}")
                else:
                    assembly_code.append(f"mov eax, DWORD PTR [rbp{register_allocation[operand1]}]")
                if operand2.isdigit():
                    assembly_code.append(f"sub eax, {operand2}")
                else:
                    assembly_code.append(f"sub eax, DWORD PTR [rbp{register_allocation[operand2]}]")
                memory_location -= 4
                assembly_code.append(f"mov DWORD PTR [rbp{memory_location}], eax")
            else:
                if right.isdigit():
                    assembly_code.append(f"mov DWORD PTR [rbp{memory_location}], {right}")
                else:
                    assembly_code.append(f"mov DWORD PTR [rbp{memory_location}], DWORD PTR [rbp{register_allocation[right]}]")
                memory_location -= 4
            register_allocation[left] = memory_location
        elif "return" in line:
            assembly_code.append(f"mov eax, DWORD PTR [rbp{register_allocation[line.split()[1].strip()]}")

    return assembly_code




    
def convert_to_backend(ir, symbol_table):
    
    print("\n\n-------Janky Graph Coloring version---------")
    output = []
    output.extend(setup_preamble(ir))
    output.extend(graph_coloring_ir_to_asm(ir, 4))    
    output.extend(setup_postamble(ir))

    print_backend(output)


    print("\n")
    output2 = []
    output2.extend(setup_preamble(ir))
    output2.extend(ir_to_asm(ir))
    output2.extend(setup_postamble(ir))


    print_asm_to_file(output2)
    print_backend(output2)



    

    










































# ################################################ graph coloring attempt 2 that like kinda works but it doesn't acutally but I still want this code here for reference ################################################
# temp_vars = {}
# def ir_to_asm(intermediate_representation):
#     global temp_vars

#     assembly_code = []
#     interference_graph = {}
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
#                     assembly_code.append(f'mov eax, DWORD PTR [rbp{temp_vars[operand1]}]')
#                 if operand2.isdigit():
#                     assembly_code.append(f'add eax, {operand2}')
#                 else:
#                     assembly_code.append(f'add eax, DWORD PTR [rbp{temp_vars[operand2]}]')
#                 memory_location -= 4
#                 assembly_code.append(f'mov DWORD PTR [rbp{memory_location}], eax')
#             elif '*' in right:
#                 operand1, operand2 = right.split('*')
#                 operand1 = operand1.strip()
#                 operand2 = operand2.strip()
#                 if operand1.isdigit():
#                     assembly_code.append(f'mov eax, {operand1}')
#                 else:
#                     assembly_code.append(f'mov eax, DWORD PTR [rbp{temp_vars[operand1]}]')
#                 if operand2.isdigit():
#                     assembly_code.append(f'imul eax, {operand2}')
#                 else:
#                     assembly_code.append(f'imul eax, DWORD PTR [rbp{temp_vars[operand2]}]')
#                 memory_location -= 4
#                 assembly_code.append(f'mov DWORD PTR [rbp{memory_location}], eax')
#             elif '-' in right:
#                 operand1, operand2 = right.split('-')
#                 operand1 = operand1.strip()
#                 operand2 = operand2.strip()
#                 if operand1.isdigit():
#                     assembly_code.append(f'mov eax, {operand1}')
#                 else:
#                     assembly_code.append(f'mov eax, DWORD PTR [rbp{temp_vars[operand1]}]')
#                 if operand2.isdigit():
#                     assembly_code.append(f'sub eax, {operand2}')
#                 else:
#                     assembly_code.append(f'sub eax, DWORD PTR [rbp{temp_vars[operand2]}]')
#                 memory_location -= 4
#                 assembly_code.append(f'mov DWORD PTR [rbp{memory_location}], eax')
#             else:
#                 if right.isdigit():
#                     assembly_code.append(f'mov DWORD PTR [rbp{memory_location}], {right}')
#                 else:
#                     pass  # Handle other cases as needed
#             temp_vars[left] = memory_location

#             # Update interference graph
#             if left not in interference_graph:
#                 interference_graph[left] = set()

#             for var in [operand1, operand2]:
#                 if var and var != left:
#                     # Check if var is in interference_graph before adding left as a neighbor
#                     if var not in interference_graph:
#                         interference_graph[var] = set()
#                     interference_graph[left].add(var)
#                     interference_graph[var].add(left)

#     return assembly_code, interference_graph


# def calculate_spill_cost(node, interference_graph, colored_nodes):
#     # Example spill cost: the higher the degree (number of neighbors), the higher the cost
#     if node in interference_graph:
#         degree = len(interference_graph[node])
#     else:
#         # Set a default cost if the node is not in interference_graph
#         degree = 0
#     return degree


# def color_graph(interference_graph, temp_vars, registers):
#     colored_nodes = {}

#     while interference_graph:
#         node = min(interference_graph, key=lambda x: len(interference_graph[x]))
#         neighbors = interference_graph[node]

#         del interference_graph[node]
#         for neighbor in neighbors:
#             interference_graph[neighbor].remove(node)

#         available_registers = set(registers) - set(colored_nodes.values())
#         if available_registers:
#             colored_nodes[node] = available_registers.pop()
#         else:
#             # Spill to memory based on spill cost
#             spilled_node = min(colored_nodes, key=lambda x: calculate_spill_cost(x, interference_graph, colored_nodes))
#             colored_nodes[spilled_node] = f'DWORD PTR [rbp{temp_vars[spilled_node]}]'

#     return colored_nodes



# def convert_to_backend(ir, symbol_table):
#     global temp_vars

#     assembly_code, interference_graph = ir_to_asm(ir)
#     registers = ['eax', 'ebx', 'ecx']
#     colored_nodes = color_graph(interference_graph, temp_vars, registers)


#     print_backend(assembly_code)

#     print(f"Colored Nodes: {colored_nodes}")

#     for i, line in enumerate(assembly_code):
#         for temp_var, reg_or_mem in colored_nodes.items():
#             print(f"Replacing {temp_var} with {reg_or_mem}")
#             print(f"Assembly Code: {assembly_code[i]}")
#             assembly_code[i] = assembly_code[i].replace(f'[{temp_var}]', f'[{reg_or_mem}]')
#             print(f"Assembly Code: {assembly_code[i]}")

    
#     print_backend(assembly_code)

#     return assembly_code























    

    


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


















































# https://github.com/johnflanigan/graph-coloring-via-register-allocation/tree/master
class Dec:
    def __init__(self, reg: str, dead: bool):
        self.reg = reg
        self.dead = dead


class Use:
    def __init__(self, reg: str, dead: bool):
        self.reg = reg
        self.dead = dead

# register graph 
class Graph:
    
    def __init__(self):
        self.adjacency_list= {}
    
    
    # add an edge to the graph 
    def add_edge(self, x, y):
        # add y to x's list
        x_list = self.adjacency_list.get(x, [])
        if y not in x_list:
            x_list.append(y)
        self.adjacency_list[x] = x_list

        # add x to y's list
        y_list = self.adjacency_list.get(y, [])
        if x not in y_list:
            y_list.append(x)
        self.adjacency_list[y] = y_list


    def contains_edge(self, x, y):
        return y in self.adjacency_list.get(x, [])

    def remove_node(self, node):
        if node in self.adjacency_list:
            self.adjacency_list.pop(node)

        for key in self.adjacency_list.keys():
            if node in self.adjacency_list.get(key):
                self._adjacency_list.get(key).remove(node)

    def rename_node(self, from_label, to_label):
        from_list = self._adjacency_list.pop(from_label, [])
        to_list = self._adjacency_list.get(to_label, [])
        self._adjacency_list[to_label] = list(set(from_list + to_list))

        for key in self._adjacency_list.keys():
            self._adjacency_list[key] = list(set(
                [to_label if value == from_label else value for value in self._adjacency_list[key]]
            ))

    
    def neighbors(self, node):
        return self.adjacency_list.get(node, [])

    
    def plot(self, coloring, title):
        G = nx.Graph()

        # sort for repeatable graphs 
        nodes = sorted(self.adjacency_list.keys())
        ordered_coloring = [coloring.get(node, 'grey') for node in nodes]

        G.add_nodes_from(nodes)

        for key in self.adjacency_list.keys():
            for value in self.adjacency_list[key]:
                G.add_edge(key, value)


        plt.title(title)

        nx.draw(G, pos=nx.circular_layout(G), node_color=ordered_coloring, with_labels=True, font_weight='bold')
        plt.show()



def run(ir, colors: List[str]):
    graph, coloring = color_ir(ir, colors)

    if coloring is None:
        graph.plot({}, 'Initial')
        cost = estimate_spill_costs(il)
        spilled = decide_spills(il, graph, colors, cost)
        insert_spill_code(il, spilled)
        graph, coloring = color_il(il, colors)
        graph.plot({}, 'After Spilling')
        graph.plot(coloring, 'Colored')

    return graph, coloring


def color_ir(ir, colors: List[str]):
    graph = build_graph(ir)
    graph.plot({}, 'Initial')
    
    coalesce_nodes(ir, graph)

    coloring = color_graph(graph, il.registers(), colors)



