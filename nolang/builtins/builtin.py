from nolang.builtins.spec import unwrap_spec


@unwrap_spec()
def len(space, w_obj):
    return space.newint(space.len(w_obj))
