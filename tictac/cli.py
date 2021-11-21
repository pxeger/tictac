from argparse import ArgumentParser

from tictac.parser import parse
from tictac.interpreter import Interpreter


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
    link = parse(code)
    inputs = (eval(arg) for arg in args.args)
    outputs = Interpreter(link).run(*inputs)
    for output in outputs:
        print(output)
