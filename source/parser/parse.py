from tokens import Token, TokenType
from .tree import Element, Node, Leaf

from scanner import Scanner


class Parser:
    scanner: Scanner[Token]

    def __init__(self, tokens: list[Token]):
        self.scanner = Scanner[Token](tokens)

    def parse(self) -> Element:
        lines = []
        while self._next_type != TokenType.EOF:
            lines.append(self.parse_line())
            assert self.scanner.consume().type == TokenType.NEW_LINE
        return Node(lines)

    def parse_line(self) -> Element:
        if self.scanner.peek.type == TokenType.OUTPUT:
            return self.parse_output()
        return self.parse_expression()

    def parse_output(self) -> Element:
        return Node([
            Leaf(self.scanner.consume()),
            self.parse_expression()
        ])

    def parse_expression(self, precedence: int = 0) -> Element:
        def valid_operator():
            next_precedence = self._next_type.precedence
            return next_precedence is not None and next_precedence >= precedence
        left = self.parse_primary()
        while valid_operator():
            operator = self.scanner.consume()
            # pass same precedence for right associativity
            right = self.parse_expression(operator.type.precedence + 1)
            left = Node([left, Leaf(operator), right])
        return left

    @property
    def _next_type(self) -> TokenType:
        return self.scanner.peek.type

    def parse_primary(self) -> Element:
        if self.scanner.peek.type == TokenType.PAREN_OPEN:
            self.scanner.consume()
            inner = self.parse_expression()
            assert self.scanner.consume().type == TokenType.PAREN_CLOSE
        else:
            inner = self.parse_number()
        return inner

    def parse_number(self) -> Element:
        assert self.scanner.peek.type == TokenType.NUMBER
        return Leaf(self.scanner.consume())
