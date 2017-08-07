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

    def __repr__(self):
        return '<AppError %r>' % (self.w_exception,)
