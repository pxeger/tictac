from functools import wraps
from typing import final


def vectorise(arity, level):
    def decorator(func):
        if arity == 0:
            return func

        @wraps(func)
        def inner(*args):
            match args:
                case (List() as xs), (List() as ys):
                    return List(func(x, y) for x, y in zip(xs, ys))
                case (List() as xs), y:
                    return List(func(x, y) for x in xs)
                case x, (List() as ys):
                    return List(func(x, y) for y in ys)
                case x, y:
                    return func(x, y)
                case (List() as xs),:
                    return List(func(x) for x in xs)
                case x,:
                    return func(x)
                case ():
                    return func()
        return inner
    return decorator


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
