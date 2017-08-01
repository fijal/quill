
""" Various specifications for builtins
"""

import types
import py
from nolang.function import W_BuiltinFunction, W_Property
from nolang.objects.usertype import W_UserType

def unwrap_spec(**spec):
    def wrapper(func):
        func.unwrap_spec = spec
        return func
    return wrapper

def parameters(**args):
    def wrapper(func):
        func.unwrap_parameters = args
        return func
    return wrapper

class TypeSpec(object):
    def __init__(self, name, constructor, methods, properties):
        self.constructor = constructor
        self.name = name
        self.methods = methods
        self.properties = properties

def wrap_function(f):
    name = f.__name__
    argnames = f.__code__.co_varnames[:f.__code__.co_argcount]
    lines = ['def %s(space, args_w):' % name]
    j = 0
    numargs = 0
    for i, argname in enumerate(argnames):
        if argname == 'space':
            argval = 'space'
        elif argname == 'args_w':
            argval = 'args_w'
            numargs = -1
            assert i == len(argnames) - 1
        elif argname.startswith('w_'):
            argval = 'args_w[%d]' % j
            j += 1
            numargs += 1
        else:
            spec = f.unwrap_spec.get(argname, None)
            numargs += 1
            if spec is None:
                raise Exception("No spec found for %s while wrapping %s" %
                                (argname, name))
            if spec == 'str':
                argval = 'space.str(args_w[%d])' % j
                j += 1
            else:
                assert False
        lines.append('    arg%d = %s' % (i, argval))
    args = ", ".join(['arg%d' % i for i in range(len(argnames))])
    lines.append('    return orig_%s(%s)' % (name, args))
    src = py.code.Source("\n".join(lines))
    d = {'orig_' + name: f}
    exec src.compile() in d
    exported_name = name
    if getattr(f, 'unwrap_parameters', None):
        exported_name = f.unwrap_parameters.get('name', exported_name)
    return W_BuiltinFunction(exported_name, d[name], numargs)

def wrap_type(tp):
    spec = tp.spec
    allocate = wrap_function(spec.constructor)
    properties = []
    for name, (get_prop, set_prop) in spec.properties.iteritems():
        if set_prop is not None:
            set_prop = set_prop.im_func
        properties.append(W_Property(name, get_prop.im_func, set_prop))
    return W_UserType(allocate, spec.name, properties, None, default_alloc=False)

def wrap_builtin(builtin):
    if isinstance(builtin, types.FunctionType):
        return wrap_function(builtin)
    else:
        return wrap_type(builtin)
