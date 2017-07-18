
""" Base class that contains all the methods on W_Root which is the root
objects of everything wrapped and presented to the user
"""

class UnimplementedOperation(Exception):
    pass

class W_Root(object):
    def int_w(self, space):
        raise UnimplementedOperation

class W_None(object):
    pass
