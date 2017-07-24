
""" Common errors and error handling
"""

class AppError(Exception):
    def __init__(self, w_exception):
        self.w_exception = w_exception

    def __repr__(self):
        return '<AppError %r>' % (self.w_exception,)

class ArgumentMismatchError(Exception):
    pass
