
def freeze(space, w_obj):
    space.freeze(w_obj)


def thaw(space, w_obj):
    return space.thaw(w_obj)


def is_frozen(space, w_obj):
    return space.is_frozen(w_obj)


functions = [freeze, thaw, is_frozen]
