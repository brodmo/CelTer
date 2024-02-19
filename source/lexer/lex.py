from pathlib import Path
from .scanner import Scanner
from .tokens import Token, TokenType, GenericTokenType, \
    WhitespaceTokenType, MathTokenType, CompTokenType


TEST_FILE = Path(__file__).parents[1] / 'data' / 'test.ter'


def lex(code: str) -> list[Token]:
    scanner = Scanner(code)
    tokens = []
    while not scanner.done():
        if scanner.char.isspace():
            tt = lex_whitespace(scanner)
        elif scanner.char.isdigit():
            tt = lex_digits(scanner)
        elif scanner.char.isalpha():
            tt = lex_text(scanner)
        else:
            tt = lex_symbol(scanner)
        if tt is not None:
            tokens.append(Token(tt, scanner.pop_consumed()))
    tokens.append(Token(WhitespaceTokenType.EOF, ''))
    return tokens


def lex_whitespace(scanner: Scanner) -> TokenType | None:
    if scanner.char == '\n':
        scanner.consume()
        return WhitespaceTokenType.NEW_LINE
    return scanner.discard()


def lex_digits(scanner: Scanner) -> TokenType:
    while scanner.char.isdigit():
        scanner.consume()
    return GenericTokenType.NUMBER


def lex_text(scanner: Scanner) -> TokenType:
    pass


def lex_symbol(scanner: Scanner) -> TokenType:
    symbol_map = {  # math
        '+': lambda: MathTokenType.PLUS,
        '-': lambda: MathTokenType.MINUS
    } | {  # comp
        '<': lambda: lex_less(scanner),
    }
    # bool
    # brackets
    assert scanner.char in symbol_map
    return symbol_map[scanner.consume()]()


def lex_less(scanner):
    if scanner.char == '<':
        tt = GenericTokenType.OUTPUT
        scanner.consume()
    elif scanner.char == '=':
        tt = CompTokenType.EQUAL_LESS
        scanner.consume()
    else:
        tt = CompTokenType.STRICT_LESS
    return tt
