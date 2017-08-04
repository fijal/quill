
""" AST nodes and corresponding compile functions. The basic AstNode comes
with compile() interface that produces bytecode
"""

from nolang import opcodes
from nolang.function import W_Function
from nolang.objects.usertype import W_UserType
from nolang.bytecode import compile_bytecode
from nolang.compiler import compile_class

from rply.token import BaseBox


class NameAlreadyDefined(Exception):
    def __init__(self, name):
        self.name = name


class StoringIntoGlobal(Exception):
    def __init__(self, name):
        self.name = name


class AstNode(BaseBox):
    def __init__(self, srcpos=None):
        if srcpos is None:
            srcpos = (None, None)
        self._startidx, self._endidx = srcpos

    def getsrcpos(self):
        return (self._startidx, self._endidx)

    def getstartidx(self):
        return self._startidx

    def getendidx(self):
        return self._endidx

    def compile(self, state):
        raise NotImplementedError("abstract base class")

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, ", ".join([
            "%s=%s" % (k, v) for k, v in self.__dict__.iteritems()
            if k != '_srcpos']))

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        to_compare = self.__dict__.copy()
        other = other.__dict__.copy()
        del to_compare['_startidx']
        del to_compare['_endidx']
        del other['_startidx']
        del other['_endidx']
        return to_compare == other

    def __ne__(self, other):
        return not self == other


