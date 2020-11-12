from opcodes  import *
from tokens   import *
from scanner  import scanner_init, scan_token
from chunk    import Chunk, chunk_write, add_constant
from coloring import failure, success, warning
from interpreter import interpreter_init, interpret

# Parser
class Parser():

    previous = None
    current  = None

    had_error = False

parser = Parser()

# Compiler
class Compiler():
    
    chunk = Chunk()
    scope_depth = 0

    global_variables = []
    local_variables  = []

global current
current = None

# Initialize compiler
def compiler_init(compiler):

    # Set current compiler
    global current
    current = compiler

# Get current chunk
def current_chunk():
    return current.chunk

# Error at Token
def error_at(kind, message, token):

    # Already have an error? 
    if (parser.had_error): return
    parser.had_error = True

    # Make the error message and print it to the screen
    error_message = "[{0}:{1}] {2}".format(token.line, token.column, kind)

    if (token.kind == TOKEN_END):
        error_message += " at end"
    elif (token.kind == TOKEN_ERROR):
        error_message += ""
    else:
        error_message += " at '{0}'".format(token.content)

    error_message += ":\n>>\t{0}".format(message)
    print(failure(error_message))

# Error at previous token
def error(kind, message):
    error_at(kind, message, parser.previous)

# Error at current token
def error_current(kind, message):
    error_at(kind, message, parser.current)

# Begin scope
def begin_scope():
    current.scope_depth += 1

# End scope
def end_scope():
    current.scope_depth -= 1

    # Clear local variables array
    if (current.scope_depth == 0):
        current.local_variables = []

# Advance Token
def advance():
    
    # Get the previous token
    parser.previous = parser.current

    # Error?
    while (True):
        
        # Get the current token
        parser.current = scan_token()

        # Error?
        if (parser.current.kind != TOKEN_ERROR): break
        error_current("Error", parser.current.content) 

# Check current kind
def check(kind):

    return (parser.current.kind == kind)

# Consume Token
def consume(kind, error, message):

    # Check current kind
    if (check(kind)):
        advance()
        return

    error_current(error, message)

# Check if current kind match
def match(kind):

    # Check
    if (not check(kind)): return False

    advance()
    return True

# Emit Byte
def emit_byte(byte):
    chunk_write(current_chunk(), byte, parser.previous.line, parser.previous.column)

# Emit Bytes
def emit_bytes(byte1, byte2):
    emit_byte(byte1)
    emit_byte(byte2)

# Make Constant
def make_constant(value):

    # Add constant to chunk
    constant = add_constant(current_chunk(), value)
    return constant

# Emit Constant
def emit_constant(value):
    emit_bytes(OP_CONSTANT, make_constant(value))

# Emit Operator
def emit_operator(kind):

    if (kind == TOKEN_PLUS):          emit_byte(OP_ADD)
    if (kind == TOKEN_MINUS):         emit_byte(OP_SUB)
    if (kind == TOKEN_STAR):          emit_byte(OP_MUL)
    if (kind == TOKEN_SLASH):         emit_byte(OP_DIV)
    if (kind == TOKEN_BANG_EQUAL):    emit_byte(OP_NOT_EQUAL)
    if (kind == TOKEN_GREATER):       emit_byte(OP_GREATER)
    if (kind == TOKEN_GREATER_EQUAL): emit_byte(OP_GREATER_THAN)
    if (kind == TOKEN_LESS):          emit_byte(OP_LESS)
    if (kind == TOKEN_LESS_EQUAL):    emit_byte(OP_LESS_THAN)
    if (kind == TOKEN_EQUAL_EQUAL):   emit_byte(OP_EQUALS)
    if (kind == TOKEN_AND):           emit_byte(OP_AND)
    if (kind == TOKEN_OR):            emit_byte(OP_OR)

# Emit Unary Operator
def emit_unary_operator(kind):

    if (kind == TOKEN_MINUS):  emit_byte(OP_NEGATE)
    elif (kind == TOKEN_BANG): emit_byte(OP_NOT)

