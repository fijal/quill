from nolang.objects.root import W_Root


class W_StrObject(W_Root):
    def __init__(self, utf8val):
        self.utf8val = utf8val

    def utf8_w(self, space):
        return self.utf8val

    def str(self, space):
        return self.utf8_w(space)

    def eq(self, space, w_other):
        return space.newbool(self.utf8val == space.utf8_w(w_other))
