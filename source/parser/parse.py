from tokens import Token, TokenType
from .tree import Element, Node, Leaf

from scanner import Scanner


class Parser:
    scanner: Scanner[Token]

    def __init__(self, tokens: list[Token]):
        self.scanner = Scanner[Token](tokens)

    def parse(self) -> Element:
        return self.parse_line()

    def parse_line(self) -> Element:
        if self.scanner.peek.type == TokenType.OUTPUT:
            return self.parse_output()
        else:
            return self.parse_expression()

    def parse_output(self) -> Element:
        return Node([
            Leaf(self.scanner.consume()),
            self.parse_expression()
        ])

    def parse_expression(self) -> Element:
        return self.parse_binary(self.parse_number())

    def parse_binary(self, lhs: Element) -> Element:
        if self.scanner.peek.type not in (TokenType.PLUS, TokenType.MINUS):
            return lhs
        node = Node([
            lhs, Leaf(self.scanner.consume()), self.parse_number()
        ])
        return self.parse_binary(node)

    def parse_number(self) -> Element:
        assert self.scanner.peek.type == TokenType.NUMBER
        return Leaf(self.scanner.consume())
