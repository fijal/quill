
import re

from support import reformat_code
from nolang.main import main


class TestMain(object):
    def test_main(self, tmpdir):
        fname = tmpdir.join("foo.q")
        fname.write(reformat_code("""
        def main() {
            print(3);
        }
        """))
        assert main(['nolang-c', str(fname)]) == 0

    def test_main_lex_error(self, tmpdir, capsys):
        fname = tmpdir.join("foo.q")
        fname.write(reformat_code("""
            def main() {
                $
            }
            """))
        assert main(['nolang-c', str(fname)]) == 1
        out, err = capsys.readouterr()
        assert out.find("unrecognized token") > 0

    def test_main_traceback_formatting(self, tmpdir, capfd):
        fname = tmpdir.join("foo.q")
        fname.write(reformat_code("""
            def foo() {
                raise Exception("foo")
            }

            def main() {
                foo()
            }
            """))
        assert main(['nolang-c', str(fname)]) == 1
        out, err = capfd.readouterr()
        expected = [
            'file .*/foo.q, line 2',
            'raise Exception\("foo"\)',
            'file .*/foo.q, line 5',
            'foo\(\)',
            'Exception: foo'
        ]
        lines = err.splitlines()
        assert len(lines) == len(expected)
        for i in range(len(lines)):
            assert re.search(expected[i], lines[i])
