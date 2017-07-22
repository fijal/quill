
from rply import LexerGenerator

RULES = [
    ('INTEGER', r'\d+'),
    ('PLUS', r'\+'),
    ('LT', r'\<'),
    ('EQUALS', r'='),
    ('FUNCTION', r'function'),
    ('RETURN', r'return'),
    ('VAR', r'var'),
    ('WHILE', r'while'),
    ('IF', r'if'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('LEFT_CURLY_BRACE', r'\{'),
    ('LEFT_PAREN', r'\('),
    ('RIGHT_PAREN', r'\)'),
    ('RIGHT_CURLY_BRACE', r'\}'),
    ('COMMA', r','),
    ('SEMICOLON', r';'),
]

TOKENS = [x[0] for x in RULES]

def get_lexer():
    lg = LexerGenerator()

    for name, rule in RULES:
        lg.add(name, rule)
    lg.ignore('\s+')
    return lg.build()
