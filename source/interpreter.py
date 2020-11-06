from opcodes  import *
from coloring import failure, success, warning
from utils    import to_number

# Interpreter
class Interpreter():

    stack       = []
    stack_count = 0

    chunk = None

    index = 0
    had_error = False

    global_variables = {}
    local_variables  = []

interpreter = Interpreter()
last_constant = -1

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

    return interpreter.stack[distance]

# Is code end?
def is_end():

    return (interpreter.index >= interpreter.chunk.count)

# Read byte
def read_byte():

    if (interpreter.index < interpreter.chunk.count):
        interpreter.index += 1

    return interpreter.chunk.code[interpreter.index - 1]

# Read Jump
def read_jump():
    interpreter.index += 1
    return (interpreter.chunk.code[interpreter.index - 1])

# Read Constant
def read_constant():
    return interpreter.chunk.constants[read_byte()]

# Initialize Interpreter
def interpreter_init(chunk):

    interpreter.chunk = chunk

    for i in range(1000):
        i = i
        interpreter.stack.append(0)
        interpreter.local_variables.append(0)

# Interpret bytecode
def interpret():

    print("\033[92mResult:\n")

    # Start interpreting
    while (not is_end() and not interpreter.had_error):

        byte = read_byte()

        # Constant
        if (byte == OP_CONSTANT): push(read_constant())

        # Boolean
        if (byte == OP_TRUE):  push(True)
        if (byte == OP_FALSE): push(False)
        if (byte == OP_NULL):  push(None)

        # Add
        if (byte == OP_ADD):

            b = pop()
            a = pop()

            # Shitty way to remove '.0' from string
            if (type(a) == str and type(b) == float):
                b = str(b)
                if (b[-2] == '.' and int(b[-1]) == 0):
                    b = b[0 : -2]

            # Shitty way to add null instead of None
            if (b == None):
                b = "null"

            if (type(a) == str):
                push(str(a + str(b)))
            elif (type(a) == float and type(b) == float):
                push(float(a + b))
            elif (type(a) == float and type(b) == str):
                b = to_number(b)

                # Can't convert value to a number
                if (type(b) == str):
                    runtime_error("Can't convert '{0}' to number.".format(b))
                    return

                push(float(a + b))

            else:
                runtime_error("Operands must be two numbers, a number and a string or a string and other value.")

        # Subtract
        if (byte == OP_SUB): 

            b = pop()
            a = pop()

            if (type(a) == float and type(b) == float):
                push(float(a - b))
            elif (type(a) == float and type(b) == str):
                b = to_number(b)

                # Can't convert value to a number
                if (type(b) == str):
                    runtime_error("Can't convert '{0}' to number.".format(b))
                    return

                push(float(a - b))
            else:
                runtime_error("Operands must be two numbers or a number and a string.")

        # Multiply
        if (byte == OP_MUL):

            b = pop()
            a = pop()

            if (not (type(a) == type(b))): 
                runtime_error("Operands must be the same type.")
                return

            if (type(a) == float):
                push(float(a * b))
            else:
                runtime_error("Operands must be two numbers.")

        # Divide
        if (byte == OP_DIV):

            b = pop()
            a = pop()

            if (not (type(a) == type(b))): 
                runtime_error("Operands must be the same type.")
                return

            if (type(a) == float):
                push(float(a / b))
            else:
                runtime_error("Operands must be two numbers.")

        # Negate
        if (byte == OP_NEGATE): 
            
            a = pop()

            if (type(a) == float):
                push(float(-a))
            else:
                runtime_error("Operand must be a number.")

        # Not
        if (byte == OP_NOT): 
            
            a = pop()

            if (type(a) in [float, bool]):
                push(bool(not a))
            else:
                runtime_error("Operand must be a number or a boolean.")

        # Not Equal
        if (byte == OP_NOT_EQUAL):

            b = pop()
            a = pop()

            if (not (type(a) == type(b))): 
                runtime_error("Operands must be the same type.")
                return

            if ((type(a) == float and type(b) == float) or (type(a) == str and type(b) == str) or (type(a) == bool and type(b) == bool)):
                push(bool(not (a == b)))
            else:
                runtime_error("Operands must be two numbers or two strings or two booleans.")

        # Greater
        if (byte == OP_GREATER):

            b = pop()
            a = pop()

            if (not (type(a) == type(b))): 
                runtime_error("Operands must be the same type.")
                return

            if (type(a) == float):
                push(bool(a > b))
            else:
                runtime_error("Operands must be two numbers.")

        # Greater Than
        if (byte == OP_GREATER_THAN):

            b = pop()
            a = pop()

            if (not (type(a) == type(b))): 
                runtime_error("Operands must be the same type.")
                return

            if (type(a) == float):
                push(bool(a >= b))
            else:
                runtime_error("Operands must be two numbers.")

        # Less
        if (byte == OP_LESS):

            b = pop()
            a = pop()

            if (not (type(a) == type(b))): 
                runtime_error("Operands must be the same type.")
                return

            if (type(a) == float):
                push(bool(a < b))
            else:
                runtime_error("Operands must be two numbers.")
        
        # Less Than
        if (byte == OP_LESS_THAN):

            b = pop()
            a = pop()

            if (not (type(a) == type(b))): 
                runtime_error("Operands must be the same type.")
                return

            if (type(a) == float):
                push(bool(a <= b))
            else:
                runtime_error("Operands must be two numbers.")

        # Equals
        if (byte == OP_EQUALS):

            b = pop()
            a = pop()

            if (not (type(a) == type(b))): 
                runtime_error("Operands must be the same type.")
                return

            if (type(a) == float):
                push(bool(a == b))
            elif (type(a) == str):
                push(bool(a == b))
            elif (type(a) == bool):
                push(bool(a == b))
            else:
                runtime_error("Operands must be two numbers or two strings or two booleans.")
        
        # And
        if (byte == OP_AND):

            b = pop()
            a = pop()

            if (not (type(a) == type(b))): 
                runtime_error("Operands must be the same type.")
                return

            if (type(a) == bool):
                push(bool(a and b))
            else:
                runtime_error("Operands must be two booleans.")

        # Or
        if (byte == OP_OR):

            b = pop()
            a = pop()

            if (not (type(a) == type(b))): 
                runtime_error("Operands must be the same type.")
                return

            if (type(a) == bool):
                push(bool(a or b))
            else:
                runtime_error("Operands must be two booleans.")

        # Jump If False
        if (byte == OP_JUMP_IF_FALSE):

            offset = read_jump()
            if (not bool(peek(0))): interpreter.index += offset

        # Jump
        if (byte == OP_JUMP):

            offset = read_jump()
            interpreter.index += offset

        # Pop
        if (byte == OP_POP):
            pop()

        # Set Global
        if (byte == OP_SET_GLOBAL):

            name = str(read_constant())
            interpreter.global_variables[name] = pop()

        # Get Global
        if (byte == OP_GET_GLOBAL):

            name = str(read_constant())
            push(interpreter.global_variables[name])

        # Set Local
        if (byte == OP_SET_LOCAL):

            slot = read_byte()
            interpreter.local_variables[slot] = pop()

        # Get Local
        if (byte == OP_GET_LOCAL):

            slot = read_byte()
            push(interpreter.local_variables[slot])
            
        # Print
        if (byte == OP_PRINT): 
            
            a = pop()

            # Shitty way to show null instead of None
            if (a == None):
                print("null")
            elif (a == True):
                print("true")
            elif (a == False):
                print("false")
            elif (type(a) == str):
                a = a.split("\\n")

                for i in range(len(a)):
                    print(a[i])
            else:
                print(str(a))

    print("\033[0m")