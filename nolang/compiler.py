""" Main module compiler
"""

from nolang.module import W_Module
from nolang.objects.userobject import W_UserObject
from nolang.builtins.spec import wrap_function

from rpython.rlib.objectmodel import specialize


def _gather_names(ast, builtins):
    name_mapping = {}
    if builtins is not None:
        for item in builtins:
            name_mapping[item.name] = len(name_mapping)
    for item in ast.get_element_list():
        item.add_name(name_mapping)
    return name_mapping


def compile_module(space, name, source, ast, importer):
    name_mapping = _gather_names(ast, space.builtins_w)
    if space.builtins_w is not None:
        globals_w = space.builtins_w[:]
    else:
        globals_w = []
    w_mod = W_Module(name, name_mapping, globals_w)
    for item in ast.get_element_list():
        item.add_global_symbols(space, globals_w, source, w_mod)
    importer.register_module(w_mod)
    importer.add_missing_imports(space, ast, w_mod, globals_w)
    return w_mod


def new_user_object(space, args_w):
    return W_UserObject(args_w[0])


@specialize.memo()
def get_alloc(space):
    return wrap_function(space, new_user_object)


def compile_class(space, source, ast, w_mod, parent=None):
    if parent is not None:
        w_parent = w_mod.functions[w_mod.name2index[parent]]
    else:
        w_parent = None
    if w_parent is not None:
        alloc = w_parent.allocate
        default_alloc = w_parent.default_alloc
    else:
        alloc = get_alloc(space)
        default_alloc = True
    class_elements_w = []
    for item in ast.get_element_list():
        item.add_global_symbols(space, class_elements_w, source, w_mod)
    return alloc, class_elements_w, w_parent, default_alloc
