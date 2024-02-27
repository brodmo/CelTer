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
        return self.parse_expression()

    def parse_output(self) -> Element:
        return Node([
            Leaf(self.scanner.consume()),
            self.parse_expression()
        ])

    def parse_expression(self):
        return self.parse_binary(self.parse_primary(), 0)

    # https://en.wikipedia.org/wiki/Operator-precedence_parser#Precedence_climbing_method
    def parse_binary(self, lhs: Element, precedence: int) -> Element:
        def valid_operator(comp_precedence: int, equals_ok: bool):
            lookahead_precedence = self.scanner.peek.type.precedence
            return lookahead_precedence is not None and (
                lookahead_precedence >= comp_precedence if equals_ok
                else lookahead_precedence > comp_precedence
            )
        while valid_operator(precedence, equals_ok=True):
            operator = self.scanner.consume()
            rhs = self.parse_primary()
            op_precedence = operator.type.precedence
            while valid_operator(op_precedence, equals_ok=False):  # or right associative
                rhs = self.parse_binary(rhs, op_precedence + 1)  # + 0 if right associative
                op_precedence = self.scanner.peek.type.precedence
            lhs = Node([lhs, Leaf(operator), rhs])
        return lhs

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
