import sys

from libgolf.list import List
import sympy.core.numbers


def convert(value):
    """convert a generic Python object to tictac format"""
    if isinstance(value, (str, List, sympy.Basic)):
        # already supported
        return value
    elif isinstance(value, (tuple, list, set)):
        return List(convert(i) for i in value)
    elif isinstance(value, (int, float, complex)):
        return sympy.sympify(value)
    else:
        # TODO(pxeger): bool, dict
        raise TypeError(f"unsupported value {value!r}")


def fixed_point(func, start):
    prev = start
    while True:
        new = func(prev)
        if new == prev:
            return new
        else:
            prev = new


def print_stderr(*args, file=sys.stderr, **kwargs):
    print(*args, **kwargs)
