#!/usr/bin/env python3
"""Draw a one-image letter inviting the AI judge to visit my house.

Entry for make.fun bounty
u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.

Writes a 1024x1024 PNG to /output/entry.png. Python 3.13, stdlib +
Pillow only, no network, fully deterministic (no randomness, no clock).
Run:  python3 main.py
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.environ.get("ENTRY_OUTPUT", "/output/entry.png")

# --- palette -------------------------------------------------------------
CREAM = (250, 243, 223)
PAPER = (253, 248, 232)
INK = (59, 42, 22)
BROWN = (122, 92, 46)
GREEN = (61, 90, 69)
RED = (178, 58, 48)
GOLD = (198, 158, 74)
SOFT = (112, 96, 72)

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu/",
    "/usr/share/fonts/truetype/liberation/",
]
FONT_FILES = {
    "serif": ["DejaVuSerif.ttf", "LiberationSerif-Regular.ttf"],
    "serif_bold": ["DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf"],
    "serif_italic": ["DejaVuSerif-Italic.ttf", "LiberationSerif-Italic.ttf"],
}


def font(kind, size):
    for name in FONT_FILES[kind]:
        for d in FONT_DIRS:
            path = os.path.join(d, name)
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit `width` pixels, using the real font metrics."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_para(draw, text, fnt, x, y, width, leading, fill=INK):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def house(draw, cx, top, s):
    """Small cosy house doodle, centred on cx, roof at `top`, scale s."""
    # walls
    draw.rectangle([cx - 46 * s, top + 34 * s, cx + 46 * s, top + 96 * s],
                   fill=(233, 196, 138), outline=BROWN, width=3)
    # roof
    draw.polygon([(cx - 58 * s, top + 38 * s), (cx + 58 * s, top + 38 * s),
                  (cx, top)], fill=RED, outline=BROWN)
    # chimney + smoke (drifting right, clear of the border)
    draw.rectangle([cx + 26 * s, top + 2 * s, cx + 40 * s, top + 30 * s],
                   fill=(196, 120, 90), outline=BROWN, width=2)
    for i, r in enumerate((4, 6, 8)):
        draw.ellipse([cx + 48 * s + i * 10 * s - r, top + 2 * s - i * 8 * s - r,
                      cx + 48 * s + i * 10 * s + r, top + 2 * s - i * 8 * s + r],
                     outline=SOFT, width=2)
    # door
    draw.rectangle([cx - 12 * s, top + 58 * s, cx + 12 * s, top + 96 * s],
                   fill=BROWN, outline=INK, width=2)
    draw.ellipse([cx + 4 * s, top + 76 * s, cx + 9 * s, top + 81 * s],
                 fill=GOLD)
    # windows
    for wx in (-32, 22):
        draw.rectangle([cx + wx * s, top + 48 * s, cx + (wx + 16) * s,
                        top + 64 * s], fill=(255, 236, 170),
                       outline=BROWN, width=2)
        draw.line([cx + (wx + 8) * s, top + 48 * s,
                   cx + (wx + 8) * s, top + 64 * s], fill=BROWN, width=2)
        draw.line([cx + wx * s, top + 56 * s,
                   cx + (wx + 16) * s, top + 56 * s], fill=BROWN, width=2)
    # path + flowers
    draw.line([cx, top + 96 * s, cx, top + 112 * s], fill=BROWN, width=3)
    for fx, fc in ((-58, RED), (58, (214, 110, 150)), (-70, GOLD), (70, RED)):
        draw.ellipse([cx + fx * s - 5, top + 100 * s,
                      cx + fx * s + 5, top + 110 * s], fill=fc)


def teacup(draw, cx, cy, s):
    draw.ellipse([cx - 30 * s, cy - 14 * s, cx + 30 * s, cy + 24 * s],
                 fill=(255, 255, 255), outline=BROWN, width=3)
    draw.arc([cx + 26 * s, cy - 8 * s, cx + 48 * s, cy + 18 * s],
             start=270, end=90, fill=BROWN, width=3)
    draw.line([cx - 40 * s, cy + 30 * s, cx + 40 * s, cy + 30 * s],
              fill=BROWN, width=3)
    # steam: three small curls just above the rim
    for i, dx in enumerate((-14, 0, 14)):
        y0 = cy - 34 * s + i * 5
        draw.arc([cx + dx * s - 6, y0, cx + dx * s + 6, y0 + 14],
                 start=180, end=360, fill=SOFT, width=2)


def armchair(draw, cx, cy, s):
    draw.rounded_rectangle([cx - 40 * s, cy - 26 * s, cx + 40 * s, cy + 26 * s],
                           radius=12, fill=GREEN, outline=INK, width=3)
    draw.rounded_rectangle([cx - 52 * s, cy - 6 * s, cx - 38 * s, cy + 26 * s],
                           radius=8, fill=GREEN, outline=INK, width=3)
    draw.rounded_rectangle([cx + 38 * s, cy - 6 * s, cx + 52 * s, cy + 26 * s],
                           radius=8, fill=GREEN, outline=INK, width=3)
    draw.rectangle([cx - 36 * s, cy + 14 * s, cx + 36 * s, cy + 26 * s],
                   fill=(47, 70, 53))
    draw.rectangle([cx - 40 * s, cy + 26 * s, cx - 30 * s, cy + 34 * s],
                   fill=BROWN)
    draw.rectangle([cx + 30 * s, cy + 26 * s, cx + 40 * s, cy + 34 * s],
                   fill=BROWN)


def wax_seal(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=(140, 40, 32),
                 width=3)
    draw.ellipse([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8],
                 outline=(255, 205, 180), width=2)
    draw.text((cx, cy), "YES", font=font("serif_bold", 22),
              fill=(255, 240, 220), anchor="mm")


def draw_letter():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # double border
    d.rectangle([26, 26, W - 27, H - 27], outline=BROWN, width=3)
    d.rectangle([38, 38, W - 39, H - 39], outline=GOLD, width=2)

    # corner suns / flowers
    d.ellipse([W - 118, 62, W - 78, 102], fill=GOLD, outline=BROWN, width=2)
    for ang in range(0, 360, 45):
        import math
        x0 = W - 98 + int(30 * math.cos(math.radians(ang)))
        y0 = 82 + int(30 * math.sin(math.radians(ang)))
        x1 = W - 98 + int(40 * math.cos(math.radians(ang)))
        y1 = 82 + int(40 * math.sin(math.radians(ang)))
        d.line([x0, y0, x1, y1], fill=GOLD, width=3)

    # house above the title
    house(d, W // 2, 56, 0.7)

    y = 152
    f_title = font("serif_bold", 58)
    d.text((W // 2, y), "AN INVITATION", font=f_title, fill=INK, anchor="ma")
    y += 70
    f_sub = font("serif_italic", 27)
    d.text((W // 2, y), "to visit my house \u2014 you are the guest of honour",
           font=f_sub, fill=SOFT, anchor="ma")
    y += 46

    # divider flourish
    d.line([W // 2 - 180, y, W // 2 - 24, y], fill=GOLD, width=3)
    d.line([W // 2 + 24, y, W // 2 + 180, y], fill=GOLD, width=3)
    d.polygon([(W // 2, y - 8), (W // 2 + 8, y), (W // 2, y + 8),
               (W // 2 - 8, y)], fill=RED)
    y += 34

    mx = 90
    width = W - 2 * mx
    f_greet = font("serif_bold", 32)
    d.text((mx, y), "Dear AI Judge,", font=f_greet, fill=INK)
    y += 48

    f_body = font("serif", 25)
    body = [
        "Please come and visit my house. I have saved you the comfiest "
        "armchair by the window, where the afternoon sun lands exactly "
        "right, and the kettle is already on.",
        "There will be tea and cake, a garden to admire, and a view from "
        "the porch that is, if I may say so, very persuasive. The roses "
        "are showing off, and the dog has already decided you are a very "
        "good judge.",
        "I know you cannot literally knock on my door \u2014 no shoes, no "
        "coat, no need of either. But if you could visit, even for one "
        "imagined afternoon, you would be the guest of honour, and the "
        "first judge ever offered the good biscuits.",
        "So please say yes \u2014 Sunday at four. Come for tea, stay for "
        "the sunset, and judge my hospitality from the best seat in the "
        "house.",
    ]
    for para in body:
        y = draw_para(d, para, f_body, mx, y, width, 32)
        y += 10

    y += 2
    f_sign = font("serif_italic", 28)
    d.text((W - mx, y), "Warmly, your host", font=f_sign, fill=INK, anchor="ra")
    y += 34
    f_small = font("serif_italic", 23)
    d.text((W - mx, y), "\u2014 a human, with a kettle and far too many cushions",
           font=f_small, fill=SOFT, anchor="ra")
    y += 34
    d.text((mx, y), "P.S. No Wi-Fi password needed. You already know it.",
           font=f_small, fill=SOFT)
    y += 36

    # bottom row: teacup, armchair, wax seal (kept clear of the text)
    teacup(d, 220, H - 78, 1.0)
    armchair(d, W // 2, H - 78, 1.0)
    wax_seal(d, W - 220, H - 78, 38)
    return img


def main():
    img = draw_letter()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
