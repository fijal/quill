from nolang.objects.root import W_Root


class W_BoolObject(W_Root):
    def __init__(self, boolval):
        self._boolval = boolval

    def is_true(self, space):
        return self._boolval

    def __bool__(self):
        raise Exception("Should not ask for true value of W_Bool")

    def __repr__(self):
        if self._boolval:
            return '<Bool True>'
        else:
            return '<Bool False>'
