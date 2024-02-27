from pathlib import Path

from lexer.lex import lex
from parser.parse import Parser


TEST_FILE = Path(__file__).parents[1] / 'data' / 'test.ter'


def main():
    test_code = TEST_FILE.read_text()
    tree = Parser(lex(test_code)).parse()
    print(tree)


if __name__ == '__main__':
    main()
