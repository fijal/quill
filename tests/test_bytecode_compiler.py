
from nolang.parser import ParsingState, get_parser
from nolang.lexer import get_lexer
from nolang.bytecode import compile_bytecode

import re
from support import reformat_code

class TestBytecodeCompiler(object):
    def setup_class(self):
        self.parser = get_parser()
        self.lexer = get_lexer()

    def compile(self, body):
        program = reformat_code(body)
        ast = self.parser.parse(self.lexer.lex(program), ParsingState(program))
        return compile_bytecode(ast.elements[0])

    def assert_equals(self, bytecode, expected):
        def reformat(lines):
            # find first non empty
            for line in lines:
                if line.strip(" ") != "":
                    break
            m = re.match(" +", line)
            skip = len(m.group(0))
            return [line[(skip - 2):] for line in lines if line.strip(" ") != ""]

        lines = bytecode.repr().splitlines()
        exp_lines = reformat(expected.splitlines())
        assert lines == exp_lines

    def test_bytecode_simple(self):
        body = """
        x = 3;
        """
        self.assert_equals(self.compile(body), """
            LOAD_CONSTANT 0
            STORE 0
            """)

    def test_bytecode_bit_more_complext(self):
        body = """
        x = 3;
        x = x + 1;
        """
        bc = self.compile(body)
        self.assert_equals(bc,"""
            LOAD_CONSTANT 0
            STORE 0
            LOAD_VARIABLE 0
            LOAD_CONSTANT 1
            ADD
            STORE 0
            """)
        assert bc.stack_depth == 2
