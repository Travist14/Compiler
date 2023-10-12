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


# converts the assignment subtree into 3 address code
def convert_assignment_to_tac(assignments):
    tac = []
    for assignment in assignments:
        if 'children' in assignment:
            print(assignment)
            tac.append(assignment['children'][0]) # this will always be variable name
            tac.append(assignment['children'][1]) # this will always be equals sign 
      
    return tac

def convert_to_ir(tree, symbol_table):

    ir = []

    ir += find_assignments(tree)
    
    print_ir(ir)

    ir = convert_assignment_to_tac(ir)
