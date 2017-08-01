from nolang.objects.root import W_Root


class Frame(W_Root):
    def __init__(self, bytecode, f_back):
        self.bytecode = bytecode
        self.f_back = f_back
        if bytecode.module is not None:  # for tests
            self.globals_w = bytecode.module.functions
        self.locals_w = [None] * len(bytecode.varnames)
        self.stack_w = [None] * bytecode.stack_depth
        self.resume_stack = [0] * bytecode.resume_stack_depth
        self.resume_stack_depth = 0
        self.pos = 0

    def populate_args(self, args_w):
        for i in range(len(args_w)):
            self.locals_w[i] = args_w[i]

    def push(self, w_val):
        self.stack_w[self.pos] = w_val
        self.pos += 1

    def pop(self):
        new_pos = self.pos - 1
        w_res = self.stack_w[new_pos]
        assert new_pos >= 0
        self.pos = new_pos
        return w_res

    def peek(self):
        return self.stack_w[self.pos - 1]

    def store_var(self, index):
        self.locals_w[index] = self.pop()
