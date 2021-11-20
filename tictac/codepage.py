codepage = ""
# (note: these characters are often detected as the wrong width by terminals;
# extra spaces have been inserted to improve their legibility)
codepage += "🯰🯱🯲🯳🯴🯵🯶🯷🯸🯹          ".replace(" ", "")
codepage += "◊"
codepage += "⓵⓶⓷⓸⓹⓺⓻⓼⓽⓾            ".replace(" ", "")
codepage += "«»⊢⊣◉⟬⟭⟦⟧     ".replace(" ", "")
codepage += "𝕒𝕓  ".replace(" ", "")
assert len(codepage) == 32, f"{len(codepage)} != 32"
# ASCII
codepage += "¬"
codepage += "!\"#$%&'()*+,-./"
codepage += "0123456789"
codepage += ":;<=>?@"
codepage += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
codepage += "[\\]^_`"
codepage += "abcdefghijklmnopqrstuvwxyz"
codepage += "{|}~"

codepage += "£"
assert len(codepage) == 128

codepage += "𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫   ".replace(" ", "")
codepage += "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙              ".replace(" ", "")
codepage += "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳     ".replace(" ", "")
codepage += "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩       ".replace(" ", "")
codepage += "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃                ".replace(" ", "")

assert len(codepage) == len(set(codepage)) == 256


codepage_map = {c: i for i, c in enumerate(codepage)}


if __name__ == "__main__":
    # print markdown table of codepage
    codepage2 = [{
        "`": "<code>&#96;</code>",
        "|": "<code>&#124;</code>",
    }.get(c, f"`{c}`") for c in codepage]
    hexdigits = "0123456789ABCDEF"
    print("| |" + " | ".join(f"_{n}" for n in hexdigits))
    print(" | ".join("---" for _ in range(17)))
    for i, n in enumerate(hexdigits):
        print(f"**{n}_** | " + " | ".join(f"{c}" for c in codepage2[i*16:i*16+16]))
    print()
    print("```")
    print(codepage)
    print("```")
