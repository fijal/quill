
from rply import LexerGenerator
from rply.lexer import Lexer, LexerStream
from rply.token import SourcePosition, Token

class ParseError(Exception):
    def __init__(self, msg, line, filename, lineno, start_colno, end_colno):
        self.msg = msg
        self.line = line
        self.filename = filename
        self.lineno = lineno
        self.start_colno = start_colno
        self.end_colno = end_colno

    def __str__(self):
        # 6 comes from formatting of ParseError by pytest
        return (self.line + "\n" + " " * (self.start_colno - 6) +
                "^" * (self.end_colno - self.start_colno))

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

    def __init__(self, lexer, filename, s):
        self._filename = filename
        LexerStream.__init__(self, lexer, s)

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
            last_nl = self.s.rfind("\n", 0, self.idx)
            if last_nl < 0:
                colno = self.idx - 1
            else:
                colno = self.idx - last_nl - 1
            raise ParseError("unrecognized token",
                             self.s.splitlines()[self._lineno - 1],
                             self._filename, self._lineno, colno, colno + 1)


class QuillLexer(Lexer):
    def lex(self, filename, s):
        return QuillLexerStream(self, filename, s)

class QuillLexerGenerator(LexerGenerator):
    def build(self):
        return QuillLexer(self.rules, self.ignore_rules)

def get_lexer():
    lg = QuillLexerGenerator()

    for name, rule in RULES:
        lg.add(name, rule)
    lg.ignore('\s+')
    return lg.build()
