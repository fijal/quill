from nolang.objects.root import W_Root


class W_ListObject(W_Root):
    def __init__(self, w_items):
        self._w_items = w_items

    def str(self, space):
        return '[' + ', '.join([space.str(i) for i in self._w_items]) + ']'

    def len(self, space):
        return len(self._w_items)

    def getitem(self, space, w_index):
        return self._w_items[space.int_w(w_index)]

    def setitem(self, space, w_index, w_value):
        self._w_items[space.int_w(w_index)] = w_value
