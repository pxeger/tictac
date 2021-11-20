# Syntax
Tictac has a simple syntax. Understanding it can be broken down into two separate steps: lexing, also known as
tokenisation, and parsing - which is, at the moment, basically just about grouping code correctly.

## Lexing
Most characters that are in the Tictac codepage are single tokens themselves. The other types of tokens are:
- digraphs
- number literals
- string literals

In addition, spaces and newlines can be used to separate tokens but do not comprise tokens themselves (they are just
ignored). Neither space nor newline are part of the Tictac codepage; the assumption is that they will never be used in
competitive golfing and therefore their existance would waste what could otherwise be a single-byte builtin.

Tictac also has comments, which start at `§` and continue to the end of the line (or the end of the file). `§` is also
not in the Tictac codepage.

All other characters that are not in the Tictac codepage are not allowed in programs.

A digraph is two characters which are part of the same token; this syntax is used for operations that don't deserve a
single-byte instruction. The first character of a digraph must currently be `𝕜` (other characters will be introduced in
future), and the second character can be anything other than whitespace.

A number literal is either `0`, or a non-zero digit (`1`-`9`) followed by one or more digits (`0`-`9`). For example:

```
0    -> one literal with the value 0
12   -> one literal with the value 12
```

A string literal starts with `"` and ends with a matching `"` or at the end of the file. All ASCII characters (other
than `"`) in between are included in the content of the string; non-ASCII characters are not allowed.

Literals correspond to operations that return constant values.

## Parsing
Parsing takes a list of tokens and produces a link, which is a list of operations. For example, `xyz` is just parsed
into the sequence of operations `x, y, z`.

Most operations just represent builtin functions, but some operations need to operate on a list of other operations,
such as a map. These are called *operations taking links*, or *link-ops* for short. Conventionally, link-ops use the
double-struck letters in Tictac's codepage (`𝕒` to `𝕫`).

By default, a link-op consumes all code to its left (up to the start of the source code). However, if there is a `⟦`
character to its left, it stops there and consumes all code until it. For example, `xyz𝕞` results in `𝕞(x, y, z)`, but
`x⟦yz𝕞` produces `x, 𝕞(y, z)`

Link-ops can be thought of as postfix operators on other bits of code: `x𝕞𝕗` results in `𝕗(𝕞(x))`. (the `()`s here
aren't really function application, but just show which bits of code are inside the other bits of code.)

Some link-ops need more than one link - in this case, the process is simply repeated multiple times.
