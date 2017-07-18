
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
    Opcode('LOAD_VARIABLE', 1, 1, 'load variable onto stack'),
    Opcode('LOAD_CONSTANT', 1, 1, 'load constant onto stack'),
    Opcode('STORE', 1, -1, 'store top of the stack into variable'),
    Opcode('DISCARD', 1, -1, 'discard top of the stack'),
    Opcode('ADD', 0, -1, 'load two values from the stack and store the result'
                         ' of addition'),
]

def setup():
    for i, opcode in enumerate(opcodes):
        globals()[opcode.name] = i

setup()