from compiler import compile
from coloring import success
from pathlib  import Path

import sys

# Get command line arguments
if (len(sys.argv) == 1): # REPL
    
    # Get code input
    code = ""
    done = False
    line = 1

    while (not done):

        x = input("{0}. ".format(line))
        if (x == "\\0"):
            done = True
        else:
            code += x + "\n"
            line += 1

    # Compile
    compile(code)
elif (len(sys.argv) == 2): # Run file

    # Get file name
    file_name = sys.argv[1]

    # Read file
    try:
        f    = open(file_name, "r")
        code = f.read()

        # Compile
        compile(code)
    except FileNotFoundError:
        print("Failed to read file: '{0}'.".format(file_name))
else:
    print("Usage:\n\n\t- python main.py\n\t- python main.py file.pr")