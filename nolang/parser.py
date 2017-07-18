
import rply

from nolang.lexer import TOKENS
from nolang import astnodes as ast

class ParsingState(object):
    def __init__(self, input):
        self.input = input

class ParseError(Exception):
    def __init__(self, line, filename, lineno, start_colno, end_colno):
        self.line = line
        self.filename = filename
        self.lineno = lineno
        self.start_colno = start_colno
        self.end_colno = end_colno

    def __str__(self):
        # 6 comes from formatting of ParseError by pytest
        return (self.line + "\n" + " " * (self.start_colno - 6) +
                "^" * (self.end_colno - self.start_colno))

def errorhandler(state, lookahead):
    lines = state.input.splitlines()
    sourcepos = lookahead.getsourcepos()
    line = lines[sourcepos.lineno - 1]
    raise ParseError(line, '<input>', sourcepos.lineno, sourcepos.colno - 1,
                     len(lookahead.value) + sourcepos.colno - 1)

def get_parser():
    pg = rply.ParserGenerator(TOKENS, precedence=[])
    pg.error(errorhandler)

    @pg.production('program : body')
    def program_body(state, p):
        return p[0]

    @pg.production('body :')
    def body_empty(state, p):
        return ast.Program([])

    @pg.production('body : body body_element')
    def body_body_element(state, p):
        p[0].get_element_list().append(p[1])
        return p[0]

    @pg.production('body_element : function')
    def body_function(state, p):
        return p[0]

    @pg.production('function : FUNCTION IDENTIFIER arglist LEFT_CURLY_BRACE'
                   ' function_body RIGHT_CURLY_BRACE')
    def function_function_body(state, p):
        return ast.Function(p[1], p[2], p[4].get_element_list())

    @pg.production('function_body :')
    def function_body_empty(state, p):
        return ast.FunctionBody([])

    @pg.production('function_body : function_body statement')
    def function_body_statement(state, p):
        p[0].get_element_list().append(p[1])
        return p[0]

    @pg.production('statement : expression SEMICOLON')
    def statement_expression(state, p):
        return ast.Statement(p[0])

    @pg.production('statement : VAR IDENTIFIER SEMICOLON')
    def statement_variable(state, p):
        return ast.VarDeclaration([p[1].getstr()])

    @pg.production('statement : IDENTIFIER EQUALS expression SEMICOLON')
    def statement_identifier_equals_expr(state, p):
        return ast.Assignment(p[0].getstr(), p[2])

    @pg.production('arglist : LEFT_PAREN RIGHT_PAREN')
    def arglist(state, p):
        return ast.Arglist()

    @pg.production('expression : INTEGER')
    def expression_number(state, p):
        return ast.Number(int(p[0].getstr()))

    @pg.production('expression : IDENTIFIER')
    def expression_identifier(state, p):
        return ast.Variable(p[0].getstr())

    @pg.production('expression : expression PLUS expression')
    def expression_plus_expression(state, p):
        return ast.Add(p[0], p[2])

    return pg.build()
