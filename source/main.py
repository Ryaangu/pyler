from compiler    import compile, compiler
from interpreter import interpreter_init, interpret
from coloring    import success

# Get code input
code = ""
done = False
line = 1

while (not done):

    x = input("\033[94m{0}. ".format(line))
    if (x == "\\0"):
        done = True
    else:
        code += x + "\n"
        line += 1

print("\033[0m")

# Compile code
chunk = compile(code)

# Interpret chunk
if (not compiler.had_error): # Check for compile errors
    interpreter_init(chunk)
    interpret()