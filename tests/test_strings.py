# -*- coding: utf-8 -*-

from support import BaseTest


class TestStrings(BaseTest):
    def test_string_literal(self):
        w_res = self.interpret_expr('return "foo";')
        assert self.space.utf8_w(w_res) == "foo"

    def test_unicode_literal(self):
        w_res = self.interpret_expr(u'return "wziąść";'.encode('utf8'))
        assert self.space.utf8_w(w_res) == u"wziąść".encode('utf8')

    def test_string_equality(self):
        assert self.interpret_expr('return "foo" == "foo";') is self.space.w_True
        assert self.interpret_expr('return "foo" == "bar";') is self.space.w_False


class TestInterpolatedStrings(BaseTest):
    def test_simple_expressions(self):
        w_res = self.interpret_expr('return `${1} + ${2} = ${1 + 2}`;')
        assert self.space.utf8_w(w_res) == "1 + 2 = 3"

    def test_string_expressions(self):
        w_res = self.interpret_expr('''return `${'a'} + ${"b"} = ${r'c'}`;''')
        assert self.space.utf8_w(w_res) == "a + b = c"

    def test_vars_and_calls(self):
        w_res = self.interpret('''
            def foo(a, b) {
                return a + b;
            }

            def main() {
                var x, y;
                x = "hello";
                y = 7;
                return `[${x} ${y} ${foo(1, 2)}]`;
            }
        ''')
        assert self.space.utf8_w(w_res) == "[hello 7 3]"

    def test_nested(self):
        w_res = self.interpret_expr('return `[${"o"}]`;')
        assert self.space.utf8_w(w_res) == "[o]"
        w_res = self.interpret_expr('return `[${`<${"o"}>`}]`;')
        assert self.space.utf8_w(w_res) == "[<o>]"
        w_res = self.interpret_expr('return `[${`<${`(${"o"})`}>`}]`;')
        assert self.space.utf8_w(w_res) == "[<(o)>]"
