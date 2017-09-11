
from support import BaseTest
from StringIO import StringIO
from nolang.serializer import Serializer, Unserializer
from nolang.importer import Importer


class TestSerializer(BaseTest):
    def test_serialize_module(self):
        w_mod = self.compile_module("""
            class A {
                def __init__(self, x=3) {
                    self.x = x
                }

                def method(self, x, y='a') {
                    return str(x) + y + str(self.x)
                }
            }
            """)
        space = self.space
        w_A = space.getattr(w_mod, 'A')
        w_a = space.call(w_A, [], None)
        w_r = space.call(space.getattr(w_a, 'method'), [space.newint(1)], None)
        assert space.utf8_w(w_r) == '1a3'
        out = StringIO()
        ser = Serializer(out)
        w_mod.serialize_module(ser)
        imp = Importer(space)
        w_mod2 = Unserializer(StringIO(out.getvalue()), self.space,
                              imp).unserialize()
        w_A = space.getattr(w_mod2, 'A')
        w_a = space.call(w_A, [], None)
        w_r = space.call(space.getattr(w_a, 'method'), [space.newint(1)], None)
        assert space.utf8_w(w_r) == '1a3'
