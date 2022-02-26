SUBSTITUTIONS = {
    "⋄": "\n",
    "¬": " ",
    "¦": "\\",
    "°": "`",
}


def process_string(string):
    out = ""
    it = iter(string)
    for char in it:
        if char == "∎":
            out += next(it, "∎")
        elif char in SUBSTITUTIONS:
            out += SUBSTITUTIONS[char]
        elif char.isascii():
            out += char
        else:
            raise NotImplementedError("unknown character in string literal {}")
    return 0, lambda state: out
