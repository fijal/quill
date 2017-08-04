from nolang.objects.root import W_Root


class W_BufObject(W_Root):
    def __init__(self, chars):
        self._chars = chars

    def buffer_w(self, space):
        return self._chars

    def str(self, space):
        return 'buffer(' + ''.join([str(c) for c in self._chars]) + ')'
