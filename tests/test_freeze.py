
from support import BaseTest


class TestFreeze(BaseTest):
    def interpret_expr(self, code):
        return BaseTest.interpret_expr(self, code, 'import core.freezing{freeze,thaw,is_frozen}')

    def test_freeze_already_frozen(self):
        assert self.space.is_true(self.interpret_expr('return is_frozen(none)'))
        assert self.space.is_true(self.interpret_expr('return is_frozen("foo")'))
        self.interpret_expr('freeze(none)')
        self.interpret_expr('freeze("foo")')
        # assert did not explode

    def test_cant_freeze_stringbuilder(self):
        w_res = self.interpret('''
            import core.freezing.freeze
            import core.text.StringBuilder

            def main() {
                try {
                    freeze(StringBuilder())
                } except FreezeError {
                    return 1
                }
                return 0
            }
            ''')
        assert self.space.int_w(w_res) == 1
