# -*- coding: utf-8 -*-

from support import BaseTest


class TestBuffer(BaseTest):
    def test_buffer_from_utf8(self):
        w_res = self.interpret_expr('return buffer_from_utf8("foo");')
        assert self.space.buffer_w(w_res) == ['f', 'o', 'o']

    def test_empty_buffer(self):
        w_res = self.interpret_expr("return buffer(3);")
        assert self.space.buffer_w(w_res) == ['\x00', '\x00', '\x00']
