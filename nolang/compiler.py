
""" Main module compiler
"""

from nolang.module import W_Module

class NameAlreadyDefined(Exception):
    def __init__(self, name):
        self.name = name

def _gather_names(ast):
    name_mapping = {}
    for item in ast.get_element_list():
        if item.name in name_mapping:
            raise NameAlreadyDefined(item.name)
        name_mapping[item.name] = len(name_mapping)
    return name_mapping

def compile_module(source, ast):
    name_mapping = _gather_names(ast)
    globals_w = []
    w_mod = W_Module(name_mapping, globals_w)
    for item in ast.get_element_list():
        globals_w.append(item.wrap_as_global_symbol(source, w_mod))
    return w_mod

def compile_class(source, ast, w_mod):
    class_elements_w = []
    for item in ast.get_element_list():
        class_elements_w.append(item.wrap_as_global_symbol(source, w_mod))
    return class_elements_w
