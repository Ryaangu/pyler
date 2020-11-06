# Check if character is an alpha
def is_alpha(c):
    return ((c >= 'a' and c <= 'z') or
            (c >= 'A' and c <= 'Z') or
            (c == '_'))

# Check if character is a digit
def is_digit(c):
    return (c >= '0' and c <= '9')

# To number
def to_number(v):
    try:
        return float(v)
    except ValueError:
        return str(v)