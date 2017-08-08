from nolang.builtins.io import magic_print
from nolang.module import create_module
from nolang.builtins.buffer import buffer, buffer_from_utf8
from nolang.builtins.dict import W_DictObject
from nolang.builtins.exception import W_Exception
from nolang.builtins.list import W_ListObject
from nolang.builtins.spec import wrap_function, wrap_type
from nolang.builtins.core.reflect import get_current_frame, W_FrameWrapper


def wrap_module(name, functions):
    raise NotImplementedError


def default_builtins(space):
    # XXX all of this should be more streamlined
    reflect_module = create_module('reflect',
                                   [wrap_function(space, get_current_frame)])
    frame_wrapper_tp = wrap_type(space, W_FrameWrapper)
    W_FrameWrapper.cls_w_type = frame_wrapper_tp
    core_module = create_module('core', [reflect_module])

    return [
        magic_print, buffer, buffer_from_utf8, W_Exception, W_ListObject,
        W_DictObject,
    ], core_module
