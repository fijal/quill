""" Main parts of import system
"""

import os

from nolang.module import create_module
from nolang.parser import ParsingState
from nolang.compiler import compile_module


class Importer(object):
    def __init__(self, basepath=None, parser=None, lexer=None):
        # XXX basepath is a hack
        self.basepath = basepath
        self.selfmod = create_module('self', [])
        self.parser = parser
        self.lexer = lexer
        self.cache = {}

    def register_module(self, w_mod):
        w_self_mod = self.selfmod
        w_self_mod.add_element(w_mod)

    def add_missing_imports(self, space, ast, w_mod, globals_w):
        for item in ast.get_element_list():
            item.add_missing_imports(space, w_mod, globals_w, self)

    def import_package(self, space, imp_path):
        # XXX all of this is a bunch of hacks for now
        dotted_name = ".".join(imp_path)
        if imp_path[0] == 'self':
            try:
                return self.cache[dotted_name]
            except KeyError:
                pass
            items = imp_path[1:]
            assert len(items) == 1
            pth = os.path.join(self.basepath, items[0]) + ".q"
            source = open(pth).read()
            ast = self.parser.parse(self.lexer.lex(pth, source),
                                    ParsingState(pth, source))
            w_mod = compile_module(space, pth, source, ast, self)
            self.cache[dotted_name] = w_mod
            return w_mod
        elif imp_path[0] == 'core':
            return space.coremod
        else:
            raise Exception("unimplemented")
