
import struct
from rpython.rlib.rstruct import runpack

from nolang.module import W_Module
from nolang.function import W_Function
from nolang.bytecode import Bytecode
from nolang.objects.usertype import W_UserType
from nolang.compiler import get_alloc


class UnserializingError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return '<UnserializingError %s>' % self.msg


class Serializer(object):
    def __init__(self, o):
        self.o = o

    def write(self, s):
        self.o.write(s)

    def write_int(self, i):
        self.o.write(struct.pack("l", i))

    def write_str(self, s):
        self.write_int(len(s))
        self.o.write(s)

    def write_list_str(self, l):
        self.write_int(len(l))
        for item in l:
            self.write_str(item)

    def write_list_obj(self, l_w):
        self.write_int(len(l_w))
        for w_item in l_w:
            w_item.serialize(self)

    def write_list_int(self, l):
        self.write_int(len(l))
        for item in l:
            self.write_int(item)



class Unserializer(object):
    def __init__(self, o, space, importer):
        self.o = o
        self.space = space
        self.importer = importer

    def read(self, no):
        s = self.o.read(no)
        if len(s) != no:
            raise UnserializingError("unexpected end of file")
        return s

    def read_list_str(self):
        lgt = self.read_int()
        l = []
        for i in range(lgt):
            l.append(self.read_str())
        return l

    def read_list_int(self):
        lgt = self.read_int()
        l = []
        for i in range(lgt):
            l.append(self.read_int())
        return l

    def read_int(self):
        return runpack.runpack("l", self.read(8))

    def read_str(self):
        lgt = self.read_int()
        return self.read(lgt)

    def read_list_obj(self):
        item_no = self.read_int()
        items = []
        for i in range(item_no):
            item_tp = self.read(2)
            if item_tp == "bf" or item_tp == "bt":
                name = self.read_str()
                w_item = self.space.builtin_dict[name]
            elif item_tp == "bm":
                name = self.read_str()
                w_item = self.importer.get_module(self.space, name.split("."))
            elif item_tp == "ut":
                name = self.read_str()
                elems_w = self.read_list_obj()
                w_item = W_UserType(get_alloc(self.space), name, elems_w,
                    None, self.w_mod)
            elif item_tp == "uf":
                name = self.read_str()
                filename = self.read_str()
                varnames = self.read_list_int()
                arglist = self.read_list_str()
                defaults = self.read_list_int()
                consts = self.read_list_obj()
                bc = self.read_str()
                bytecode = Bytecode(filename, '', varnames, self.w_mod, [],
                    bc, arglist, [None] * len(arglist), defaults, [])
                bytecode.constants = consts
                w_item = W_Function(name, bytecode, self.w_mod)
            elif item_tp == "cs":
                w_item = self.space.newtext(self.read_str())
            elif item_tp == "ci":
                w_item = self.space.newint(self.read_int())
            else:
                raise UnserializingError("Unknown marker %s" % item_tp)
            items.append(w_item)
        return items

    def map_items(self, items):
        map = {}
        for i, item in enumerate(items):
            map[item.name] = i
        return map

    def unserialize(self):
        if self.read_int() != 0xBABACACA:
            raise UnserializingError("wrong magic no")
        version = self.read_int()
        if version != 13:
            raise UnserializingError("wrong version %d" % version)
        name = self.read_str()
        exp_no = self.read_int()
        export_names = []
        self.w_mod = W_Module(name, name, {}, [])
        for i in range(exp_no):
            export_names.append(self.read_str())
        items = self.read_list_obj()
        mapping = self.map_items(items)
        self.w_mod.functions = items
        self.w_mod.name2index = mapping
        return self.w_mod
