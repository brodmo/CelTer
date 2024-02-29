from abc import ABC, abstractmethod
from dataclasses import dataclass

from tokens import Token


def _assert_exclusive_choice(*args):
    assert len(list(map(lambda arg: arg is not None, args))) == 1


class Element(ABC):
    def accept(self, visitor: 'Visitor'):
        visitor.enter(self)
        result = self._simple_accept(visitor)
        visitor.exit(self)
        return result

    @abstractmethod
    def _simple_accept(self, visitor: 'Visitor'):
        pass


@dataclass(frozen=True)
class Root(Element):
    lines: list['Line']

    def _simple_accept(self, visitor: 'Visitor'):
        return visitor.visit_root(self)


@dataclass(frozen=True)
class Line(Element):
    line_content: 'LineContent'
    new_line_token: Token

    def _simple_accept(self, visitor: 'Visitor'):
        return self.line_content.accept(visitor)


class LineContent(Element, ABC):
    pass


@dataclass(frozen=True)
class Output(LineContent):
    output_token: Token
    expression: 'Expression'

    def _simple_accept(self, visitor: 'Visitor'):
        return visitor.visit_output(self)


class Expression(LineContent, ABC):
    pass


@dataclass(frozen=True)
class ParenExpression(Expression):
    paren_open_token: Token
    expression: Expression
    paren_close_token: Token

    def _simple_accept(self, visitor: 'Visitor'):
        return self.expression.accept(visitor)


@dataclass(frozen=True)
class Binary(Expression):
    left: Expression
    op_token: Token
    right: Expression

    def _simple_accept(self, visitor: 'Visitor'):
        return visitor.visit_binary(self)


@dataclass(frozen=True)
class Number(Expression):
    number_token: Token

    def _simple_accept(self, visitor: 'Visitor'):
        return visitor.visit_number(self)


class Visitor[T](ABC):

    def enter(self, element: Element):
        pass

    def exit(self, element: Element):
        pass

    def visit_root(self, root: Root) -> T:
        for line in root.lines:
            line.accept(self)
        return None

    def visit_output(self, output: Output) -> T:
        output.expression.accept(self)
        return None

    def visit_binary(self, binary: Binary) -> T:
        binary.left.accept(self)
        binary.right.accept(self)
        return None

    def visit_number(self, number: Number) -> T:
        return None


class StringVisitor(Visitor[str]):

    def visit_root(self, root: Root) -> str:
        return ''.join(
            line.accept(self) + line.new_line_token.text
            for line in root.lines
        )

    def visit_output(self, output: Output) -> str:
        return output.output_token.text + ' ' + output.expression.accept(self)

    def visit_binary(self, binary: Binary) -> str:
        return f'({binary.left.accept(self)} {binary.op_token.text} {binary.right.accept(self)})'

    def visit_number(self, number: Number) -> str:
        return number.number_token.text
