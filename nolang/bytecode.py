
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

class StringConstant(BaseConstant):
    def __init__(self, v):
        self._strval = v

    def wrap(self, space):
        return space.newtext(self._strval)

class InvalidStackDepth(Exception):
    pass

class Bytecode(object):
    def __init__(self, source, varnames, module, constants, bytecode, arglist,
                 exception_blocks):
        self.source = source
        self.varnames = varnames
        self.module = module
        self._constants = constants
        self.constants = None
        self.bytecode = bytecode
        r = self.compute_stack_depth(bytecode)
        self.stack_depth, self.resume_stack_depth = r
        self.arglist = arglist
        self.exception_blocks = exception_blocks

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
                argval = (ord(bc[i + 1]) << 8) + ord(bc[i + 2])
                res.append("  %s %d" % (opcode.name, argval))
                i += 3
            else:
                assert opcode.numargs == 2
                arg1 = (ord(bc[i + 1]) << 8) + ord(bc[i + 2])
                arg2 = (ord(bc[i + 3]) << 8) + ord(bc[i + 4])
                res.append("  %s %d %d" % (opcode.name, arg1, arg2))
                i += 5
            res.append("\n")
        return res.build()

    @staticmethod
    def compute_stack_depth(bc):
        i = 0
        stack_depth = 0
        max_stack_depth = 0
        resume_stack_depth = 0
        max_resume_stack_depth = 0
        while i < len(bc):
            opcode = opcodes.opcodes[ord(bc[i])]
            if opcode.stack_effect == 255:
                var = (ord(bc[i + 1]) << 8) + ord(bc[i + 2])
                stack_depth -= var
            else:
                stack_depth += opcode.stack_effect
            if ord(bc[i]) == opcodes.PUSH_RESUME_STACK:
                resume_stack_depth += 1
                max_resume_stack_depth = max(max_resume_stack_depth,
                                             resume_stack_depth)
            if ord(bc[i]) == opcodes.POP_RESUME_STACK:
                resume_stack_depth -= 1
            if opcode.numargs == 0:
                i += 1
            elif opcode.numargs == 1:
                i += 3
            else:
                assert opcode.numargs == 2
                i += 5
            max_stack_depth = max(max_stack_depth, stack_depth)
        if stack_depth != 0 or resume_stack_depth != 0:
            raise InvalidStackDepth()
        return max_stack_depth, max_resume_stack_depth

class UndeclaredVariable(Exception):
    def __init__(self, name):
        self.name = name

class ExceptionBlock(object):
    def __init__(self, types_w):
        self.types_w = types_w
        self.position = 0

    def match(self, space, w_exception):
        for w_type in self.types_w:
            if space.issubclass(space.type(w_exception), w_type):
                return True
        return False

class _BytecodeBuilder(object):
    def __init__(self, w_mod, arglist):
        self.vars = {}
        self.varnames = []
        self.builder = []
        self.constants = [] # XXX implement interning of integers, strings etc.
        self.exception_blocks = []
        self.w_mod = w_mod
        for name in arglist:
            self.register_variable(name)
        self.arglist = arglist

    def add_constant(self, const):
        no = len(self.constants)
        self.constants.append(const)
        return no

    def add_int_constant(self, v):
        return self.add_constant(IntegerConstant(v))

    def add_str_constant(self, v):
        return self.add_constant(StringConstant(v))

    def get_variable(self, name):
        try:
            return opcodes.LOAD_VARIABLE, self.vars[name]
        except KeyError:
            pass
        try:
            return opcodes.LOAD_GLOBAL, self.w_mod.name2index[name]
        except KeyError:
            pass
        raise UndeclaredVariable(name)

    def register_variable(self, v):
        no = len(self.vars)
        self.varnames.append(no) # XXX should we rely on dicts being ordered?
        self.vars[v] = no
        assert len(self.vars) == len(self.varnames)

    def register_exception_setup(self, exc_names):
        types_w = []
        for name in exc_names:
            types_w.append(self.w_mod.functions[self.w_mod.name2index[name]])
        self.exception_blocks.append(ExceptionBlock(types_w))
        return len(self.exception_blocks) - 1

    def emit(self, opcode, arg0=0, arg1=0):
        self.builder.append(chr(opcode))
        assert arg0 < 0x10000
        assert arg1 < 0x10000
        numargs = opcodes.opcodes[opcode].numargs
        if numargs > 0:
            self.builder.append(chr(arg0 >> 8))
            self.builder.append(chr(arg0 & 0xff))
        if numargs > 1:
            self.builder.append(chr(arg1 >> 8))
            self.builder.append(chr(arg1 & 0xff))
        assert numargs <= 2

    def get_position(self):
        return len(self.builder)

    def get_patch_position(self):
        return len(self.builder) - 2

    def patch_position(self, pos, target):
        assert target < 0x10000
        self.builder[pos] = chr(target >> 8)
        self.builder[pos + 1] = chr(target & 0xff)

    def build(self, source):
        return Bytecode(source, self.varnames, self.w_mod, self.constants,
                        "".join(self.builder), self.arglist,
                        self.exception_blocks)

def compile_bytecode(ast, source, w_mod, arglist=[]):
    """ Compile the bytecode from produced AST.
    """
    builder = _BytecodeBuilder(w_mod, arglist[:])
    ast.compile(builder)
    # hack to enable building for now
    builder.emit(opcodes.LOAD_NONE)
    builder.emit(opcodes.RETURN)
    return builder.build(source)
