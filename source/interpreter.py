from opcodes  import *
from coloring import failure, success, warning
from utils    import to_number

# Interpreter
class Interpreter():

    stack       = []
    stack_count = 0

    chunk = None

    index     = 0
    had_error = False

    global_variables = {}
    local_variables  = []

interpreter = Interpreter()

# Runtime Error
def runtime_error(message):

    # Set had error to true
    interpreter.had_error = True

    # Get line and column
    line   = interpreter.chunk.lines[interpreter.index - 1]
    column = interpreter.chunk.columns[interpreter.index - 1]

    # Show the error message
    error_message = "[{0}:{1}] Runtime Error:".format(line, column)
    error_message += "\n>>\t{0}".format(message)
    print(failure(error_message))

# Push to the stack
def push(value):
    
    # Set that stack slot to the push value and increase stack count
    interpreter.stack[interpreter.stack_count] = value
    interpreter.stack_count += 1

# Pop from the stack
def pop():

    # Get the pop value
    value = interpreter.stack[interpreter.stack_count - 1]

    # Decrease stack count and set that stack slot to 0
    interpreter.stack_count -= 1
    interpreter.stack[interpreter.stack_count] = 0

    # Return the pop value
    return value

# Peek
def peek(distance):

    # Get the value at distance
    return interpreter.stack[(interpreter.stack_count - 1) - distance]

# Read byte
def read_byte():

    # Increase index and return the old index value
    interpreter.index += 1
    return interpreter.chunk.code[interpreter.index - 1]

# Read Jump
def read_jump():

    # Increase index and return the old index value
    interpreter.index += 1
    return (interpreter.chunk.code[interpreter.index - 1])

# Read Constant
def read_constant():

    # Read constant and return it
    return interpreter.chunk.constants[read_byte()]

# Binary Op
def binary_op(operator):

    # Type checking
    if (type(peek(0)) != float or type(peek(1)) != float):
        runtime_error("Operands must be two numbers.")
        return

    # Pop values to be calculated
    b = float(pop())
    a = float(pop())

    # Calculate
    if (operator == OP_ADD): push(float(a + b)) # Addition
    if (operator == OP_SUB): push(float(a - b)) # Subtraction
    if (operator == OP_MUL): push(float(a * b)) # Multiplication
    if (operator == OP_DIV): push(float(a / b)) # Division

    if (operator == OP_LESS):         push(bool(a <  b)) # Less
    if (operator == OP_LESS_THAN):    push(bool(a <= b)) # Less than
    if (operator == OP_GREATER):      push(bool(a >  b)) # Greater
    if (operator == OP_GREATER_THAN): push(bool(a >= b)) # Greater than

# Unary Op
def unary_op(operator):

    # Type checking
    if (type(peek(0)) != float):
        runtime_error("Operand must be a number.")
        return

    # Pop value to be calculated
    a = float(pop())

    # Calculate
    if (operator == OP_NEGATE): push(float(-a)) # Negative

# Initialize Interpreter
def interpreter_init(chunk):

    interpreter.chunk = chunk

    for i in range(255):
        i = i
        interpreter.stack.append(0)
        interpreter.local_variables.append(0.0)

