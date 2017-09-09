
from rpython.rlib.rstring import StringBuilder

from nolang.objects.root import W_Root
from nolang.builtins.spec import TypeSpec, unwrap_spec


class W_StringBuilder(W_Root):
    def __init__(self, length):
        self._s = StringBuilder(length)

    @unwrap_spec(txt='utf8')
    def append(self, txt):
        self._s.append(txt)

    def build(self, space):
        return space.newtext(self._s.build())


@unwrap_spec(length='int')
def new_stringbuilder(space, w_tp, length=0):
    return W_StringBuilder(length)


W_StringBuilder.spec = TypeSpec(
    'StringBuilder',
    methods={
        'append': W_StringBuilder.append,
        'build': W_StringBuilder.build,
    },
    constructor=new_stringbuilder,
)
