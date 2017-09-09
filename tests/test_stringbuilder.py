
from support import BaseTest


class TestStringBuilder(BaseTest):
    def test_basic(self):
        w_res = self.interpret("""
            import core.text.StringBuilder

            def main() {
                var s = StringBuilder()
                log(s.build())
                s = StringBuilder(11)
                s.append("foo")
                s.append("a\\n")
                return s.build()
            }
            """)
        assert self.space.utf8_w(self.space.log[0]) == ''
        assert self.space.utf8_w(w_res) == "fooa\n"
