from .scanner import Scanner
from .tokens import Token, TokenType, GenericTokenType, SymbolTokenType, TokenTypeTree


def lex(code: str) -> list[Token]:
    tokens = []
    scanner = Scanner(code)
    symbol_tree = TokenTypeTree(list(SymbolTokenType), 0)
    while not scanner.done():
        if scanner.char.isspace():
            tt = lex_whitespace(scanner)
        elif scanner.char.isdigit():
            tt = lex_digits(scanner)
        elif scanner.char.isalpha():
            tt = lex_text(scanner)
        else:
            tt = symbol_tree.walk(scanner)
        if tt is not None:
            tokens.append(Token(tt, scanner.pop_consumed()))
    tokens.append(Token(GenericTokenType.EOF, ''))
    return tokens


def lex_whitespace(scanner: Scanner) -> TokenType | None:
    if scanner.char == '\n':
        scanner.consume()
        return GenericTokenType.NEW_LINE
    return scanner.discard()


def lex_digits(scanner: Scanner) -> TokenType:
    while scanner.char.isdigit():
        scanner.consume()
    return GenericTokenType.NUMBER


def lex_text(scanner: Scanner) -> TokenType:
    pass
