from tokens import Token, TokenType
from .tree import Root, Line, Output, Expression, ParenExpression, Binary, Number

from scanner import Scanner


class Parser:
    scanner: Scanner[Token]

    def __init__(self, tokens: list[Token]):
        self.scanner = Scanner[Token](tokens)

    def parse(self) -> Root:
        lines = []
        while self._next_type != TokenType.EOF:
            lines.append(self.parse_line())
        return Root(lines)

    def parse_line(self) -> Line:
        if self.scanner.peek.type == TokenType.OUTPUT:
            content = self.parse_output()
        else:
            content = self.parse_expression()
        assert self.scanner.peek.type == TokenType.NEW_LINE
        return Line(content, self.scanner.consume())

    def parse_output(self) -> Output:
        return Output(self.scanner.consume(), self.parse_expression())

    def parse_expression(self, precedence: int = 0) -> Expression:
        def valid_operator():
            next_precedence = self._next_type.precedence
            return next_precedence is not None and next_precedence >= precedence
        left = self.parse_primary()
        while valid_operator():
            operator = self.scanner.consume()
            # pass same precedence for right associativity
            right = self.parse_expression(operator.type.precedence + 1)
            left = Binary(left, operator, right)
        return left

    @property
    def _next_type(self) -> TokenType:
        return self.scanner.peek.type

    def parse_primary(self) -> Expression:
        if self.scanner.peek.type == TokenType.PAREN_OPEN:
            paren_open = self.scanner.consume()
            inner = self.parse_expression()
            assert self.scanner.peek.type == TokenType.PAREN_CLOSE
            return ParenExpression(paren_open, inner, self.scanner.consume())
        else:
            inner = self.parse_number()
        return inner

    def parse_number(self) -> Number:
        assert self.scanner.peek.type == TokenType.NUMBER
        return Number(self.scanner.consume())
