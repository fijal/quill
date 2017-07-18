
from nolang.lexer import get_lexer
from nolang.parser import get_parser, ParsingState
from nolang import astnodes as ast

from tests.support import reformat_expr


class BaseTest(object):
    def setup_class(self):
        self.parser = get_parser()
        self.lexer = get_lexer()

class TestExpressionParser(BaseTest):
    def parse(self, expr):
        program = "function foo () { " + expr + "; }"
        ast = self.parser.parse(self.lexer.lex(program), ParsingState(program))
        return ast.elements[0].body[0].expr

    def test_add(self):
        assert self.parse('1 + 1') == ast.BinOp('+', ast.Number(1), ast.Number(1))

class TestParseFunctionBody(BaseTest):
    def parse(self, body):
        program = reformat_expr(body)
        ast = self.parser.parse(self.lexer.lex(program), ParsingState(program))
        return ast.elements[0].body

    def test_var(self):
        r = self.parse('''
            var x;
            x = 3;
            x = x + 1;
            ''')
        assert r == [ast.VarDeclaration(['x']), ast.Assignment('x',
                 ast.Number(3)), ast.Assignment('x', ast.BinOp('+',
                    ast.Variable('x'), ast.Number(1)))]

    def test_while_loop(self):
        r = self.parse('''
            var i, s;
            i = 0;
            while i < 10 {
                i = i + 1;
                s = s + i;
            }
            return s;
            ''')
        assert r == [ast.VarDeclaration(['i', 's']),
                     ast.Assignment('i', ast.Number(0)),
                     ast.While(ast.BinOp('<', ast.Variable('i'),
                        ast.Number(10)), [
                          ast.Assignment('i', ast.BinOp('+',
                            ast.Variable('i'), ast.Number(1))),
                          ast.Assignment('s', ast.BinOp('+',
                            ast.Variable('s'), ast.Variable('i')))]),
                     ast.Return(ast.Variable('s'))]


# class TestFullProgram(BaseTest):

#     def parse(self, code):
#         program = xxx

#     def test_function_declaration(self):
#         r = self.parse('''
#             function foo() {
#                 var x;
#             }

#             function main() {
#             }
#             ''')
#         assert r == 3