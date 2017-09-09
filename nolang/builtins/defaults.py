from nolang.builtins.io import magic_print
from nolang.module import create_module
from nolang.builtins.buffer import buffer, buffer_from_utf8
from nolang.builtins.builtin import len
from nolang.builtins.exception import W_Exception
from nolang.builtins.spec import wrap_function, wrap_type
from nolang.builtins.core.reflect import get_current_frame, W_FrameWrapper
from nolang.builtins.core.text import W_StringBuilder
from nolang.objects.dict import W_DictObject
from nolang.objects.int import W_IntObject
from nolang.objects.list import W_ListObject
from nolang.objects.unicode import W_StrObject


def wrap_module(name, functions):
    raise NotImplementedError


def default_builtins(space):
    # XXX all of this should be more streamlined
    reflect_module = create_module('reflect',
                                   [wrap_function(space, get_current_frame)])
    text_module = create_module('text',
        [wrap_type(space, W_StringBuilder)])
    core_module = create_module('core', [reflect_module, text_module])

    return [
        # builtins
        magic_print, len, buffer, buffer_from_utf8, W_Exception, W_ListObject,
        W_DictObject, W_StrObject, W_IntObject
    ], core_module, [
        # non-builtins that need to be wrapped
        W_FrameWrapper,
    ]
