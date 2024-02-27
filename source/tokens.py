from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):

    def __new__(cls, symbol: str | None, precedence: int | None = None):
        self = object.__new__(cls)
        self._value_ = auto()
        self.symbol = symbol
        self.precedence = precedence
        return self

    NUMBER = None
    IDENTIFIER = None

    # whitespace
    EOF = None
    NEW_LINE = None

    # braces
    PAREN_OPEN = '('
    PAREN_CLOSE = ')'
    BRACKET_OPEN = '['
    BRACKET_CLOSE = ']'
    BRACE_OPEN = '{'
    BRACE_CLOSE = '}'

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
