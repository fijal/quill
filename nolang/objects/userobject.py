
""" User supplied objects
"""

from nolang.objects.root import W_Root
from nolang.function import W_Function, W_BoundMethod

class W_UserObject(W_Root):
    def __init__(self, w_type):
        self.w_type = w_type
        self.dict_w = {}

    def setattr(self, space, attrname, w_val):
        self.dict_w[attrname] = w_val

    def getattr(self, space, attrname):
        try:
            return self.dict_w[attrname]
        except KeyError:
            # look up on the type
            return self._potentially_wrap(self.w_type.getattr(space, attrname))

    def _potentially_wrap(self, w_obj):
        if isinstance(w_obj, W_Function):
            return W_BoundMethod(self, w_obj)
        return w_obj
