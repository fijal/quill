
from nolang.error import AppError

from support import BaseTest


class TestFunctions(BaseTest):
    def assert_argerror(self, code, msg=None):
        try:
            self.interpret(code)
        except AppError as e:
            if e.match(self.space, self.space.w_argerror):
                if msg is not None:
                    assert e.w_exception.message == msg
            else:
                raise
        else:
            raise Exception("did not raise")

    def test_simple_function(self):
        w_res = self.interpret('''
            def foo() {
                return 13
            }

            def main() {
                return foo()
            }
        ''')
        assert self.space.int_w(w_res) == 13

    def test_simple_args(self):
        w_res = self.interpret('''
            def foo(a, b) {
                return a + b
            }

            def main() {
                return foo(10, 3)
            }
        ''')
        assert self.space.int_w(w_res) == 13

    def test_named_args(self):
        w_res = self.interpret('''
            def foo(a, b) {
                return a * 10 + b
            }

            def main() {
                return foo(a=2, b=3)
            }
        ''')
        assert self.space.int_w(w_res) == 23

        w_res = self.interpret('''
            def foo(a, b) {
                return a * 10 + b
            }

            def main() {
                return foo(b=3, a=2)
            }
        ''')
        assert self.space.int_w(w_res) == 23

    def test_too_few_args(self):
        self.assert_argerror('''
            def foo(a, b) {
                return a * 10 + b
            }

            def main() {
                return foo(1)
            }
        ''', "Function foo got 1 arguments, expected 2")

    def test_too_many_args(self):
        self.assert_argerror('''
            def foo(a, b) {
                return a * 10 + b
            }

            def main() {
                return foo(1, 2, 3)
            }
        ''', "Function foo got 3 arguments, expected 2")
        self.assert_argerror('''
            def foo(a, b) {
                return a * 10 + b
            }

            def main() {
                return foo(1, b=2, c=3)
            }
        ''', "Function foo got 3 arguments, expected 2")

    def test_unexpected_keyword(self):
        self.assert_argerror('''
            def foo(a, b) {
                return a * 10 + b
            }

            def main() {
                return foo(1, c=2)
            }
        ''', "Function foo got unexpected keyword argument 'c'")

    def test_duplicate_args(self):
        self.assert_argerror('''
            def foo(a, b) {
                return a * 10 + b
            }

            def main() {
                return foo(1, a=2)
            }
        ''', "Function foo got multiple values for argument 'a'")
        self.assert_argerror('''
            def foo(a, b) {
                return a * 10 + b
            }

            def main() {
                return foo(b=1, b=2)
            }
        ''', "Function foo got multiple values for argument 'b'")

    def test_default_args(self):
        w_res = self.interpret('''
            def foo(a, b=1, c="foo") {
                return a * 10 + b + len(c)
            }

            def main() {
                return foo(2, 3, c="x") * 1000 + foo(2)
            }
        ''')
        assert self.space.int_w(w_res) == 24000 + 24

        w_res = self.interpret('''
            def foo(a, b=1) {
                return a * 10 + b
            }

            def main() {
                return foo(2)
            }
        ''')
        assert self.space.int_w(w_res) == 21

        w_res = self.interpret('''
            def foo(a=1, b=2) {
                return a * 100 + b
            }

            def main() {
                return foo() * 100 + foo(3, 4)
            }
            ''')
        assert self.space.int_w(w_res) == 10504
