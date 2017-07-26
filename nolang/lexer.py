
from rply import LexerGenerator
from rply.lexer import Lexer, LexerStream
from rply.token import SourcePosition, Token
from rply.errors import LexingError

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
    ('FINALLY', r'finally'),
    ('AS', r'as'),
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

class QuillLexerStream(LexerStream):
    _last_token = None

    def next(self):
        while True:
            if self.idx >= len(self.s):
                raise StopIteration
            assert len(self.lexer.ignore_rules) == 1
            whitespace_rule = self.lexer.ignore_rules[0]
            match = whitespace_rule.matches(self.s, self.idx)
            if match is not None:
                lineno = self._lineno
                colno = self._update_pos(match)
                if "\n" in self.s[match.start:match.end]:
                    if self._last_token.name not in ('RIGHT_CURLY_BRACE',
                        'RIGHT_PAREN', 'IDENTIFIER', 'INTEGER'):
                        continue
                    source_pos = SourcePosition(match.start, lineno, colno)
                    token = Token(
                        'SEMICOLON', self.s[match.start:match.end], source_pos
                    )
                    self._last_token = token
                    return token
            else:
                break

        for rule in self.lexer.rules:
            match = rule.matches(self.s, self.idx)
            if match:
                lineno = self._lineno
                colno = self._update_pos(match)
                source_pos = SourcePosition(match.start, lineno, colno)
                token = Token(
                    rule.name, self.s[match.start:match.end], source_pos
                )
                self._last_token = token
                return token
        else:
            raise LexingError(None, SourcePosition(self.idx, -1, -1))


class QuillLexer(Lexer):
    def lex(self, s):
        return QuillLexerStream(self, s)

class QuillLexerGenerator(LexerGenerator):
    def build(self):
        return QuillLexer(self.rules, self.ignore_rules)

def get_lexer():
    lg = QuillLexerGenerator()

    for name, rule in RULES:
        lg.add(name, rule)
    lg.ignore('\s+')
    return lg.build()
