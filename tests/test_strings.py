# -*- coding: utf-8 -*-

from support import BaseTest


class TestStrings(BaseTest):
    def test_string_literal(self):
        w_res = self.interpret_expr('return "foo";')
        assert self.space.utf8_w(w_res) == "foo"

    def test_unicode_literal(self):
        w_res = self.interpret_expr(u'return "wziąść";'.encode('utf8'))
        assert self.space.utf8_w(w_res) == u"wziąść".encode('utf8')

    def test_string_equality(self):
        assert self.interpret_expr('return "foo" == "foo";') is self.space.w_True
        assert self.interpret_expr('return "foo" == "bar";') is self.space.w_False
