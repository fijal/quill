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
    def __init__(self, name, constructor, methods=None, properties=None,
                 parent_name=None, set_cls_w_type=False):
        self.constructor = constructor
        self.name = name
        if methods is None:
            methods = {}
        self.methods = methods
        if properties is None:
            properties = {}
        self.properties = properties
        self.parent_name = parent_name
        self.set_cls_w_type = set_cls_w_type


def wrap_function(space, f, name=None, exp_name=None):
    if name is None:
        name = f.__name__
    argnames = f.__code__.co_varnames[:f.__code__.co_argcount]
    lines = ['def %s(space, args_w):' % name]
    j = 0
    numargs = 0
    argdefaults = [None] * len(argnames)
    defs = []
    if f.__defaults__ is not None:
        defs = f.__defaults__
        firstdefault = len(argnames) - len(defs)
        for i in range(len(defs)):
            if defs[i] is None:
                argdefaults[i + firstdefault] = space.w_None
            elif isinstance(defs[i], int):
                argdefaults[i + firstdefault] = space.newint(defs[i])
            else:
                raise NotImplementedError(
                    "Default handling not supported for %s" % (defs[i],))

    d = {'orig_' + name: f, 'argdefaults': argdefaults}
    for i, argname in enumerate(argnames):
        extralines = []
        if argname == 'space':
            argval = 'space'
        elif argname == 'args_w':
            argval = 'args_w'
            numargs = -1
            assert i == len(argnames) - 1
        elif argname == 'self':
            if not isinstance(f, types.MethodType):
                raise Exception("self argument, but argument is not a method")
            argval = 'args_w[0]'
            j += 1
            numargs += 1
            msg = "Expected %s object, got %%s" % exp_name
            extralines = [
                '    if not isinstance(arg%d, self_tp):' % i,
                '        raise space.apperr(space.w_typeerror, "%s" %% '
                '(space.type(arg%d).name,))' % (msg, i),
            ]
            d['self_tp'] = f.im_class
        elif argname.startswith('w_'):
            argval = 'args_w[%d]' % j
            j += 1
            numargs += 1
        else:
            if hasattr(f, 'unwrap_spec'):
                spec = f.unwrap_spec.get(argname, None)
            else:
                spec = None
            numargs += 1
            if spec is None:
                raise Exception("No spec found for %s while wrapping %s" %
                                (argname, name))
            if spec == 'str':
                argval = 'space.utf8_w(args_w[%d])' % j
                j += 1
            elif spec == 'int':
                argval = 'space.int_w(args_w[%d])' % j
                j += 1
            elif spec == 'list':
                argval = 'space.listview(args_w[%d])' % j
                j += 1
            elif spec == 'dict':
                argval = 'space.dictview(args_w[%d])' % j
                j += 1
            else:
                assert False
        if argdefaults[i] is not None:
            lines.append('    if len(args_w) <= %d:' % (numargs - 1))
            lines.append('        arg%d = argdefaults[%d]' % (i, i))
            lines.append('    else:')
            lines.append('        arg%d = %s' % (i, argval))
        else:
            lines.append('    arg%d = %s' % (i, argval))
        lines += extralines
    args = ", ".join(['arg%d' % i for i in range(len(argnames))])
    lines.append('    return orig_%s(%s)' % (name, args))
    src = py.code.Source("\n".join(lines))
    exec src.compile() in d
    exported_name = name
    if getattr(f, 'unwrap_parameters', None):
        exported_name = f.unwrap_parameters.get('name', exported_name)
    return W_BuiltinFunction(exported_name, d[name],
        min_args=numargs - len(defs),
        max_args=numargs)


def wrap_type(space, tp):
    spec = tp.spec
    if spec.constructor is None:
        allocate = None
    else:
        allocate = wrap_function(space, spec.constructor)
    properties = []
    for name, (get_prop, set_prop) in spec.properties.iteritems():
        if set_prop is not None:
            set_prop = set_prop.im_func
        properties.append(W_Property(name, get_prop.im_func, set_prop))
    for name, meth in spec.methods.iteritems():
        properties.append(wrap_function(space, meth, name=name, exp_name=spec.name))
    if spec.parent_name is None:
        parent = None
    else:
        parent = space.builtin_dict[spec.parent_name]
    w_tp = W_UserType(allocate, spec.name, properties, parent, default_alloc=False)
    if spec.set_cls_w_type:
        tp.cls_w_type = w_tp
    return w_tp


def wrap_builtin(space, builtin):
    if isinstance(builtin, types.FunctionType):
        return wrap_function(space, builtin)
    else:
        return wrap_type(space, builtin)
