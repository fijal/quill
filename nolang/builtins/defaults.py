
from nolang.builtins.io import magic_print
from nolang.builtins.exception import W_Exception

def default_builtins():
    return [magic_print, W_Exception]
