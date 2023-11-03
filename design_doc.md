##Compiler for a subset of the C programming langauge.##

###Symbols:###
    * int: the only supported data type 
    * ID: a sequence of letters 
    * parameters: a comma separated list of function parameters, each of which is an int followed by an ID  
    * statements: a list of statements that can include return, declaration, and assignment statements 
    * assignment: a statement that assigns a value to a previously declared variable
    * expression: a mathematical expression that can include terms separated by + or - operators
    * term: a mathematical term that can include factors separated by * or / operators 
    * factor: a mathematical factor that can be an ID, a NUMBER, or an expression enclosed in parentheses
    

###Grammar:###
    program -> function* 
    function -> 'int' ID '('parameters ')' '{' statements '}'
    parameters -> parameter (',' parameter)* | empty
    parameter -> 'int' ID
    statements -> 'return' expression ';' | declaration | assignment ';' 
    declaration -> 'int' ID ';'
    assignment -> ID '=' expression
    expression -> term (('+' | '-') term)*
    term -> factor (('*' | '/') term)*
    factor -> ID | NUMBER | '(' expression ')'

###tree###:
    The parse tree returned by this program is a full parse tree for the given c file. It retains syntax and structure based on the grammar above. 

###Intermediate Representation###:
    The intermediate representation returned by this program is a three address code that maintains the original semantic meaning of the program

###Optimization###
    The only two optimizations that are supported are constant folding and constant propagation. 
    optimizations are only supported for a single function. Optimizations performed on files with more than one function may break the IR

###usage###:
    description: 
        this program takes in a c file and parses that c file into a parse tree and then converts that parse tree into an intermediate representation with the option to optimize that intermediate representation

    dependencies:
        >= python3.8
        
        install dependencies:
            pip3 install -r requirements.txt
        
    usage:
        python3 compiler.py <cfile>
        
    options:
        -t or --tokenize
            will print the list of tokens in the input c file to the screen 
        -p or --parse
            will print the full parse tree to the screen as well as its associated symbol table
        -i 
            prints out the unoptimized intermediate representation
        -o or --optimize
            prints out the optimized intermediate representation
        -h or --help
            will print help information to the screen


    example usage:
        python3 compiler.py -t -p test_programs/mult_func.c
        python3 compiler.py -p -i -o test_programs/mult_declare_and_assign.c 
        python3 compiler.py -t test_programs/params.c 


###Caveats###:
    * the only return types that are supported are int and void 
    * the only data type that is supported is int 
    * for loops are not supported, but while loops are
    * includes are not supported 
    * optimizations will sometimes break if you try to assign a variable to itself. e.g. if you had "a = a + 3 + 4;" could lead to the first variable being optimized away
    * IR optimization is only supported on files with a single function
    