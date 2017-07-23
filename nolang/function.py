
""" Main declaration of function
"""

from nolang.objects.root import W_Root
from nolang.frameobject import Frame
from nolang.error import ArgumentMismatchError

class W_Function(W_Root):
    def __init__(self, name, bytecode):
        self.name = name
        self.bytecode = bytecode

    def setup(self, space):
        self.bytecode.setup(space)

    def call(self, space, interpreter, args_w):
        frame = Frame(self.bytecode)
        if len(self.bytecode.arglist) != len(args_w):
            raise ArgumentMismatchError()
        frame.populate_args(args_w)
        return interpreter.interpret(space, self.bytecode, frame)

class BuiltinFunction(W_Root):
    def __init__(self, name, callable, num_args):
        self.name = name
        self.num_args = num_args
        self.callable = callable

    def setup(self, space):
        pass

    def call(self, space, interpreter, args_w):
        if self.num_args != len(args_w):
            raise ArgumentMismatchError()
        self.callable(space, args_w)

class W_BoundMethod(W_Root):
    def __init__(self, w_self, w_function):
        self.w_self = w_self
        self.w_function = w_function

    def call(self, space, interpreter, args_w):
        return space.call(self.w_function, [self.w_self] + args_w)
