
""" Main module compiler
"""

from nolang.module import W_Module

class NameAlreadyDefined(Exception):
    def __init__(self, name):
        self.name = name

def _gather_names(ast, builtins):
    name_mapping = {}
    if builtins is not None:
        for item in builtins:
            name_mapping[item.name] = len(name_mapping)
    for item in ast.get_element_list():
        if item.name in name_mapping:
            raise NameAlreadyDefined(item.name)
        name_mapping[item.name] = len(name_mapping)
    return name_mapping

def compile_module(source, ast, builtins=None):
    name_mapping = _gather_names(ast, builtins)
    if builtins is not None:
        globals_w = builtins[:]
    else:
        globals_w = []
    w_mod = W_Module(name_mapping, globals_w)
    for item in ast.get_element_list():
        globals_w.append(item.wrap_as_global_symbol(source, w_mod))
    return w_mod

def compile_class(source, ast, w_mod, parent=None):
    class_elements_w = []
    if parent is not None:
        w_parent = w_mod.functions[w_mod.name2index[parent]]
    else:
        w_parent = None
    for item in ast.get_element_list():
        class_elements_w.append(item.wrap_as_global_symbol(source, w_mod))
    return class_elements_w, w_parent
