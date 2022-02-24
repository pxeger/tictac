from typing import Any, Callable

from tictac.interpreter import State


OpFunction = Callable[[State, ...], Any]
Op = tuple[int, OpFunction]

OPS: dict[str, Op]
OPS = {
    "+": (2, lambda state, a, b: a + b),
}

MODIFIERS: dict[str, Callable[[Callable[[], Op]], Op]]
MODIFIERS = {}

assert not (OPS.keys() & MODIFIERS.keys())
