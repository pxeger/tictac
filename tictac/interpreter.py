from collections.abc import Iterable
from numbers import Number
from typing import Any

from libgolf.list import List
from libgolf.string import Character, String
from sympy import sympify


class State:
    def __init__(self, parent_state, args, recurse=None):
        self.parent_state = parent_state
        self.args = args
        self.recurse = recurse or parent_state.recurse


def interpret(code: str, *args):
    # have to import inside function to prevent circular import
    # :/ python why are you like this
    from tictac.parser import parse

    function = parse(code, len(args))
    state = State(None, args, function)
    if args == ():
        args = (0,)
    return function(state, *args)


def convert(obj):
    if isinstance(obj, String):
        return String(obj)
    elif isinstance(obj, Iterable):
        return List(convert(i) for i in obj)
    elif isinstance(obj, bool):
        return convert(int(obj))
    elif isinstance(obj, Number):
        return sympify(obj)
    else:
        return obj


def parse_input(s: str) -> Any:
    return convert(eval(s, {"c": Character}))
