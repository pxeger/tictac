from argparse import ArgumentParser

from tictac.interpreter import interpret


def main():
    parser = ArgumentParser()
    parser.add_argument("-c", action="store_true", dest="string")
    parser.add_argument("program")
    parser.add_argument("args", nargs="...")
    args = parser.parse_args()
    if args.string:
        code = args.program
    else:
        with open(args.program, "r") as f:
            code = f.read()
    inputs = (eval(a) for a in args.args)
    output = interpret(code, *inputs)
    print(output)
