from tictac.ops import simple_ops, ops_taking_links
from tictac.utils import List


class Interpreter:
    def __init__(self, link):
        self.link = link
        self.stack = []
        self.negative_stack = []

    def push_constant(self, obj):
        assert not (self.negative_stack and self.stack)
        self.stack.append(obj)
        if self.negative_stack:
            self.negative_stack.pop()()

    def do_func(self, func, arity, multi_output=False):
        if arity > len(self.stack):  # not enough args
            curried_args = self.stack.copy()
            self.stack.clear()
            f = lambda: self.do_func(lambda *more_args: func(*curried_args, *more_args), arity - len(curried_args), multi_output)
            self.negative_stack.append(f)
        else:
            args = (self.stack.pop() for _ in range(arity))
            result = func(*args)
            if multi_output:
                for x in result:
                    self.push_constant(x)
            else:
                self.push_constant(result)

    def run(self, *inputs):
        self.stack = []
        self.negative_stack = []
        for element in self.link:
            match element:
                case "literal", value:
                    self.push_constant(value)
                case op, *links:
                    link_functions = (
                        # run and return top of stack
                        lambda *args: Interpreter(link).run(*args)[-1]
                        for link in links)
                    n_links, metafunc = ops_taking_links[op]
                    assert len(links) == n_links
                    arity, func = metafunc(*link_functions)
                    self.do_func(func, arity)
                case op:
                    arity, func = simple_ops[op]
                    multi_output = False
                    if arity < 0:
                        arity = ~arity
                        multi_output = True
                    self.do_func(func, arity, multi_output)
        for i in inputs:
            self.push_constant(i)
        return self.stack
