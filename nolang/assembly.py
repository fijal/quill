
""" This fie will have to get rewritten but it seems we can't start
going without having a temporary hack
"""


import os
from nolang.parser import ParsingState
from nolang.importer import Importer
from nolang.compiler import compile_module
from nolang.serializer import Serializer
from nolang.error import InterpreterError
from nolang.specreader import read_spec


class AssemblyError(InterpreterError):
    pass


def add_package(space, pkg_name, directory, outname):
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
                raise AssemblyError("Error reading file %s" % fname)
            ast = space.parser.parse(space.parser.lexer.lex(fname, source),
                ParsingState(fname, source))
            w_mod = compile_module(space, fname, "self." + k.strip(".q"),
                source, ast, importer)
            w_mod.setup(space)
            modules.append(w_mod)
    try:
        f = open(outname, "w")
        s = Serializer(f)
        for module in modules:
            module.serialize_module(s)
        f.close()
    except (OSError, IOError):
        raise AssemblyError("Cannot write file %s" % outname)


def compile_assembly(space, fname):
    spec = read_spec(fname, ["output", "packages"], True)
    for package, directory in spec['packages'].iteritems():
        add_package(space, package, directory, spec['output']['output'])
    return 0
