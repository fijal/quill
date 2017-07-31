
""" Main declaration of a module
"""

from nolang.objects.root import W_Root

class W_Module(W_Root):
    def __init__(self, name2index, functions):
        self.name2index = name2index
        self.functions = functions

    def initialize(self, space):
        for item in self.functions:
            item.setup(space)

    def getattr(self, space, name):
        return self.functions[self.name2index[name]] # XXX error handling
