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
    The tree returned by this program is a full parse tree for the given c file. It retains syntax and structure based on the grammar above. 

###usage###:
    description: 
        this program takes in a c file and returns a parse tree for the given c file.

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
        -h or --help
            will print help information to the screen


    example usage:
        python3 compiler.py -t -p test_programs/mult_func.c
        python3 compiler.py -p test_programs/mult_declare_and_assign.c 
        python3 compiler.py -t test_programs/params.c 


###Caveats###:
    * the only return type that is supported is int 
    * the only data type that is supported is int 
    * conditionals are not supported
    * loops are not supported 
    * global variables are not supported
    * includes are not supported 
    