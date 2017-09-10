from nolang.builtins.spec import unwrap_spec, parameters
from nolang.objects.usertype import W_UserType


@unwrap_spec()
def len(space, w_obj):
    return space.newint(space.len(w_obj))


@parameters(name='isinstance')
def builtin_isinstance(space, w_obj, w_type):
    if not isinstance(w_type, W_UserType):
        # typename = space.type(w_type).name
        # XXX improve the error message
        raise space.apperr(space.w_typeerror, "isinstance right argument is "
            "not a type")
    return space.newbool(space.isinstance(w_obj, w_type))


@parameters(name='str')
def builtin_str(space, w_obj):
    return space.newtext(space.str(w_obj))
