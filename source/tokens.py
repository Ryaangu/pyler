# Token Types
TOKEN_ERROR = 0 # Error
TOKEN_END   = 1 # \0

TOKEN_IDENTIFIER = 2 # Identifier
TOKEN_NUMBER     = 3 # Number
TOKEN_STRING     = 4 # String

TOKEN_LEFT_PAREN    = 5  # ( 
TOKEN_RIGHT_PAREN   = 6  # )
TOKEN_LEFT_BRACE    = 7  # {
TOKEN_RIGHT_BRACE   = 8  # }
TOKEN_LEFT_BRACKET  = 9  # [
TOKEN_RIGHT_BRACKET = 10 # ]
TOKEN_COMMA        = 11 # ,
TOKEN_DOT          = 12 # .
TOKEN_MINUS        = 13 # -
TOKEN_PLUS         = 14 # +
TOKEN_SEMICOLON    = 15 # ;
TOKEN_SLASH        = 16 # /
TOKEN_STAR         = 17 # *
TOKEN_QUESTION     = 18 # ?
TOKEN_PERCENT      = 19 # %
TOKEN_COLON        = 20 # :

TOKEN_BANG          = 21 # !
TOKEN_BANG_EQUAL    = 22 # !=
TOKEN_EQUAL         = 23 # =
TOKEN_EQUAL_EQUAL   = 24 # ==
TOKEN_GREATER       = 25 # >
TOKEN_GREATER_EQUAL = 26 # >=
TOKEN_LESS          = 27 # <
TOKEN_LESS_EQUAL    = 28 # <=
TOKEN_PLUS_PLUS     = 29 # ++
TOKEN_MINUS_MINUS   = 30 # --
TOKEN_PLUS_EQUAL    = 31 # +=
TOKEN_MINUS_EQUAL   = 32 # -=
TOKEN_SLASH_EQUAL   = 33 # /=
TOKEN_STAR_EQUAL    = 34 # *=
TOKEN_PERCENT_EQUAL = 35 # %=

TOKEN_AND      = 36 # &&
TOKEN_ELSE     = 37 # else
TOKEN_FALSE    = 38 # false
TOKEN_FOR      = 39 # for
TOKEN_FUNCTION = 40 # function
TOKEN_IF       = 41 # if
TOKEN_NULL     = 42 # null
TOKEN_OR       = 43 # ||
TOKEN_PRINT    = 44 # print
TOKEN_RETURN   = 45 # return
TOKEN_TRUE     = 46 # true
TOKEN_WHILE    = 47 # while
TOKEN_GLOBAL   = 48 # global
TOKEN_VAR      = 49 # var

# Token
class Token():

    kind    = -1
    content = ""
    length  = 0
    line    = 0
    column  = 0

    # Initialize
    def __init__(self, kind, content, length, line, column):
        
        self.kind    = kind
        self.content = content
        self.length  = length
        self.line    = line
        self.column  = column