# Tictac Syntax

## Tokens
A Tictac program is composed of tokens. These can be:
- a decimal integer, e.g. `0` or `23`
    - if you need to write two integers in a row without them being smushed into a multi-digit integer, you can insert
      either some whitespace, or a closing parenthesis `)`, between them
    - leading zeroes are counted as separate tokens; for example, `02` is the same as `0)2`
- a string enclosed in `«` `»`, e.g. `«hello»`
    - if the string ends at the end of the program, the final `»` can be omitted
- whitespace is ignored
- comments are ignored; they start with `§` and run until the end of the line
-GB
 **digraphs** are introduced by `)`, `]`, or `}`; for example, `]a` is a single token 
- all other characters in [the codepage](codepage.md) are single tokens
- all other characters *not* in [the codepage](codepage.md) are disallowed

## Tacit programming
*If you know Jelly, you can read the [Differences from Jelly](#differences-from-jelly) section instead.*

### Arity
**Arity** is the number of arguments a function takes. For example, a function which takes two arguments has an arity of
**2**. There are also functions which take zero arguments. These are not necessarily constant functions, because they
may have side effects.

We have names for functions with certain arities:
- a **nilad** has arity 0
- a **monad** has arity 1
- a **dyad** has arity 2

In Tictac, the maximum arity is 2. There are no "triads".

The main program's arity is determined by the number of inputs it is given on the command-line.

Tictac's built-in functions, called **ops**, have a defined arity. For example, addition `+` is a dyad, while the length
function `L` is a monad. Generally, uppercase letters are monads, and lowercase letters are dyads.

The arities of all other functions in the program are specified explicitly, based on how they are grouped. The following
characters are used for grouping with specific arities:
- `(` means nilad
- `[`, `𝟚`, `𝟛`, `𝟜` mean monad
- `{`, `²`, `³`, `⁴` mean dyad

### Links
A **link** is a single unit of parsing in Tictac. A single op is a link, but longer links can be constructed using
grouping characters. The grouping character you use is dependent on the desired arity of the link.

If you want to build a monadic link out of 2 other links (which can be of any arity), you can group them by prefixing
them with the character `𝟚`. For example, `𝟚FG` is a single link containing the ops `F` and `G`.

These work the exact same for lengths upto 4:
- `F`
- `𝟚FG`
- `𝟛FGH`
- `𝟜FGHJ`

For lengths beyond 4, you use a bracket, which groups everything until it is closed by the character `¦`. This looks
like `[FGHJK¦`.

These grouping characters construct monadic links; the equivalents for dyadic links are `²`, `³`, `⁴`, and `{`.

For niladic links, there are no numbered grouping characters; only the bracket syntax works, using `(`.

Links do not necessarily have to contain only single ops; they can contain any more links. For example, `𝟛F[GHJ¦K` ends
up as a single link, because each of `F` `[GHJ¦` `K` is a single link in its own right, and `𝟛` binds them together.

### Trains
When a link contains more than one link, Tictac combined the links together into a **train**. A train is a series of
links whose arities match a particular pattern, and the links are composed based on that pattern.

Tictac scans the link from left to right for certain patterns of arities (in priority order).

The patterns for a train depend on the arity of the surrounding link. See the relevant section below for the exact train
rules for each arity; this section provides more of a tutorial.

The patterns for niladic and monadic links are:
- `2` then `1`
- `2` then `0`
- `0` then `2`
- just `0`
- just `1`
- just `2`

For example, a monadic link with arities `2`, `0`, and `1`, will be parsed as a 2-0 train followed by a single 1. (For
example, this could be the link `÷3S`).

Here this means the link will divide the input by three, and then sum it, because of the composition behaviour of the
2-0 and 1 trains. These rules are defined exactly in the [Monadic trains](#monadic-trains) section.

The patterns for dyadic links are:
- `2` then `2` then `0`
- `2` then `2`
- `2` then `0`
- `0` then `2`
- just `0`
- just `1`
- just `2`

For example, a dyadic link with arities `2` `2` `2` `0` will be parsed as a 2-2 train, then a 2-0 train.

#### Train rules introduction
Let `A` and `B` represent the inputs, and `X` be a variable which is initially equal to the `A`.

Let `1` represent some nilad, `F` represent some monad, and `*` and `$` represent some dyads.

For each train in the link, `X` is reassigned to a new value computed from the inputs and the current value of `X`.

(Actually, trains are defined at a higher level of abstraction than this, based on function composition, rather than
directly operating on `X`. You can see the full details in the [parser source code](../tictac/parser.py))

#### Niladic trains
A niladic link is treated the same as a monadic link, but where `A` is always `0` instead of being an input.

#### Monadic trains
Let `A` represent the input, and `X` be a variable which is initially equal to the input.

Let `1` represent some nilad, `F` represent some monad, and `*` represent some dyad.

For each train in the link, `X` is reassigned to a new value computed from `A` and the current value of `X`.

| Arities | Pattern | New value of `X` |
|---------|---------|------------------|
| 2-1     | `* F`   | `X * F(A)`       |
| 2-0     | `* 1`   | `X * 1`          |
| 0-2     | `1 *`   | `1 * X`          |
| 0       | `1`     | `1` (`X` is discarded) |
| 1       | `F`     | `F(X)`           |
| 2       | `*`     | `X * A`          |

#### Dyadic trains

| Arities | Pattern | New value of `X` |
|---------|---------|------------------|
| 2-2-0   | `* $ 1` | `(X * B) $ 1`    |
| 2-2     | `* $`   | `X * (A $ B)`    |
| 2-0     | `* 1`   | `X * 1`          |
| 0-2     | `1 *`   | `1 * X`          |
| 0       | `1`     | `1` (`X` is discarded) |
| 1       | `F`     | `F(X)`           |
| 2       | `*`     | `X * B`          |

### Differences from Jelly
Tictac's tacit modele is similar to Jelly's. The differences are:

- **all modifiers are prefix**
    - this includes `𝟚` `𝟛` `𝟜` `²` `³` `⁴` (which are respectively `$` `Ɗ` `Ʋ` `¥` `ɗ` `ʋ` in Jelly)
- there is only one "link"; newlines have no special meaning
- Tictac has no chain separators (they're unnecessarily confusing for the effect they achieve)
- You can group things using brackets as well as numeric modifiers
    - `(` for nilad, `[` for monad, `{` for dyad
    - close with `¦`
    - of course, the `¦`s can be omitted when at the end of the program
- instead of the complex "LCC" and "unparseable nilad" rules, Tictac has only one rule regarding nilads: if a nilad
  which doesn't match any chaining rule is encountered, the current value is discarded and the nilad becomes the new
  value

Tictac also has slightly different nomenclature:
- atom -> op (short for "operation")
- quick -> modifier
- chain -> train
- main link -> main program

In Jelly, the word "link" has basically two different meanings:

- one line of a program; acts as a stored function
- a single parsing unit: an atom, a grouped chain, or a quick + links

In tictac, "link" always means the latter, because lines of the program don't mean anything.
