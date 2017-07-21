
""" Main module compiler
"""

from nolang.bytecode import compile_bytecode
from nolang.module import W_Module
from nolang.function import W_Function

class NameAlreadyDefined(Exception):
    def __init__(self, name):
        self.name = name

def compile_module(source, ast):
    name_mapping = {}
    for item in ast.get_element_list():
        if item.name in name_mapping:
            raise NameAlreadyDefined(item.name)
        name_mapping[item.name] = len(name_mapping)

    functions = []
    w_mod = W_Module(name_mapping, functions)
    for item in ast.get_element_list():
        functions.append(W_Function(item.name, compile_bytecode(item, source,
                                    w_mod, item.arglist)))
    return w_mod
