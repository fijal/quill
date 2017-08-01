from nolang.builtins.spec import unwrap_spec
from nolang.objects.int import W_IntObject
from nolang.objects.unicode import W_StrObject


@unwrap_spec()
def buffer(space, w_size):
    if not isinstance(w_size, W_IntObject):
        raise space.apperr(space.w_exception, "Expected int.")
    return space.newbuf(['\x00'] * w_size._intval)


@unwrap_spec()
def buffer_from_utf8(space, w_str):
    if not isinstance(w_str, W_StrObject):
        raise space.apperr(space.w_exception, "Expected str.")
    return space.newbuf([c for c in w_str.utf8val])
