from nolang.builtins.spec import unwrap_spec, TypeSpec
from nolang.objects.dict import W_DictObject


@unwrap_spec(items_w='dict')
def allocate(space, w_tp, items_w):
    return space.newdict(items_w)


@unwrap_spec()
def merge(space, w_self, w_other):
    return w_self.merge(space, w_other)


@unwrap_spec()
def get(space, w_self, w_key, w_default):
    # XXX Make w_default default to w_None when we have optional args.
    return w_self.get(space, w_key, w_default)


W_DictObject.spec = TypeSpec(
    'Dict',
    constructor=allocate,
    methods={
        'merge': merge,
        'get': get,
    },
    properties={},
    set_cls_w_type=True
)
