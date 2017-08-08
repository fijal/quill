from rpython.rlib.objectmodel import compute_hash

from nolang.error import AppError
from nolang.objects.root import W_Root


class W_StrObject(W_Root):
    def __init__(self, utf8val):
        self.utf8val = utf8val

    def utf8_w(self, space):
        return self.utf8val

    def str(self, space):
        return self.utf8_w(space)

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
