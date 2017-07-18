
import re

from nolang.parser import get_parser, ParsingState
from nolang.lexer import get_lexer
from nolang.bytecode import compile_bytecode

def reformat_code(body):
    bodylines = body.split("\n")
    cut = 0
    while bodylines[cut].strip(" ") == '':
        cut += 1
    bodylines = bodylines[cut:]
    m = re.match(" +", bodylines[0])
    lgt = len(m.group(0))
    newlines = []
    for i, line in enumerate(bodylines):
        if line.strip(" ") == "":
            continue
        if line[:lgt] != " " * lgt:
            raise Exception("bad formatting, line: %d\n%s" % (i, line))
        newlines.append(" " * 4 + line[lgt:])
    return "function foo () {\n" + "\n".join(newlines) + "}"

class BaseTest(object):
    def setup_class(self):
        self.parser = get_parser()
        self.lexer = get_lexer()

    def compile(self, body):
        program = reformat_code(body)
        ast = self.parser.parse(self.lexer.lex(program), ParsingState(program))
        return compile_bytecode(ast.elements[0], program)
