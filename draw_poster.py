#!/usr/bin/env python3
"""Draw the front-page poster for 26 November 2026 world news.

Newspaper-style poster, 1024x1024, PIL shapes and typography only.
No photos, no external assets, no network. Deterministic output.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (24, 24, 22)
RED = (178, 34, 34)
DARK = (38, 38, 44)
GOLD = (214, 158, 46)
TEAL = (18, 110, 110)
GREY = (96, 92, 84)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
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


def text_block(draw, x, y, text, fnt, fill, max_w, leading=None):
    """Draw wrapped text, return y after the last line."""
    if leading is None:
        leading = int(fnt.size * 1.18)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text, color=RED):
    f = font(SANS_B, 21)
    draw.text((x, y), text, font=f, fill=color)
    return y + 28


def panel(draw, x0, y0, x1, y1, fill=(255, 255, 255)):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=fill,
                           outline=INK, width=2)


def flame(draw, cx, base_y, size, c1=(232, 90, 20), c2=(245, 180, 40)):
    """A simple two-tone flame, centred at cx, base at base_y."""
    s = size
    outer = [(cx - 0.55 * s, base_y), (cx - 0.62 * s, base_y - 0.55 * s),
             (cx - 0.25 * s, base_y - 0.75 * s), (cx, base_y - 1.25 * s),
             (cx + 0.30 * s, base_y - 0.85 * s), (cx + 0.60 * s, base_y - 0.45 * s),
             (cx + 0.55 * s, base_y)]
    draw.polygon(outer, fill=c1)
    inner = [(cx - 0.28 * s, base_y), (cx - 0.30 * s, base_y - 0.42 * s),
             (cx, base_y - 0.72 * s), (cx + 0.28 * s, base_y - 0.38 * s),
             (cx + 0.26 * s, base_y)]
    draw.polygon(inner, fill=c2)


def draw_refinery(draw, x0, y0, x1, y1):
    """Oil refinery silhouette with flame and sun, inside a box."""
    draw.rectangle([x0, y0, x1, y1], fill=(30, 42, 58))
    draw.ellipse([x1 - 78, y0 + 14, x1 - 18, y0 + 74], fill=(245, 190, 60))
    # storage tanks
    for tx, tw in ((x0 + 18, 74), (x0 + 104, 60)):
        draw.rounded_rectangle([tx, y1 - 78, tx + tw, y1 - 14], radius=8,
                               fill=(70, 88, 110))
        draw.arc([tx, y1 - 92, tx + tw, y1 - 64], 180, 360, fill=(70, 88, 110), width=4)
    # distillation towers
    for tx in (x0 + 196, x0 + 246):
        draw.rectangle([tx, y1 - 150, tx + 34, y1 - 14], fill=(52, 66, 88))
        draw.rectangle([tx + 12, y1 - 178, tx + 22, y1 - 150], fill=(52, 66, 88))
    # chimney with flame
    draw.rectangle([x0 + 296, y1 - 170, x0 + 312, y1 - 14], fill=(52, 66, 88))
    flame(draw, x0 + 304, y1 - 168, 26)
    # ground line and pipes
    draw.line([x0, y1 - 14, x1, y1 - 14], fill=(20, 28, 40), width=4)
    draw.line([x0 + 92, y1 - 60, x0 + 196, y1 - 60], fill=(120, 130, 145), width=5)


def draw_mini_icon(draw, kind, x, y):
    """Small 54x54 icon in the corner of a story panel."""
    if kind == "flame":
        draw.rectangle([x, y, x + 54, y + 54], fill=(30, 42, 58))
        flame(draw, x + 27, y + 50, 22)
    elif kind == "chip":
        draw.rectangle([x, y, x + 54, y + 54], fill=(232, 236, 242),
                       outline=INK, width=2)
        draw.rectangle([x + 14, y + 14, x + 40, y + 40], fill=DARK)
        draw.text((x + 19, y + 19), "AI", font=font(SANS_B, 16),
                  fill=(255, 255, 255))
    else:  # balloon
        draw.rectangle([x, y, x + 54, y + 54], fill=(238, 232, 246),
                       outline=INK, width=2)
        draw.ellipse([x + 10, y + 6, x + 44, y + 34], fill=RED, outline=INK,
                     width=2)
        draw.line([x + 20, y + 34, x + 24, y + 48], fill=INK, width=2)
        draw.line([x + 34, y + 34, x + 30, y + 48], fill=INK, width=2)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 148], fill=(20, 20, 26))
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 74)
    d.text(((W - d.textlength(title, font=tf)) / 2, 18), title, font=tf,
           fill=(248, 244, 233))
    date = "THURSDAY  ·  26 NOVEMBER 2026"
    df = font(SANS_B, 34)
    d.text(((W - d.textlength(date, font=df)) / 2, 100), date, font=df,
           fill=(245, 190, 60))
    d.line([28, 156, W - 28, 156], fill=INK, width=3)
    d.line([28, 162, W - 28, 162], fill=INK, width=1)
    tag = "One day's news from every corner of the world"
    tgf = font(SANS, 22)
    d.text(((W - d.textlength(tag, font=tgf)) / 2, 168), tag, font=tgf, fill=GREY)

    # ---- Lead story: Houthis / oil ----
    panel(d, 28, 204, 996, 486)
    x = 52
    y = kicker(d, x, 224, "MIDDLE EAST  ·  ENERGY")
    y = text_block(d, x, y + 4, "HOUTHIS CLAIM STRIKE ON SAUDI REFINERY",
                   font(SANS_B, 40), INK, 560, leading=48)
    y = text_block(d, x, y + 8,
                   "Brent crude tops $94 as oil jumps on fears of a supply disruption.",
                   font(SANS, 25), DARK, 560, leading=32)
    d.text((x, 436), "Ras Tanura and Riyadh targeted, the group says",
           font=font(SANS, 21), fill=GREY)
    draw_refinery(d, 648, 224, 972, 466)

    # ---- Row 2: tariffs / Bank of Korea ----
    panel(d, 28, 502, 506, 716)
    y = kicker(d, 52, 520, "TRADE  ·  UNITED STATES")
    y = text_block(d, 52, y + 4, "US PROPOSES NEW TARIFFS ON 14 PARTNERS",
                   font(SANS_B, 28), INK, 430, leading=34)
    text_block(d, 52, y + 8,
               "Washington targets factory overcapacity; China faces the highest rates.",
               font(SANS, 20), DARK, 430, leading=26)

    panel(d, 518, 502, 996, 716)
    y = kicker(d, 542, 520, "ASIA  ·  ECONOMY")
    y = text_block(d, 542, y + 4, "SOUTH KOREA RAISES RATES TO 3.25%",
                   font(SANS_B, 28), INK, 430, leading=34)
    text_block(d, 542, y + 8,
               "Bank of Korea resumes tightening as a chip-led export boom runs hot.",
               font(SANS, 20), DARK, 430, leading=26)

    # ---- Row 3: three stories ----
    cols = [
        (28,  "EGYPT", "FUEL TANKER FIRE NEAR CAIRO KILLS AT LEAST 30",
         "A crash on the ring road sets a tanker ablaze.", "flame"),
        (358, "TECH  ·  MARKETS", "S&P PUTS NVIDIA ON DOWNGRADE WATCH",
         "Governance questions after the CEO's exit and return.", "chip"),
        (688, "UNITED STATES", "THANKSGIVING: MACY'S PARADE PUT OFF BY STORM",
         "The 100th parade moves to Saturday — a first for weather.", "balloon"),
    ]
    for x0, kick, head, deck, art in cols:
        x1 = x0 + 308
        panel(d, x0, 732, x1, 940)
        draw_mini_icon(d, art, x0 + 14, 744)
        kicker(d, x0 + 78, 756, kick)
        y = text_block(d, x0 + 18, 806, head, font(SANS_B, 23), INK, 272,
                       leading=28)
        text_block(d, x0 + 18, y + 4, deck, font(SANS, 17), DARK, 272,
                   leading=22)

    # ---- Footer ticker ----
    d.rectangle([0, 956, W, H], fill=(20, 20, 26))
    tf2 = font(SANS_B, 16)
    tick1 = ("ALSO TODAY:  Norway court voids disputed oil licences  ·  "
             "Kenya's last Ebola patient discharged")
    tick2 = "North Korea's Kim calls for wider deployment of tactical nuclear arms"
    d.text(((W - d.textlength(tick1, font=tf2)) / 2, 964), tick1, font=tf2,
           fill=(248, 244, 233))
    d.text(((W - d.textlength(tick2, font=tf2)) / 2, 988), tick2, font=tf2,
           fill=(245, 190, 60))

    return img


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build().save(out, "PNG", optimize=True)
    print("wrote", out)
