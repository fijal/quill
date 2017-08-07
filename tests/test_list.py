import py

from support import BaseTest


class TestList(BaseTest):
    def test_empty_list(self):
        w_res = self.interpret_expr('return [];')
        assert self.space.len(w_res) == 0

    def test_short_list(self):
        w_res = self.interpret_expr('return ["foo"];')
        assert self.space.len(w_res) == 1

    def test_get_item(self):
        py.test.skip("not implemented yet")
        w_res = self.interpret_expr('return ["foo"][0];')
        assert self.space.utf8_w(w_res) == "foo"
