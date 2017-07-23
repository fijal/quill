
def target(driver, args):
    driver.exe_name = 'nolang-c'
    config = driver.config

    from rpython.config.config import to_optparse, SUPPRESS_USAGE
    parser = to_optparse(config, parserkwargs={'usage': SUPPRESS_USAGE })
    parser.parse_args(args)

    from nolang.main import entry_point
    return entry_point, None
