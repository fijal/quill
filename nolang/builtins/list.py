from nolang.builtins.spec import unwrap_spec, TypeSpec
from nolang.objects.list import W_ListObject


@unwrap_spec(items_w='list')
def allocate(space, w_tp, items_w):
    return space.newlist(items_w)


@unwrap_spec()
def append(space, w_self, w_item):
    w_self.append(space, w_item)


@unwrap_spec()
def extend(space, w_self, w_other):
    w_self.extend(space, w_other)


W_ListObject.spec = TypeSpec(
    'List',
    constructor=allocate,
    methods={
        'append': append,
        'extend': extend,
    },
    properties={},
    set_cls_w_type=True
)
