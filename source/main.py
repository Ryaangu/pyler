from compiler    import compile
from interpreter import interpreter_init, interpret
from coloring    import success

# Get code input
code = ""
done = False

while (not done):

    x = input(("\033[94m> "))
    if (x == "\\0"):
        done = True
    else:
        code += x + " "

print("\033[0m")

# Compile code
chunk = compile(code)

# Interpret chunk
interpreter_init(chunk)
interpret()