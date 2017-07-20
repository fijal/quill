
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

    def call(self, space, interpreter):
        frame = Frame(self.bytecode)
        return interpreter.interpret(space, self.bytecode, frame)
