from compiler.compile import LlvmIrGenerator
from lexer.lex import lex
from parser.parse import Parser
from parser.tree import StringVisitor
from paths import SourceFile
from runner.run import run


def main():
    file = SourceFile('test')
    test_code = file.base.read_text()
    tokens = lex(test_code)
    block = Parser(tokens).parse_statement_block()
    print(StringVisitor().visit_root(block))
    module = LlvmIrGenerator().visit_root(block)
    file.ll.write_text('\n'.join(module._get_body_lines()))  # beware, no metadata
    run(file)


if __name__ == '__main__':
    main()
