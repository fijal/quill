
""" User supplied objects
"""

from nolang.objects.root import W_Root

class W_UserObject(W_Root):
    def __init__(self, w_type):
        self.w_type = w_type
        self.dict_w = {}

    def setattr(self, attrname, w_val):
        self.dict_w[attrname] = w_val

    def getattr(self, attrname):
        return self.dict_w[attrname]
