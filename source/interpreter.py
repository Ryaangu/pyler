from opcodes  import OpCode
from coloring import failure, success, warning

# Interpreter
class Interpreter():

    stack       = []
    stack_count = 0

    chunk = None

    index = 0
    had_error = False

    variables = {}

interpreter = Interpreter()
last_constant = -1

# Runtime Error
def runtime_error(message):

    interpreter.had_error = True

    line   = interpreter.chunk.lines[interpreter.index - 1]
    column = interpreter.chunk.columns[interpreter.index - 1]

    error_message = "[{0}:{1}] ".format(line, column)
    length = len(error_message)
    error_message += "RuntimeError in main():"

    spaces = ""
    for i in range(length - 2):
        i = i
        spaces += " "

    error_message += "\n>>{0}{1}".format(spaces, message)
    print(failure(error_message))

# Push to the stack
def push(value):
    
    interpreter.stack[interpreter.stack_count] = value
    interpreter.stack_count += 1

# Pop from the stack
def pop():

    interpreter.stack_count -= 1
    v = interpreter.stack[interpreter.stack_count]
    interpreter.stack[interpreter.stack_count] = 0
    return v

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

    for i in range(64):
        i = i
        interpreter.stack.append(0)

# Interpret bytecode
def interpret():

    print("\033[92mResult:\n")

    # Start interpreting
    while (not is_end() and not interpreter.had_error):

        byte = read_byte()

        # Constant
        if (byte == OpCode.Constant): push(read_constant())

        # Boolean
        if (byte == OpCode.True_):  push(True)
        if (byte == OpCode.False_): push(False)
        if (byte == OpCode.Null):   push(None)

        # Add
        if (byte == OpCode.Add):

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
            else:
                runtime_error("Operands must be two numbers or a string and other value.")

        # Subtract
        if (byte == OpCode.Subtract): 

            b = pop()
            a = pop()

            if (not (type(a) == type(b))): 
                runtime_error("Operands must be the same type.")
                return

            if (type(a) == float):
                push(float(a - b))
            else:
                runtime_error("Operands must be two numbers.")

        # Multiply
        if (byte == OpCode.Multiply):

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
        if (byte == OpCode.Divide):

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
        if (byte == OpCode.Negate): 
            
            a = pop()

            if (type(a) == float):
                push(float(-a))
            else:
                runtime_error("Operand must be a number.")

        # Not
        if (byte == OpCode.Not): 
            
            a = pop()

            if (type(a) in [float, bool]):
                push(bool(not a))
            else:
                runtime_error("Operand must be a number or a boolean.")

        # Not Equal
        if (byte == OpCode.NotEqual):

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
        if (byte == OpCode.Greater):

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
        if (byte == OpCode.GreaterThan):

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
        if (byte == OpCode.Less):

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
        if (byte == OpCode.LessThan):

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
        if (byte == OpCode.Equals):

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
        if (byte == OpCode.And):

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
        if (byte == OpCode.Or):

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
        if (byte == OpCode.JumpIfFalse):

            offset = read_jump()
            if (not bool(peek(0))): interpreter.index += offset

        # Jump
        if (byte == OpCode.Jump):

            offset = read_jump()
            interpreter.index += offset

        # Pop
        if (byte == OpCode.Pop):
            pop()

        # Set Global
        if (byte == OpCode.SetGlobal):

            name = str(read_constant())
            interpreter.variables[name] = pop()

        # Get Global
        if (byte == OpCode.GetGlobal):

            name = str(read_constant())

            if (name in interpreter.variables):
                push(interpreter.variables[name])
            else:
                runtime_error("Undefined variable '{0}'.".format(name))

        # Print
        if (byte == OpCode.Print): 
            
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