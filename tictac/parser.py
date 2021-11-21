from tictac.codepage import codepage_map
from tictac.ops import ops_taking_links


digraph_introducers = frozenset("𝕜")
digits = frozenset("0123456789")


class _Lexer:
    def __init__(self, code: str):
        self.it = iter(code)
        self.most_recent_digraph = None

    def lex(self):
        for char in self.it:
            yield from self.step(char)

    def step(self, char):
        match char:
            case "«":
                yield from self.string_literal()
            case char if char in digits:
                yield from self.number_literal(char)
            case char if char in digraph_introducers:
                digraph = char + next(self.it, "")
                self.most_recent_digraph = digraph
                yield digraph
            case "⓾":
                if self.most_recent_digraph is not None:
                    yield self.most_recent_digraph
                else:
                    yield "⓾"
            case char if char in codepage_map:
                yield char
            # note that space and § are not actually in the codepage, but provide some useful syntax for non-golfing
            # and they are not treated as invalid characters for convenience
            case "§":
                self.comment()
            case " " | "\n":
                # NOP
                pass
            case char:
                raise SyntaxError("invalid character {char}")

    def string_literal(self):
        value = ""
        for char in self.it:
            if char == "»":
                break
            elif char.isascii():
                value += char
            else:
                raise SyntaxError("unimplemented string literal command {char}")
            # TODO: string escape
        yield "literal", value

    def number_literal(self, char):
        value = int(char)
        if value == 0:
            # leading zero is always a separate token
            yield "literal", 0
        else:
            char = None
            for char in self.it:
                if char in digits:
                    value *= 10
                    value += int(char)
                else:
                    break
            else:
                char = None
            yield "literal", value
            if char is not None:
                yield from self.step(char)

    def comment(self):
        # comment
        for char in self.it:
            if self.char == "\n":
                break
        yield from self.step(char)


def parse(code: str):
    link = []
    groups = []
    for op in _Lexer(code).lex():
        if op == "⟦":
            groups.append(link)
            link = []
        elif op in ops_taking_links:
            arg_links = []
            n_links, _ = ops_taking_links[op]
            for _ in range(n_links):
                if groups:
                    # grouped op
                    arg_links.append(link)
                    # restore previous group as current link
                    link = groups.pop()
                else:
                    # no group: take entire link
                    arg_links.append(link)
                    link = []
            link.append((op, *arg_links))
        else:
            # general op
            link.append(op)
    return link
