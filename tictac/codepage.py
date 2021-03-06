CODEPAGE = """\
๐๐๐๐๐๐ยฒยณโดโตโรฦฦฦรฦฦ๊ชรฦโฑฎรรฦค๊ฦฌรฦฒโฑฒฦณศค\
ยฌ!"#$%&'()*+,-./0123456789:;<=>?\
@ABCDEFGHIJKLMNOPQRSTUVWXYZ[ยฆ]^_\
ยฐabcdefghijklmnopqrstuvwxyz{|}~ยฃ\
แบ๐ธ๐นโ๐ป๐ผ๐ฝ๐พโ๐๐๐๐๐โ๐โโโ๐๐๐๐๐๐๐โคโฆโโงโโ\
รท๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐ ๐ก๐ข๐ฃ๐ค๐ฅ๐ฆ๐ง๐จ๐ฉ๐ช๐ซยซโยปโโ\
รโตโถฮฮโทโธะฮะะฮะะฮรฮ ะฆฮฃะจะชฮฆะฏฮจฮฉแบรรรลาจวท\
รฅฮฑฮฒฮณฮดฮตฮถฮทฮธฮนฮบฮปฮผฮฝฮพรธฯฯฯฯฯฯฯฯฯรรพรงรฆลษโ\
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
