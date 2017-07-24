
from support import BaseTest

class TestExceptions(BaseTest):
    def test_exc_initialize(self):
        w_res = self.interpret_expr('return Exception("ekhe");')
        assert self.space.utf8_w(self.space.getattr(w_res, 'message')) == 'ekhe'
