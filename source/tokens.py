from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):

    def __new__(cls, symbol: str | None, precedence: int | None):
        self = object.__new__(cls)
        self._value_ = auto()
        self.symbol = symbol
        self.precedence = precedence
        return self

    NUMBER = None, None
    IDENTIFIER = None, None

    # whitespace
    EOF = None, None
    NEW_LINE = None, None

    # math
    PLUS = '+', 5
    MINUS = '-', 5
    MUL = '*', 6
    DIV = '/', 6

    # comp
    STRICT_LESS = '<', 10
    EQUAL_LESS = '<=', 10

    # io
    OUTPUT = '<<', None


@dataclass(frozen=True)
class Token:
    type: TokenType
    text: str

    def __repr__(self):
        return f'Token | {self}'

    def __str__(self):
        return self.type.name + ' ' + self.text.replace('\n', r'\n')
