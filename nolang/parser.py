
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
        return ast.Function(p[1].getstr(), p[2].get_element_list(),
                            p[4].get_element_list())

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

    @pg.production('statement : VAR IDENTIFIER var_decl SEMICOLON')
    def statement_var_decl(state, p):
        return ast.VarDeclaration([p[1].getstr()] + p[2].get_names())

    @pg.production('var_decl : ')
    def var_decl_empty(state, p):
        return ast.VarDeclPartial([])

    @pg.production('var_decl : COMMA IDENTIFIER var_decl')
    def var_decl_identifier(state, p):
        return ast.VarDeclPartial([p[1].getstr()] + p[2].get_names())

    @pg.production('statement : IDENTIFIER EQUALS expression SEMICOLON')
    def statement_identifier_equals_expr(state, p):
        return ast.Assignment(p[0].getstr(), p[2])

    @pg.production('statement : RETURN expression SEMICOLON')
    def statement_return(state, p):
        return ast.Return(p[1])

    @pg.production('statement : WHILE expression LEFT_CURLY_BRACE function_body'
                   ' RIGHT_CURLY_BRACE')
    def statement_while_loop(state, p):
        return ast.While(p[1], p[3].get_element_list())

    @pg.production('statement : IF expression LEFT_CURLY_BRACE function_body'
                   ' RIGHT_CURLY_BRACE')
    def statement_if_block(state, p):
        return ast.If(p[1], p[3].get_element_list())

    @pg.production('arglist : LEFT_PAREN RIGHT_PAREN')
    def arglist(state, p):
        return ast.ArgList([])

    @pg.production('arglist : LEFT_PAREN IDENTIFIER var_decl RIGHT_PAREN')
    def arglist_non_empty(state, p):
        return ast.ArgList([p[1].getstr()] + p[2].get_names())

    @pg.production('expression : INTEGER')
    def expression_number(state, p):
        return ast.Number(int(p[0].getstr()))

    @pg.production('expression : IDENTIFIER')
    def expression_identifier(state, p):
        return ast.Identifier(p[0].getstr())

    @pg.production('expression : expression OR expression')
    def expression_or_expression(state, p):
        return ast.Or(p[0], p[2])

    @pg.production('expression : expression AND expression')
    def expression_and_expression(state, p):
        return ast.And(p[0], p[2])

    @pg.production('expression : TRUE')
    def expression_true(state, p):
        return ast.True()

    @pg.production('expression : FALSE')
    def expression_false(state, p):
        return ast.False()

    @pg.production('expression : expression LEFT_PAREN expression_list '
                   'RIGHT_PAREN')
    def expression_call(state, p):
        return ast.Call(p[0], p[2].get_element_list())

    @pg.production('expression : LEFT_PAREN expression RIGHT_PAREN')
    def expression_paren_expression_paren(state, p):
        return p[1]

    @pg.production('expression : expression PLUS expression')
    def expression_plus_expression(state, p):
        return ast.BinOp('+', p[0], p[2])

    @pg.production('expression : expression LT expression')
    def expression_lt_expression(state, p):
        return ast.BinOp('<', p[0], p[2])

    @pg.production('expression_list : ')
    def expression_list_empty(state, p):
        return ast.ExpressionListPartial([])

    @pg.production('expression_list : expression expression_sublist')
    def expression_list_expression(state, p):
        return ast.ExpressionListPartial([p[0]] + p[1].get_element_list())

    @pg.production('expression_sublist : ')
    def expression_sublist_empty(state, p):
        return ast.ExpressionListPartial([])

    @pg.production('expression_sublist : COMMA expression expression_sublist')
    def expression_sublist_expression(state, p):
        return ast.ExpressionListPartial([p[1]] + p[2].get_element_list())

    return pg.build()