# Interpret bytecode
def interpret():

    # Start interpreting
    while (not interpreter.had_error):

        # Get OpCode
        byte = read_byte()

        # Constant
        if (byte == OP_CONSTANT): push(read_constant())

        # Boolean Constants
        if (byte == OP_TRUE):  push(True)  # true
        if (byte == OP_FALSE): push(False) # false
        if (byte == OP_NULL):  push(None)  # null

        # Add
        if (byte == OP_ADD):

            # Type checking
            if (not(type(peek(0)) == type(peek(1)))):
                runtime_error("Operands must be the same type.")
                return

            # Pop values to be calculated
            b = pop()
            a = pop()

            # Calculate
            if (type(a) == str):   push(str(a + b))   # String
            if (type(a) == float): push(float(a + b)) # Number

        # Subtract
        if (byte == OP_SUB): binary_op(OP_SUB)

        # Multiply
        if (byte == OP_MUL): binary_op(OP_MUL)

        # Divide
        if (byte == OP_DIV): binary_op(OP_DIV)

        # Negate
        if (byte == OP_NEGATE): unary_op(OP_NEGATE)

        # Not
        if (byte == OP_NOT): 
            
            # Type checking
            if (type(peek(0)) != bool):
                runtime_error("Operand must be a boolean.")
                return

            # Pop value to be compared
            a = bool(pop())

            # Push new boolean
            push(bool(not a))

        # Not Equal
        if (byte == OP_NOT_EQUAL):

            # Type checking
            if (not(type(peek(0)) == type(peek(1)))):
                runtime_error("Operands must be the same type.")
                return

            # Pop values to be compared
            b = pop()
            a = pop()

            # Compare
            if (type(a) == str):   push(bool(not (a == b))) # String
            if (type(a) == float): push(bool(not (a == b))) # Number

        # Less
        if (byte == OP_LESS): binary_op(OP_LESS)
        
        # Less Than
        if (byte == OP_LESS_THAN): binary_op(OP_LESS_THAN)

        # Greater
        if (byte == OP_GREATER): binary_op(OP_GREATER)

        # Greater Than
        if (byte == OP_GREATER_THAN): binary_op(OP_GREATER_THAN)

        # Equals
        if (byte == OP_EQUALS):

            # Type checking
            if (not(type(peek(0)) == type(peek(1)))):
                runtime_error("Operands must be the same type.")
                return

            # Pop values to be compared
            b = pop()
            a = pop()

            # Compare
            if (type(a) == float):  # Numbers
                push(bool(a == b))
            elif (type(a) == str):  # Strings
                push(bool(a == b))
            elif (type(a) == bool): # Booleans
                push(bool(a == b))
            else:
                runtime_error("Operands must be two numbers, two strings or two booleans.")
        
        # And
        if (byte == OP_AND):

            # Type checking
            if (type(peek(0)) != bool or type(peek(1)) != bool):
                runtime_error("Operands must be two booleans.")
                return

            # Pop values to be compared
            b = pop()
            a = pop()

            # Push new boolean
            push(bool(a and b))

        # Or
        if (byte == OP_OR):

            # Type checking
            if (type(peek(0)) != bool or type(peek(1)) != bool):
                runtime_error("Operands must be two booleans.")
                return

            # Pop values to be compared
            b = pop()
            a = pop()

            # Push new boolean
            push(bool(a or b))

        # Jump If False
        if (byte == OP_JUMP_IF_FALSE):

            # Read jump offset
            offset = read_jump()

            # If false, jump to that offset
            if (not bool(peek(0))): 
                interpreter.index += offset

        # Jump
        if (byte == OP_JUMP):

            # Read jump offset
            offset = read_jump()

            # Jump to that offset
            interpreter.index += offset

        # Pop
        if (byte == OP_POP):

            # Just pop
            pop()

        # Set Global
        if (byte == OP_SET_GLOBAL):

            # Read variable name
            name = str(read_constant())

            # Set variable value
            interpreter.global_variables[name] = pop()

        # Get Global
        if (byte == OP_GET_GLOBAL):

            # Read variable name
            name = str(read_constant())

            # Push variable value
            push(interpreter.global_variables[name])

        # Set Local
        if (byte == OP_SET_LOCAL):

            # Read variable slot
            slot = read_byte()

            # Set variable value
            interpreter.local_variables[slot] = pop()

        # Get Local
        if (byte == OP_GET_LOCAL):

            # Read variable slot
            slot = read_byte()

            # Push variable value
            push(interpreter.local_variables[slot])
            
        # Print
        if (byte == OP_PRINT): 
            
            # Pop value to be printed
            a = pop()

            # Print
            if (a == None):                        print("null")  # null
            elif (a == True  and type(a) == bool): print("true")  # true
            elif (a == False and type(a) == bool): print("false") # false
            elif (type(a) == str):                                # String

                # Split all new lines and print each one
                a = a.split("\\n")

                for i in range(len(a)):
                    print(a[i])
            else: # Anything
                print(a)

        # Loop
        if (byte == OP_LOOP):
            
            # Read jump offset
            offset = read_jump()

            # Go back to that offset
            interpreter.index -= offset

        # Exit
        if (byte == OP_EXIT):
            # Do nothing, just leave the loop
            break