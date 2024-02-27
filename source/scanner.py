from typing import Sequence


class Scanner[T]:
    _consumed_count: int
    _sequence: Sequence[T]
    _index: int

    def __init__(self, text: Sequence[T]):
        self._sequence = text
        self._index = 0
        self._consumed_count = 0

    def done(self) -> bool:
        return self._index >= len(self._sequence)

    @property
    def peek(self, offset: int = 0) -> T:
        return self._sequence[self._index + offset]

    def consume(self) -> T:
        char = self.peek
        self._index += 1
        self._consumed_count += 1
        return char

    def discard(self):
        self._index += 1

    def pop_consumed(self) -> T:
        consumed = self._sequence[self._index - self._consumed_count: self._index]
        self._consumed_count = 0
        return consumed
