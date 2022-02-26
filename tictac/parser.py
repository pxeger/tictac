from collections.abc import Iterator
from typing import Callable

from tictac.codepage import CODEPAGE_MAP
from tictac.interpreter import State
from tictac.ops import OpFunction, OPS, MODIFIERS
from tictac.string import process_string


def _lex(code):
    it = iter(code)
    return [token for char in it for token in _lex_one(it, char)]


DIGRAPH_START = {*")]}"}


def _lex_one(it, char):
    if char == "0":
        yield "literal", 0
    if char in {*"123456789"}:
        number = ""
        while char in {*"0123456789"}:
            number += char
            char = next(it, "")
        yield "literal", int(number)
        if char:
            yield from _lex_one(it, char)
    elif char == "«":
        string = ""
        while True:
            char = next(it, "»")
            if char == "∎":
                # escape character
                char += next(it, "")
            if char == "»":
                break
            else:
                string += char
        yield "string", string
    elif char == "§":
        while char != "\n":
            char = next(it, "\n")
    elif char.isspace():
        return
    elif char in DIGRAPH_START:
        char2 = next(it, "")
        if char == ")" and char2 in {*"0123456789"}:
            # )123 is equivalent to 123, but is a separate token
            yield from _lex_one(it, char2)
        else:
            # digraph
            yield char + char2
    elif char in CODEPAGE_MAP:
        yield char
    else:
        raise SyntaxError(f"unknown character {char}")


def parse(code: str, arity: int):
    arity2, function = _parse(iter(_lex(code)), arity)
    assert arity == arity2
    return function


def _parse(it: Iterator, arity: int, *, length: int = -1):
    links = []
    while (link := _parse_one(it)) and length:
        length -= 1
        links.append(link)
    return arity, _train(links, arity)


MONAD_GROUPERS = {"𝟚": 2, "𝟛": 3, "𝟜": 4}
DYAD_GROUPERS = {"²": 2, "³": 3, "⁴": 4}


def _parse_one(it: Iterator):
    match next(it, None):
        case None | "¦":
            return None
        case "𝟚" | "𝟛" | "𝟜" as grouper:
            return _parse(it, 1, length=MONAD_GROUPERS[grouper])
        case "²" | "³" | "⁴" as grouper:
            return _parse(it, 2, length=DYAD_GROUPERS[grouper])
        case "(":
            return _parse(it, 0)
        case "[":
            return _parse(it, 1)
        case "{":
            return _parse(it, 2)
        case mod if mod in MODIFIERS:
            return MODIFIERS[mod](lambda: _parse_one(it))
        case op if op in OPS:
            return OPS[op]
        case "literal", value:
            return (0, lambda state: value)
        case "string", string:
            return process_string(string)
        case unknown:
            assert False, f"unexpected token {unknown}"


_TRAINS: dict[int, dict[tuple[int, ...], Callable[[OpFunction, ...], OpFunction]]]
_TRAINS = {
    1: {
        (2, 1): lambda c, f, g: lambda state, a: f(state, c(state, a), g(state, a)),
        (2, 0): lambda c, f, g: lambda state, a: f(state, c(state, a), g(state)),
        (0, 2): lambda c, f, g: lambda state, a: g(state, f(state), c(state, a)),
        (0,): lambda c, f: lambda state, a: f(state),
        (1,): lambda c, f: lambda state, a: f(state, c(state, a)),
        (2,): lambda c, f: lambda state, a: f(state, a, c(state, a)),
    },
    2: {
        (2, 2, 0): lambda c, f, g, h: lambda state, a, b: g(state, f(state, c(state, a, b), b), h(state)),
        (2, 2): lambda c, f, g: lambda state, a, b: f(state, c(state, a, b), g(state, a, b)),
        (2, 0): lambda c, f, g: lambda state, a, b: f(state, c(state, a, b), g(state)),
        (0, 2): lambda c, f, g: lambda state, a, b: g(f(state), c(state, a, b)),
        (0,): lambda c, f: lambda state, a, b: f(state),
        (1,): lambda c, f: lambda state, a, b: f(state, c(state, a, b)),
        (2,): lambda c, f: lambda state, a, b: f(state, a, c(state, a, b)),
    },
}

_TRAIN_START = {
    1: lambda state, a: a,
    2: lambda state, a, b: a,
}


def _train(stack, arity):
    if arity == 0:
        arity = 1
    c = _TRAIN_START[arity]
    arities, functions = zip(*stack)
    while arities:
        for pattern, combinator in _TRAINS[arity].items():
            magnitude = len(pattern)
            if arities[:magnitude] == pattern:
                break
        c = combinator(c, *functions[:magnitude])
        arities = arities[magnitude:]
        functions = functions[magnitude:]
    return lambda parent_state, *args: c(State(parent_state, args), *args)
