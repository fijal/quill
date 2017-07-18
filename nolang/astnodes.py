
""" AST nodes and corresponding compile functions. The basic AstNode comes
with compile() interface that produces bytecode
"""

from nolang import opcodes

from rply.token import BaseBox

class AstNode(BaseBox):
    def compile(self, state):
        raise NotImplementedError("abstract base class")

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, ", ".join([
            "%s=%s" % (k, v) for k, v in self.__dict__.iteritems()]))

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

class Number(AstNode):
    def __init__(self, value):
        self.value = value

    def compile(self, state):
        no = state.add_int_constant(self.value)
        state.emit(opcodes.LOAD_CONSTANT, no)

class Add(AstNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def compile(self, state):
        self.left.compile(state)
        self.right.compile(state)
        state.emit(opcodes.ADD)

class Program(AstNode):
    def __init__(self, elements):
        self.elements = elements

    def get_element_list(self):
        return self.elements

class Function(AstNode):
    def __init__(self, name, arglist, body):
        self.name = name
        self.arglist = arglist
        self.body = body

    def compile(self, state):
        for item in self.body:
            item.compile(state)

class Statement(AstNode):
    def __init__(self, expr):
        self.expr = expr

class Arglist(AstNode):
    def __init___(self):
        pass

class FunctionBody(AstNode):
    def __init__(self, elements):
        self.elements = elements

    def get_element_list(self):
        return self.elements

class VarDeclaration(AstNode):
    def __init__(self, varnames):
        self.varnames = varnames

class Variable(AstNode):
    def __init__(self, name):
        self.name = name

    def compile(self, state):
        no = state.get_variable(self.name)
        state.emit(opcodes.LOAD_VARIABLE, no)
 
class Assignment(AstNode):
    def __init__(self, varname, expr):
        self.varname = varname
        self.expr = expr

    def compile(self, state):
        self.expr.compile(state)
        varno = state.get_variable(self.varname)
        state.emit(opcodes.STORE, varno)
