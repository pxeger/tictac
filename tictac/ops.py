import math
from functools import reduce
from itertools import accumulate

from libgolf.list import List

from tictac.utils import fixed_point


constants = {
    "h": "Hello, World!",
}


def simple_op(arity, func, multi_output=False):
    def inner(interpreter):
        args = []
        for _ in range(arity):
            args.append((yield interpreter.demand_pop))
        res = func(*args)
        if multi_output:
            for i in res:
                interpreter.push(i)
        else:
            interpreter.push(res)
    return inner


ops = {
    ",": simple_op(2, lambda a, b: [a, b]),
    "+": simple_op(2, lambda a, b: a + b),
    "-": simple_op(2, lambda a, b: a - b),
    "*": simple_op(2, lambda a, b: a * b),
    "/": simple_op(2, lambda a, b: a / b),
    "%": simple_op(2, lambda a, b: a % b),
    "^": simple_op(2, lambda a, b: a ** b),
    "¬": simple_op(1, lambda a: not a),
    "&": simple_op(2, lambda a, b: a and b),
    "|": simple_op(2, lambda a, b: a or b),
    "<": simple_op(2, lambda a, b: a < b),
    ">": simple_op(2, lambda a, b: a > b),
    "=": simple_op(2, lambda a, b: a == b),
    "~": simple_op(2, lambda a, b: (b, a), True),  # swap
    "a": simple_op(1, lambda a: a[0]),  # first
    "h": simple_op(1, lambda a: a[:-1]),  # head
    "i": simple_op(2, lambda a, b: a[b]),
    "r": simple_op(2, List.wrap(range)),
    "t": simple_op(1, lambda a: a[1:]),  # tail
    "w": simple_op(1, lambda a: a[-1]),  # last
    "F": simple_op(1, lambda a: math.gamma(a + 1)),  # factorial
    "L": simple_op(1, len),
    "O": simple_op(1, lambda a: ord(a) if isinstance(a, str) else chr(a)),
    "P": simple_op(1, lambda a: print(a) or a),
    "Q": simple_op(1, lambda l: l.unique()),
    "R": simple_op(1, List.wrap(reversed)),
    "S": simple_op(1, sum),
    "Z": simple_op(2, List.wrap(zip)),
    **{"𝕜" + key: lambda i: i.push(value) for key, value in constants.items()},
}


ops_taking_links = {
    # scan / cumulative reduce
    "𝕔": (1, lambda f: simple_op(1, lambda i: List(accumulate(i, f)))),
    # fixed-point
    "𝕡": (1, lambda f: simple_op(1, lambda i: fixed_point(f, i))),
    # sort
    "𝕤": (1, lambda f: simple_op(1, lambda i: List(sorted(i, key=f)))),
    # reduce
    "𝕣": (1, lambda f: simple_op(1, lambda i: reduce(f, i))),
    # map
    "𝕞": (1, lambda f: simple_op(1, lambda i: List(map(f, i)))),
    # filter (where)
    "𝕨": (1, lambda f: simple_op(1, lambda i: List(filter(f, i)))),
    # zipwith
    "𝕫": (1, lambda f: simple_op(2, lambda i, j: List(map(f, i, j)))),
}

# check disjoint
assert len(set(ops) & set(ops_taking_links)) == 0
