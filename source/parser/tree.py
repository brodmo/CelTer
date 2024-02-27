from abc import ABC, abstractmethod
from dataclasses import dataclass

from tokens import Token


class Element(ABC):
    @abstractmethod
    def str_depth(self, depth: int):
        pass


@dataclass(frozen=True)
class Node(Element):
    children: list['Element']

    def __str__(self):
        def valid(line: str) -> bool:
            return any(line) and not line.isspace()
        lines = self.str_depth(0).split('\n')
        return '\n'.join(filter(valid, lines))

    def str_depth(self, depth: int):
        prefix = '\n' + depth * '    '
        return ''.join(
            prefix + child.str_depth(depth + 1)
            for child in self.children
        )


@dataclass(frozen=True)
class Leaf(Element):
    token: Token

    def __str__(self):
        return str(self.token)

    def str_depth(self, depth: int):
        return str(self.token)
