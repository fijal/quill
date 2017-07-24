
""" Execute:

nolang-c <program.no>
"""

import sys

from nolang.interpreter import Interpreter
from nolang.parser import get_parser, ParsingState
from nolang.compiler import compile_module
from nolang.function import BuiltinFunction
from nolang.lexer import get_lexer
from nolang.objects.space import Space

def main(argv=None):
    if argv is None:
        argv = sys.argv
    if len(argv) != 2:
        print __doc__
        return 1
    return run_code(argv[1])

def magic_print(space, args_w):
    print space.str(args_w[0])

parser = get_parser()
lexer = get_lexer()
interpreter = Interpreter()
space = Space(interpreter)

def run_code(fname):
    try:
        source = open(fname).read()
    except (OSError, IOError):
        print "Error reading file %s" % fname
        return 1
    # XXX error handling
    ast = parser.parse(lexer.lex(source), ParsingState(source))
    builtins = [BuiltinFunction('print', magic_print, 1)]
    w_mod = compile_module(source, ast, builtins)
    w_mod.initialize(space)
    space.call_method(w_mod, 'main', [])
    return 0

if __name__ == '__main__':
    sys.exit(main())
