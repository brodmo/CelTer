from pathlib import Path

from lexer.lex import lex


TEST_FILE = Path(__file__).parents[1] / 'data' / 'test.ter'


def main():
    test_code = TEST_FILE.read_text()
    print(lex(test_code))


if __name__ == '__main__':
    main()
