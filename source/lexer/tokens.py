from dataclasses import dataclass
from enum import Enum

from .scanner import Scanner


class TokenType(Enum):
    pass


class GenericTokenType(TokenType):
    NUMBER = '0-9'
    IDENTIFIER = 'a-Z'

    # whitespace
    EOF = 'eof'
    NEW_LINE = r'\n'


class SymbolTokenType(TokenType):
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


class TokenTypeTree:
    token_type: TokenType | None
    sub_dict: dict[str, 'TokenTypeTree']

    def __init__(self, tts: list[TokenType], depth: int):
        self.token_type = None
        sub_dict_prep = {}
        for tt in tts:
            if len(tt.value) == depth:
                # tts share suffix -> here at most once
                assert not self.token_type
                self.token_type = tt
            else:
                sub_dict_prep.setdefault(tt.value[depth], []).append(tt)
        self.sub_dict = {
            char: TokenTypeTree(sub_tts, depth + 1)
            for char, sub_tts in sub_dict_prep.items()
        }  # sub_dict_prep ! fst -> TokenTypeTree[snd, depth + 1] ` Map

    def walk(self, scanner: Scanner) -> TokenType:
        if scanner.char in self.sub_dict:
            return self.sub_dict[scanner.consume()].walk(scanner)
        assert self.token_type
        return self.token_type

    def __repr__(self):
        return f'TTT | {str(self)}]'

    def __str__(self):
        return f'{self.token_type}, {self.sub_dict}'
