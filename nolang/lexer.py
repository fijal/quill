
from rply import LexerGenerator
from rply.lexer import Lexer

RULES = [
    ('INTEGER', r'\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('LT', r'\<'),
    ('STAR', r'\*'),
    ('DOT', r'\.'),
    ('TRUEDIV', r'\/\/'),
    ('EQ', r'=='),
    ('ASSIGN', r'='),
    ('FUNCTION', r'def'),
    ('CLASS', r'class'),
    ('RETURN', r'return'),
    ('VAR', r'var'),
    ('WHILE', r'while'),
    ('IF', r'if'),
    ('OR', r'or'),
    ('AND', r'and'),
    ('TRUE', r'true'),
    ('FALSE', r'false'),
    ('TRY', r'try'),
    ('EXCEPT', r'except'),
    ('RAISE', r'raise'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('LEFT_CURLY_BRACE', r'\{'),
    ('LEFT_PAREN', r'\('),
    ('RIGHT_PAREN', r'\)'),
    ('RIGHT_CURLY_BRACE', r'\}'),
    ('COMMA', r','),
    ('SEMICOLON', r';'),
    ('STRING', r'"[^"]*"'),
]

TOKENS = [x[0] for x in RULES]

class QuillLexer(Lexer):
    pass

class QuillLexerGenerator(LexerGenerator):
    def build(self):
        return QuillLexer(self.rules, self.ignore_rules)

def get_lexer():
    lg = QuillLexerGenerator()

    for name, rule in RULES:
        lg.add(name, rule)
    lg.ignore('\s+')
    return lg.build()
