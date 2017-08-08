from nolang.error import AppError
from support import BaseTest


class TestDict(BaseTest):
    def test_empty_dict(self):
        w_res = self.interpret_expr('return {};')
        assert self.space.type(w_res) is self.space.builtin_dict['Dict']
        assert self.space.len(w_res) == 0

    def test_short_dict(self):
        w_res = self.interpret_expr('return {"a": "foo", 1: "bar"};')
        space = self.space
        assert space.len(w_res) == 2
        assert space.utf8_w(space.getitem(w_res, space.newtext('a'))) == "foo"
        assert space.utf8_w(space.getitem(w_res, space.newint(1))) == "bar"

    def test_getitem(self):
        w_res = self.interpret_expr('''
            return {
                "a": "foo",
                1: "bar"
            }[1];
        ''')
        assert self.space.utf8_w(w_res) == "bar"

    def test_setitem(self):
        w_res = self.interpret_expr('''
            var x;
            x = {
                "a": "foo",
                1: "bar"
            };
            x["c"] = "baz";
            return x;
        ''')
        space = self.space
        assert self.space.len(w_res) == 3
        assert space.utf8_w(space.getitem(w_res, space.newtext("c"))) == "baz"

    def test_getitem_missing(self):
        try:
            self.interpret_expr('return {"foo": "bar"}["baz"];')
        except AppError as ae:
            assert ae.w_exception.w_type.name == 'KeyError'
            assert ae.w_exception.message == 'baz'
        else:
            raise Exception("Applevel KeyError not raised.")

    def test_execution_order(self):
        w_res = self.interpret('''
            def check(l, x) {
                l.append(x);
                return x;
            }

            def main() {
                var l;
                l = [];
                {check(l, 0): check(l, 1), check(l, 2): check(l, 3)};
                return l;
            }
        ''')
        w_ls = self.space.list_w(w_res)
        assert [self.space.int_w(w) for w in w_ls] == [0, 1, 2, 3]
