
""" Base implementation of W_Int which is a machine-sized integer
"""

from nolang.objects.root import W_Root
from nolang.builtins.spec import TypeSpec, unwrap_spec


class W_IntObject(W_Root):
    def __init__(self, intval):
        self._intval = intval

    def str(self, space):
        return str(self._intval)

    def int_w(self, space):
        return self._intval

    def lt(self, space, w_other):
        return space.newbool(self._intval < w_other._intval)

    def eq(self, space, w_other):
        return space.newbool(self._intval == w_other._intval)

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


@unwrap_spec(value='int')
def new_int(space, value):
    return space.newint(value)


W_IntObject.spec = TypeSpec('Int', new_int)
