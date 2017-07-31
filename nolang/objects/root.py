
""" Base class that contains all the methods on W_Root which is the root
objects of everything wrapped and presented to the user
"""

class W_Root(object):
    def int_w(self, space):
        return space.w_NotImplemented

    def getattr(self, space, attrname):
        return space.w_NotImplemented

    def bind(self, space, w_obj):
        return self

class W_None(W_Root):
    pass
