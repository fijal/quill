from support import BaseTest, reformat_code
from nolang.main import run_code


class TestImport(BaseTest):
    def test_basic_import_self(self, tmpdir):
        main_file = tmpdir.join('main.q')
        main_file.write(reformat_code('''
            import self.foo.bar
            import self.foo

            def main() {
                print(bar(3) + foo.bar(13))
            }
            '''))

        foo_file = tmpdir.join('foo.q')
        foo_file.write(reformat_code('''
            def bar(i) {
                return i + 3
            }
        '''))
        run_code(str(main_file))
