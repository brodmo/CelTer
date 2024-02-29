import subprocess as sp
from pathlib import Path

from paths import SourceFile


LLVM_BIN = Path('/opt/homebrew/opt/llvm/bin')


def run(file: SourceFile):
    generate_binary(file)
    run_binary(file)


def generate_binary(file: SourceFile):
    # or use lli
    sp.run([
        LLVM_BIN / 'llc',
        '-filetype=obj',
        file.ll,
        '-o',
        file.o
    ])
    sp.run([
        LLVM_BIN / 'clang',
        file.o,
        '-o',
        file.binary
    ])


def run_binary(file: SourceFile):
    sp.run(file.binary)
