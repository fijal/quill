
""" Class containing convinient shortcut for calling all things
on objects
"""

from nolang.objects.root import W_None, W_Root
from nolang.objects.int import W_IntObject
from nolang.objects.bool import W_BoolObject
from nolang.objects.unicode import W_StrObject
from nolang.objects.buffer import W_BufObject
from nolang.builtins.spec import wrap_builtin

class Space(object):
    def __init__(self):
        self.w_None = W_None() # singleton
        self.w_True = W_BoolObject(True)
        self.w_False = W_BoolObject(False)
        self.w_NotImplemented = W_Root()

    def setup(self, interpreter):
        self.interpreter = interpreter

    def setup_builtins(self, builtins, coremod):
        self.builtins_w = [wrap_builtin(builtin) for builtin in builtins]
        self.builtin_dict = {}
        for builtin in self.builtins_w:
            self.builtin_dict[builtin.name] = builtin
        self.w_exception = self.builtin_dict['Exception']
        self.coremod = coremod

    def import_symbols(self, import_names):
        package = import_names[0]
        if package == 'core':
            return self.coremod
        raise Exception("importing unimplemented")

    def setattr(self, w_obj, attrname, w_value):
        w_obj.setattr(self, attrname, w_value)

    def getattr(self, w_obj, attrname):
        w_res = w_obj.getattr(self, attrname)
        if w_res is self.w_NotImplemented:
            return self.getattr(self.type(w_obj), attrname).bind(self, w_obj)
        return w_res

    def str(self, w_obj):
        return w_obj.str(self)

    # object stuff, hacks so far
    def issubclass(self, w_left, w_right):
        return w_left.issubclass(w_right)

    def type(self, w_obj):
        # for builtin types we know exactly what type is it based on class
        return w_obj.gettype(self)

    # newfoo wrappers
    def newint(self, intval):
        return W_IntObject(intval)

    def newbool(self, boolval):
        if boolval:
            return self.w_True
        return self.w_False

    def newtext(self, utf8val):
        return W_StrObject(utf8val)

    def newbuf(self, charsval):
        return W_BufObject(charsval)

    # foo_w unwrappers
    def int_w(self, w_obj):
        return w_obj.int_w(self)

    def utf8_w(self, w_obj):
        return w_obj.utf8_w(self)

    def buffer_w(self, w_obj):
        return w_obj.buffer_w(self)

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

    def binop_mul(self, w_one, w_two):
        return w_one.mul(self, w_two)

    def binop_truediv(self, w_one, w_two):
        return w_one.truediv(self, w_two)

    # various calls
    def call_method(self, w_object, method_name, args):
        w_obj = w_object.getattr(self, method_name)
        return w_obj.call(self, self.interpreter, args)

    def call(self, w_object, args):
        return w_object.call(self, self.interpreter, args)
