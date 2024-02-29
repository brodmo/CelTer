from llvmlite import ir

from parser.tree import Binary, Number, Output, Root, Visitor
from tokens import TokenType


class LlvmIrGenerator(Visitor[ir.values.Value]):
    def __init__(self):
        self.integer = ir.IntType(64)
        self.module = ir.Module(name=__file__)
        self.func = ir.Function(self.module, ir.FunctionType(self.integer, tuple()), name="main")
        block = self.func.append_basic_block()
        self.builder = ir.IRBuilder(block)

    def visit_root(self, root: Root) -> ir.values.Value:
        for line in root.lines:
            line.accept(self)
        self.builder.ret(self.integer(0))
        return self.func

    def visit_output(self, output: Output) -> ir.values.Value:
        return printf(self.builder, "%d\n", output.expression.accept(self))

    def visit_binary(self, binary: Binary) -> ir.values.Value:
        left = binary.left.accept(self)
        right = binary.right.accept(self)
        fun = {
            TokenType.PLUS: self.builder.add,
            TokenType.MINUS: self.builder.sub,
            TokenType.MUL: self.builder.mul
        }[binary.op_token.type]
        return fun(left, right)

    def visit_number(self, number: Number) -> ir.values.Value:
        return self.integer(int(number.number_token.text))


def make_bytearray(buf):
    byt = bytearray(buf)
    return ir.Constant(ir.ArrayType(ir.IntType(8), len(byt)), byt)


int32_t = ir.IntType(32)
voidptr_t = ir.IntType(8).as_pointer()


# https://github.com/numba/numba/blob/c699ef8679316f40af8d0678219fa197522a741f/numba/cgutils.py#L975
def printf(builder: ir.IRBuilder, format_: str, *args):
    fmt_bytes = make_bytearray((format_ + '\00').encode('ascii'))
    fmt_ptr = builder.alloca(fmt_bytes.type)  # no idea if this is needed
    builder.store(fmt_bytes, fmt_ptr)
    try:
        fn = builder.module.get_global('printf')
    except KeyError:
        fnty = ir.FunctionType(int32_t, [voidptr_t], var_arg=True)
        fn = ir.Function(builder.module, fnty, name="printf")
    fmt_ptr_void = builder.bitcast(fmt_ptr, voidptr_t)
    return builder.call(fn, [fmt_ptr_void] + list(args))
