import py
from support import BaseTest, reformat_code
from nolang.main import run_code


class TestImport(BaseTest):
    def test_basic_import_self(self, tmpdir):
        py.test.skip("skip for now")
        main_file = tmpdir.join('main.q')
        main_file.write(reformat_code('''
            import self.foo

            def main() {
                print(foo.bar(3))
            }
            '''))

        foo_file = tmpdir.join('foo.q')
        foo_file.write(reformat_code('''
            def bar(i) {
                return i + 3
            }
        '''))
        run_code(str(main_file))
