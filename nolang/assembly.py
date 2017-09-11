
""" This fie will have to get rewritten but it seems we can't start
going without having a temporary hack
"""


import os
from nolang.parser import ParsingState
from nolang.importer import Importer
from nolang.compiler import compile_module
from nolang.serializer import Serializer


class Error(Exception):
    def __init__(self, msg):
        self.msg = msg


def add_package(space, pkg_name, directory):
    importer = Importer(space, directory)
    modules = []
    for k in os.listdir(directory):
        fname = os.path.join(directory, k)
        if os.path.isfile(fname) and fname.endswith('.q'):
            try:
                f = open(fname)
                source = f.read()
                f.close()
            except (OSError, IOError):
                raise Error("Error reading file %s" % fname)
            # XXX errors
            ast = space.parser.parse(space.parser.lexer.lex(fname, source),
                ParsingState(fname, source))
            w_mod = compile_module(space, fname, "self." + k.strip(".q"),
                source, ast, importer)
            w_mod.setup(space)
            modules.append(w_mod)
    f = open("output.asm", "w")
    s = Serializer(f)
    for module in modules:
        module.serialize_module(s)
    f.close()


def compile_assembly(space, fname):
    try:
        source = open(fname).read()
    except (OSError, IOError):
        print "Error reading %s" % (fname,)
        return 1
    lines = source.split("\n")
    lines = [line.strip() for line in lines if line.strip()]
    for line in lines:
        elems = line.split(':')
        if len(elems) != 2:
            print "Unknown line %s" % line
            return 2
        package = elems[0]
        directory = elems[1]
        try:
            add_package(space, package, directory)
        except Error as e:
            print e.msg
            return 1
    return 0
