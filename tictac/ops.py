from typing import Any, Callable

from tictac.interpreter import State


Op = Callable[[State, ...], Any]

OPS: dict[str, Op]
OPS = {
    "+": (2, lambda state, a, b: a + b),
}

MODIFIERS: dict[str, Callable[[list[tuple[int, Op]], int], None]]
MODIFIERS = {}

assert not (OPS.keys() & MODIFIERS.keys())
