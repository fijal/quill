""" User supplied objects
"""

from nolang.objects.root import W_Root


class W_UserObject(W_Root):
    def __init__(self, w_type):
        self.w_type = w_type
        self._dict_w = {}

    def gettype(self, space):
        return self.w_type

    def setattr(self, space, attrname, w_val):
        if self.w_type.force_names is not None:
            if attrname not in self.w_type.force_names:
                msg = '%s is not an allowed attribute of object of class %s' % (
                    attrname, self.w_type.name)
                raise space.apperr(space.w_attrerror, msg)
        self._dict_w[attrname] = w_val

    def getattr(self, space, attrname):
        try:
            return self._dict_w[attrname]
        except KeyError:
            return space.w_NotImplemented
