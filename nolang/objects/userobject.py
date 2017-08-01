""" User supplied objects
"""

from nolang.objects.root import W_Root


class W_UserObject(W_Root):
    def __init__(self, w_type):
        self.w_type = w_type
        self.dict_w = {}

    def gettype(self, space):
        return self.w_type

    def setattr(self, space, attrname, w_val):
        self.dict_w[attrname] = w_val

    def getattr(self, space, attrname):
        try:
            return self.dict_w[attrname]
        except KeyError:
            return space.w_NotImplemented
