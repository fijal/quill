from nolang.error import AppError
from support import BaseTest


class TestList(BaseTest):
    def test_empty_list(self):
        w_res = self.interpret_expr('return [];')
        assert self.space.len(w_res) == 0

    def test_short_list(self):
        w_res = self.interpret_expr('return ["foo", "bar"];')
        space = self.space
        assert space.len(w_res) == 2
        assert space.utf8_w(space.getitem(w_res, space.newint(0))) == "foo"
        assert space.utf8_w(space.getitem(w_res, space.newint(1))) == "bar"

    def test_getitem(self):
        w_res = self.interpret_expr('return ["foo", "bar"][0];')
        assert self.space.utf8_w(w_res) == "foo"

    def test_setitem(self):
        w_res = self.interpret_expr('''
            var x;
            x = ["foo"];
            x[0] = "bar";
            return x[0];
        ''')
        assert self.space.utf8_w(w_res) == "bar"

    def test_getitem_out_of_range(self):
        try:
            self.interpret_expr('return ["foo", "bar"][2];')
        except AppError as ae:
            assert ae.w_exception.w_type.name == 'IndexError'
            assert ae.w_exception.message == 'list index out of range'
        else:
            raise Exception("Applevel IndexError not raised.")

    def test_getitem_index_not_int(self):
        try:
            self.interpret_expr('return ["foo", "bar"]["zero"];')
        except AppError as ae:
            assert ae.w_exception.w_type.name == 'TypeError'
            assert ae.w_exception.message == 'list index must be int'
        else:
            raise Exception("Applevel TypeError not raised.")
