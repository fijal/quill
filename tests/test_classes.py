
from support import BaseTest


class TestClasses(BaseTest):
    def test_simple_class(self):
        w_res = self.interpret('''
            class X {
                def __init__(self) {
                    self.x = 13
                }
            }

            def main() {
                var x
                x = X()
                return x.x
            }
            ''')
        assert self.space.int_w(w_res) == 13

    def test_method_call(self):
        w_res = self.interpret('''
            class X {
                def method(self) {
                    return 3
                }
            }

            def main() {
                var x
                x = X()
                return x.method() + x.method()
            }
            ''')
        assert self.space.int_w(w_res) == 6

    def test_inheritance_basic(self):
        w_res = self.interpret('''
            class X {
                def method(self) {
                    return 3
                }
            }
            class Y(X) {
            }
            def main() {
                var x
                x = Y()
                return x.method()
            }
            ''')
        assert self.space.int_w(w_res) == 3

    def test_inheritance(self):
        w_res = self.interpret('''
            class X {
                def method(self) {
                    return 1
                }
            }

            class Y(X) {
                def method(self) {
                    return 2
                }
            }

            def main() {
                var x, y
                x = X()
                y = Y()
                return x.method() * 10 + y.method()
            }
            ''')
        assert self.space.int_w(w_res) == 12

    def test_class_attributes(self):
        import py
        py.test.skip("foo")
        w_res = self.interpret("""
            class X {
                var attr;

                def __init__(self, x) {
                    self.attr = x;
                }
            }

            def main() {
                var x;
                x = X(13);
                return x.attr;
            }
            """)
        assert self.space.int_w(w_res) == 13
