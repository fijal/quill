from nolang.builtins.spec import unwrap_spec


@unwrap_spec(size='int')
def buffer(space, size):
    return space.newbuf(['\x00'] * size)


@unwrap_spec(utf8='utf8')
def buffer_from_utf8(space, utf8):
    return space.newbuf([c for c in utf8])
