
from support import BaseTest


class TestTypes(BaseTest):
    def test_str_enforcement(self):
        self.interpret("""
            def main() {
                var x: Str
                x = 13
            }
            """)
