from opcodes  import *
from tokens   import *
from scanner  import scanner_init, scan_token
from chunk    import Chunk, chunk_write, add_constant
from coloring import failure, success, warning

# Compiler
class Compiler():
    
    chunk = Chunk()

    previous = None
    current  = None

    had_error   = False
    scope_depth = 0

    global_variables = []
    local_variables  = []

compiler = Compiler()

# Error at Token
def error_at(kind, message, token):
    if (compiler.had_error): return
    compiler.had_error = True

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
    error_at(kind, message, compiler.previous)

# Error at current token
def error_current(kind, message):
    error_at(kind, message, compiler.current)

# Begin scope
def begin_scope():
    compiler.scope_depth += 1

# End scope
def end_scope():
    compiler.scope_depth -= 1

    # Clear local variables array
    if (compiler.scope_depth == 0):
        compiler.local_variables = []

# Advance Token
def advance():
    
    # Get the previous token
    compiler.previous = compiler.current

    # Error?
    while (True):
        
        # Get the current token
        compiler.current = scan_token()

        # Error?
        if (compiler.current.kind != TOKEN_ERROR): break
        error_current("Error", compiler.current.content) 

# Check current kind
def check(kind):

    return (compiler.current.kind == kind)

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
    chunk_write(compiler.chunk, byte, compiler.previous.line, compiler.previous.column)

# Emit Bytes
def emit_bytes(byte1, byte2):
    emit_byte(byte1)
    emit_byte(byte2)

# Make Constant
def make_constant(value):

    # Add constant to chunk
    constant = add_constant(compiler.chunk, value)
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
    return compiler.chunk.count - 1

# Patch Jump
def patch_jump(offset):

    # Calculate the amount to jump
    jump = compiler.chunk.count - offset - 1

    # Set the amount to jump
    compiler.chunk.code[offset] = jump

# Get token number
def get_number():

    return float(compiler.previous.content)

# Get token string
def get_string():

    return str(compiler.previous.content[1 : compiler.previous.length - 1])

# Get previous token
def get_previous():

    return compiler.previous

# Grouping Expression
def grouping():
    expression()
    consume(TOKEN_RIGHT_PAREN, "Syntax Error", "Expect ')' after expression.")

# Literal
def literal():

    if (match(TOKEN_FALSE)):        emit_byte(OP_FALSE)
    elif (match(TOKEN_TRUE)):       emit_byte(OP_TRUE)
    elif (match(TOKEN_NULL)):       emit_byte(OP_NULL)
    elif (match(TOKEN_NUMBER)):     emit_constant(get_number())
    elif (match(TOKEN_STRING)):     emit_constant(get_string())
    elif (match(TOKEN_LEFT_PAREN)): grouping()
    elif (match(TOKEN_IDENTIFIER)): variable_assignment(True)
    else:
        error_current("Syntax Error", "Unexpected token.")

# Unary
def unary():

    while (compiler.current.kind in [TOKEN_BANG, TOKEN_MINUS]):

        advance()

        operator = compiler.previous.kind
        unary()
        emit_unary_operator(operator)

    literal()

# Multiplication
def multiplication():

    unary()

    while (compiler.current.kind in [TOKEN_SLASH, TOKEN_STAR]):
        
        advance()

        operator = compiler.previous.kind
        unary()
        emit_operator(operator)

# Addition
def addition():

    multiplication()

    while (compiler.current.kind in [TOKEN_MINUS, TOKEN_PLUS]):
        
        advance()

        operator = compiler.previous.kind
        multiplication()
        emit_operator(operator)

# Comparison
def comparison():

    addition()

    while (compiler.current.kind in [TOKEN_GREATER, TOKEN_GREATER_EQUAL, TOKEN_LESS, TOKEN_LESS_EQUAL, TOKEN_OR, TOKEN_AND]):
        
        advance()

        operator = compiler.previous.kind
        addition()
        emit_operator(operator)

# Equality
def equality():

    comparison()

    while (compiler.current.kind in [TOKEN_BANG_EQUAL, TOKEN_EQUAL_EQUAL]):
        
        advance()

        operator = compiler.previous.kind
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

    while (not match(TOKEN_RIGHT_BRACE) and not match(TOKEN_END)):
        statement()

    if (compiler.previous.kind == TOKEN_END):
        error_current("Syntax Error", "Expect '}' after statement.")

    # End scope
    end_scope()

# If Statement
def if_statement():

    consume(TOKEN_LEFT_PAREN, "Syntax Error", "Expect '(' after 'if'.")
    grouping()

    then_jump = emit_jump(OP_JUMP_IF_FALSE)
    emit_byte(OP_POP)
    statement()

    else_jump = emit_jump(OP_JUMP)

    patch_jump(then_jump)
    emit_byte(OP_POP)

    if (match(TOKEN_ELSE)):
        statement()

    patch_jump(else_jump)

# Variable assignment
def variable_assignment(is_expression = False):

    # Check if variable exists
    if (not (compiler.previous.content in compiler.global_variables or compiler.previous.content in compiler.local_variables)):
        error("Compile Error", "The variable '{0}' is not declared!".format(compiler.previous.content))
        return

    # Make the variable
    variable = make_constant(compiler.previous.content)

    # Get the opcodes
    opcode_set = OP_SET_GLOBAL
    opcode_get = OP_GET_GLOBAL

    if (compiler.scope_depth > 0): # Local
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
    if (compiler.previous.content in compiler.global_variables or compiler.previous.content in compiler.local_variables):
        error("Compile Error", "The variable '{0}' is already declared!".format(compiler.previous.content))
        return

    # Expect identifier
    if (force_global):
        consume(TOKEN_IDENTIFIER, "Syntax Error", "Expect variable name after 'global'.")
    else:
        consume(TOKEN_IDENTIFIER, "Syntax Error", "Expect variable name after 'var'.")

    # Make the variable
    variable = make_constant(compiler.previous.content)

    # Get the opcode
    opcode_set = OP_SET_GLOBAL

    if (compiler.scope_depth > 0 and not force_global): # Local
        opcode_set = OP_SET_LOCAL

    # Declare the variable
    if (compiler.scope_depth > 0 and not force_global):
        compiler.local_variables.append(compiler.previous.content)
    else:
        compiler.global_variables.append(compiler.previous.content)

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

# Statement
def statement():

    # Advance
    advance()

    # Check token kind
    token = compiler.previous.kind

    if (token == TOKEN_PRINT):
        print_statement()
    elif (token == TOKEN_IF):
        if_statement()
    elif (token == TOKEN_LEFT_BRACE):
        block()
    elif (token == TOKEN_IDENTIFIER):
        variable_assignment()
    elif (token == TOKEN_VAR):
        variable_declaration()
    elif (token == TOKEN_GLOBAL):
        variable_declaration(True)
    else:
        error_current("Compile Error", "Expect statement.")

# Compile
def compile(source):

    # Initialize scanner
    scanner_init(source)

    # Start Compiling
    advance()

    while (not match(TOKEN_END) and not compiler.had_error):
        statement()

    # Emit OP_EXIT
    emit_byte(OP_EXIT)

    # Return the compiler chunk
    return compiler.chunk