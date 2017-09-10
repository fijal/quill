""" Base class that contains all the methods on W_Root which is the root
objects of everything wrapped and presented to the user
"""

# XXX add formatting of types, e.g. "expected integer, got %s"


class NotImplementedOp(Exception):
    pass


class W_Root(object):
    cls_w_type = None

    def int_w(self, space):
        raise space.apperr(space.w_typeerror, 'expected integer')

    def utf8_w(self, space):
        raise space.apperr(space.w_typeerror, 'expected string')

    def buffer_w(self, space):
        raise space.apperr(space.w_typeerror, 'expected buffer')

    def listview(self, space):
        raise space.apperr(space.w_typeerror, 'expected list')

    def dictview(self, space):
        raise space.apperr(space.w_typeerror, 'expected dict')

    def hash(self, space):
        raise space.apperr(space.w_typeerror, 'unhashable type')

    def iter(self, space):
        raise space.apperr(space.w_typeerror, 'uniterable type')

    def iter_next(self, space):
        raise space.apperr(space.w_typeerror, 'object not an iterator')

    def getattr(self, space, attrname):
        return space.w_NotImplemented

    def bind(self, space, w_obj):
        return self

    def gettype(self, space):
        return self.cls_w_type

    def str(self, space):
        raise space.apperr(space.w_typeerror,
            'object cannot be converted to str')

    def len(self, space):
        raise space.apperr(space.w_typeerror, 'unsized type')

    def is_true(self, space):
        return True

    def lt(self, space, w_obj):
        raise space.apperr(space.w_typeerror, 'object not comparable')

    def eq(self, space, w_other):
        if self is w_other:
            return True
        if space.type(self) is not space.type(w_other):
            raise NotImplementedOp
        return False

    def add(self, space, w_other):
        raise space.apperr(space.w_typeerror, 'no implementation for `+`')

    def sub(self, space, w_other):
        raise space.apperr(space.w_typeerror, 'no implementation for `-`')

    def mul(self, space, w_other):
        raise space.apperr(space.w_typeerror, 'no implementation for `*`')

    def truediv(self, space, w_other):
        raise space.apperr(space.w_typeerror, 'no implementation for `/`')

    def call(self, space, interpreter, args, kwargs):
        raise space.apperr(space.w_typeerror, 'object is not callable')

    def freeze(self, space):
        if self.is_frozen(space):
            return
        raise space.apperr(space.w_freezeerror, 'object not freezable')

    def thaw(self, space):
        raise space.apperr(space.w_freezeerror, 'object does not know '
            'how to thaw, this should be an internal error')

    def is_frozen(self, space):
        return False


class W_None(W_Root):

    def is_true(self, space):
        return False

    def is_frozen(self, space):
        return True
