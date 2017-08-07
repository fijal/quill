from nolang.builtins.spec import unwrap_spec, TypeSpec
from nolang.objects.list import W_ListObject


@unwrap_spec(items_w='list')
def allocate(space, w_tp, items_w):
    return space.newlist(items_w)


@unwrap_spec()
def append(space, w_self, w_item):
    w_self.append(space, w_item)


W_ListObject.spec = TypeSpec(
    'List',
    constructor=allocate,
    methods={
        'append': append,
    },
    properties={}
)
