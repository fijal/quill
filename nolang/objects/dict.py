from rpython.rlib.objectmodel import r_dict

from nolang.objects.root import W_Root


class W_DictObject(W_Root):
    def __init__(self, key_eq, key_hash, items_w):
        self._items_w = r_dict(key_eq, key_hash)
        for k, v in items_w:
            self._items_w[k] = v

    def str(self, space):
        return '{' + ', '.join([space.str(k) + ': ' + space.str(v)
                                for k, v in self._items_w.items()]) + '}'

    def dictview(self, space):
        return self._items_w

    def len(self, space):
        return len(self._items_w)

    def getitem(self, space, w_key):
        if w_key not in self._items_w:
            raise space.apperr(space.w_keyerror, space.str(w_key))
        return self._items_w[w_key]

    def get(self, space, w_key, w_default):
        if w_key not in self._items_w:
            return w_default
        return self._items_w[w_key]

    def dict_pop(self, space, w_key):
        if w_key not in self._items_w:
            raise space.apperr(space.w_keyerror, space.str(w_key))
        return self._items_w.pop(w_key)

    def setitem(self, space, w_key, w_value):
        self._items_w[w_key] = w_value

    def merge(self, space, w_other):
        other_w = space.dictview(w_other)
        w_res = space.newdict([])
        w_res._items_w.update(self._items_w)
        w_res._items_w.update(other_w)
        return w_res

    def keys(self, space):
        return space.newlist(self._items_w.keys())

    def values(self, space):
        return space.newlist(self._items_w.values())
