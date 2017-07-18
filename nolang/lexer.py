
from rply import LexerGenerator

RULES = [
    ('INTEGER', r'\d+'),
    ('PLUS', r'\+'),
    ('EQUALS', r'='),
    ('FUNCTION', r'function'),
    ('VAR', r'var'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('LEFT_CURLY_BRACE', r'\{'),
    ('LEFT_PAREN', r'\('),
    ('RIGHT_PAREN', r'\)'),
    ('RIGHT_CURLY_BRACE', r'\}'),
    ('SEMICOLON', r';'),
]

TOKENS = [x[0] for x in RULES]

def get_lexer():
    lg = LexerGenerator()

    for name, rule in RULES:
        lg.add(name, rule)
    lg.ignore('\s+')
    return lg.build()
