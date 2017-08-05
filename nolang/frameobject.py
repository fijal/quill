from nolang.objects.root import W_Root


class Frame(W_Root):
    def __init__(self, bytecode):
        self.bytecode = bytecode
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


def find_line(bytecode, target_pc):
    src = bytecode.source
    pos = 0
    lineno = 0
    target_position = bytecode.lnotab[target_pc]
    prev_pos = 0
    while pos < target_position:
        prev_pos = pos
        pos = src.find("\n", pos + 1)
        lineno += 1
        if pos < 0:
            return src[prev_pos + 1:], lineno
    return src[prev_pos + 1:pos], lineno


def format_traceback(space, apperr):
    lines = []
    w_exception = apperr.w_exception
    tb_list = []
    tb = apperr.traceback
    while tb:
        tb_list.append(tb)
        tb = tb.next

    for i in range(len(tb_list) - 1, -1, -1):
        tb = tb_list[i]
        line, lineno = find_line(tb.bytecode, tb.position)
        lines.append("file \"%s\", line %d" % (tb.bytecode.filename, lineno))
        lines.append("  " + line.strip())
    lines.append("%s: %s" % (space.type(w_exception).name, w_exception.message))
    lines.append("")
    return "\n".join(lines)
