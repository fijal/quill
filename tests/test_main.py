
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
        try:
            main(str(fname))
        except SystemExit as e:
            assert e.code == 1
        else:
            raise Exception('did not get system exit')
