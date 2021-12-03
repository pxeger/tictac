import os

from tictac.ops import ops, ops_taking_links
from tictac.utils import List, print_stderr


try:
    WIDTH, _ = os.get_terminal_size()
except (OSError, AttributeError):
    # OSError: no terminal connected
    # AttributeError: this Python doesn't support os.get_terminal_size
    # use a conservative default
    WIDTH = 60


class Interpreter:
    def __init__(self, link, parent=None):
        self.link = link
        self.stack = []
        self.negative_stack = []
        # store reference to interpreter instance running parent stack frame, for debugging
        self.parent = parent

    def push(self, obj):
        assert not (self.negative_stack and self.stack)
        if self.negative_stack:
            # resume
            generator = self.negative_stack.pop()
            self.run_generator(generator, obj)
        else:
            self.stack.append(obj)

    def run_generator(self, generator, value_to_send):
        try:
            demand = generator.send(value_to_send)
        except StopIteration:
            # no more demands
            return
        if demand is self.demand_pop:
            if self.stack:
                self.run_generator(generator, self.stack.pop())
            else:
                # suspend
                self.negative_stack.append(generator)
        else:
            raise ValueError("invalid demand")

    def do_func(self, func):
        r = func(self)
        if r is None:
            return
        else:
            generator = iter(r)
            self.run_generator(generator, None)

    def run(self, *inputs):
        self.stack = []
        self.negative_stack = []
        for element in self.link:
            match element:
                case "literal", value:
                    self.push(value)
                case "¿":
                    print_stderr("¿" * WIDTH)
                    self.breakpoint()
                    print_stderr("¿" + "?" * (WIDTH - 1))
                case op, *links:
                    link_functions = (
                        # run and return top of stack
                        lambda *args: Interpreter(link, parent=self).run(*args)[-1]
                        for link in links)
                    n_links, metafunc = ops_taking_links[op]
                    assert len(links) == n_links
                    func = metafunc(*link_functions)
                    self.do_func(func)
                case op:
                    func = ops[op]
                    self.do_func(func)
        for i in inputs:
            self.push(i)
        return self.stack

    def breakpoint(self):
        if self.parent:
            self.parent.breakpoint()
            print_stderr("¿" * 3)
        assert not (self.stack and self.negative_stack)
        if self.stack:
            for item in self.stack:
                print_stderr("¿", item)
        elif self.negative_stack:
            print_stderr("¿" * 3, "waiting for:")
            for generator in self.negative_stack:
                print_stderr("¿", generator)

    demand_pop = object()
