
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
            elif op == opcodes.STORE:
                frame.store_var(arg0)
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