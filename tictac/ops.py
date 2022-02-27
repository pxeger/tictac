from typing import Any, Callable

from libgolf.vectorise import vectorise

from tictac.interpreter import State


OpFunction = Callable[[State, ...], Any]
Op = tuple[int, OpFunction]

OPS: dict[str, Op]
OPS = {
    # basic arithmetic
    "+": (2, vectorise(lambda state, a, b: a + b)),
    "-": (2, vectorise(lambda state, a, b: a - b)),
    "*": (2, vectorise(lambda state, a, b: a * b)),
    "÷": (2, vectorise(lambda state, a, b: a / b)),
    ":": (2, vectorise(lambda state, a, b: a // b)),
    "%": (2, vectorise(lambda state, a, b: a % b)),
    "^": (2, vectorise(lambda state, a, b: a ** b)),
    # logic
    "&": (2, lambda state, a, b: a and b),
    "|": (2, lambda state, a, b: a or b),
    "<": (2, lambda state, a, b: a < b),
    ">": (2, lambda state, a, b: a > b),
    "≈": (2, vectorise(lambda state, a, b: a == b)),
    "=": (2, lambda state, a, b: a == b),
    "¬": (1, lambda state, a: not a),
}

MODIFIERS: dict[str, Callable[[Callable[[], Op]], Op]]
MODIFIERS = {}

assert not (OPS.keys() & MODIFIERS.keys())
