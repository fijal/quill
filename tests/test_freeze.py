
from support import BaseTest


class TestFreeze(BaseTest):
    def interpret_expr(self, code):
        return BaseTest.interpret_expr(self, code, 'import core.freezing{freeze,thaw,is_frozen}')

    def test_freeze_already_frozen(self):
        assert self.space.is_true(self.interpret_expr('return is_frozen(none)'))
        assert self.space.is_true(self.interpret_expr('return is_frozen("foo")'))
