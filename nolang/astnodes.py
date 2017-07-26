
""" AST nodes and corresponding compile functions. The basic AstNode comes
with compile() interface that produces bytecode
"""

from nolang import opcodes
from nolang.function import W_Function
from nolang.objects.usertype import W_UserType
from nolang.bytecode import compile_bytecode
from nolang.compiler import compile_class

from rply.token import BaseBox

class StoringIntoGlobal(Exception):
    pass

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

class String(AstNode):
    def __init__(self, value):
        self.value = value

    def compile(self, state):
        no = state.add_str_constant(self.value)
        state.emit(opcodes.LOAD_CONSTANT, no)

class BinOp(AstNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def compile(self, state):
        self.left.compile(state)
        self.right.compile(state)
        if self.op == '+':
            state.emit(opcodes.ADD)
        elif self.op == '-':
            state.emit(opcodes.SUB)
        elif self.op == '//':
            state.emit(opcodes.TRUEDIV)
        elif self.op == '*':
            state.emit(opcodes.MUL)
        elif self.op == '<':
            state.emit(opcodes.LT)
        elif self.op == '==':
            state.emit(opcodes.EQ)
        else:
            assert False

class And(AstNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def compile(self, state):
        self.left.compile(state)
        state.emit(opcodes.JUMP_IF_FALSE_NOPOP, 0)
        pos = state.get_patch_position()
        state.emit(opcodes.DISCARD)
        self.right.compile(state)
        state.patch_position(pos, state.get_position())

class Or(AstNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def compile(self, state):
        self.left.compile(state)
        state.emit(opcodes.JUMP_IF_TRUE_NOPOP, 0)
        pos = state.get_patch_position()
        state.emit(opcodes.DISCARD)
        self.right.compile(state)
        state.patch_position(pos, state.get_position())

class TrueNode(AstNode):
    def compile(self, state):
        state.emit(opcodes.LOAD_TRUE)

class FalseNode(AstNode):
    def compile(self, state):
        state.emit(opcodes.LOAD_FALSE)

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

    def get_name(self):
        return self.name

    def compile(self, state):
        for item in self.body:
            item.compile(state)

    def wrap_as_global_symbol(self, source, w_mod):
        return W_Function(self.name, compile_bytecode(self, source,
                          w_mod, self.arglist))

class ClassDefinition(AstNode):
    def __init__(self, name, body, parent=None):
        self.name = name
        self.body = body
        self.parent = parent

    def get_name(self):
        return self.name

    def get_element_list(self):
        return self.body.get_element_list()

    def wrap_as_global_symbol(self, source, w_mod):
        class_elements_w, w_parent = compile_class(source, self, w_mod,
                                                   self.parent)
        return W_UserType(self.name, class_elements_w, w_parent)

class While(AstNode):
    def __init__(self, expr, block):
        self.expr = expr
        self.block = block

    def compile(self, state):
        jump_pos = state.get_position()
        self.expr.compile(state)
        state.emit(opcodes.JUMP_IF_FALSE, 0)
        patch_pos = state.get_patch_position()
        for item in self.block:
            item.compile(state)
        state.emit(opcodes.JUMP_ABSOLUTE, jump_pos)
        state.patch_position(patch_pos, state.get_position())

class If(AstNode):
    def __init__(self, expr, block):
        self.expr = expr
        self.block = block

    def compile(self, state):
        self.expr.compile(state)
        state.emit(opcodes.JUMP_IF_FALSE, 0)
        patch_pos = state.get_patch_position()
        for item in self.block:
            item.compile(state)
        state.patch_position(patch_pos, state.get_position())

class TryExcept(AstNode):
    def __init__(self, block, except_blocks):
        self.block = block
        if isinstance(except_blocks[-1], FinallyClause):
            self.finally_clause = except_blocks[-1]
            self.except_blocks = except_blocks[:-1]
        else:
            self.finally_clause = None
            self.except_blocks = except_blocks

    def compile(self, state):
        state.emit(opcodes.PUSH_RESUME_STACK, 0)
        pos = state.get_patch_position()
        for item in self.block:
            item.compile(state)
        state.emit(opcodes.POP_RESUME_STACK)
        state.emit(opcodes.JUMP_ABSOLUTE, 0)
        jump_pos = state.get_patch_position()
        state.patch_position(pos, state.get_position())
        state.accumulator = [jump_pos]
        for item in self.except_blocks:
            item.compile(state)
        for pos in state.accumulator:
            state.patch_position(pos, state.get_position())
        if self.finally_clause is not None:
            self.finally_clause.compile(state)
        state.emit(opcodes.RERAISE)
        state.accumulator = None

class Raise(AstNode):
    def __init__(self, expr):
        self.expr = expr

    def compile(self, state):
        self.expr.compile(state)
        state.emit(opcodes.RAISE)

class Statement(AstNode):
    def __init__(self, expr):
        self.expr = expr

    def compile(self, state):
        if self.expr:
            self.expr.compile(state)
            state.emit(opcodes.DISCARD)

class Getattr(AstNode):
    def __init__(self, lhand, identifier):
        self.lhand = lhand
        self.identifier = identifier

    def compile(self, state):
        self.lhand.compile(state)
        no = state.add_str_constant(self.identifier)
        state.emit(opcodes.GETATTR, no)

class Setattr(AstNode):
    def __init__(self, lhand, identifier, rhand):
        self.lhand = lhand
        self.identifier = identifier
        self.rhand = rhand

    def compile(self, state):
        self.lhand.compile(state)
        self.rhand.compile(state)
        no = state.add_str_constant(self.identifier)
        state.emit(opcodes.SETATTR, no)

class ArgList(AstNode):
    def __init__(self, arglist):
        self.arglist = arglist

    def get_names(self):
        return self.arglist

class FunctionBody(AstNode):
    def __init__(self, elem, next):
        self.elem = elem
        self.next = next

    def get_element_list(self):
        count = 0
        cur = self
        while cur.next is not None:
            if cur.elem is not None:
                count += 1
            cur = cur.next
            assert isinstance(cur, FunctionBody)
        if cur.elem is not None:
            count += 1
        cur = self
        lst = [None] * count
        i = len(lst) - 1
        while cur.next is not None:
            if cur.elem is not None:
                lst[i] = cur.elem
                i -= 1
            cur = cur.next
            assert isinstance(cur, FunctionBody)
        if cur.elem is not None:
            lst[i] = cur.elem
        return lst

class VarDeclaration(AstNode):
    def __init__(self, varnames):
        self.varnames = varnames

    def compile(self, state):
        for varname in self.varnames:
            state.register_variable(varname)

class Identifier(AstNode):
    def __init__(self, name):
        self.name = name

    def compile(self, state):
        op, no = state.get_variable(self.name)
        state.emit(op, no)
 
class Assignment(AstNode):
    def __init__(self, varname, expr):
        self.varname = varname
        self.expr = expr

    def compile(self, state):
        self.expr.compile(state)
        op, varno = state.get_variable(self.varname)
        if op == opcodes.LOAD_GLOBAL:
            raise StoringIntoGlobal()
        state.emit(opcodes.STORE, varno)

class Call(AstNode):
    def __init__(self, expr, arglist):
        self.left_hand = expr
        self.arglist = arglist

    def compile(self, state):
        self.left_hand.compile(state)
        for arg in self.arglist:
            arg.compile(state)
        state.emit(opcodes.CALL, len(self.arglist))

class Return(AstNode):
    def __init__(self, expr):
        self.expr = expr

    def compile(self, state):
        self.expr.compile(state)
        state.emit(opcodes.RETURN)

class ExpressionListPartial(AstNode):
    def __init__(self, elements):
        self.elements = elements

    def get_element_list(self):
        return self.elements

class VarDeclPartial(AstNode):
    def __init__(self, names):
        self.names = names

    def get_names(self):
        return self.names

class ExceptClause(AstNode):
    def __init__(self, exception_names, varname, block):
        self.exception_names = exception_names
        self.varname = varname
        self.block = block

    def compile(self, state):
        no = state.register_exception_setup(self.exception_names)
        state.emit(opcodes.COMPARE_EXCEPTION, no, 0)
        pos = state.get_patch_position()
        if self.varname is not None:
            state.emit(opcodes.PUSH_CURRENT_EXC)
            no = state.register_variable(self.varname)
            state.emit(opcodes.STORE, no)
        for item in self.block:
            item.compile(state)
        state.emit(opcodes.CLEAR_CURRENT_EXC)
        state.emit(opcodes.JUMP_ABSOLUTE, 0)
        state.accumulator.append(state.get_patch_position())
        state.patch_position(pos, state.get_position())

class BaseExcNode(AstNode):
    def gather_list(self):
        count = 1
        cur = self
        while cur.next is not None:
            cur = cur.next
            assert isinstance(cur, BaseExcNode)
            count += 1
        lst = [None] * count
        lst[0] = self.get_exc_clause()
        pos = 1
        cur = self
        while cur.next is not None:
            cur = cur.next
            assert isinstance(cur, BaseExcNode)
            lst[pos] = cur.get_exc_clause()
            pos += 1
        return lst

class ExceptClauseList(BaseExcNode):
    def __init__(self, exception_names, varname, block, next):
        self.exception_names = exception_names
        self.varname = varname
        self.block = block
        self.next = next

    def get_exc_clause(self):
        return ExceptClause(self.exception_names, self.varname, self.block)

class FinallyClause(BaseExcNode):
    next = None

    def __init__(self, block):
        self.block = block

    def compile(self, state):
        for item in self.block:
            item.compile(state)

    def get_exc_clause(self):
        return self
