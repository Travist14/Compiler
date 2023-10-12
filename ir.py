# returns a list of declarations where every declaration is a subtree
def find_declarations(tree, declarations=[]):
    if tree['value'] == "DECLARATION":
        declarations.append(tree)
    if 'children' in tree:
        for child in tree['children']:
            declarations = find_declarations(child, declarations)

    return declarations


# returns a list of assignments where every assignment is a subtree
def find_assignments(tree, assignments=[]):
    if tree['value'] == "ASSIGNMENT":
        assignments.append(tree)
    if 'children' in tree:
        for child in tree['children']:
            assignments = find_assignments(child, assignments)

    return assignments


# prints every tree subtree
def print_tree(tree, indent=0):
    indentation = " " * indent
    # if tree['value'] not in ["DECLARATION", "ASSIGNMENT", "EXPR", "FACTOR", "TERM"]:
    #     print(f"{indentation}{tree['value']}")
    print(f"{indentation}{tree['value']}")
    if 'children' in tree:
        for child in tree['children']:
            print_tree(child, indent + 4)

# main function to print ir
def print_ir(ir):
    print("\n", "-" * 50, "IR", "-" * 50, "\n")
    for tree in ir:
        print_tree(tree) # this can conceptually be thought of as pringting lines


def convert_assign_to_tac(assignments):
    for assign in assignments:
        print(assign['children'][0]) # the variable will always be index 0
        print(assign['children'][1]) # the assignment operator "=" will always be index 1
        print(assign['children'][2]) # the expression will always be index 2
        print("\n")
        
        print(len(assign['children']))

def convert_to_ir(tree, symbol_table):

    print(tree)

    ir = [] # dont love ir as a list but works for right now, my intuition is that every entry is a line, also lists work well becuase I can reuse elements if needed 
    
    # ir += find_declarations(tree)
    # ir += find_assignments(tree)
    # print(ir)

    # print_ir(ir) 

    assigns = find_assignments(tree)
    convert_assign_to_tac(assigns)
    print_ir(assigns)
