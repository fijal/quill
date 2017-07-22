
""" Class containing convinient shortcut for calling all things
on objects
"""

from nolang.objects.root import W_None
from nolang.objects.int import W_IntObject
from nolang.objects.bool import W_BoolObject

class Space(object):
    def __init__(self, interpreter):
        self.w_None = W_None() # singleton
        self.w_True = W_BoolObject(True)
        self.w_False = W_BoolObject(False)
        self.interpreter = interpreter

    # newfoo wrappers
    def newint(self, intval):
        return W_IntObject(intval)

    def newbool(self, boolval):
        if boolval:
            return self.w_True
        return self.w_False

    # foo_w unwrappers
    def int_w(self, w_obj):
        return w_obj.int_w(self)

    # unary operations
    def is_true(self, w_obj):
        return w_obj.is_true(self)

    # binary operations
    def binop_lt(self, w_one, w_two):
        return w_one.lt(self, w_two)

    def binop_eq(self, w_one, w_two):
        return w_one.eq(self, w_two)

    def binop_add(self, w_one, w_two):
        return w_one.add(self, w_two)

    def binop_sub(self, w_one, w_two):
        return w_one.sub(self, w_two)

    # various calls
    def call_method(self, w_object, method_name, args):
        w_obj = w_object.getattr_w(method_name)
        return w_obj.call(self, self.interpreter, args)

    def call(self, w_object, args):
        return w_object.call(self, self.interpreter, args)
