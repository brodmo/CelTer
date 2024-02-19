from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    pass


class GenericTokenType(TokenType):
    NUMBER = auto()
    IDENTIFIER = auto()
    OUTPUT = auto()


class WhitespaceTokenType(TokenType):
    EOF = auto()
    NEW_LINE = auto()


class MathTokenType(TokenType):
    PLUS = auto()
    MINUS = auto()


class CompTokenType(TokenType):
    STRICT_LESS = auto()
    EQUAL_LESS = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    text: str
