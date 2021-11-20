from collections.abc import Iterator
from typing import Callable

from tictac.interpreter import State
from tictac.ops import Op, OPS, MODIFIERS
from tictac.codepage import CODEPAGE_MAP


def _lex(code):
    it = iter(code)
    return [token for char in it for token in _lex_one(it, char)]


DIGRAPH_START = set()


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
            if char == "»":
                break
            else:
                string += char
        yield "literal", string
    elif char == "§":
        while char != "\n":
            char = next(it, "\n")
    elif char.isspace():
        return
    elif char in DIGRAPH_START:
        yield char + next(it, "")
    elif char in CODEPAGE_MAP:
        yield char
    else:
        raise SyntaxError(f"unknown character {char}")


def parse(code: str, arity: int):
    return _parse(iter(_lex(code)), arity)


def _parse(it: Iterator, arity: int):
    # no one-line pattern matching :/
    def is_literal(token):
        match token:
            case "literal", value:
                return value
        return None

    stack = []
    for token in it:
        if token == "¦":
            break
        elif token in {*"𝟚𝟛𝟜"}:
            stack.append(_train([stack.pop() for _ in range(int(token))], 1))
        elif token in {*"²³⁴"}:
            stack.append(_train([stack.pop() for _ in range(int(token))], 2))
        elif token == "(":
            stack.append(_parse(it, 1))
        elif token == "[":
            stack.append(_parse(it, 2))
        elif token in MODIFIERS:
            MODIFIERS[token](stack, arity)
        elif token in OPS:
            stack.append(OPS[token])
        elif value := is_literal(token):
            stack.append((0, lambda state: value))
        else:
            assert False
    return _train(stack, arity)


_TRAINS: dict[int, dict[tuple[int, ...], Callable[[Op, ...], Op]]]
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
