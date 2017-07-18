
from nolang.lexer import get_lexer
from nolang.parser import get_parser, ParsingState
from nolang import astnodes as ast
import re

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
        assert self.parse('1 + 1') == ast.Add(ast.Number(1), ast.Number(1))

class TestParseFunctionBody(BaseTest):
    def parse(self, body):
        bodylines = body.split("\n")
        cut = 0
        while bodylines[cut].strip(" ") == '':
            cut += 1
            bodylines = bodylines[cut:]
        m = re.match(" +", bodylines[0])
        lgt = len(m.group(0))
        newlines = []
        for i, line in enumerate(bodylines):
            if line[:lgt] != " " * lgt:
                raise Exception("bad formatting, line: %d\n%s" % (i, line))
            newlines.append(" " * 4 + line[lgt:])
        program = "function foo () {\n" + "\n".join(newlines) + "}"
        ast = self.parser.parse(self.lexer.lex(program), ParsingState(program))
        return ast.elements[0].body

    def test_var(self):
        r = self.parse('''
            var x;
            x = 3;
            x = x + 1;
            ''')
        assert r == [ast.VarDeclaration(['x']), ast.Assignment('x',
                 ast.Number(3)), ast.Assignment('x', ast.Add(
                    ast.Variable('x'), ast.Number(1)))]

