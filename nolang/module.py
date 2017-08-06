
""" Main declaration of a module
"""

from nolang.objects.root import W_Root


def create_module(name, functions):
    name2index = {}
    for i, func in enumerate(functions):
        name2index[func.name] = i
    return W_Module(name, name2index, functions[:])


class W_Module(W_Root):
    def __init__(self, name, name2index, functions):
        self.name = name
        self.name2index = name2index
        self.functions = functions

    def setup(self, space):
        for item in self.functions:
            item.setup(space)

    def add_element(self, element):
        no = len(self.functions)
        self.functions.append(element)
        self.name2index[element.name] = no

    def getattr(self, space, name):
        return self.functions[self.name2index[name]]  # XXX error handling

    def __repr__(self):
        return '<Module %s %d functions>' % (self.name, len(self.functions))
