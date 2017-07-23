
from support import BaseTest

class TestClasses(BaseTest):
    def test_simple_class(self):
        w_res = self.interpret('''
            class X {
                def __init__(self) {
                    self.x = 13;
                }
            }

            def main() {
                var x;
                x = X();
                return x.x;
            }
            ''')
        assert self.space.int_w(w_res) == 13

    def test_method_call(self):
        w_res = self.interpret('''
            class X {
                def method(self) {
                    return 3;
                }
            }

            def main() {
                var x;
                x = X();
                return x.method() + x.method();
            }
            ''')
        assert self.space.int_w(w_res) == 6
