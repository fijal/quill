
""" Main declaration of function
"""

from nolang.objects.root import W_Root
from nolang.frameobject import Frame

class W_Function(W_Root):
    def __init__(self, name, bytecode):
        self.name = name
        self.bytecode = bytecode

    def setup(self, space):
        self.bytecode.setup(space)

    def call(self, space, interpreter, args_w):
        frame = Frame(self.bytecode)
        frame.populate_args(args_w)
        return interpreter.interpret(space, self.bytecode, frame)
