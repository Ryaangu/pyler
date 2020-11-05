from tokens import TokenType, Token
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

# Keywords
keywords = {
    "and":      TokenType.And,
    "else":     TokenType.Else,
    "false":    TokenType.False_,
    "for":      TokenType.For,
    "function": TokenType.Function,
    "if":       TokenType.If,
    "null":     TokenType.Null,
    "or":       TokenType.Or,
    "print":    TokenType.Print,
    "return":   TokenType.Return,
    "true":     TokenType.True_,
    "while":    TokenType.While
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

    return Token(TokenType.Error, message, 
            len(message), scanner.line, scanner.column)

# Is scanner end?
def is_end():

    if (scanner.current >= scanner.length): return True
    return (scanner.source[scanner.current] == '\0')

# Advance scanner
def advance():

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
    return TokenType.Identifier

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
    return make_token(TokenType.Number)

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
    return make_token(TokenType.String)

# Scan Token
def scan_token():

    # Skip Whitespace
    skip_whitespace()
    scanner.start = scanner.current

    # Is End?
    if (is_end()):
        scanner.start = scanner.current + 1
        return make_token(TokenType.End)

    # Advance
    c = advance()

    # Check character(s)
    if (is_alpha(c)): return make_identifier() # Identifier
    if (is_digit(c)): return make_number()     # Number

    if (c == '('):   return make_token(TokenType.LeftParen)        # (
    elif (c == ')'): return make_token(TokenType.RightParen)       # )
    elif (c == '{'): return make_token(TokenType.LeftBrace)        # {
    elif (c == '}'): return make_token(TokenType.RightBrace)       # }
    elif (c == '['): return make_token(TokenType.LeftBracket)      # [
    elif (c == ']'): return make_token(TokenType.RightBracket)     # ]
    elif (c == ';'): return make_token(TokenType.Semicolon)        # ;
    elif (c == ','): return make_token(TokenType.Comma)            # ,
    elif (c == '.'): return make_token(TokenType.Dot)              # .
    elif (c == '?'): return make_token(TokenType.Question)         # ?
    elif (c == ':'): return make_token(TokenType.Colon)            # :
    elif (c == '-'): 
        if (match('-')): return make_token(TokenType.MinusMinus)   # --
        if (match('=')): return make_token(TokenType.MinusEqual)   # -=
        return make_token(TokenType.Minus)                         # -
    elif (c == '+'): 
        if (match('+')): return make_token(TokenType.PlusPlus)     # ++
        if (match('=')): return make_token(TokenType.PlusEqual)    # +=
        return make_token(TokenType.Plus)                          # +
    elif (c == '/'): 
        if (match('=')): return make_token(TokenType.SlashEqual)   # /=
        return make_token(TokenType.Slash)                         # /
    elif (c == '*'):
        if (match('=')): return make_token(TokenType.StarEqual)    # *=
        return make_token(TokenType.Star)                          # *
    elif (c == '%'):
        if (match('=')): return make_token(TokenType.PercentEqual) # %=
        return make_token(TokenType.Percent)                       # %
    elif (c == '!'): 
        if (match('=')): return make_token(TokenType.BangEqual)    # !=
        return make_token(TokenType.Bang)                          # !
    elif (c == '='): 
        if (match('=')): return make_token(TokenType.EqualEqual)   # ==
        return make_token(TokenType.Equal)                         # =
    elif (c == '<'): 
        if (match('=')): return make_token(TokenType.LessEqual)    # <=
        return make_token(TokenType.Less)                          # <
    elif (c == '>'): 
        if (match('=')): return make_token(TokenType.GreaterEqual) # >=
        return make_token(TokenType.Greater)                       # >
    elif (c == '&'):                                               
        if (match('&')): return make_token(TokenType.And)          # &&
    elif (c == '|'):                                               
        if (match('|')): return make_token(TokenType.Or)           # ||
    elif (c == '"'):
        return make_string()                                       # String

    # Unexpected character
    return make_error_token("Unexpected character '{0}'.".format(c))