from rpython.rlib.objectmodel import compute_hash

from nolang.error import AppError
from nolang.objects.root import W_Root
from nolang.builtins.spec import TypeSpec, unwrap_spec


class W_StrObject(W_Root):
    def __init__(self, utf8val, lgt=-1):
        assert isinstance(utf8val, str)
        self.utf8val = utf8val
        self.lgt = lgt

    def utf8_w(self, space):
        return self.utf8val

    def str(self, space):
        return self.utf8_w(space)

    def len(self, space):
        if self.lgt == -1:
            # XXX compute it better once utf8 lands
            self.lgt = len(self.utf8val.decode('utf-8'))
        return self.lgt

    def hash(self, space):
        return compute_hash(self.utf8val)

    def eq(self, space, w_other):
        try:
            other = space.utf8_w(w_other)
        except AppError as ae:
            if space.type(ae.w_exception) is space.w_typeerror:
                return space.w_NotImplemented
            raise
        return space.newbool(self.utf8val == other)


@unwrap_spec(value='utf8')
def new_str(space, value):
    return space.newtext(value)


W_StrObject.spec = TypeSpec('Str', new_str)
