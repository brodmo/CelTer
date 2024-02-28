from tokens import Token, TokenType
from scanner import Scanner
from .tree import TokenTypeTree


def lex(code: str) -> list[Token]:
    tokens = []
    scanner = Scanner[str](code + '\n')
    symbol_tts = [tt for tt in list(TokenType) if tt.symbol is not None]
    symbol_tree = TokenTypeTree(list(symbol_tts), 0)
    while not scanner.done():
        if scanner.peek.isspace():
            tt = lex_whitespace(scanner)
        elif scanner.peek.isdigit():
            tt = lex_digits(scanner)
        elif scanner.peek.isalpha():
            tt = lex_text(scanner)
        else:
            tt = symbol_tree.walk(scanner)
        if tt is not None:
            tokens.append(Token(tt, scanner.pop_consumed()))
    tokens.append(Token(TokenType.EOF, ''))
    return tokens


def lex_whitespace(scanner: Scanner) -> TokenType | None:
    if scanner.peek == '\n':
        while not scanner.done() and scanner.peek == '\n':
            scanner.consume()
        return TokenType.NEW_LINE
    return scanner.discard()


def lex_digits(scanner: Scanner) -> TokenType:
    while scanner.peek.isdigit():
        scanner.consume()
    return TokenType.NUMBER


def lex_text(scanner: Scanner) -> TokenType:
    pass
