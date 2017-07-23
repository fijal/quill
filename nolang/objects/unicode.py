
from nolang.objects.root import W_Root

class W_StrObject(W_Root):
    def __init__(self, utf8val):
        self.utf8val = utf8val

    def utf8_w(self, space):
        return self.utf8val
