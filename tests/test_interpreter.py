
from support import BaseTest
from nolang.interpreter import Interpreter
from nolang.frameobject import Frame
from nolang.objects.space import Space

class TestInterpreterBasic(BaseTest):
    def test_interpret(self):
        space = Space()
        interpreter = Interpreter()
        bytecode = self.compile('''
            x = 1;
            ''')
        bytecode.setup(space)
        f = Frame(bytecode)
        w_res = interpreter.interpret(space, bytecode, f)
        assert w_res is space.w_None
