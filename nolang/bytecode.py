
""" Bytecode representation and compilation. See opcodes.py for
details about bytecodes
"""

from nolang import opcodes

from rpython.rlib.rstring import StringBuilder

class BaseConstant(object):
    pass

class IntegerConstant(BaseConstant):
    def __init__(self, v):
        self._intval = v

    def wrap(self, space):
        return space.newint(self._intval)

class InvalidStackDepth(Exception):
    pass

class Bytecode(object):
    def __init__(self, source, varnames, constants, bytecode):
        self.source = source
        self.varnames = varnames
        self._constants = constants
        self.constants = None
        self.bytecode = bytecode
        self.stack_depth = self.compute_stack_depth(bytecode)

    def setup(self, space):
        self.constants = [None] * len(self._constants)
        for i, constant in enumerate(self._constants):
            self.constants[i] = constant.wrap(space)

    def repr(self):
        i = 0
        res = StringBuilder()
        bc = self.bytecode
        while i < len(bc):
            opcode = opcodes.opcodes[ord(bc[i])]
            if opcode.numargs == 0:
                res.append("  " + opcode.name)
                i += 1
            elif opcode.numargs == 1:
                res.append("  %s %d" % (opcode.name, ord(bc[i + 1])))
                i += 2
            else:
                assert opcode.numargs == 2
                res.append("  %s %d %d" % (opcode.name, ord(bc[i + 2]),
                                           ord(bc[i + 3])))
                i += 3
            res.append("\n")
        return res.build()

    @staticmethod
    def compute_stack_depth(bc):
        i = 0
        stack_depth = 0
        max_stack_depth = 0
        while i < len(bc):
            opcode = opcodes.opcodes[ord(bc[i])]
            stack_depth += opcode.stack_effect
            if opcode.numargs == 0:
                i += 1
            elif opcode.numargs == 1:
                i += 2
            else:
                assert opcode.numargs == 2
                i += 3
            max_stack_depth = max(max_stack_depth, stack_depth)
        if stack_depth != 0:
            raise InvalidStackDepth()
        return max_stack_depth

class UndeclaredVariable(Exception):
    def __init__(self, name):
        self.name = name

class _CompileBuilder(object):
    def __init__(self):
        self.vars = {}
        self.varnames = []
        self.builder = StringBuilder()
        self.constants = [] # XXX implement interning of integers, strings etc.

    def add_constant(self, const):
        no = len(self.constants)
        self.constants.append(const)
        return no

    def add_int_constant(self, v):
        return self.add_constant(IntegerConstant(v))

    def get_variable(self, name):
        try:
            return self.vars[name]
        except KeyError:
            raise UndeclaredVariable(name)

    def register_variable(self, v):
        no = len(self.vars)
        self.varnames.append(no) # XXX should we rely on dicts being ordered?
        self.vars[v] = no
        assert len(self.vars) == len(self.varnames)

    def emit(self, opcode, arg0=0, arg1=0):
        self.builder.append(chr(opcode))
        assert arg0 < 256
        assert arg1 < 256
        numargs = opcodes.opcodes[opcode].numargs
        if numargs > 0:
            self.builder.append(chr(arg0))
        if numargs > 1:
            self.builder.append(chr(arg1))
        assert numargs <= 2

    def build(self, source):
        return Bytecode(source, self.varnames, self.constants, self.builder.build())

def compile_bytecode(ast, source):
    """ Compile the bytecode from produced AST.
    """
    builder = _CompileBuilder()
    ast.compile(builder)
    # hack to enable building for now
    builder.emit(opcodes.LOAD_NONE)
    builder.emit(opcodes.RETURN)
    return builder.build(source)
