
from support import BaseTest
from nolang.interpreter import Interpreter
from nolang.frameobject import Frame
from nolang.objects.space import Space

class TestInterpreterBasic(BaseTest):
    def setup_method(self, meth):
        self.space = Space()

    def interpret(self, code):
        interpreter = Interpreter()
        bytecode = self.compile(code)
        bytecode.setup(self.space)
        f = Frame(bytecode)
        return interpreter.interpret(self.space, bytecode, f)

    def test_interpret(self):
        w_res = self.interpret('''
            var x;
            x = 1;
            ''')
        assert w_res is self.space.w_None

    def test_var_assign(self):
        w_res = self.interpret('''
            var x;
            x = 3;
            return x;
        ''')
        assert self.space.int_w(w_res) == 3

    def test_while_loop(self):
        w_r = self.interpret('''
            var i, s;
            i = 0;
            while i < 10 {
                i = i + 1;
                s = s + i;
            }
            return s;
            ''')
        assert self.space.int_w(w_r) == 45        
