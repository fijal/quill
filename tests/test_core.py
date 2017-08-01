
from support import BaseTest

class TestCore(BaseTest):
    def test_core_reflect_getframe(self):
        self.interpret('''
            import core.reflect

            def main() {
                var frame
                frame = reflect.get_current_frame()
                return frame
            }
            ''')
