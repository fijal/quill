from nolang.builtins.spec import unwrap_spec, TypeSpec
from nolang.objects.dict import W_DictObject


@unwrap_spec(items_w='dict')
def allocate(space, w_tp, items_w):
    return space.newdict(items_w)


@unwrap_spec()
def merge(space, w_self, w_other):
    return w_self.merge(space, w_other)


W_DictObject.spec = TypeSpec(
    'Dict',
    constructor=allocate,
    methods={
        'merge': merge,
    },
    properties={},
    set_cls_w_type=True
)
