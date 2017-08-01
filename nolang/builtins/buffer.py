from nolang.builtins.spec import parameters
from nolang.objects.int import W_IntObject
from nolang.objects.unicode import W_StrObject


@parameters(name='buffer')
def buffer(space, args_w):
    if isinstance(args_w[0], W_StrObject):
        return space.newbuf([c for c in args_w[0].utf8val])
    if isinstance(args_w[0], W_IntObject):
        return space.newbuf(['\x00'] * args_w[0]._intval)
