
from rply.token import BaseBox

class AstNode(BaseBox):
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

class Add(AstNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

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
 
class Assignment(AstNode):
    def __init__(self, varname, expr):
        self.varname = varname
        self.expr = expr
