from opcodes  import OpCode
from tokens   import TokenType, Token
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

    error_message = "[{0}:{1}] ".format(token.line, token.column)
    length = len(error_message)
    error_message += kind

    if (token.kind == TokenType.End):
        error_message += " at end"
    elif (token.kind == TokenType.Error):
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
        if (compiler.current.kind != TokenType.Error): break
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
    emit_bytes(OpCode.Constant, make_constant(value))

# Emit Operator
def emit_operator(kind):

    if (kind == TokenType.Plus):         emit_byte(OpCode.Add)
    if (kind == TokenType.Minus):        emit_byte(OpCode.Subtract)
    if (kind == TokenType.Star):         emit_byte(OpCode.Multiply)
    if (kind == TokenType.Slash):        emit_byte(OpCode.Divide)
    if (kind == TokenType.BangEqual):    emit_byte(OpCode.NotEqual)
    if (kind == TokenType.Greater):      emit_byte(OpCode.Greater)
    if (kind == TokenType.GreaterEqual): emit_byte(OpCode.GreaterThan)
    if (kind == TokenType.Less):         emit_byte(OpCode.Less)
    if (kind == TokenType.LessEqual):    emit_byte(OpCode.LessThan)
    if (kind == TokenType.EqualEqual):   emit_byte(OpCode.Equals)
    if (kind == TokenType.And):          emit_byte(OpCode.And)
    if (kind == TokenType.Or):           emit_byte(OpCode.Or)

# Emit Unary Operator
def emit_unary_operator(kind):

    if (kind == TokenType.Minus):  emit_byte(OpCode.Negate)
    elif (kind == TokenType.Bang): emit_byte(OpCode.Not)

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
    consume(TokenType.RightParen, "Syntax Error", "Expect ')' after expression.")

# Literal
def literal():

    if (match(TokenType.False_)):       emit_byte(OpCode.False_)
    elif (match(TokenType.True_)):      emit_byte(OpCode.True_)
    elif (match(TokenType.Null)):       emit_byte(OpCode.Null)
    elif (match(TokenType.Number)):     emit_constant(get_number())
    elif (match(TokenType.String)):     emit_constant(get_string())
    elif (match(TokenType.LeftParen)):  grouping()
    elif (match(TokenType.Identifier)): variable_assignment(True)
    else:
        error_current("Syntax Error", "Unexpected token.")

# Unary
def unary():

    while (compiler.current.kind in [TokenType.Bang, TokenType.Minus]):

        advance()

        operator = compiler.previous.kind
        unary()
        emit_unary_operator(operator)

    literal()

# Multiplication
def multiplication():

    unary()

    while (compiler.current.kind in [TokenType.Slash, TokenType.Star]):
        
        advance()

        operator = compiler.previous.kind
        unary()
        emit_operator(operator)

# Addition
def addition():

    multiplication()

    while (compiler.current.kind in [TokenType.Minus, TokenType.Plus]):
        
        advance()

        operator = compiler.previous.kind
        multiplication()
        emit_operator(operator)

# Comparison
def comparison():

    addition()

    while (compiler.current.kind in [TokenType.Greater, TokenType.GreaterEqual, TokenType.Less, TokenType.LessEqual, TokenType.Or, TokenType.And]):
        
        advance()

        operator = compiler.previous.kind
        addition()
        emit_operator(operator)

# Equality
def equality():

    comparison()

    while (compiler.current.kind in [TokenType.BangEqual, TokenType.EqualEqual]):
        
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
    emit_byte(OpCode.Print)

    # Optional Semicolon
    match(TokenType.Semicolon)

# Block
def block():

    # Begin scope
    begin_scope()

    while (not match(TokenType.RightBrace) and not match(TokenType.End)):
        statement()

    if (compiler.previous.kind == TokenType.End):
        error_current("Syntax Error", "Expect '}' after statement.")

    # End scope
    end_scope()

# If Statement
def if_statement():

    consume(TokenType.LeftParen, "Syntax Error", "Expect '(' after 'if'.")
    grouping()

    then_jump = emit_jump(OpCode.JumpIfFalse)
    emit_byte(OpCode.Pop)
    statement()

    else_jump = emit_jump(OpCode.Jump)

    patch_jump(then_jump)
    emit_byte(OpCode.Pop)

    if (match(TokenType.Else)):
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
    opcode_set = OpCode.SetGlobal
    opcode_get = OpCode.GetGlobal

    if (compiler.scope_depth > 0): # Local
        opcode_set = OpCode.SetLocal
        opcode_get = OpCode.GetLocal

    # Declare the variable
    if (match(TokenType.Equal)): 
        expression()
        emit_bytes(opcode_set, variable)

        # Is assigning inside an expression
        if (is_expression):
            emit_bytes(opcode_get, variable)
        else:
            # Optional Semicolon
            match(TokenType.Semicolon)
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
        consume(TokenType.Identifier, "Syntax Error", "Expect variable name after 'global'.")
    else:
        consume(TokenType.Identifier, "Syntax Error", "Expect variable name after 'var'.")

    # Make the variable
    variable = make_constant(compiler.previous.content)

    # Get the opcode
    opcode_set = OpCode.SetGlobal

    if (compiler.scope_depth > 0 and not force_global): # Local
        opcode_set = OpCode.SetLocal

    # Declare the variable
    if (compiler.scope_depth > 0 and not force_global):
        compiler.local_variables.append(compiler.previous.content)
    else:
        compiler.global_variables.append(compiler.previous.content)

    if (match(TokenType.Equal)): 
        expression()
        emit_bytes(opcode_set, variable)

        # Optional Semicolon
        match(TokenType.Semicolon)
    else:
        emit_byte(OpCode.Null)
        emit_bytes(opcode_set, variable)

        # Optional Semicolon
        match(TokenType.Semicolon)

# Statement
def statement():

    # Advance
    advance()

    # Check token kind
    token = compiler.previous.kind

    if (token == TokenType.Print):
        print_statement()
    elif (token == TokenType.If):
        if_statement()
    elif (token == TokenType.LeftBrace):
        block()
    elif (token == TokenType.Identifier):
        variable_assignment()
    elif (token == TokenType.Var):
        variable_declaration()
    elif (token == TokenType.Global):
        variable_declaration(True)
    else:
        error("Compile Error", "Expect statement.")

# Compile
def compile(source):

    # Initialize scanner
    scanner_init(source)

    # Start Compiling
    advance()

    while (not match(TokenType.End) and not compiler.had_error):
        statement()

    # Return the compiler chunk
    return compiler.chunk