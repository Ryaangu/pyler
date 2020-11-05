from enum import Enum

# Operand Codes
class OpCode(Enum):

    Return       = 0
    Constant     = 1
    Print        = 2
    False_       = 3
    True_        = 4
    Null         = 5
    Add          = 6
    Subtract     = 7
    Multiply     = 8
    Divide       = 9
    Negate       = 10
    Not          = 11
    NotEqual     = 12
    Greater      = 13
    GreaterThan  = 14
    Less         = 15
    LessThan     = 16
    Equals       = 17
    And          = 18
    Or           = 19
    JumpIfFalse  = 20
    Jump         = 21
    Pop          = 22
    SetGlobal    = 23
    GetGlobal    = 24