# Chunk
class Chunk():

    count           = 0
    constants_count = 0

    code      = []
    lines     = []
    columns   = []
    constants = []

# Write to chunk
def chunk_write(chunk, byte, line, column):

    chunk.code.append(byte)
    chunk.lines.append(line)
    chunk.columns.append(column)

    chunk.count += 1

# Add constant to chunk
def add_constant(chunk, value):

    chunk.constants.append(value)
    chunk.constants_count += 1

    return (chunk.constants_count - 1)