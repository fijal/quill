
from support import BaseTest, reformat_code
from nolang.interpreter import Interpreter
from nolang.compiler import compile_module
from nolang.frameobject import Frame
from nolang.objects.space import Space

class TestInterpreterBasic(BaseTest):
    def setup_method(self, meth):
        self.space = Space(None)

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
            s = 0;
            while i < 10 {
                i = i + 1;
                s = s + i;
            }
            return s;
            ''')
        assert self.space.int_w(w_r) == 55

    def test_simple_if(self):
        w_r = self.interpret('''
            if 0 < 3 {
                return 3;
            }
            ''')
        assert self.space.int_w(w_r) == 3

    def test_logical_or_and(self):
        w_r = self.interpret('''
            return 0 or 1;
            ''')
        assert self.space.int_w(w_r) == 1
        w_r = self.interpret('''
            var x;
            return 15 or x;
            ''')
        # unitialized x ignored (for now)
        assert self.space.int_w(w_r) == 15
        w_r = self.interpret('''
            return 1 and 2;
            ''')
        assert self.space.int_w(w_r) == 2
        w_r = self.interpret('''
            var x;
            return 0 and x;
            ''')
        assert self.space.int_w(w_r) == 0
        w_r = self.interpret('''
            return 1 and true;
            ''')
        assert self.space.w_True is w_r

    def test_longer_blocks(self):
        code = '\n'.join(['if 0 < 3 {'] + ['    1;'] * 300 + ['}'])
        self.interpret(code) # assert did not crash

class TestInterpreter(BaseTest):
    def interpret(self, code):
        interpreter = Interpreter()
        source = reformat_code(code)
        ast = self.parse(source)
        w_mod = compile_module(source, ast)
        self.space = Space(interpreter)
        w_mod.initialize(self.space)
        return self.space.call_method(w_mod, 'main', [])

    def test_basic(self):
        w_res = self.interpret('''
            function main() {
                return 3;
            }
            ''')
        assert self.space.int_w(w_res) == 3

    def test_function_declaration_and_call(self):
        w_res = self.interpret('''
            function foo() {
                return 3;
            }

            function main() {
                return foo() + 1;
            }
            ''')
        assert self.space.int_w(w_res) == 4

    def test_function_call_args(self):
        w_res = self.interpret('''
            function foo(a0, a1)
            {
                return a0 + a1;
            }
            function main() {
                return foo(1, 3);
            }
            ''')
        assert self.space.int_w(w_res) == 4

    def test_recursive_call(self):
        w_res = self.interpret('''
            function fib(n) {
                if (n == 0) or (n == 1) {
                    return 1;
                }
                return fib(n - 1) + fib(n - 2);
            }
            function main() {
                return fib(5);
            }
            ''')
        assert self.space.int_w(w_res) == 8
