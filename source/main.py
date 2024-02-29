from paths import SourceFile
from lexer.lex import lex
from parser.parse import Parser
from parser.tree import StringVisitor
from compiler.compile import LlvmIrGenerator
from runner.run import run


def main():
    file = SourceFile('test')
    test_code = file.base.read_text()
    tokens = lex(test_code)
    root = Parser(tokens).parse()
    print(root.accept(StringVisitor()))
    func = root.accept(LlvmIrGenerator())
    file.ll.write_text('\n'.join(func.module._get_body_lines()))  # no metadata for now
    run(file)


if __name__ == '__main__':
    main()
