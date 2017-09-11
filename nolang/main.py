
""" Execute:

nolang-c <program.no>
nolang-c -c <spec to compile>
nolang-c -s <spec to run>
"""

import os
import sys

from rpython.rlib.objectmodel import we_are_translated

from nolang.interpreter import Interpreter
from nolang.parser import get_parser, ParsingState, ParseError
from nolang.compiler import compile_module
from nolang.builtins.defaults import default_builtins
from nolang.lexer import get_lexer
from nolang import assembly
from nolang.frameobject import format_traceback
from nolang.importer import Importer
from nolang.objects.space import Space
from nolang.error import AppError, InterpreterError


def dirname(p):
    """Returns the directory component of a pathname"""
    i = p.rfind(os.path.sep) + 1
    assert i >= 0
    head = p[:i]
    if head and head != os.path.sep * len(head):
        head = head.rstrip(os.path.sep)
    return head


def path_split(p):
    """Split a pathname.  Returns tuple "(head, tail)" where "tail" is
    everything after the final slash.  Either part may be empty."""
    i = p.rfind('/') + 1
    assert i >= 0
    head, tail = p[:i], p[i:]
    if head and head != '/' * len(head):
        head = head.rstrip('/')
    return head, tail


def main(argv):
    try:
        if len(argv) == 2:
            return run_code(argv[1])
        if len(argv) == 1:
            # run repl here
            print __doc__
            return 0
        if len(argv) == 3 and argv[1] == '-c':
            return assembly.compile_assembly(space, argv[2])
        if len(argv) == 3 and argv[2] == '-s':
            return run_spec(argv[1])
    except InterpreterError as e:
        print e.repr()
        if not we_are_translated(): # get a full traceback interpreted
            raise
        return 1
    except ParseError as pe:
        format_parser_error(pe)
        return 1
    except AppError as e:
        os.write(2, format_traceback(space, e))
        return 1
    print __doc__
    return 1


lexer = get_lexer()
parser = get_parser(lexer)
space = Space(parser)
space.setup_builtins(*default_builtins(space))


def format_parser_error(pe):
    print "Error parsing input file %s, line %d: %s" % (pe.filename, pe.lineno,
        pe.msg)
    print "  " + pe.line
    print "  " + " " * pe.start_colno + "^" * (pe.end_colno - pe.start_colno)


def parse_name(fname):
    name = path_split(fname)[-1]
    p = name.rfind(".")
    if p > 0:
        name = name[:p]
    name = name.replace(".", "_")  # explode?
    return "self." + name


def run_code(fname):
    interpreter = Interpreter()
    space.setup(interpreter)
    try:
        source = open(fname).read()
    except (OSError, IOError):
        print "Error reading file %s" % fname
        return 1
    ast = parser.parse(lexer.lex(fname, source), ParsingState(fname,
                           source))
    importer = Importer(space, dirname(os.path.abspath(fname)))
    dotted_name = parse_name(fname)
    w_mod = compile_module(space, fname, dotted_name, source, ast, importer)
    w_mod.setup(space)
    space.call_method(w_mod, 'main', [], None)
    return 0


def run_spec(spec_fname):
    xxx


if __name__ == '__main__':
    sys.exit(main(sys.argv))
