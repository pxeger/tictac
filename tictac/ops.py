import math
from functools import reduce

from tictac.utils import *


constants = {
    "h": "Hello, World!",
}


simple_ops = {
    # op: arity, function
    # change arity to ~arity to enable multi-output mode
    ",": (2, lambda a, b: [a, b]),
    "+": (2, lambda a, b: a + b),
    "-": (2, lambda a, b: a - b),
    "*": (2, lambda a, b: a * b),
    "/": (2, lambda a, b: a / b),
    "%": (2, lambda a, b: a % b),
    "^": (2, lambda a, b: a ** b),
    "¬": (1, lambda a: not a),
    "&": (2, lambda a, b: a and b),
    "|": (2, lambda a, b: a or b),
    "<": (2, lambda a, b: a < b),
    ">": (2, lambda a, b: a > b),
    "=": (2, lambda a, b: a == b),
    "~": (~2, lambda a, b: (b, a)),  # swap
    "a": (1, lambda a: a[0]),  # first
    "h": (1, lambda a: a[:-1]),  # head
    "i": (2, lambda a, b: a[b]),
    "r": (2, List.wrap(range)),
    "t": (1, lambda a: a[1:]),  # tail
    "w": (1, lambda a: a[-1]),  # last
    "F": (1, lambda a: math.gamma(a + 1)),  # factorial
    "L": (1, len),
    "O": (1, lambda a: ord(a) if isinstance(a, str) else chr(a)),
    "P": (1, lambda a: print(a) or a),
    "Q": (1, unique),
    "R": (1, List.wrap(reversed)),
    "S": (1, sum),
    "Z": (2, List.wrap(zip)),
    **{"𝕜" + k: (0, lambda: v) for k, v in constants.items()},
}


ops_taking_links = {
    # if
    "𝕚": (1, lambda f: (1, lambda i: i and f())),
    # sort
    "𝕤": (1, lambda f: (1, lambda i: List(sorted(i, key=f)))),
    # filter
    "𝕗": (1, lambda f: (1, lambda i: List(filter(f, i)))),
    # reduce
    "𝕣": (1, lambda f: (1, lambda i: List(reduce(f, i)))),
    # map
    "𝕞": (1, lambda f: (1, lambda i: List(map(f, i)))),
    # zipwith
    "𝕫": (1, lambda f: (2, lambda i, j: List(map(f, i, j)))),
}

# check disjoint
assert len(set(simple_ops) & set(ops_taking_links)) == 0
