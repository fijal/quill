
""" Main declaration of a module
"""

from nolang.objects.root import W_Root


def create_module(name, dotted_name, functions):
    name2index = {}
    for i, func in enumerate(functions):
        name2index[func.name] = i
    return W_Module(name, dotted_name, name2index, functions[:])


class W_Module(W_Root):
    def __init__(self, name, dotted_name, name2index, functions):
        self.name = name
        self.dotted_name = dotted_name
        self.name2index = name2index
        self.functions = functions
        self.exports = []

    def setup(self, space):
        for item in self.functions:
            item.setup(space)

    def add_element(self, element):
        no = len(self.functions)
        self.functions.append(element)
        self.name2index[element.name] = no

    def getattr(self, space, name):
        try:
            return self.functions[self.name2index[name]]
        except KeyError:
            return W_Root.getattr(self, space, name)  # let it raise

    def serialize(self, serializer, w_mod):
        if w_mod is self:
            assert False
        serializer.write("bm")
        serializer.write_str(self.dotted_name)

    def serialize_module(self, serializer):
        serializer.write_int(0xBABACACA) # magic number
        serializer.write_int(13) # version tag
        serializer.write_str(self.name)
        serializer.write_int(len(self.exports))
        for item in self.exports:
            serializer.write_str(item.name)
        serializer.write_int(len(self.functions))
        for item in self.functions:
            item.serialize(serializer, self)

    def __repr__(self):
        return '<Module %s %d functions>' % (self.name, len(self.functions))
