
import py
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
        pass
        #w_res = self.interpret_expr('''
        #    ''')

    def test_exc_double_except(self):
        py.test.skip("in progress")
        w_res = self.interpret_expr('''
            class A(Exception) {
            }
            class B(Exception) {
            }

            try {
                raise Exception("foo");
            }
            ''')

    def test_exc_raise_catch_as_e(self):
        py.test.skip("later")
        w_res = self.interpret_expr('''
            try {
                 raise Exception("foo");
            } except Exception as e {
                 return e.message;
            }
            ''')
        assert self.space.int_w(w_res) == 13
