from nolang.objects.root import W_Root


class W_BoolObject(W_Root):
    def __init__(self, boolval):
        self._boolval = boolval

    def is_true(self, space):
        return self._boolval
