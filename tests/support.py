
import re

def reformat_code(body):
    bodylines = body.split("\n")
    cut = 0
    while bodylines[cut].strip(" ") == '':
        cut += 1
    bodylines = bodylines[cut:]
    m = re.match(" +", bodylines[0])
    lgt = len(m.group(0))
    newlines = []
    for i, line in enumerate(bodylines):
        if line[:lgt] != " " * lgt:
            raise Exception("bad formatting, line: %d\n%s" % (i, line))
        newlines.append(" " * 4 + line[lgt:])
    return "function foo () {\n" + "\n".join(newlines) + "}"