class Number(AstNode):
    def __init__(self, value, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.value = value

    def compile(self, state):
        no = state.add_int_constant(self.value)
        state.emit(self.getstartidx(), opcodes.LOAD_CONSTANT, no)


class String(AstNode):
    def __init__(self, value, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.value = value

    def compile(self, state):
        no = state.add_str_constant(self.value)
        state.emit(self.getstartidx(), opcodes.LOAD_CONSTANT, no)


class BinOp(AstNode):
    def __init__(self, op, left, right, oppos, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.op = op
        self.oppos = oppos
        self.left = left
        self.right = right

    def compile(self, state):
        self.left.compile(state)
        self.right.compile(state)
        if self.op == '+':
            state.emit(self.oppos[0], opcodes.ADD)
        elif self.op == '-':
            state.emit(self.oppos[0], opcodes.SUB)
        elif self.op == '//':
            state.emit(self.oppos[0], opcodes.TRUEDIV)
        elif self.op == '*':
            state.emit(self.oppos[0], opcodes.MUL)
        elif self.op == '<':
            state.emit(self.oppos[0], opcodes.LT)
        elif self.op == '==':
            state.emit(self.oppos[0], opcodes.EQ)
        else:
            assert False


class And(AstNode):
    def __init__(self, left, right, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.left = left
        self.right = right

    def compile(self, state):
        self.left.compile(state)
        state.emit(self.left.getendidx(), opcodes.JUMP_IF_FALSE_NOPOP, 0)
        pos = state.get_patch_position()
        state.emit(self.right.getstartidx(), opcodes.DISCARD)
        self.right.compile(state)
        state.patch_position(pos, state.get_position())


class Or(AstNode):
    def __init__(self, left, right, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.left = left
        self.right = right

    def compile(self, state):
        self.left.compile(state)
        state.emit(self.left.getendidx(), opcodes.JUMP_IF_TRUE_NOPOP, 0)
        pos = state.get_patch_position()
        state.emit(self.right.getstartidx(), opcodes.DISCARD)
        self.right.compile(state)
        state.patch_position(pos, state.get_position())


class TrueNode(AstNode):
    def compile(self, state):
        state.emit(self.getstartidx(), opcodes.LOAD_TRUE)


class FalseNode(AstNode):
    def compile(self, state):
        state.emit(self.getstartidx(), opcodes.LOAD_FALSE)


class Program(AstNode):
    def __init__(self, elements, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.elements = elements

    def get_element_list(self):
        return self.elements


class Function(AstNode):
    def __init__(self, name, arglist, body, lineno=None, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.name = name
        self.arglist = arglist
        self.body = body
        self.lineno = lineno

    def get_name(self):
        return self.name

    def add_name(self, mapping):
        if self.name in mapping:
            raise NameAlreadyDefined(self.name)
        mapping[self.name] = len(mapping)

    def compile(self, state):
        for item in self.body:
            item.compile(state)

    def add_global_symbols(self, space, globals_w, source, w_mod):
        w_g = W_Function(self.name, compile_bytecode(self, source,
                         w_mod, self.arglist, self.lineno))
        globals_w.append(w_g)


class ClassDefinition(AstNode):
    def __init__(self, name, body, parent=None, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.name = name
        self.body = body
        self.parent = parent

    def get_name(self):
        return self.name

    def add_name(self, mapping):
        if self.name in mapping:
            raise NameAlreadyDefined(self.name)
        mapping[self.name] = len(mapping)

    def get_element_list(self):
        return self.body.get_element_list()

    def add_global_symbols(self, space, globals_w, source, w_mod):
        t = compile_class(space, source, self, w_mod, self.parent)
        alloc, class_elements_w, w_parent, default_alloc = t
        w_g = W_UserType(alloc, self.name, class_elements_w, w_parent,
                         default_alloc)
        globals_w.append(w_g)


class While(AstNode):
    def __init__(self, expr, block, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.expr = expr
        self.block = block

    def compile(self, state):
        jump_pos = state.get_position()
        self.expr.compile(state)
        state.emit(self.expr.getendidx(), opcodes.JUMP_IF_FALSE, 0)
        patch_pos = state.get_patch_position()
        for item in self.block:
            item.compile(state)
        state.emit(self.block[-1].getendidx(), opcodes.JUMP_ABSOLUTE, jump_pos)
        state.patch_position(patch_pos, state.get_position())


class If(AstNode):
    def __init__(self, expr, block, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.expr = expr
        self.block = block

    def compile(self, state):
        self.expr.compile(state)
        state.emit(self.expr.getendidx(), opcodes.JUMP_IF_FALSE, 0)
        patch_pos = state.get_patch_position()
        for item in self.block:
            item.compile(state)
        state.patch_position(patch_pos, state.get_position())


class TryExcept(AstNode):
    def __init__(self, block, except_blocks, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.block = block
        if isinstance(except_blocks[-1], FinallyClause):
            self.finally_clause = except_blocks[-1]
            self.except_blocks = except_blocks[:-1]
        else:
            self.finally_clause = None
            self.except_blocks = except_blocks

    def compile(self, state):
        state.emit(self.getstartidx(), opcodes.PUSH_RESUME_STACK, 0)
        pos = state.get_patch_position()
        for item in self.block:
            item.compile(state)
        if self.block:
            idx = self.block[-1].getendidx()
        else:
            idx = self.getstartidx()
        state.emit(idx, opcodes.POP_RESUME_STACK)
        state.emit(idx, opcodes.JUMP_ABSOLUTE, 0)
        jump_pos = state.get_patch_position()
        state.patch_position(pos, state.get_position())
        state.accumulator = [jump_pos]
        for item in self.except_blocks:
            item.compile(state)
        for pos in state.accumulator:
            state.patch_position(pos, state.get_position())
        if self.finally_clause is not None:
            self.finally_clause.compile(state)
        state.emit(self.getendidx(), opcodes.RERAISE)
        state.accumulator = None


class Raise(AstNode):
    def __init__(self, expr, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.expr = expr

    def compile(self, state):
        self.expr.compile(state)
        state.emit(self.expr.getstartidx(), opcodes.RAISE)


class Statement(AstNode):
    def __init__(self, expr, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.expr = expr

    def compile(self, state):
        if self.expr:
            self.expr.compile(state)
            state.emit(self.expr.getstartidx(), opcodes.DISCARD)


class Getattr(AstNode):
    def __init__(self, lhand, identifier, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.lhand = lhand
        self.identifier = identifier

    def compile(self, state):
        self.lhand.compile(state)
        no = state.add_str_constant(self.identifier)
        state.emit(self.lhand.getendidx(), opcodes.GETATTR, no)


class Setattr(AstNode):
    def __init__(self, lhand, identifier, rhand, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.lhand = lhand
        self.identifier = identifier
        self.rhand = rhand

    def compile(self, state):
        self.lhand.compile(state)
        self.rhand.compile(state)
        no = state.add_str_constant(self.identifier)
        state.emit(self.rhand.getendidx(), opcodes.SETATTR, no)


class ArgList(AstNode):
    def __init__(self, arglist, srcpos=None):
        AstNode.__init__(self, srcpos)
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
    def __init__(self, varnames, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.varnames = varnames

    def compile(self, state):
        for varname in self.varnames:
            state.register_variable(varname)


class Identifier(AstNode):
    def __init__(self, name, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.name = name

    def compile(self, state):
        op, no = state.get_variable(self.name)
        state.emit(self.getstartidx(), op, no)


class Assignment(AstNode):
    def __init__(self, varname, expr, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.varname = varname
        self.expr = expr

    def compile(self, state):
        self.expr.compile(state)
        op, varno = state.get_variable(self.varname)
        if op == opcodes.LOAD_GLOBAL:
            raise StoringIntoGlobal(self.varname)
        state.emit(self.expr.getstartidx(), opcodes.STORE, varno)


class Call(AstNode):
    def __init__(self, expr, arglist, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.left_hand = expr
        self.arglist = arglist

    def compile(self, state):
        self.left_hand.compile(state)
        for arg in self.arglist:
            arg.compile(state)
        state.emit(self.left_hand.getendidx(), opcodes.CALL, len(self.arglist))


class Return(AstNode):
    def __init__(self, expr, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.expr = expr

    def compile(self, state):
        self.expr.compile(state)
        state.emit(self.getstartidx(), opcodes.RETURN)


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
    def __init__(self, exception_names, varname, block, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.exception_names = exception_names
        self.varname = varname
        self.block = block

    def compile(self, state):
        no = state.register_exception_setup(self.exception_names)
        state.emit(self.getstartidx(), opcodes.COMPARE_EXCEPTION, no, 0)
        pos = state.get_patch_position()
        if self.varname is not None:
            state.emit(self.getstartidx(), opcodes.PUSH_CURRENT_EXC)
            no = state.register_variable(self.varname)
            state.emit(self.getstartidx(), opcodes.STORE, no)
        for item in self.block:
            item.compile(state)
        idx = self.getendidx()
        state.emit(idx, opcodes.CLEAR_CURRENT_EXC)
        state.emit(idx, opcodes.JUMP_ABSOLUTE, 0)
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
    def __init__(self, exception_names, varname, block, next, srcpos=None):
        self.exception_names = exception_names
        self.varname = varname
        self.block = block
        self.next = next
        self.clause_srcpos = srcpos

    def get_exc_clause(self):
        return ExceptClause(
            self.exception_names, self.varname, self.block, self.clause_srcpos)


class FinallyClause(BaseExcNode):
    next = None

    def __init__(self, block, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.block = block

    def compile(self, state):
        for item in self.block:
            item.compile(state)

    def get_exc_clause(self):
        return self


class Import(AstNode):
    def __init__(self, import_part, names, srcpos=None):
        AstNode.__init__(self, srcpos)
        self.import_part = import_part
        self.names = names

    def add_name(self, mapping):
        if not self.names:
            names = self.import_part
        else:
            names = self.names
        for name in names:
            if name in mapping:
                raise NameAlreadyDefined(name)
            mapping[name] = len(mapping)

    def add_global_symbols(self, space, globals_w, source, w_mod):
        w_module = space.import_symbols(self.import_part)
        if self.names is None:
            globals_w.append(w_module)
        else:
            assert len(self.import_part) == 1
            for name in self.names:
                globals_w.append(space.getattr(w_module, name))


class IdentifierListPartial(AstNode):
    def __init__(self, name, next, extra=None):
        self.name = name
        self.next = next
        self.extra = extra

    def get_names(self):
        count = 0
        cur = self
        while cur is not None:
            count += 1
            assert isinstance(cur, IdentifierListPartial)
            cur = cur.next
        lst = [None] * count
        i = 0
        cur = self
        while cur is not None:
            assert isinstance(cur, IdentifierListPartial)
            lst[i] = cur.name
            cur = cur.next
            i += 1
        return lst
