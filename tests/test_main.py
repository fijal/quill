
from support import reformat_code
from nolang.main import main

class TestMain(object):
    def test_main(self, tmpdir):
        fname = tmpdir.join("foo.no")
        fname.write(reformat_code("""
        def main() {
            print(3);
        }
        """))
        assert main(['nolang-c', str(fname)]) == 0

    def test_main_lex_error(self, tmpdir, capsys):
        fname = tmpdir.join("foo.no")
        fname.write(reformat_code("""
            def main() {
                $
            }
            """))
        assert main(['nolang-c', str(fname)]) == 1
        out, err = capsys.readouterr()
        assert out.find("unrecognized token") > 0
