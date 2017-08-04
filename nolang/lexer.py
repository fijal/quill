from rply import LexerGenerator
from rply.lexer import Lexer, LexerStream
from rply.token import Token


class SourceRange(object):
    def __init__(self, start, end, lineno, colno):
        self.start = start
        self.end = end
        self.lineno = lineno
        self.colno = colno

    def __getitem__(self, i):
        return (self.start, self.end, self.lineno)[i]

    def __repr__(self):
        return "SourceRange(start=%d, end=%d, lineno=%d, colno=%d)" % (
            self.start, self.end, self.lineno, self.colno)


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
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('LEFT_CURLY_BRACE', r'\{'),
    ('LEFT_PAREN', r'\('),
    ('RIGHT_PAREN', r'\)'),
    ('RIGHT_CURLY_BRACE', r'\}'),
    ('COMMA', r','),
    ('SEMICOLON', r';'),
    ('STRING', r'"[^"]*"'),
]

KEYWORDS = [
    'def',
    'class',
    'return',
    'var',
    'while',
    'if',
    'or',
    'and',
    'true',
    'false',
    'try',
    'except',
    'finally',
    'as',
    'raise',
    'import',
]

TOKENS = [x[0] for x in RULES] + [x.upper() for x in KEYWORDS]

KEYWORD_DICT = dict.fromkeys(KEYWORDS)


class QuillLexerStream(LexerStream):
    _last_token = None

    def __init__(self, lexer, filename, s):
        self._filename = filename
        LexerStream.__init__(self, lexer, s)

    def _update_pos(self, match):
        lineno = self._lineno
        self.idx = match.end
        self._lineno += self.s.count("\n", match.start, match.end)
        last_nl = self.s.rfind("\n", 0, match.start)
        if last_nl < 0:
            colno = match.start + 1
        else:
            colno = match.start - last_nl
        return SourceRange(match.start, match.end, lineno, colno)

    def next(self):
        while True:
            if self.idx >= len(self.s):
                raise StopIteration
            assert len(self.lexer.ignore_rules) == 1
            whitespace_rule = self.lexer.ignore_rules[0]
            match = whitespace_rule.matches(self.s, self.idx)
            if match is not None:
                source_range = self._update_pos(match)
                if "\n" in self.s[match.start:match.end]:
                    if self._last_token.name not in \
                       ('RIGHT_CURLY_BRACE', 'RIGHT_PAREN', 'IDENTIFIER', 'INTEGER'):
                        continue
                    token = Token(
                        'SEMICOLON', self.s[match.start:match.end], source_range
                    )
                    self._last_token = token
                    return token
            else:
                break

        for rule in self.lexer.rules:
            match = rule.matches(self.s, self.idx)
            if match:
                source_range = self._update_pos(match)
                val = self.s[match.start:match.end]
                if val in KEYWORD_DICT:
                    name = val.upper()
                else:
                    name = rule.name
                token = Token(name, val, source_range)
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
