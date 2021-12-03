from functools import wraps
from typing import final
import sys

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


@final
class List:
    __match_args__ = ()

    def __init__(self, i):
        self.cache = []
        self.it = iter(i)

    def __iter__(self):
        i = 0
        while True:
            x = self.cache[i:]
            i += len(x)
            yield from x
            try:
                self.cache.append(next(self.it))
            except StopIteration as e:
                return e.value

    def __reversed__(self):
        exhaust(self)
        return reversed(self.cache)

    def __len__(self):
        exhaust(self)
        return len(self.cache)

    @classmethod
    def wrap(cls, func):
        @wraps(func)
        def inner(*args, **kwargs):
            return cls(func(*args, **kwargs))
        return inner

    def __repr__(self):
        return repr(list(self))

    def __getitem__(self, arg):
        if isinstance(arg, slice):
            return List(islice(self, arg.start, arg.stop, arg.step))
        if isinstance(arg, float):
            arg = int(arg)
        if arg >= 0:
            # loop allows modular indexing without needing to exhaust self
            i = iter(self.loop())
            exhaust(zip(range(arg), i))
            return next(i)
        elif arg < 0:
            exhaust(self)
            return self.cache[arg]

    def _loop(self):
        while True:
            yield from self

    def loop(self):
        return List(self._loop())

    # comparison operators are always as lazy as possible

    def __eq__(self, other):
        # fast path
        if self is other:
            return True

        try:
            other = List(other)
        except TypeError:
            return NotImplemented

        return all(x == y for x, y in zip(self, other)) and len(self) == len(other)

    def __ne__(self, other):
        # fast path
        if self is other:
            return False

        try:
            other = List(other)
        except TypeError:
            return NotImplemented

        return any(x != y for x, y in zip(self, other)) or len(self) != len(other)

    def __lt__(self, other):
        # fast path
        if self is other:
            return False

        try:
            other = List(other)
        except TypeError:
            return NotImplemented

        for x, y in zip(self, other):
            if x < y:
                return True
            elif x > y:
                return False
        return len(self) < len(other)

    def __le__(self, other):
        # fast path
        if self is other:
            return True

        try:
            other = List(other)
        except TypeError:
            return NotImplemented

        for x, y in zip(self, other):
            if x < y:
                return True
            elif x > y:
                return False
        return len(self) <= len(other)

    def __gt__(self, other):
        # fast path
        if self is other:
            return False

        try:
            other = List(other)
        except TypeError:
            return NotImplemented
        for x, y in zip(self, other):
            if x > y:
                return True
            elif x < y:
                return False
        return len(self) > len(other)

    def __ge__(self, other):
        # fast path
        if self is other:
            return True

        # slow path
        try:
            other = List(other)
        except TypeError:
            return NotImplemented
        for x, y in zip(self, other):
            if x > y:
                return True
            elif x < y:
                return False
        return len(self) >= len(other)


def exhaust(i):
    """forcibly eagerly evaluate i"""
    for _ in i:
        pass


@List.wrap
def unique(items):
    known = []
    # optimisation for hashable items
    known_fast = set()
    for item in items:
        try:
            if item in known_fast:
                continue
            else:
                known_fast.add(item)
        except TypeError:
            if item in known:
                continue
            else:
                known.append(item)

        yield item


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
