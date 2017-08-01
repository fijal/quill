
from nolang.builtins.io import magic_print
from nolang.module import W_Module
from nolang.builtins.exception import W_Exception
from nolang.builtins.spec import wrap_function
from nolang.builtins.core.reflect import get_current_frame

def wrap_module(name, functions):
    xxx

def default_builtins():
    reflect_module = W_Module('reflect', {'get_current_frame': 0},
        [wrap_function(get_current_frame)])
    core_module = W_Module('core', {'reflect': 0}, [reflect_module])

    return [magic_print, W_Exception], core_module
