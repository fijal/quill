
""" Main declaration of a module
"""

from nolang.objects.root import W_Root

class W_Module(W_Root):
    def __init__(self, dict_w):
        self.dict_w = dict_w

    def initialize(self, space):
        for item in self.dict_w.values():
            item.setup(space)

    def getattr_w(self, name):
        return self.dict_w[name] # XXX error handling
