""" Main declaration of function
"""

from nolang.objects.root import W_Root
from nolang.frameobject import Frame


def argerr(space, msg):
    return space.apperr(space.w_argerror, msg)


def argerr_number(space, bytecode, name, arglen):
    if bytecode.minargs == bytecode.maxargs:
        msg = "expected %d" % bytecode.minargs
    else:
        msg = "expected between %d and %d" % (
            bytecode.minargs, bytecode.maxargs)
    raise argerr(space, "Function %s got %d arguments, %s" % (
        name, arglen, msg))


def prepare_args(space, name, bytecode, args_w, namedargs_w):
    num_args = len(bytecode.arglist)
    if namedargs_w is None:
        # fastpath for just args
        if not bytecode.minargs <= len(args_w) <= bytecode.maxargs:
            raise argerr_number(space, bytecode, name, len(args_w))
        if bytecode.first_default >= 0:
            args_w = args_w + [bytecode.constants[bytecode.defaults[i]]
                for i in range(len(args_w), bytecode.maxargs)]
        return args_w

    if (not bytecode.minargs <= len(args_w) + len(namedargs_w)
                             <= bytecode.maxargs):
        raise argerr_number(
            space, bytecode, name, len(namedargs_w) + len(args_w))

    vals_w = args_w + [None] * (num_args - len(args_w))
    for k, w_v in namedargs_w:
        try:
            index = bytecode.argmapping[k]
        except KeyError:
            raise argerr(space, "Function %s got unexpected keyword "
                "argument '%s'" % (name, k))
        if vals_w[index] is not None:
            raise argerr(space, "Function %s got multiple values for "
                "argument '%s'" % (name, k))
        vals_w[index] = w_v

    if bytecode.first_default >= 0:
        for i in range(bytecode.first_default, len(bytecode.defaults)):
            def_no = bytecode.defaults[i]
            if def_no != -1 and vals_w[i] is not None:
                vals_w[i] = bytecode.constants[def_no]

    for item in vals_w:
        if item is None:
            raise argerr(space, "Function %s didn't receive enough positional "
                "arguments" % (name,))

    return vals_w


class W_Function(W_Root):
    def __init__(self, name, bytecode, w_mod):
        self.name = name
        self.bytecode = bytecode
        self.w_mod = w_mod

    def setup(self, space):
        self.bytecode.setup(space)

    def serialize(self, serializer, w_mod):
        if w_mod is not self.w_mod:
            xxx
        serializer.write("uf")
        serializer.write_str(self.name)
        self.bytecode.serialize(serializer, w_mod)

    def call(self, space, interpreter, args_w, kwargs):
        frame = Frame(self.bytecode, self.name)
        args_w = prepare_args(space, self.name, self.bytecode, args_w, kwargs)
        frame.populate_args(args_w)
        return interpreter.interpret(space, self.bytecode, frame)

    def bind(self, space, w_obj):
        return W_BoundMethod(w_obj, self)


class W_BuiltinFunction(W_Root):
    def __init__(self, name, callable, min_args, max_args):
        self.name = name
        self.min_args = min_args
        self.max_args = max_args
        self.callable = callable

    def setup(self, space):
        pass

    def call(self, space, interpreter, args_w, kwargs):
        if kwargs is not None:
            raise Exception('unimplemented')
        if self.min_args != -1 and not self.min_args <= len(args_w) <= self.max_args:
            if self.min_args == self.max_args:
                msg = "Function %s got %d arguments, expected %d" % (self.name,
                    len(args_w), self.min_args)
            else:
                msg = "Function %s got %d arguments, expected %d-%d" % (
                    self.name, len(args_w), self.min_args, self.max_args)
            raise space.apperr(space.w_argerror, msg)
        return self.callable(space, args_w)

    def bind(self, space, w_obj):
        return W_BoundMethod(w_obj, self)

    def serialize(self, serializer, w_mod):
        serializer.write("bf")
        serializer.write_str(self.name)

    def __repr__(self):
        return "<BuiltinFunction %s/%d-%d>" % (self.name, self.min_args,
            self.max_args)


class W_Property(W_Root):
    def __init__(self, name, getter, setter):
        self.name = name
        self.getter = getter
        self.setter = setter

    def bind(self, space, w_obj):
        return self.getter(w_obj, space)

    def setup(self, space):
        pass


class W_BoundMethod(W_Root):
    def __init__(self, w_self, w_function):
        self.w_self = w_self
        self.w_function = w_function

    def call(self, space, interpreter, args_w, kwargs):
        return space.call(self.w_function, [self.w_self] + args_w, kwargs)
