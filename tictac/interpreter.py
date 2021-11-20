class State:
    def __init__(self, parent_state, args, recurse=None):
        self.parent_state = parent_state
        self.args = args
        self.recurse = recurse or parent_state.recurse


def interpret(code: str, *args):
    # have to import inside function to prevent circular import
    # :/ python why are you like this
    from tictac.parser import parse

    function = parse(code, len(args))
    state = State(None, args, function)
    if args == ():
        args = (0,)
    return function(state, *args)
