from tictac.ops import ops, ops_taking_links
from tictac.utils import List


class Interpreter:
    def __init__(self, link):
        self.link = link
        self.stack = []
        self.negative_stack = []

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
                case op, *links:
                    link_functions = (
                        # run and return top of stack
                        lambda *args: Interpreter(link).run(*args)[-1]
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

    demand_pop = object()
