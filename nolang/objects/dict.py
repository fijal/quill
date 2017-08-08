from rpython.rlib.objectmodel import r_dict

from nolang.objects.root import W_Root


class W_DictObject(W_Root):
    def __init__(self, key_eq, key_hash, dict_w):
        self._dict_w = r_dict(key_eq, key_hash)
        self._dict_w.update(dict_w)

    def str(self, space):
        return '{' + ', '.join([space.str(k) + ': ' + space.str(v)
                                for k, v in self._dict_w.items()]) + '}'

    def dict_w(self, space):
        return self._dict_w

    def len(self, space):
        return len(self._dict_w)

    def getitem(self, space, w_key):
        if w_key not in self._dict_w:
            raise space.apperr(space.w_keyerror, space.str(w_key))
        return self._dict_w[w_key]

    def setitem(self, space, w_key, w_value):
        self._dict_w[w_key] = w_value
