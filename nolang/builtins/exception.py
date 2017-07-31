
from nolang.builtins.spec import unwrap_spec, TypeSpec
from nolang.objects.userobject import W_UserObject

class W_Exception(W_UserObject):
    def __init__(self, w_tp, message, frame=None):
        W_UserObject.__init__(self, w_tp)
        self.message = message
        self.frame = frame

    def get_message(self, space):
        return space.newtext(self.message)

@unwrap_spec(msg='str')
def allocate(space, w_tp, msg):
    return W_Exception(w_tp, msg)

W_Exception.spec = TypeSpec('Exception',
    constructor=allocate,
    methods={
    },
    properties={
        'message': (W_Exception.get_message, None)
    }
)
