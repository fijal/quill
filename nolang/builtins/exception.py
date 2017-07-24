
def exception_init(space, args_w):
    args_w[0].dict_w['message'] = args_w[1]
