
import py
from support import BaseTest

class TestClasses(BaseTest):
    def test_simple_class(self):
        py.test.skip("unimplemented")
        w_res = self.interpret('''
            class X {
                def __init__(self) {
                    self.x = 13;
                }
            }

            def main() {
                x = X();
                return x.x;
            }
            ''')
        assert self.space.int_w(w_res) == 13
