
from support import BaseTest

class TestCore(BaseTest):
    def test_core_reflect_getframe(self):
        w_res = self.interpret('''
            import core.reflect

            def main() {
                var frame
                frame = reflect.get_current_frame()
                return frame.filename
            }
            ''')
        assert self.space.utf8_w(w_res) == 'test'
