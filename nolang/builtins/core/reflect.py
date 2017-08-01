
from nolang.objects.root import W_Root
from nolang.builtins.exception import W_Exception

class W_FrameWrapper(W_Root):
    def __init__(self, frameref):
        self.frameref = frameref

def get_exception_frame(space, w_exc):
    pass

def get_current_frame(space):
    return W_FrameWrapper(space.interpreter.topframeref)
