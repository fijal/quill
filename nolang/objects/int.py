
""" Base implementation of W_Int which is a machine-sized integer
"""

from nolang.objects.root import W_Root

class W_IntObject(W_Root):
    def __init__(self, intval):
        self._intval = intval

    def int_w(self, space):
        return self._intval
