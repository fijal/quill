from nolang.objects.root import W_Root


class W_ListObject(W_Root):
    def __init__(self, items):
        self._items = items

    def str(self, space):
        return '[' + ', '.join([space.str(i) for i in self._items]) + ']'

    def len(self, space):
        return len(self._items)
