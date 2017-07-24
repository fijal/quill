
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

    def test_exc_raise_catch_as_e(self):
        py.test.skip(";ater")
        w_res = self.interpret_expr('''
            try {
                 raise Exception("foo");
            } except Exception as e {
                 return e.message;
            }
            ''')
        assert self.space.int_w(w_res) == 13
