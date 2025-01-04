from enum import Enum
from dataclasses import dataclass

TokenType = Enum("TokenType", [
    # Literals
    "NUMBER", "STRING", "IDENTIFIER",

    # Single-character tokens
    "LEFT_PAREN", "RIGHT_PAREN", "LEFT_BRACE", "RIGHT_BRACE",
    "COMMA", "DOT", "MINUS", "PLUS", "SEMICOLON", "SLASH", "STAR",

    # One or two character tokens
    "BANG", "BANG_EQUAL",
    "EQUAL", "EQUAL_EQUAL",
    "GREATER", "GREATER_EQUAL",
    "LESS", "LESS_EQUAL",

    # Keywords
    "AND", "CLASS", "ELSE", "FALSE", "FOR", "FUN", "IF", "NIL", "OR",
    "PRINT", "RETURN", "SUPER", "THIS", "TRUE", "VAR", "WHILE",

    # Special
    "EOF"
])

@dataclass
class Token():
    type: TokenType
    lexeme: str
    literal: str | int | float | None
    line: int