class Scanner:
    _consumed_count: int
    _text: str
    _index: int

    def __init__(self, text: str):
        self._text = text
        self._index = 0
        self._consumed_count = 0

    def done(self) -> bool:
        return self._index >= len(self._text)

    @property
    def char(self) -> str:
        return self._text[self._index]

    def consume(self) -> str:
        char = self.char
        self._index += 1
        self._consumed_count += 1
        return char

    def discard(self):
        self._index += 1

    def pop_consumed(self) -> str:
        consumed = self._text[self._index - self._consumed_count: self._index]
        self._consumed_count = 0
        return consumed
