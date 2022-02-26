CODEPAGE = """\
𝟘𝟙𝟚𝟛𝟜𝟝²³⁴⁵⋄ÄƁƇƊËƑƓꞪÏƘⱮÑÖƤꟅƬÜƲⱲƳȤ\
¬!"#$%&'()*+,-./0123456789:;<=>?\
@ABCDEFGHIJKLMNOPQRSTUVWXYZ[¦]^_\
°abcdefghijklmnopqrstuvwxyz{|}~£\
Ẍ𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ⟦⌘⟧↑→\
÷𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫«≈»↓←\
ÅℵℶΓΔℷℸБΘДЖΛИЛΞØΠЦΣШЪΦЯΨΩẞÞÇÆŒҨǷ\
åαβγδεζηθικλμνξøπρστυφχψωßþçæœə∎\
"""

assert len(CODEPAGE) == len(set(CODEPAGE)) == 256

CODEPAGE_MAP = {c: i for i, c in enumerate(CODEPAGE)}


if __name__ == "__main__":
    # print markdown table of codepage
    print("# Codepage")
    codepage2 = [{
        "|": "<code>&#124;</code>",
    }.get(c, f"`{c}`") for c in CODEPAGE]
    hexdigits = "0123456789ABCDEF"
    print("| |" + " | ".join(f"_{n}" for n in hexdigits))
    print(" | ".join("---" for _ in range(17)))
    for i, n in enumerate(hexdigits):
        print(f"**{n}_** | " + " | ".join(f"{c}" for c in codepage2[i*16:i*16+16]))
    print()
    print("```")
    print(CODEPAGE)
    print("```")
