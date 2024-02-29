from paths import SourceFile
from lexer.lex import lex
from parser.parse import Parser
from parser.tree import StringVisitor


def main():
    file = SourceFile('test')
    test_code = file.base.read_text()
    tokens = lex(test_code)
    root = Parser(tokens).parse()
    print(root.accept(StringVisitor()))


if __name__ == '__main__':
    main()
