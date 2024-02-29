from pathlib import Path

DATA_DIR = Path(__file__).parents[1] / 'data'


class SourceFile:
    base: Path

    def __init__(self, name: str):
        self.base = (DATA_DIR / name).with_suffix('.ter')

    @property
    def ll(self):
        return self.base.with_suffix('.ll')

    @property
    def o(self):
        return self.base.with_suffix('.o')

    @property
    def binary(self):
        return self.base.with_suffix('')
