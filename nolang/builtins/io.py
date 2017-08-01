from nolang.builtins.spec import parameters


@parameters(name='print')
def magic_print(space, args_w):
    print space.str(args_w[0])
