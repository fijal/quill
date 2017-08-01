from nolang.objects.root import W_Root
from nolang.builtins.spec import TypeSpec


class W_FrameWrapper(W_Root):
    def __init__(self, frameref):
        self.frameref = frameref

    def get_filename(self, space):
        return space.newtext(self.frameref.bytecode.filename)


W_FrameWrapper.spec = TypeSpec('Frame',
    constructor=None,
    methods={},
    properties={
        'filename': (W_FrameWrapper.get_filename, None)
    },
)


def get_exception_frame(space, w_exc):
    pass


def get_current_frame(space):
    return W_FrameWrapper(space.interpreter.topframeref)
