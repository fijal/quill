
from support import BaseTest, reformat_code
from nolang.compiler import compile_module
from nolang.module import W_Module

class TestCompiler(BaseTest):
    def test_compile_module(self):
        code = reformat_code('''
            def foo() {
                return 3;
            }
        ''')
        w_mod = compile_module(code, self.parse(code))
        assert isinstance(w_mod, W_Module)
        assert w_mod.name2index == {'foo': 0}
