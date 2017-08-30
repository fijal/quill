import re
from support import BaseTest


class TestBytecodeCompiler(BaseTest):

    def assert_equals(self, bytecode, expected):
        def reformat(lines):
            # find first non empty
            for line in lines:
                if line.strip(" ") != "":
                    break
            m = re.match(" +", line)
            skip = len(m.group(0))
            return [line[(skip - 2):] for line in lines if line.strip(" ") != ""]

        lines = bytecode.repr(False).splitlines()
        exp_lines = reformat(expected.splitlines())
        assert lines == exp_lines

    def test_bytecode_simple(self):
        body = """
        var x
        x = 3
        """
        self.assert_equals(self.compile(body), """
            LOAD_CONSTANT 0
            STORE 0
            LOAD_NONE
            RETURN
            """)

    def test_bytecode_bit_more_complex(self):
        body = """
        var x
        x = 3
        x = x + 1
        """
        bc = self.compile(body)
        self.assert_equals(bc, """
            LOAD_CONSTANT 0
            STORE 0
            LOAD_VARIABLE 0
            LOAD_CONSTANT 1
            ADD
            STORE 0
            LOAD_NONE
            RETURN
            """)
        assert bc.stack_depth == 2

    def test_loop(self):
        body = """
        var i
        i = 0

        while i < 10 {
           i = i + 1
        }
        """
        bc = self.compile(body)
        self.assert_equals(bc, """
            LOAD_CONSTANT 0
            STORE 0
            LOAD_VARIABLE 0
            LOAD_CONSTANT 1
            LT
            JUMP_IF_FALSE 29
            LOAD_VARIABLE 0
            LOAD_CONSTANT 2
            ADD
            STORE 0
            JUMP_ABSOLUTE 6
            LOAD_NONE
            RETURN
            """)

    def test_compile_exc_handling(self):
        bc = self.compile("""
        try {

        } except Exception {

        }
        """)
        self.assert_equals(bc, """
            PUSH_RESUME_STACK 7
            POP_RESUME_STACK
            JUMP_ABSOLUTE 16
            COMPARE_EXCEPTION 0 16
            CLEAR_CURRENT_EXC
            JUMP_ABSOLUTE 16
            RERAISE
            LOAD_NONE
            RETURN
        """)

    def test_compile_try_just_finally(self):
        bc = self.compile('''
        try {
        } except Exception {
        } finally {
            return 3
        }
        ''')
        self.assert_equals(bc, """
            PUSH_RESUME_STACK 7
            POP_RESUME_STACK
            JUMP_ABSOLUTE 16
            COMPARE_EXCEPTION 0 16
            CLEAR_CURRENT_EXC
            JUMP_ABSOLUTE 16
            LOAD_CONSTANT 0
            RETURN
            RERAISE
            LOAD_NONE
            RETURN
        """)

    def test_compile_try_finally(self):
        bc = self.compile('''
        try {
        } finally {
            return 3
        }
        ''')
        self.assert_equals(bc, """
            PUSH_RESUME_STACK 7
            POP_RESUME_STACK
            JUMP_ABSOLUTE 7
            LOAD_CONSTANT 0
            RETURN
            RERAISE
            LOAD_NONE
            RETURN
        """)

    def test_for_loop(self):
        bc = self.compile('''
            for i in 1 { 1; }
            ''')
        self.assert_equals(bc, """
            LOAD_CONSTANT 0
            CREATE_ITER
            ITER_NEXT
            JUMP_IF_EMPTY 18
            STORE 0
            LOAD_CONSTANT 1
            DISCARD
            JUMP_ABSOLUTE 4
            DISCARD
            DISCARD
            LOAD_NONE
            RETURN
            """)
