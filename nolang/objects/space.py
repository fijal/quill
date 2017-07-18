
""" Class containing convinient shortcut for calling all things
on objects
"""

from nolang.objects.root import W_None
from nolang.objects.int import W_IntObject

class Space(object):
    def __init__(self):
        self.w_None = W_None() # singleton

    # newxxx methods
    def newint(self, intval):
        return W_IntObject(intval)

    # xxx_w methods
    def int_w(self, w_obj):
        return w_obj.int_w(self)
