from nolang.error import AppError
from nolang.objects.root import W_Root
from nolang.builtins.spec import unwrap_spec, TypeSpec


class W_ListObject(W_Root):
    def __init__(self, items_w):
        self._items_w = items_w[:]

    def str(self, space):
        return '[' + ', '.join([space.str(i) for i in self._items_w]) + ']'

    def listview(self, space):
        return self._items_w

    def len(self, space):
        return len(self._items_w)

    def contains(self, space, w_obj):
        for w_item in self._items_w:
            if space.is_true(space.binop_eq(w_obj, w_item)):
                return space.w_True
        return space.w_False

    def unwrap_index(self, space, w_index):
        try:
            i = space.int_w(w_index)
        except AppError as ae:
            if ae.match(space, space.w_typeerror):
                raise space.apperr(space.w_typeerror, 'list index must be int')
            raise
        if i < 0 or i >= len(self._items_w):
            raise space.apperr(space.w_indexerror, 'list index out of range')
        return i

    def getitem(self, space, w_index):
        return self._items_w[self.unwrap_index(space, w_index)]

    def setitem(self, space, w_index, w_value):
        self._items_w[self.unwrap_index(space, w_index)] = w_value

    def append(self, space, w_obj):
        self._items_w.append(w_obj)

    def extend(self, space, w_other):
        self._items_w.extend(space.listview(w_other))


@unwrap_spec(items_w='list')
def allocate(space, w_tp, items_w):
    return space.newlist(items_w)


W_ListObject.spec = TypeSpec(
    'List',
    constructor=allocate,
    methods={
        'append': W_ListObject.append,
        'extend': W_ListObject.extend,
    },
    properties={},
    set_cls_w_type=True
)
