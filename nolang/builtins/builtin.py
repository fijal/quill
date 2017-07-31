
from nolang.builtins.io import magic_print
from nolang.builtins.exceptions import W_Exception

def wrap_builtin(space, f):
    xxx

def default_builtins(space):
    return [wrap_builtin(space, x) for x in [magic_print, W_Exception]]
