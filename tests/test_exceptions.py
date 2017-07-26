
from support import BaseTest

class TestExceptions(BaseTest):
    def test_exc_initialize(self):
        w_res = self.interpret_expr('return Exception("ekhe");')
        assert self.space.utf8_w(self.space.getattr(w_res, 'message')) == 'ekhe'

    def test_exc_raise(self):
        w_res = self.interpret_expr('''
            try {
                 raise Exception("foo");
            } except Exception {
                 return 13;
            }
            ''')
        assert self.space.int_w(w_res) == 13

    def test_exc_function_call(self):
        w_res = self.interpret('''
            class X(Exception) {

            }
            def foo() {
                raise X("message 2");
            }
            def main() {
                try {
                    foo();
                } except Exception {
                    return 13;
                }
            }
            ''')
        assert self.space.int_w(w_res) == 13

    def test_nested_exc_block(self):
        w_res = self.interpret('''
            class X(Exception) {

            }

            def main() {
                try {
                    try {
                        raise Exception("foo");
                    } except X {
                        return 18;
                    }
                } except Exception {
                    return 15;
                }
            }
            ''')
        assert self.space.int_w(w_res) == 15

    def test_exc_double_except(self):
        w_res = self.interpret('''
            class A(Exception) {
            }
            class B(Exception) {
            }

            def main() {
                try {
                    raise Exception("foo");
                } except A {
                    return 1;
                } except B {
                    return 2;
                } except Exception {
                    return 13;
                }
            }
            ''')
        assert self.space.int_w(w_res) == 13

    def test_exc_raise_catch_as_e(self):
        w_res = self.interpret_expr('''
            try {
                 raise Exception("foo");
            } except Exception as e {
                 return e.message;
            }
            ''')
        assert self.space.utf8_w(w_res) == "foo"
