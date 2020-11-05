from enum import Enum

# Token Types
class TokenType(Enum):

    Error = 0 # Error
    End   = 1 # \0

    Identifier = 2 # Identifier
    Number     = 3 # Number
    String     = 4 # String

    LeftParen    = 5  # ( 
    RightParen   = 6  # )
    LeftBrace    = 7  # {
    RightBrace   = 8  # }
    LeftBracket  = 9  # [
    RightBracket = 10 # ]
    Comma        = 11 # ,
    Dot          = 12 # .
    Minus        = 13 # -
    Plus         = 14 # +
    Semicolon    = 15 # ;
    Slash        = 16 # /
    Star         = 17 # *
    Question     = 18 # ?
    Percent      = 19 # %
    Colon        = 20 # :

    Bang         = 21 # !
    BangEqual    = 22 # !=
    Equal        = 23 # =
    EqualEqual   = 24 # ==
    Greater      = 25 # >
    GreaterEqual = 26 # >=
    Less         = 27 # <
    LessEqual    = 28 # <=
    PlusPlus     = 29 # ++
    MinusMinus   = 30 # --
    PlusEqual    = 31 # +=
    MinusEqual   = 32 # -=
    SlashEqual   = 33 # /=
    StarEqual    = 34 # *=
    PercentEqual = 35 # %=

    And      = 36 # and &&
    Else     = 37 # else
    False_   = 38 # false
    For      = 39 # for
    Function = 40 # function
    If       = 41 # if
    Null     = 42 # null
    Or       = 43 # or ||
    Print    = 44 # print
    Return   = 45 # return
    True_    = 46 # true
    While    = 47 # while

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