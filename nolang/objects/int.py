""" Base implementation of W_Int which is a machine-sized integer
"""

from nolang.error import AppError
from nolang.objects.root import W_Root


class W_IntObject(W_Root):
    def __init__(self, intval):
        self._intval = intval

    def str(self, space):
        return str(self._intval)

    def hash(self, space):
        return hash(self._intval)

    def int_w(self, space):
        return self._intval

    def lt(self, space, w_other):
        return space.newbool(self._intval < w_other._intval)

    def eq(self, space, w_other):
        try:
            other = space.int_w(w_other)
        except AppError as ae:
            if space.type(ae.w_exception) is space.w_typeerror:
                return space.w_NotImplemented
            raise
        return space.newbool(self._intval == other)

    def add(self, space, w_other):
        return space.newint(self._intval + w_other._intval)

    def sub(self, space, w_other):
        return space.newint(self._intval - w_other._intval)

    def mul(self, space, w_other):
        return space.newint(self._intval * w_other._intval)

    def truediv(self, space, w_other):
        return space.newint(self._intval // w_other._intval)

    def is_true(self, space):
        return self._intval != 0
