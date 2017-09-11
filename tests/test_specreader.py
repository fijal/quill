
import py

from StringIO import StringIO
from nolang.specreader import _read_spec, SpecReadingError

class TestReadSpec(object):
    def test_basic(self):
        res = _read_spec("fname", StringIO("""
            [section]
            a = 1
            b = 2
            """))
        assert res == {'section': {'a': '1', 'b': '2'}}

    def test_raises(self):
        input1 = """
        [sec
        a = 3
        """
        input2 = """
        [sec]
        a =
        """
        input3 = """
        a = 4
        """
        input4 = """
        [section]
        a = 1
        a=2
        """
        for inp in [input1, input2, input3, input4]:
            py.test.raises(SpecReadingError, _read_spec, "fname",
                StringIO(inp))
