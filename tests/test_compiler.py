
from support import BaseTest, reformat_code
from nolang.compiler import compile_module
from nolang.module import W_Module
from nolang.importer import Importer


class TestCompiler(BaseTest):
    def test_compile_module(self):
        code = reformat_code('''
            def foo() {
                return 3;
            }
        ''')
        imp = Importer(self.space)
        w_mod = compile_module(self.space, 'test', 'self.test', code,
                               self.parse(code), imp)
        assert isinstance(w_mod, W_Module)
        assert w_mod.name2index['foo'] == len(self.space.builtins_w)
