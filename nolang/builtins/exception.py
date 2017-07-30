
def exception_init(space, args_w):
    w_exc = args_w[0]
    w_exc.dict_w['message'] = args_w[1]
