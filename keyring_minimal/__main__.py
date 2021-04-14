from . import test, get, set

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()

    subp = p.add_subparsers(title='mode')

    testp = subp.add_parser('test')
    testp.set_defaults(func=test)

    getp = subp.add_parser('get')
    getp.set_defaults(func=get)
    getp.add_argument('label')
    getp.add_argument('--username')

    setp = subp.add_parser('set')
    setp.set_defaults(func=set)
    setp.add_argument('label')
    setp.add_argument('password')
    setp.add_argument('--username')
    setp.add_argument('--notes')
    setp.add_argument('--url')

    args = p.parse_args()

    args.func(args)
