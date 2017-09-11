""" Common errors and error handling
"""


class TracebackElem(object):
    def __init__(self, frame, position, bytecode, next):
        self.frame = frame
        self.position = position
        self.bytecode = bytecode
        self.next = next


class AppError(Exception):
    def __init__(self, w_exception):
        self.w_exception = w_exception
        self.traceback = None

    def record_position(self, frame, bytecode, index):
        self.traceback = TracebackElem(frame, index, bytecode, self.traceback)

    def match(self, space, w_expected):
        return space.issubclass(space.type(self.w_exception), w_expected)

    def __repr__(self):
        return '<AppError %r>' % (self.w_exception,)
    __str__ = __repr__


class InterpreterError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def repr(self):
        return "%s: %s" % (self.__class__.__name__, self.msg)
