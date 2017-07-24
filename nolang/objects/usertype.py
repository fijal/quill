
""" Basic declaration of user type defined with class
"""

from nolang.objects.root import W_Root
from nolang.error import ArgumentMismatchError
from nolang.objects.userobject import W_UserObject

class W_UserType(W_Root):
    def __init__(self, name, class_elements_w, w_parent):
        self.name = name
        self.class_elements_w = class_elements_w
        if w_parent is not None:
            self.dict_w = w_parent.dict_w.copy()
        else:
            self.dict_w = {}
        for item in class_elements_w:
            self.dict_w[item.name] = item
        self.w_parent = w_parent

    def setup(self, space):
        for item in self.class_elements_w:
            item.setup(space)

    def call(self, space, interpreter, args_w):
        w_obj = W_UserObject(self)
        if '__init__' in self.dict_w:
            space.call(self.dict_w['__init__'], [w_obj] + args_w)
        else:
            if len(args_w) != 0:
                raise ArgumentMismatchError
        return w_obj

    def getattr(self, space, attrname):
        return self.dict_w[attrname]

    def issubclass(self, w_type):
        cur = self
        while cur is not None:
            if cur is w_type:
                return True
            cur = cur.w_parent
        return False