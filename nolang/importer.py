""" Main parts of import system
"""

import os

from nolang.module import create_module
from nolang.parser import ParsingState
from nolang.compiler import compile_module


# XXX wrap up in AppErr
class ImportError(Exception):
    pass


class Importer(object):
    def __init__(self, space, basepath=None, parser=None, lexer=None):
        # XXX basepath is a hack
        self.basepath = basepath
        self.selfmod = create_module('self', [])
        self.parser = parser
        self.lexer = lexer
        self.cache = {'core': space.coremod, 'self': self.selfmod}

    def add_missing_imports(self, space, ast, w_mod, globals_w):
        for item in ast.get_element_list():
            item.add_missing_imports(space, w_mod, globals_w, self)

    def import_module(self, space, path):
        # XXX error handling
        pth = os.path.join(self.basepath, os.path.sep.join(path)) + ".q"
        try:
            source = open(pth).read()
        except (IOError, OSError):
            raise ImportError("foo")
        ast = self.parser.parse(self.lexer.lex(pth, source),
                                ParsingState(pth, source))
        dotted_name = ".".join(['self'] + path)
        w_mod = compile_module(space, pth, dotted_name, source, ast, self)
        return w_mod

    def register_module(self, space, dotted_name, w_mod):
        parts = dotted_name.split(".")
        # XXX think what to do if we have it
        assert dotted_name not in self.cache
        self.cache[dotted_name] = w_mod
        cur_elem = w_mod
        for i in range(len(parts) - 1, -1, -1):
            cur_name = ".".join(parts[:i])
            if cur_name in self.cache:
                self.cache[cur_name].add_element(cur_elem)
                return
            raise Exception("not implemented logic")

    def get_module(self, space, imp_path):
        try:
            return self.cache[".".join(imp_path)]
        except KeyError:
            pass
        last_elem = len(imp_path) - 1
        assert last_elem >= 0
        try:
            w_mod = self.cache[".".join(imp_path[:last_elem])]
        except KeyError:
            pass
        else:
            return space.getattr(w_mod, imp_path[last_elem])
        if imp_path[0] == 'self':
            # allow extra self imports
            try:
                return self.import_module(space, imp_path[1:])
            except ImportError:
                if len(imp_path) == 2:
                    raise
                w_mod = self.import_module(space, imp_path[1:last_elem])
                return space.getattr(w_mod, imp_path[last_elem])
        raise ImportError(".".join(imp_path))

    def import_names(self, space, imp_path, names, globals_w, idx):
        for name in names:
            globals_w[idx] = self.get_module(space, imp_path[:] + [name])
            idx += 1
