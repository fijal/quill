from rply.token import SourcePosition

from nolang.lexer import get_lexer, SourceRange
from nolang.parser import get_parser, ParsingState, ParseError
from nolang import astnodes as ast

from tests.support import reformat_expr, reformat_code


class BaseTest(object):
    def setup_class(self):
        self.parser = get_parser()
        self.lexer = get_lexer()


class TestExpressionParser(BaseTest):
    def parse(self, expr):
        program = "def foo () { " + expr + "; }"
        ast = self.parser.parse(self.lexer.lex('test', program),
                                ParsingState('test', program))
        return ast.elements[0].body[0].expr

    def test_add(self):
        assert self.parse('1 + 1') == ast.BinOp('+', ast.Number(1), ast.Number(1))

    def test_various_kinds_of_calls(self):
        r = self.parse('x(1, 2, 3)')
        assert r == ast.Call(ast.Identifier('x'), [ast.Number(1), ast.Number(2),
            ast.Number(3)])
        r = self.parse('(1)(2)')
        assert r == ast.Call(ast.Number(1), [ast.Number(2)])


class TestParseFunctionBody(BaseTest):
    def parse(self, body):
        program = reformat_expr(body)
        ast = self.parser.parse(self.lexer.lex('test', program),
                                ParsingState('test', program))
        return ast.elements[0].body

    def test_var(self):
        r = self.parse('''
            var x;
            x = 3;
            x = x + 1;
            ''')
        assert r == [ast.VarDeclaration(['x']), ast.Assignment('x',
                 ast.Number(3)), ast.Assignment('x', ast.BinOp('+',
                    ast.Identifier('x'), ast.Number(1)))]

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
                     ast.While(ast.BinOp('<', ast.Identifier('i'),
                        ast.Number(10)), [
                            ast.Assignment('i', ast.BinOp('+',
                                ast.Identifier('i'), ast.Number(1))),
                            ast.Assignment('s', ast.BinOp('+',
                                ast.Identifier('s'), ast.Identifier('i')))]),
                     ast.Return(ast.Identifier('s'))]


class TestFullProgram(BaseTest):

    def parse(self, code):
        program = reformat_code(code)
        return self.parser.parse(self.lexer.lex('test', program),
                                 ParsingState('test', program))

    def test_function_declaration(self):
        r = self.parse('''
            def foo() {
                var x;
            }

            def main() {
            }
            ''')
        expected = ast.Program([
            ast.Function('foo', [], [
                ast.VarDeclaration(['x'])
            ]),
            ast.Function('main', [], [])
        ])
        assert r == expected

    def test_function_declaration_args(self):
        r = self.parse('''
            def foo(a0, a1) {
            }
            ''')
        expected = ast.Program([
            ast.Function('foo', ['a0', 'a1'], [
            ])
        ])
        assert r == expected

    def test_empty_try(self):
        try:
            self.parse('''
                def foo() {
                    try {
                    }
                }
            ''')
        except ParseError:
            pass
        else:
            raise Exception("DID NOT RAISE")

    def test_import_stuff(self):
        r = self.parse('''
            import foo
            import foo.bar
            import foo{a,b,c,d}
            import foo.bar{a,b,c};
            ''')
        expected = ast.Program([
            ast.Import(["foo"], []),
            ast.Import(["foo"], ["bar"]),
            ast.Import(["foo"], ["a", "b", "c", "d"]),
            ast.Import(["foo", "bar"], ["a", "b", 'c'])
        ])
        assert r == expected

    def test_ast_pos(self):
        r = self.parse('''
            def foo(n) {
                return n + 1;
            }

            def main() {
            }
            ''')
        expected = ast.Program([
            ast.Function('foo', ['n'], [
                ast.Return(
                    ast.BinOp(
                        '+',
                        ast.Identifier('n', srcpos=mkpos(32, 2, 16, 33, 2, 17)),
                        ast.Number(1, srcpos=mkpos(36, 2, 20, 37, 2, 21)),
                        srcpos=mkpos(32, 2, 16, 37, 2, 21)
                    ),
                    srcpos=mkpos(25, 2, 9, 38, 2, 22)
                )
            ], srcpos=mkpos(4, 1, 5, 44, 3, 6)),
            ast.Function('main', [], [], srcpos=mkpos(49, 4, 5, 67, 5, 6))
        ], srcpos=mkpos(4, 1, 5, 67, 5, 6))
        assert r == expected

    def test_ast_pos_except(self):
        r = self.parse('''
            def main() {
                try {
                    raise Exception("foo");
                } except A {
                    return 1;
                } except Exception {
                    return 13;
                }
            }
            ''')
        expected = ast.Program([
            ast.Function('main', [], [
                ast.TryExcept([
                    ast.Raise(
                        ast.Call(
                            ast.Identifier('Exception', srcpos=mkpos(49, 3, 19, 58, 3, 28)),
                            [ast.String('foo', srcpos=mkpos(59, 3, 29, 64, 3, 34))],
                            srcpos=mkpos(49, 3, 19, 65, 3, 35)),
                        srcpos=mkpos(43, 3, 13, 66, 3, 36))
                ], [
                    ast.ExceptClause(
                        ['A'], None, [
                            ast.Return(
                                ast.Number(1, srcpos=mkpos(107, 5, 20, 108, 5, 21)),
                                srcpos=mkpos(100, 5, 13, 109, 5, 22))
                        ], srcpos=mkpos(77, 4, 11, 119, 6, 10)),
                    ast.ExceptClause(
                        ['Exception'], None, [
                            ast.Return(
                                ast.Number(13, srcpos=mkpos(158, 7, 20, 160, 7, 22)),
                                srcpos=mkpos(151, 7, 13, 161, 7, 23))
                        ], srcpos=mkpos(120, 6, 11, 171, 8, 10)),
                ], srcpos=mkpos(25, 2, 9, 171, 8, 10))
            ], srcpos=mkpos(4, 1, 5, 177, 9, 6))
        ], srcpos=mkpos(4, 1, 5, 177, 9, 6))
        assert r == expected


def mkpos(si, sl, sc, ei, el, ec):
    return SourceRange(SourcePosition(si, sl, sc), SourcePosition(ei, el, ec))
