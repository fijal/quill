""" Opcode declaration
"""


class Opcode(object):
    def __init__(self, name, numargs, stack_effect, description):
        self.name = name
        self.numargs = numargs
        self.stack_effect = stack_effect
        self.description = description

    def __repr__(self):
        return '<%s>' % self.name


opcodes = [
    Opcode('INVALID', 0, 0, 'invalid opcode'),
    Opcode('LOAD_NONE', 0, 1, 'load None onto stack'),
    Opcode('LOAD_VARIABLE', 1, 1, 'load variable onto stack'),
    Opcode('LOAD_GLOBAL', 1, 1, 'load global variable'),
    Opcode('LOAD_CONSTANT', 1, 1, 'load constant onto stack'),
    Opcode('LOAD_TRUE', 0, 1, 'load true onto stack'),
    Opcode('LOAD_FALSE', 0, 1, 'load false onto stack'),
    Opcode('STORE', 1, -1, 'store top of the stack into variable'),
    Opcode('DISCARD', 0, -1, 'discard top of the stack'),
    Opcode('GETATTR', 1, 0, 'get attribut from the object on top of the stack '
                            'with string constant as an argument'),
    Opcode('SETATTR', 1, -2, 'set attribute on an object'),
    # exception handling
    Opcode('PUSH_RESUME_STACK', 1, 0, 'add a new resume point to the stack'),
    Opcode('POP_RESUME_STACK', 0, 0, 'pop one from resume stack'),
    Opcode('COMPARE_EXCEPTION', 2, 0, 'compare current exception with an arg'),
    Opcode('RAISE', 0, -1, 'raise the top of the stack'),
    Opcode('RERAISE', 0, 0, 'reraise if exception is set'),
    Opcode('PUSH_CURRENT_EXC', 0, 1, 'push the current exception on the stack'),
    Opcode('CLEAR_CURRENT_EXC', 0, 0, 'set current exception to nothing'),
    # binary ops
    Opcode('ADD', 0, -1, 'load two values from the stack and store the result'
                         ' of addition'),
    Opcode('SUB', 0, -1, 'load two values from the stack and store the result'
                         ' of subtraction'),
    Opcode('MUL', 0, -1, 'load two values from the stack and store the result'
                         ' of multiplication'),
    Opcode('TRUEDIV', 0, -1, 'load two values from the stack and store the result'
                             ' of integer division'),
    Opcode('LT', 0, -1, 'load two value from the stack and store the result'
                        ' of lower than comparison'),
    Opcode('EQ', 0, -1, 'load two value from the stack and store the result'
                        ' of comparison'),
    # jumps
    Opcode('JUMP_IF_FALSE', 1, -1, 'pop value from the stack and jump if false'
                                   ' to a given position'),
    Opcode('JUMP_IF_TRUE_NOPOP', 1, 0, 'peek value from the stack and jump if '
                                       'true to a given position'),
    Opcode('JUMP_IF_FALSE_NOPOP', 1, 0, 'peek value from the stack and jump if '
                                        'false to a given position'),
    Opcode('JUMP_ABSOLUTE', 1, 0, 'jump to an absolute position'),
    Opcode('CALL', 1, 255, 'take N arguments from the stack, pack them into'
                           'args and call the next element'),
    Opcode('RETURN', 0, -1, 'return the top of stack')
]


def setup():
    for i, opcode in enumerate(opcodes):
        globals()[opcode.name] = i


setup()
