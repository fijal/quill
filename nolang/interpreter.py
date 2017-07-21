
""" This is the main interpreter file that contains bytecode
dispatch loop.
"""

from nolang import opcodes

class InvalidOpcode(Exception):
    def __init__(self, opcode):
        self.opcode = opcode

    def __str__(self):
        try:
            return "<UnimplementedOpcode %s>" % opcodes.opcodes[self.opcode].name
        except IndexError:
            return "<InvalidOpcode %d>" % self.opcode

class UninitializedVariable(Exception):
    pass # XXX add logic to present the error

class Interpreter(object):
    def __init__(self):
        pass

    def interpret(self, space, bytecode, frame):
        index = 0
        arg0 = 0
        arg1 = 0
        bc = bytecode.bytecode
        # make annotator happy
        while True:
            op = ord(bc[index])
            numargs = opcodes.opcodes[op].numargs
            if numargs >= 1:
                arg0 = ord(bc[index + 1])
            elif numargs >= 2:
                arg1 = ord(bc[index + 2])

            if op == opcodes.LOAD_NONE:
                frame.push(space.w_None)
            elif op == opcodes.LOAD_CONSTANT:
                frame.push(bytecode.constants[arg0])
            elif op == opcodes.LOAD_VARIABLE:
                self.load_variable(space, frame, index, arg0)
            elif op == opcodes.LOAD_GLOBAL:
                self.load_global(space, frame, index, arg0)
            elif op == opcodes.ADD:
                self.binop_add(space, frame)
            elif op == opcodes.LT:
                self.binop_lt(space, frame)
            elif op == opcodes.STORE:
                frame.store_var(arg0)
            elif op == opcodes.JUMP_IF_FALSE:
                if not space.is_true(frame.pop()):
                    index = arg0
                    continue
            elif op == opcodes.JUMP_ABSOLUTE:
                index = arg0
                continue
            elif op == opcodes.CALL:
                self.call(space, frame, index, arg0)
            elif op == opcodes.RETURN:
                return frame.pop()
            else:
                raise InvalidOpcode(op)

            if numargs == 0:
                index += 1
            elif numargs == 1:
                index += 2
            else:
                index += 3

    def load_variable(self, space, frame, bytecode_index, no):
        w_res = frame.locals_w[no]
        if w_res is None:
            raise UninitializedVariable()
        frame.push(w_res)

    def load_global(self, space, frame, bytecode_index, no):
        frame.push(frame.globals_w[no])

    def call(self, space, frame, bytecode_index, no):
        args = [None] * no
        for i in range(no - 1, -1, -1):
            args[i] = frame.pop()
        w_callable = frame.pop()
        frame.push(space.call(w_callable, args))

    def binop_lt(self, space, frame):
        w_right = frame.pop()
        w_left = frame.pop()
        frame.push(space.binop_lt(w_left, w_right))

    def binop_add(self, space, frame):
        w_right = frame.pop()
        w_left = frame.pop()
        frame.push(space.binop_add(w_left, w_right))
