from rply.lexergenerator import Rule
from rply.token import Token as RplyToken


class Token(RplyToken):
    def getsrcpos(self):
        return (self.source_pos.start, self.source_pos.end)


class SourceRange(object):
    def __init__(self, start, end, lineno, colno):
        self.start = start
        self.end = end
        self.lineno = lineno
        self.colno = colno

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


QUILL_RULES = [
    ('INTEGER', r'\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('LT', r'\<'),
    ('STAR', r'\*'),
    ('DOT', r'\.'),
    ('TRUEDIV', r'\/\/'),
    ('EQ', r'=='),
    ('ASSIGN', r'='),
    ('ST_STRING', r'"'),
    ('ST_RAW', r"r'"),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('LEFT_CURLY_BRACE', r'\{'),
    ('LEFT_PAREN', r'\('),
    ('RIGHT_PAREN', r'\)'),
    ('RIGHT_CURLY_BRACE', r'\}'),
    ('COMMA', r','),
    ('SEMICOLON', r';'),
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


STRING_RULES = [
    ('ESC_QUOTE', r'\\"'),
    ('ESC_ESC', r'\\\\'),
    ('CHAR', r'[^"\\]'),
    ('ESC_SIMPLE', r'\\[abfnrtv0]'),
    ('ESC_HEX_8', r'\\x[0-9a-fA-F]{2}'),
    ('ESC_HEX_16', r'\\u[0-9a-fA-F]{4}'),
    ('ESC_HEX_ANY', r'\\u\{[0-9a-fA-F]+\}'),
    ('ESC_UNRECOGNISED', r'\\[^abfnrtv0xu"\\]'),
    ('ST_ENDSTRING', r'"'),
]


RAWSTRING_RULES = [
    ('RAW_ESC', r"\\."),
    ('RAW_CHAR', r"[^'\\]"),
    ('ST_ENDRAW', r"'"),
]


TOKENS = [x[0] for x in QUILL_RULES + STRING_RULES + RAWSTRING_RULES] + [x.upper() for x in KEYWORDS]

KEYWORD_DICT = dict.fromkeys(KEYWORDS)


class QuillLexerStream(object):
    _last_token = None

    def __init__(self, lexer, filename, s, state='INITIAL'):
        self.lexer = lexer
        self._filename = filename
        self.s = s
        self.state = self.lexer.get_state(state)

        self.idx = 0
        self._lineno = 1

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def _update_pos(self, match_start, match_end):
        lineno = self._lineno
        self.idx = match_end
        self._lineno += self.s.count("\n", match_start, match_end)
        last_nl = self.s.rfind("\n", 0, match_start)
        if last_nl < 0:
            colno = match_start + 1
        else:
            colno = match_start - last_nl
        return SourceRange(match_start, match_end, lineno, colno)

    def next(self):
        while True:
            if self.idx >= len(self.s):
                if not self.state.end_allowed:
                    raise self.parse_error("unterminated string")
                raise StopIteration
            if self.state.name == 'INITIAL':
                assert len(self.state.ignore_rules) == 1
                whitespace_rule = self.state.ignore_rules[0]
                match = whitespace_rule.matches(self.s, self.idx)
                if match is not None:
                    source_range = self._update_pos(match.start, match.end)
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
            else:
                for rule in self.state.ignore_rules:
                    match = rule.matches(self.s, self.idx)
                    if match:
                        self._update_pos(match.start, match.end)
                        break
                else:
                    break

        for rule in self.state.rules:
            match = rule.matches(self.s, self.idx)
            if match:
                source_range = self._update_pos(match.start, match.end)
                val = self.s[match.start:match.end]
                if val in KEYWORD_DICT:
                    name = val.upper()
                else:
                    name = rule.name
                token = Token(name, val, source_range)
                self._last_token = token
                if name in self.state.transitions:
                    self.state = self.lexer.get_state(self.state.transitions[name])
                print token
                return token
        else:
            raise self.parse_error("unrecognized token")

    def parse_error(self, msg):
        last_nl = self.s.rfind("\n", 0, self.idx)
        if last_nl < 0:
            colno = self.idx - 1
        else:
            colno = self.idx - last_nl - 1
        return ParseError(msg,
                          self.s.splitlines()[self._lineno - 1],
                          self._filename, self._lineno, colno, colno + 1)


class QuillLexer(object):
    def __init__(self, states):
        self.states = states

    def get_state(self, name):
        return self.states[name]

    def lex(self, filename, s):
        return QuillLexerStream(self, filename, s)


class LexerState(object):
    def __init__(self, name, end_allowed):
        self.name = name
        self.end_allowed = end_allowed
        self.rules = []
        self.ignore_rules = []
        self.transitions = {}

    def add(self, name, pattern, flags=0):
        self.rules.append(Rule(name, pattern, flags=flags))

    def ignore(self, pattern, flags=0):
        self.ignore_rules.append(Rule("", pattern, flags=flags))

    def transition(self, name, state):
        assert name not in self.transitions
        self.transitions[name] = state


class QuillLexerGenerator(object):
    def __init__(self):
        self.states = {}

    def state(self, name, end_allowed=True):
        assert name not in self.states
        self.states[name] = LexerState(name, end_allowed)
        return self.states[name]

    def build(self):
        return QuillLexer(self.states)


def get_lexer():
    lg = QuillLexerGenerator()

    initial = lg.state('INITIAL')
    for name, rule in QUILL_RULES:
        initial.add(name, rule)
    initial.ignore('\s+')
    initial.transition('ST_STRING', 'STRING')
    initial.transition('ST_RAW', 'RAWSTRING')

    string = lg.state('STRING', end_allowed=False)
    for name, rule in STRING_RULES:
        string.add(name, rule)
    string.transition('ST_ENDSTRING', 'INITIAL')

    raw = lg.state('RAWSTRING', end_allowed=False)
    for name, rule in RAWSTRING_RULES:
        raw.add(name, rule)
    raw.transition('ST_ENDRAW', 'INITIAL')

    return lg.build()