# Emit Jump
def emit_jump(byte):
    
    emit_byte(byte)
    emit_byte(-1)   # Amount to jump

    # Return the offset of amount to jump
    return current_chunk().count - 1

# Patch Jump
def patch_jump(offset):

    # Calculate the amount to jump
    jump = current_chunk().count - offset - 1

    # Set the amount to jump
    current_chunk().code[offset] = jump

# Emit loop
def emit_loop(start):
    
    emit_byte(OP_LOOP)

    # Get the loop offset
    offset = current_chunk().count - start + 1

    emit_byte(offset)

# Get token number
def get_number():

    return float(parser.previous.content)

# Get token string
def get_string():

    return str(parser.previous.content[1 : parser.previous.length - 1])

# Get previous token
def get_previous():

    return parser.previous

# Grouping Expression
def grouping():
    expression()
    consume(TOKEN_RIGHT_PAREN, "Syntax Error", "Expect ')' after expression.")

# Literal
def literal():

    if (match(TOKEN_FALSE)):        emit_byte(OP_FALSE)         # false
    elif (match(TOKEN_TRUE)):       emit_byte(OP_TRUE)          # true
    elif (match(TOKEN_NULL)):       emit_byte(OP_NULL)          # null
    elif (match(TOKEN_NUMBER)):     emit_constant(get_number()) # Number
    elif (match(TOKEN_STRING)):     emit_constant(get_string()) # String
    elif (match(TOKEN_LEFT_PAREN)): grouping()                  # Grouping Expression
    elif (match(TOKEN_IDENTIFIER)): variable_assignment(True)   # Variable
    else:
        error_current("Syntax Error", "Unexpected token.")

# Unary
def unary():

    # !, -
    while (parser.current.kind in [TOKEN_BANG, TOKEN_MINUS]):

        advance()

        operator = parser.previous.kind
        unary()
        emit_unary_operator(operator)

    literal()

# Multiplication
def multiplication():

    unary()

    # /, *
    while (parser.current.kind in [TOKEN_SLASH, TOKEN_STAR]):
        
        advance()

        operator = parser.previous.kind
        unary()
        emit_operator(operator)

# Addition
def addition():

    multiplication()

    # -, +
    while (parser.current.kind in [TOKEN_MINUS, TOKEN_PLUS]):
        
        advance()

        operator = parser.previous.kind
        multiplication()
        emit_operator(operator)

# Comparison
def comparison():

    addition()

    # >, >=, <, <=, &&, ||
    while (parser.current.kind in [TOKEN_GREATER, TOKEN_GREATER_EQUAL, TOKEN_LESS, TOKEN_LESS_EQUAL, TOKEN_OR, TOKEN_AND]):
        
        advance()

        operator = parser.previous.kind
        addition()
        emit_operator(operator)

# Equality
def equality():

    comparison()

    # !=, ==
    while (parser.current.kind in [TOKEN_BANG_EQUAL, TOKEN_EQUAL_EQUAL]):
        
        advance()

        operator = parser.previous.kind
        comparison()
        emit_operator(operator)


# Expression
def expression():
    
    equality()

# Print Statement
def print_statement():
    
    expression()
    emit_byte(OP_PRINT)

    # Optional Semicolon
    match(TOKEN_SEMICOLON)

# Block
def block():

    # Begin scope
    begin_scope()

    # Loop until a matching '}'
    while (not match(TOKEN_RIGHT_BRACE) and not match(TOKEN_END)):
        statement()

    # No '}' found?
    if (parser.previous.kind == TOKEN_END):
        error_current("Syntax Error", "Expect '}' after statement.")

    # End scope
    end_scope()

