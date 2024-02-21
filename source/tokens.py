from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    symbol: str | None

    def __new__(cls, symbol: str):
        self = object.__new__(cls)
        self._value_ = auto()
        self.symbol = symbol
        return self

    NUMBER = None
    IDENTIFIER = None

    # whitespace
    EOF = None
    NEW_LINE = None

    # math
    PLUS = '+'
    MINUS = '-'

    # comp
    STRICT_LESS = '<'
    EQUAL_LESS = '<='

    # io
    OUTPUT = '<<'


@dataclass(frozen=True)
class Token:
    type: TokenType
    text: str

    def __repr__(self):
        return f'Token | {self}'

    def __str__(self):
        return self.type.name + ' ' + self.text.replace('\n', r'\n')
