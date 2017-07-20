
""" Main module compiler
"""

from nolang.bytecode import compile_bytecode
from nolang.module import W_Module
from nolang.function import W_Function

def compile_module(source, ast):
    d = {}
    for item in ast.get_element_list():
        d[item.name] = W_Function(item.name, compile_bytecode(item, source))
    return W_Module(d)
