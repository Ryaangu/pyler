from tokens import *
from utils  import is_digit, is_alpha

# Scanner
class Scanner():

    source  = ""
    length  = 0

    start   = 0
    current = 0

    line   = 1
    column = 1

scanner = Scanner()

# Keywords tokens
keywords = {
    "else":     TOKEN_ELSE,
    "false":    TOKEN_FALSE,
    "for":      TOKEN_FOR,
    "function": TOKEN_FUNCTION,
    "if":       TOKEN_IF,
    "null":     TOKEN_NULL,
    "print":    TOKEN_PRINT,
    "return":   TOKEN_RETURN,
    "true":     TOKEN_TRUE,
    "while":    TOKEN_WHILE,
    "global":   TOKEN_GLOBAL,
    "var":      TOKEN_VAR
}

# Initialize Scanner
def scanner_init(source):

    scanner.source = source
    scanner.length = len(source)

# Make Token
def make_token(kind):

    return Token(kind, scanner.source[scanner.start : scanner.current],
            scanner.current - scanner.start, scanner.line, scanner.column)

# Make Error Token
def make_error_token(message):

    return Token(TOKEN_ERROR, message, 
            len(message), scanner.line, scanner.column)

# Is scanner end?
def is_end():

    # Current index is bigger than source length
    if (scanner.current >= scanner.length): return True
    return (scanner.source[scanner.current] == '\0')

# Advance scanner
def advance():

    # Only advance if current index is not bigger than source length
    if (scanner.current < scanner.length): 
        scanner.current += 1
        scanner.column += 1

    return scanner.source[scanner.current - 1]

# Peek current character
def peek():

    if (is_end()): return '\0'
    return scanner.source[scanner.current]

# Peek next character
def peek_next():

    if (is_end()): return '\0'
    return scanner.source[scanner.current + 1]

# Current character matches the expected character?
def match(expected):

    if (is_end()):           return False
    if (peek() != expected): return False

    advance()
    return True

# Skip Whitespace
def skip_whitespace():

    while (True):

        c = peek()

        # Spacing
        if (c in " \r\t"):
            advance()
            break
        elif (c == '\n'): # New Line
            scanner.line += 1
            scanner.column = 1
            advance()
            break
        elif (c == '#'): # Comment
            # Loop until a new line
            while (peek() != '\n' and not is_end()):
                advance()

            # Jump the new line
            scanner.line += 1
            scanner.column = 1
            advance()
            break
        else:
            return

# Get identifier type
def identifier_type():

    # Get keyword name
    keyword = scanner.source[scanner.start : scanner.current]

    # Keyword exists?
    if (keyword in keywords):
        return keywords[keyword]
    
    # No keyword found, return identifier type
    return TOKEN_IDENTIFIER

# Make Identifier Token
def make_identifier():

    # Loop while an alpha or digit character
    while (is_alpha(peek()) or is_digit(peek())):
        advance()

    # Make the token and return it
    return make_token(identifier_type())

# Make Number Token
def make_number():

    # Loop while a digit
    while (is_digit(peek())):
        advance()

    # Fractional?
    if (peek() == '.' and is_digit(peek_next())):

        # Advance the dot part
        advance()

        # Loop while a digit
        while (is_digit(peek())):
            advance()

    # Make the token and return it
    return make_token(TOKEN_NUMBER)

# Make String Token
def make_string():

    # Loop until "
    while (peek() != '"' and not is_end()):

        # New line?
        if (peek() == '\n'): scanner.line += 1
        advance()

    # No matching "
    if (is_end()): return make_error_token("Unterminated string.")

    # Advance the " part
    advance()

    # Make the token and return it
    return make_token(TOKEN_STRING)

# Scan Token
def scan_token():

    # Skip Whitespace
    skip_whitespace()
    scanner.start = scanner.current

    # Is End?
    if (is_end()):
        scanner.start = scanner.current + 1
        return make_token(TOKEN_END)

    # Advance
    c = advance()

    # Check character(s)
    if (is_alpha(c)): return make_identifier() # Identifier
    if (is_digit(c)): return make_number()     # Number

    if (c == '('):   return make_token(TOKEN_LEFT_PAREN)       # (
    elif (c == ')'): return make_token(TOKEN_RIGHT_PAREN)      # )
    elif (c == '{'): return make_token(TOKEN_LEFT_BRACE)       # {
    elif (c == '}'): return make_token(TOKEN_RIGHT_BRACE)      # }
    elif (c == '['): return make_token(TOKEN_LEFT_BRACKET)     # [
    elif (c == ']'): return make_token(TOKEN_RIGHT_BRACKET)    # ]
    elif (c == ';'): return make_token(TOKEN_SEMICOLON)        # ;
    elif (c == ','): return make_token(TOKEN_COMMA)            # ,
    elif (c == '.'): return make_token(TOKEN_DOT)              # .
    elif (c == '?'): return make_token(TOKEN_QUESTION)         # ?
    elif (c == ':'): return make_token(TOKEN_COLON)            # :
    elif (c == '-'): 
        if (match('-')): return make_token(TOKEN_MINUS_MINUS)  # --
        if (match('=')): return make_token(TOKEN_MINUS_EQUAL)  # -=
        return make_token(TOKEN_MINUS)                         # -
    elif (c == '+'): 
        if (match('+')): return make_token(TOKEN_PLUS_PLUS)    # ++
        if (match('=')): return make_token(TOKEN_PLUS_EQUAL)   # +=
        return make_token(TOKEN_PLUS)                          # +
    elif (c == '/'): 
        if (match('=')): return make_token(TOKEN_SLASH_EQUAL)  # /=
        return make_token(TOKEN_SLASH)                         # /
    elif (c == '*'):
        if (match('=')): return make_token(TOKEN_STAR_EQUAL)   # *=
        return make_token(TOKEN_STAR)                          # *
    elif (c == '%'):
        if (match('=')): return make_token(TOKEN_PERCENT_EQUAL) # %=
        return make_token(TOKEN_PERCENT)                        # %
    elif (c == '!'): 
        if (match('=')): return make_token(TOKEN_BANG_EQUAL)   # !=
        return make_token(TOKEN_BANG)                          # !
    elif (c == '='): 
        if (match('=')): return make_token(TOKEN_EQUAL_EQUAL)  # ==
        return make_token(TOKEN_EQUAL)                         # =
    elif (c == '<'): 
        if (match('=')): return make_token(TOKEN_LESS_EQUAL)   # <=
        return make_token(TOKEN_LESS)                          # <
    elif (c == '>'): 
        if (match('=')): return make_token(TOKEN_GREATER_EQUAL) # >=
        return make_token(TOKEN_GREATER)                        # >
    elif (c == '&'):                                               
        if (match('&')): return make_token(TOKEN_AND)          # &&
    elif (c == '|'):                                               
        if (match('|')): return make_token(TOKEN_OR)           # ||
    elif (c == '"'):
        return make_string()  # String
    elif (c in " \r\t#\n"):
        # We probably found spacing here, so skip that spacing, scan again and 
        # return that scanned token
        skip_whitespace()
        return scan_token()

    # Unexpected character
    return make_error_token("Unexpected character '{0}'.".format(c))