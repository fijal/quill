
class SpecReadingError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return '<SpecReadingError %s>' % self.msg

def read_spec(fname):
    try:
        f = open(fname, "r")
        return _read_spec(fname, f)
        f.close()
    except (IOError, OSError):
        raise SpecReadingError("Error reading %s" % fname)

def _read_spec(fname, f):
    lines = f.read().splitlines()
    lines = [line.strip() for line in lines if line.strip()]
    current_section = None
    res = {}
    for i, line in enumerate(lines):
        if line.startswith("["):
            if line[-1] != ']':
                raise SpecReadingError("File %s, line %d is not a proper "
                    "section spec" % (fname, i + 1))
            current_section = {}
            end = len(line) - 1
            assert end >= 0
            res[line[1:end]] = current_section
        else:
            if current_section is None:
                raise SpecReadingError("File %s not starting with a section" %
                    (fname,))
            if "=" not in line or line.count("=") != 1:
                raise SpecReadingError("File %s, line %d malformed" % (
                    fname, i + 1))
            left, right = line.split("=")
            left = left.strip()
            right = right.strip()
            if left in current_section:
                raise SpecReadingError("File %s, line %d, duplicate entry for %s" %
                    (fname, i + 1, left))
            if not right or not left:
                raise SpecReadingError("File %s, line %d, malformed line" %
                    (fname, i + 1))
            current_section[left] = right
    return res
