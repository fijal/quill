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

    def test_append(self):
        w_res = self.interpret_expr('''
            var x;
            x = ["foo"];
            x.append("bar");
            return x;
        ''')
        space = self.space
        assert space.len(w_res) == 2
        assert space.utf8_w(space.getitem(w_res, space.newint(1))) == "bar"

    def test_method_call_on_wrong_obj(self):
        try:
            self.interpret_expr('''
            List.append(1, 2)
            ''')
        except AppError as ae:
            if not ae.match(self.space, self.space.w_typeerror):
                raise
            assert ae.w_exception.message == "Expected List object, got Int"
        else:
            raise Exception("did not raise")

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

    def test_execution_order(self):
        w_res = self.interpret('''
            def check(l, x) {
                l.append(x);
                return x;
            }

            def main() {
                var l;
                l = [];
                [check(l, 0), check(l, 1)];
                return l;
            }
        ''')
        [w_0, w_1] = self.space.list_w(w_res)
        assert [self.space.int_w(w_0), self.space.int_w(w_1)] == [0, 1]
