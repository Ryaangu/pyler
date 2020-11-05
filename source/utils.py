def is_alpha(c):
    return ((c >= 'a' and c <= 'z') or
            (c >= 'A' and c <= 'Z') or
            (c == '_'))

def is_digit(c):
    return (c >= '0' and c <= '9')