# If Statement
def if_statement():

    # Expect '(' after 'if' keyword
    consume(TOKEN_LEFT_PAREN, "Syntax Error", "Expect '(' after 'if'.")

    # Condition
    grouping()

    # Emit body jump
    then_jump = emit_jump(OP_JUMP_IF_FALSE)
    emit_byte(OP_POP)

    # Statement
    statement()

    # Emit else jump
    else_jump = emit_jump(OP_JUMP)

    # Patch body jump
    patch_jump(then_jump)
    emit_byte(OP_POP)

    # Else Statement?
    if (match(TOKEN_ELSE)):
        statement()

    # Patch else jump
    patch_jump(else_jump)

# Variable assignment
def variable_assignment(is_expression = False):

    # Check if variable exists
    if (not (parser.previous.content in current.global_variables or parser.previous.content in current.local_variables)):
        error("Compile Error", "The variable '{0}' is not declared!".format(parser.previous.content))
        return

    # Make the variable
    variable = make_constant(parser.previous.content)

    # Get the opcodes
    opcode_set = OP_SET_GLOBAL
    opcode_get = OP_GET_GLOBAL

    if (current.scope_depth > 0): # Local
        opcode_set = OP_SET_LOCAL
        opcode_get = OP_GET_LOCAL

    # Declare the variable
    if (match(TOKEN_EQUAL)): 
        expression()
        emit_bytes(opcode_set, variable)

        # Is assigning inside an expression
        if (is_expression):
            emit_bytes(opcode_get, variable)
        else:
            # Optional Semicolon
            match(TOKEN_SEMICOLON)
    else:
        emit_bytes(opcode_get, variable)

# Variable declaration
def variable_declaration(force_global = False):

    # Check if variable exists
    if (parser.previous.content in current.global_variables or parser.previous.content in current.local_variables):
        error("Compile Error", "The variable '{0}' is already declared!".format(parser.previous.content))
        return

    # Expect identifier
    if (force_global):
        consume(TOKEN_IDENTIFIER, "Syntax Error", "Expect variable name after 'global'.")
    else:
        consume(TOKEN_IDENTIFIER, "Syntax Error", "Expect variable name after 'var'.")

    # Make the variable
    variable = make_constant(parser.previous.content)

    # Get the opcode
    opcode_set = OP_SET_GLOBAL

    if (current.scope_depth > 0 and not force_global): # Local
        opcode_set = OP_SET_LOCAL

    # Declare the variable
    if (current.scope_depth > 0 and not force_global):
        current.local_variables.append(parser.previous.content)
    else:
        current.global_variables.append(parser.previous.content)

    # Assignment?
    if (match(TOKEN_EQUAL)): 
        expression()
        emit_bytes(opcode_set, variable)

        # Optional Semicolon
        match(TOKEN_SEMICOLON)
    else:
        emit_byte(OP_NULL)
        emit_bytes(opcode_set, variable)

        # Optional Semicolon
        match(TOKEN_SEMICOLON)

# Expression Statement
def expression_statement():

    expression()

    # Optional Semicolon
    match(TOKEN_SEMICOLON)

# Statement
def statement():

    # Advance
    advance()

    # Check token kind
    token = parser.previous.kind

    if (token == TOKEN_PRINT):        # Print Statement
        print_statement()
    elif (token == TOKEN_IF):         # If Statement
        if_statement()
    elif (token == TOKEN_LEFT_BRACE): # Block
        block()
    elif (token == TOKEN_IDENTIFIER): # Variable Assignment
        variable_assignment()
    elif (token == TOKEN_VAR):        # Variable Declaration
        variable_declaration()
    elif (token == TOKEN_GLOBAL):     # Global Variable Declaration
        variable_declaration(True)
    else:
        error_current("Compile Error", "Expect statement.")

# Compile
def compile(source):

    # Initialize scanner
    scanner_init(source)

    # Initialize compiler
    compiler = Compiler()
    compiler_init(compiler)

    # Start Compiling
    advance()

    # Loop until source end
    while (not match(TOKEN_END) and not parser.had_error):
        statement()

    # Emit OP_EXIT
    emit_byte(OP_EXIT)

    # Interpret chunk
    if (not parser.had_error):
        interpreter_init(current_chunk())
        interpret()