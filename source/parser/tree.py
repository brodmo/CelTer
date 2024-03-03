from abc import ABC, abstractmethod
from dataclasses import dataclass

from tokens import Token


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
class StatementBlock(Element):
    lines: list['Statement']

    def _simple_accept(self, visitor: 'Visitor'):
        return visitor.visit_statement_block(self)


@dataclass(frozen=True)
class Statement(Element):
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


class Visitor[T](ABC):  # typing is a huge mess

    def visit_root(self, root: StatementBlock) -> T:
        return self.visit_statement_block(root)

    def enter(self, element: Element):
        pass

    def exit(self, element: Element):
        pass

    def visit_statement_block(self, statement_block: StatementBlock):
        for line in statement_block.lines:
            line.accept(self)
        return None

    def visit_output(self, output: Output):
        output.expression.accept(self)
        return None

    def visit_binary(self, binary: Binary):
        binary.left.accept(self)
        binary.right.accept(self)
        return None

    def visit_number(self, number: Number):
        return None


class StringVisitor(Visitor[str]):
    def __init__(self):
        self._string = ''
        self._depth = 0

    def _format(self, *tokens: Token):
        self._string += self._depth * '  ' + ''.join(str(tok) + '\n' for tok in tokens)

    def visit_root(self, root: StatementBlock) -> str:
        self.visit_statement_block(root)
        return self._string

    def enter(self, _):
        self._depth += 1

    def exit(self, _):
        self._depth -= 1

    def visit_statement_block(self, root: StatementBlock):
        for line in root.lines:
            line.accept(self)
            self._format(line.new_line_token)
            self._string += '\n\n'

    def visit_output(self, output: Output):
        self._format(output.output_token)
        output.expression.accept(self)

    def visit_binary(self, binary: Binary):
        binary.left.accept(self)
        self._format(binary.op_token)
        binary.right.accept(self)

    def visit_number(self, number: Number):
        self._format(number.number_token)
