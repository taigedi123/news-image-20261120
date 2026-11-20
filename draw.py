#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page, 1024x1024 PNG.

Everything is drawn in code with Pillow: masthead, hero story, four
story cards and a business/sport strip. No external images, no network.
Run: python3 draw.py  -> writes entry.png next to this file.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (247, 243, 234)      # warm newsprint
INK = (22, 22, 26)
NAVY = (18, 36, 72)
NAVY_LT = (30, 54, 102)
RED = (178, 32, 44)
GOLD = (198, 158, 74)
GREY = (96, 96, 100)
LINE = (190, 184, 170)
CARD = (255, 255, 255)
CHIP_BG = (232, 226, 210)
BODY_GREY = (60, 60, 66)

FONT_DIR = "/usr/share/fonts/truetype/noto/"
SERIF_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(path, size):
    return ImageFont.truetype(path, size)


F_SERIF = lambda s: font(SERIF_DIR + "DejaVuSerif-Bold.ttf", s)
F_BLACK = lambda s: font(FONT_DIR + "NotoSans-Black.ttf", s)
F_BOLD = lambda s: font(FONT_DIR + "NotoSans-Bold.ttf", s)
F_REG = lambda s: font(FONT_DIR + "NotoSans-Regular.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped paragraph, return y after last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x, y, w, color=LINE, width=2):
    draw.line([(x, y), (x + w, y)], fill=color, width=width)


def draw_flag(draw, x, y, w, h, kind):
    """Simple flat flag on a pole, drawn with rectangles only."""
    pole = (120, 116, 108)
    draw.line([(x, y), (x, y + h + 26)], fill=pole, width=4)
    draw.ellipse([x - 4, y - 6, x + 4, y + 2], fill=GOLD)
    if kind == "us":
        for i in range(7):
            draw.rectangle([x + 4, y + i * h // 7, x + 4 + w, y + (i + 1) * h // 7],
                           fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
        draw.rectangle([x + 4, y, x + 4 + w * 2 // 5, y + h * 4 // 7], fill=(28, 52, 110))
        for r in range(3):
            for c in range(4):
                draw.ellipse([x + 12 + c * 13, y + 7 + r * 13, x + 17 + c * 13, y + 12 + r * 13],
                             fill=(255, 255, 255))
    elif kind == "cn":
        draw.rectangle([x + 4, y, x + 4 + w, y + h], fill=(222, 41, 16))
        draw.ellipse([x + 14, y + 9, x + 30, y + 25], fill=(255, 222, 0))
        for sx, sy in [(44, 12), (52, 22), (50, 34), (40, 40)]:
            draw.ellipse([x + sx, y + sy, x + sx + 7, y + sy + 7], fill=(255, 222, 0))
    elif kind == "ru":
        for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
            draw.rectangle([x + 4, y + i * h // 3, x + 4 + w, y + (i + 1) * h // 3], fill=col)


def draw_scales(draw, cx, cy, r, color):
    draw.line([(cx, cy - r), (cx, cy + r)], fill=color, width=4)
    draw.line([(cx - r, cy - r + 8), (cx + r, cy - r + 8)], fill=color, width=4)
    for sx in (-r, r):
        draw.line([(cx + sx, cy - r + 8), (cx + sx, cy + 2)], fill=color, width=3)
        draw.arc([cx + sx - 12, cy - 4, cx + sx + 12, cy + 20], 0, 180, fill=color, width=3)
    draw.line([(cx - r + 4, cy + r), (cx + r - 4, cy + r)], fill=color, width=4)


def draw_cyclone(draw, cx, cy, r, color):
    for i, rr in enumerate(range(r, 6, -8)):
        start = 20 + i * 55
        draw.arc([cx - rr, cy - rr, cx + rr, cy + rr], start, start + 230, fill=color, width=5)


def draw_bridge(draw, x, y, w, h, color):
    # deck, two towers, shallow arch underneath
    draw.line([(x, y + h // 3), (x + w, y + h // 3)], fill=color, width=4)
    for tx in (x + 4, x + w - 8):
        draw.line([(tx, y), (tx, y + h)], fill=color, width=4)
    draw.arc([x, y + h // 3, x + w, y + h], 0, 180, fill=color, width=4)
    for vx in (x + w // 4, x + w // 2, x + 3 * w // 4):
        draw.line([(vx, y + h // 3), (vx, y + h // 3 + 8)], fill=color, width=3)


def draw_gavel(draw, cx, cy, color):
    # diagonal handle, double head at the top end, sound block below
    draw.line([(cx - 18, cy + 18), (cx + 14, cy - 14)], fill=color, width=6)
    for hx, hy in [(cx + 7, cy - 7), (cx + 21, cy - 21)]:
        draw.line([(hx - 6, hy - 6), (hx + 6, hy + 6)], fill=color, width=8)
    draw.line([(cx - 24, cy + 24), (cx - 6, cy + 24)], fill=color, width=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 152], fill=GOLD)
    d.text((512, 14), "THE WORLD IN ONE DAY", font=F_SERIF(58),
           fill=(255, 255, 255), anchor="ma")
    d.text((512, 88), "FRIDAY  20  NOVEMBER  2026", font=F_BLACK(34),
           fill=(255, 214, 110), anchor="ma")
    d.text((40, 128), "WORLD NEWS  •  FRIDAY EDITION", font=F_BOLD(16), fill=(180, 195, 220))
    d.text((984, 128), "SIX STORIES  •  ONE DAY", font=F_BOLD(16),
           fill=(180, 195, 220), anchor="ra")

    # ---------- hero story: trilateral summit ----------
    hy = 174
    d.text((40, hy), "HISTORIC FIRST", font=F_BLACK(22), fill=RED)
    d.text((984, hy), "SHENZHEN  •  CHINA  •  APEC", font=F_BOLD(20), fill=GREY, anchor="ra")
    y = 208
    for line in ["Trump, Xi and Putin meet", "for the first time"]:
        d.text((40, y), line, font=F_BLACK(40), fill=INK)
        y += 50
    y = para(d, 40, y + 8,
             "The three leaders hold a historic three-way summit in "
             "Shenzhen, with nuclear arms control and global security "
             "on the agenda.",
             F_REG(23), 590, 32)
    d.text((40, y + 8), "NUCLEAR ARMS CONTROL  •  GLOBAL SECURITY",
           font=F_BOLD(18), fill=NAVY_LT)
    rule(d, 40, 444, 944, color=INK, width=3)

    # hero visual: three flags + skyline
    vx, vy = 668, 194
    d.rectangle([vx - 12, vy - 12, 984, vy + 224], fill=CARD, outline=LINE, width=2)
    draw_flag(d, vx + 26, vy + 22, 78, 52, "us")
    draw_flag(d, vx + 128, vy + 22, 78, 52, "cn")
    draw_flag(d, vx + 230, vy + 22, 78, 52, "ru")
    d.text((vx + 148, vy + 112), "U.S.  •  CHINA  •  RUSSIA", font=F_BOLD(19),
           fill=INK, anchor="ma")
    d.text((vx + 148, vy + 142), "A first-ever trilateral summit", font=F_REG(18),
           fill=GREY, anchor="ma")
    d.text((vx + 148, vy + 166), "on arms control and security.", font=F_REG(18),
           fill=GREY, anchor="ma")
    # small skyline silhouette along the card bottom
    base = vy + 224
    for bx, bh in [(vx + 4, 14), (vx + 34, 24), (vx + 66, 18), (vx + 98, 28),
                   (vx + 132, 20), (vx + 164, 30), (vx + 198, 18), (vx + 232, 26),
                   (vx + 266, 16), (vx + 296, 22)]:
        d.rectangle([bx, base - bh, bx + 28, base], fill=(214, 208, 192))

    # ---------- 2x2 story grid ----------
    cards = [
        ("THE HAGUE  •  GENOCIDE CASE", RED,
         "ICJ: Myanmar likely\nsought to destroy Rohingya",
         "The court rules Myanmar's military likely intended to destroy "
         "a substantial part of the Rohingya minority in 2017.",
         "scales"),
        ("INDIA  •  CYCLONE AKVAN", NAVY_LT,
         "Cyclone Akvan bears down\non India's east coast",
         "Landfall expected today. About 80,000 people have been "
         "evacuated in Odisha and Andhra Pradesh as the storm nears.",
         "cyclone"),
        ("UKRAINE  •  WAR", RED,
         "Ukraine hits Crimean Bridge;\nKyiv embassies struck",
         "Ukraine strikes the Crimean Bridge, halting rail traffic. "
         "Russian strikes damage the Austrian and Dutch embassies "
         "in Kyiv.",
         "bridge"),
        ("SEOUL  •  MARTIAL LAW CASE", NAVY_LT,
         "South Korea court clears\nformer PM Han Duck-soo",
         "The Supreme Court overturns the conviction of former prime "
         "minister Han Duck-soo in the case linked to the 2024 martial "
         "law declaration.",
         "gavel"),
    ]
    gx, gy = 40, 460
    cw, ch, gap = 464, 184, 16
    for i, (kick, kcol, head, body, icon) in enumerate(cards):
        cx0 = gx + (i % 2) * (cw + gap)
        cy0 = gy + (i // 2) * (ch + gap)
        d.rectangle([cx0, cy0, cx0 + cw, cy0 + ch], fill=CARD, outline=LINE, width=2)
        ix, iy = cx0 + 14, cy0 + 14
        d.ellipse([ix, iy, ix + 64, iy + 64], fill=CHIP_BG, outline=GOLD, width=2)
        if icon == "scales":
            draw_scales(d, ix + 32, iy + 32, 20, NAVY)
        elif icon == "cyclone":
            draw_cyclone(d, ix + 32, iy + 32, 26, NAVY_LT)
        elif icon == "bridge":
            draw_bridge(d, ix + 10, iy + 18, 44, 28, NAVY)
        elif icon == "gavel":
            draw_gavel(d, ix + 32, iy + 32, NAVY)
        tx = cx0 + 92
        d.text((tx, cy0 + 12), kick, font=F_BOLD(15), fill=kcol)
        y = cy0 + 36
        for line in head.split("\n"):
            d.text((tx, y), line, font=F_BLACK(22), fill=INK)
            y += 26
        para(d, tx, y + 4, body, F_REG(17), cw - 104, 22, fill=BODY_GREY)

    # ---------- bottom strip: business + sport ----------
    by = 856
    d.rectangle([40, by, 984, by + 96], fill=NAVY, outline=NAVY)
    d.text((64, by + 12), "BUSINESS", font=F_BOLD(16), fill=(255, 214, 110))
    d.text((64, by + 36), "Anthropic valued at $1.5 trillion", font=F_BLACK(24),
           fill=(255, 255, 255))
    d.text((64, by + 68), "The AI firm's valuation reportedly reaches $1.5 trillion.",
           font=F_REG(17), fill=(200, 210, 228))
    d.line([(512, by + 14), (512, by + 82)], fill=(90, 110, 150), width=2)
    d.text((536, by + 12), "SPORT  •  CRICKET", font=F_BOLD(16), fill=(255, 214, 110))
    d.text((536, by + 36), "Nicholls 113* as NZ reach 243/5", font=F_BLACK(24),
           fill=(255, 255, 255))
    d.text((536, by + 68), "India v New Zealand, 1st Test, day one in Wellington.",
           font=F_REG(17), fill=(200, 210, 228))

    # ---------- footer ----------
    d.text((512, 968), "THE WORLD IN ONE DAY  •  FRIDAY 20 NOVEMBER 2026  •  SIX STORIES FROM AROUND THE GLOBE",
           font=F_BOLD(15), fill=GREY, anchor="ma")

    img.save(OUT, format="PNG")


if __name__ == "__main__":
    main()
    print("wrote", OUT)
