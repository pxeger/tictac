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
            # note that space, newline, § and ¿ are not actually in the codepage, but provide some useful syntax for
            # non-golfing and they are not treated as invalid characters for convenience
            case "§":
                self.comment()
            case " " | "\n":
                # NOP
                pass
            case "¿":
                # breakpoint
                yield "¿"
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


def _parse(tokens, *, root):
    link = []
    for op in tokens:
        if op == "»":
            if root:
                # TODO(pxeger): what should this do?
                raise SyntaxError("» in main link is undefined behaviour")
            else:
                return link
        elif op in ops_taking_links:
            n_links, _ = ops_taking_links[op]
            link_args = [_parse(tokens, root=False) for _ in range(n_links)]
            link.append((op, *link_args))
        else:
            # general op
            link.append(op)
    return link


def parse(code: str):
    tokens = _Lexer(code).lex()
    return _parse(tokens, root=True)
