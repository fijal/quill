from nolang.error import AppError
from nolang.objects.root import W_Root


class W_ListObject(W_Root):
    def __init__(self, w_items):
        self._w_items = w_items

    def str(self, space):
        return '[' + ', '.join([space.str(i) for i in self._w_items]) + ']'

    def len(self, space):
        return len(self._w_items)

    def unwrap_index(self, space, w_index):
        try:
            i = space.int_w(w_index)
        except AppError as ae:
            if space.type(ae.w_exception) is space.w_typeerror:
                raise space.apperr(space.w_typeerror, 'list index must be int')
            raise
        if i < 0 or i >= len(self._w_items):
            raise space.apperr(space.w_indexerror, 'list index out of range')
        return i

    def getitem(self, space, w_index):
        return self._w_items[self.unwrap_index(space, w_index)]

    def setitem(self, space, w_index, w_value):
        self._w_items[self.unwrap_index(space, w_index)] = w_value
