from nolang.lexer import get_lexer


class TestLexing(object):
    def test_program(self):
        tokens = [x.name for x in get_lexer().lex('', "def name () {}")]
        assert tokens == ['DEF', 'IDENTIFIER', 'LEFT_PAREN', 'RIGHT_PAREN',
                          'LEFT_CURLY_BRACE', 'RIGHT_CURLY_BRACE']

    def test_one_plus_two(self):
        tokens = [x.name for x in get_lexer().lex('', '1+1')]
        assert tokens == ['INTEGER', 'PLUS', 'INTEGER']

    def test_keyword_varname(self):
        tokens = [x.name for x in get_lexer().lex('', '1 + varfoo')]
        assert tokens == ['INTEGER', 'PLUS', 'IDENTIFIER']
        tokens = [x.name for x in get_lexer().lex('', '1 + let')]
        assert tokens == ['INTEGER', 'PLUS', 'LET']
