"""Render the front page of *The Daily Meridian* for Friday 27 November 2026.

A one-page broadsheet that sums up the day's world news, drawn entirely with
Pillow: masthead, date bar, a lead story on Ukraine, side stories on North
Korea and the Strait of Hormuz, a bottom row on the U.S. Thanksgiving storm,
the EU's failed €45bn Ukraine loan and SpaceX's satellite clearance, plus a
ticker of further headlines.  Every story carries a small drawn panel so the page reads
as pictures plus words, the way a picture editor would lay it out.

The drawing is deterministic: fixed geometry, fixed fonts, no randomness
outside a fixed seed, so two runs write the same bytes.
"""

import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
RIGHT = W - MARGIN

PAPER = (247, 243, 233)
INK = (22, 22, 22)
GRAY = (96, 92, 84)
ACCENT = (163, 32, 28)
RULE = (22, 22, 22)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, size, max_width):
    """Shrink a font until the text fits max_width."""
    while size > 8:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 2
    return font(path, size)


def wrap(draw, text, f, max_width):
    """Greedy word wrap; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=f) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, f, fill, max_width, leading):
    for line in wrap(draw, text, f, max_width):
        draw.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- panels ---

def panel_lead(d, box):
    """Dusk skyline: a capital under a low sun, smoke over rooftops."""
    x0, y0, x1, y1 = box
    for i in range(y1 - y0):
        t = i / max(1, (y1 - y0))
        d.line([(x0, y0 + i), (x1, y0 + i)],
               fill=(int(66 + 150 * t), int(72 + 96 * t), int(96 + 26 * t)))
    sun_cx, sun_cy, sun_r = x0 + (x1 - x0) * 0.68, y0 + (y1 - y0) * 0.52, 26
    d.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
              fill=(246, 214, 140))
    ground = y1 - 46
    d.rectangle([x0, ground, x1, y1], fill=(24, 24, 30))
    rng = random.Random(7)
    bx = x0 + 6
    while bx < x1 - 18:
        bw = rng.randint(16, 34)
        bh = rng.randint(18, 44)
        d.rectangle([bx, ground - bh, bx + bw, ground], fill=(24, 24, 30))
        if rng.random() < 0.5:  # a lit window or two
            d.rectangle([bx + 4, ground - bh + 6, bx + 8, ground - bh + 10],
                        fill=(250, 205, 110))
        bx += bw + rng.randint(3, 9)
    for sx in (x0 + 42, x0 + 118):  # smoke: soft puffs drifting as they rise
        for k in range(8):
            r = 3 + k
            cx = sx + k * 3
            cy = ground - 46 - k * 6
            shade = 118 + k * 7
            d.ellipse([cx - r, cy - r, cx + r, cy + r],
                      fill=(shade, shade - 4, shade - 2))


def panel_missile(d, box):
    """A missile on its pad under a night sky, red star above."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(26, 30, 46))
    rng = random.Random(11)
    for _ in range(26):
        sx, sy = rng.randint(x0 + 4, x1 - 4), rng.randint(y0 + 4, y1 - 40)
        d.point((sx, sy), fill=(230, 230, 220))
    cx = (x0 + x1) // 2
    base = y1 - 14
    d.polygon([(cx - 13, base), (cx - 13, y0 + 52), (cx, y0 + 26),
               (cx + 13, y0 + 52), (cx + 13, base)], fill=(214, 216, 222))
    d.polygon([(cx - 13, base - 26), (cx - 30, base), (cx - 13, base)],
              fill=(178, 44, 40))
    d.polygon([(cx + 13, base - 26), (cx + 30, base), (cx + 13, base)],
              fill=(178, 44, 40))
    d.rectangle([cx - 34, base, cx + 34, base + 5], fill=(120, 124, 134))
    sx, sy, r = x0 + 26, y0 + 20, 9  # red star, drawn as a diamond badge
    d.polygon([(sx, sy - r), (sx + r, sy), (sx, sy + r), (sx - r, sy)],
              fill=(206, 52, 46))


def panel_tanker(d, box):
    """A tanker at sea under a hot sun."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(238, 214, 158))
    d.ellipse([x1 - 52, y0 + 10, x1 - 18, y0 + 44], fill=(244, 176, 84))
    sea = y0 + (y1 - y0) * 0.58
    d.rectangle([x0, sea, x1, y1], fill=(38, 88, 112))
    for i in range(5):
        wy = sea + 8 + i * 7
        d.arc([x0 + 8 + i * 13, wy, x0 + 44 + i * 13, wy + 8], 180, 330,
              fill=(170, 205, 220), width=2)
    hx0, hx1 = x0 + 26, x1 - 26
    hy = sea - 16
    d.polygon([(hx0, hy), (hx1, hy), (hx1 - 14, hy + 16), (hx0 + 10, hy + 16)],
              fill=(40, 40, 44))
    d.rectangle([hx0 + 16, hy - 12, hx1 - 44, hy], fill=(150, 62, 44))
    d.rectangle([hx1 - 40, hy - 26, hx1 - 22, hy], fill=(226, 224, 216))
    d.rectangle([hx1 - 36, hy - 22, hx1 - 26, hy - 16], fill=(70, 90, 110))


def panel_storm(d, box):
    """Storm cloud and driving snow over a snowed-in house and pines."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(206, 218, 228))
    cy = y0 + 26
    for (ex, ey, er) in [(x0 + 52, cy, 30), (x0 + 96, cy - 10, 38),
                         (x0 + 142, cy, 30), (x0 + 74, cy + 12, 32),
                         (x0 + 120, cy + 12, 32)]:
        d.ellipse([ex - er, ey - er // 2, ex + er, ey + er // 2],
                  fill=(148, 160, 174))
    rng = random.Random(23)
    snow_lo = y0 + 38
    snow_hi = max(snow_lo, y1 - 18)
    for _ in range(34):
        sx, sy = rng.randint(x0 + 6, x1 - 6), rng.randint(snow_lo, snow_hi)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(250, 250, 250))
    gy = y1 - 14
    d.rectangle([x0, gy, x1, y1], fill=(232, 238, 244))
    hx = x0 + 196  # house with a snowy roof
    d.rectangle([hx, gy - 22, hx + 44, gy], fill=(96, 74, 60))
    d.polygon([(hx - 5, gy - 22), (hx + 22, gy - 36), (hx + 49, gy - 22)],
              fill=(240, 244, 248))
    d.rectangle([hx + 17, gy - 13, hx + 27, gy], fill=(52, 40, 32))
    for tx in (x0 + 40, x0 + 84, x0 + 250):  # pines
        d.polygon([(tx, gy - 30), (tx + 11, gy - 8), (tx - 11, gy - 8)],
                  fill=(52, 84, 62))
        d.polygon([(tx, gy - 40), (tx + 9, gy - 22), (tx - 9, gy - 22)],
                  fill=(52, 84, 62))
        d.rectangle([tx - 2, gy - 8, tx + 2, gy], fill=(80, 62, 46))


def panel_fire(d, box):
    """A tanker truck at night, stylised flames above the tank."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(52, 40, 40))
    gy = y1 - 18
    d.rectangle([x0, gy, x1, y1], fill=(30, 26, 26))
    tx0, tx1 = x0 + 26, x0 + 128
    ty = gy - 24
    d.rounded_rectangle([tx0, ty, tx1, ty + 22], 10, fill=(188, 190, 194))
    d.rectangle([tx1, ty + 6, tx1 + 26, gy - 8], fill=(120, 124, 130))
    d.rectangle([tx1 + 16, ty + 10, tx1 + 24, ty + 17], fill=(170, 205, 225))
    for wx in (tx0 + 16, tx0 + 52, tx1 + 12):
        d.ellipse([wx - 8, gy - 10, wx + 8, gy + 6], fill=(16, 16, 16))
    fx = tx0 + 44
    d.polygon([(fx - 20, ty - 2), (fx - 6, ty - 22), (fx + 2, ty - 12),
               (fx + 12, ty - 24), (fx + 24, ty - 4)], fill=(226, 110, 40))
    d.polygon([(fx - 10, ty - 2), (fx, ty - 15), (fx + 10, ty - 2)],
              fill=(246, 178, 60))


def panel_eu(d, box):
    """EU flag motif: a ring of gold stars on a blue field."""
    import math
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(0, 51, 153))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ring = min(x1 - x0, y1 - y0) * 0.30
    for k in range(12):
        ang = -math.pi / 2 + k * 2 * math.pi / 12
        sx, sy = cx + ring * math.cos(ang), cy + ring * math.sin(ang)
        r = 4.5
        pts = []
        for j in range(10):
            a = -math.pi / 2 + j * math.pi / 5
            rr = r if j % 2 == 0 else r * 0.42
            pts.append((sx + rr * math.cos(a), sy + rr * math.sin(a)))
        d.polygon(pts, fill=(255, 204, 0))


def panel_satellite(d, box):
    """A data-centre satellite over the curve of the Earth."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(14, 18, 38))
    rng = random.Random(31)
    for _ in range(40):
        sx, sy = rng.randint(x0 + 3, x1 - 3), rng.randint(y0 + 3, y1 - 30)
        d.point((sx, sy), fill=(235, 238, 250))
    d.arc([x0 + 6, y1 - 40, x1 - 6, y1 + 44], 180, 360, fill=(90, 140, 200),
          width=3)
    cx, cy = (x0 + x1) // 2, y0 + 44
    d.rectangle([cx - 34, cy - 12, cx - 10, cy + 12], fill=(64, 110, 190))
    d.rectangle([cx + 10, cy - 12, cx + 34, cy + 12], fill=(64, 110, 190))
    for gx in range(cx - 30, cx - 12, 6):
        d.line([(gx, cy - 12), (gx, cy + 12)], fill=(30, 60, 120), width=1)
    for gx in range(cx + 14, cx + 32, 6):
        d.line([(gx, cy - 12), (gx, cy + 12)], fill=(30, 60, 120), width=1)
    d.rectangle([cx - 9, cy - 10, cx + 9, cy + 10], fill=(206, 210, 218))
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(240, 190, 80))


PANELS = {
    "lead": panel_lead,
    "missile": panel_missile,
    "tanker": panel_tanker,
    "storm": panel_storm,
    "fire": panel_fire,
    "eu": panel_eu,
    "satellite": panel_satellite,
}


# ---------------------------------------------------------------- layout ---

def story(d, x, y, w, kicker, headline, body, h_size=27, b_size=17,
          h_font=SERIF_B, leading=22):
    d.text((x, y), kicker, font=font(SANS_B, 16), fill=ACCENT)
    y += 24
    y = text_block(d, x, y, headline, font(h_font, h_size), INK, w, h_size + 6)
    y += 2
    y = text_block(d, x, y, body, font(SANS, b_size), (40, 40, 40), w, leading)
    return y


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top line ------------------------------------------------------
    d.text((MARGIN, 22), "VOL. I · No. 27", font=font(SANS_B, 17), fill=INK)
    tag = "WORLD EDITION"
    d.text((RIGHT - d.textlength(tag, font=font(SANS_B, 17)), 22), tag,
           font=font(SANS_B, 17), fill=INK)
    d.line([(MARGIN, 50), (RIGHT, 50)], fill=RULE, width=3)
    d.line([(MARGIN, 56), (RIGHT, 56)], fill=RULE, width=1)

    # --- masthead ------------------------------------------------------
    name = "The Daily Meridian"
    f = fit_font(d, name, SERIF_B, 88, RIGHT - MARGIN)
    tw = d.textlength(name, font=f)
    d.text(((W - tw) / 2, 58), name, font=f, fill=INK)
    d.line([(MARGIN, 170), (RIGHT, 170)], fill=RULE, width=5)
    d.line([(MARGIN, 179), (RIGHT, 179)], fill=RULE, width=1)

    # --- date bar ------------------------------------------------------
    d.rectangle([MARGIN, 192, RIGHT, 242], fill=INK)
    date = "FRIDAY, NOVEMBER 27, 2026"
    f = font(SANS_B, 31)
    d.text((MARGIN + 18, 205), date, font=f, fill=(250, 248, 240))
    sub = "THE WORLD IN ONE PAGE"
    f2 = font(SANS_B, 18)
    d.text((RIGHT - 18 - d.textlength(sub, font=f2), 211), sub, font=f2,
           fill=(250, 248, 240))

    # --- lead story ----------------------------------------------------
    lx, lw = MARGIN, 604
    d.text((lx, 258), "UKRAINE WAR — APPEAL & STRIKES",
           font=font(SANS_B, 19), fill=ACCENT)
    y = text_block(d, lx, 284,
                   "TRUMP URGES PUTIN TO PULL BACK IN UKRAINE",
                   font(SERIF_B, 51), INK, lw, 58)
    body = ("President Trump said he pressed Vladimir Putin, when they met "
            "in China last week, to pull back Russia's military aggression "
            "in Europe. President Zelenskyy warned of a new mass strike as "
            "Russian missiles hit Kyiv, wounding seven and cutting power "
            "across Ukraine.")
    text_block(d, lx, y + 8, body, font(SERIF, 19), (35, 35, 35), 372, 24)
    panel_lead(d, (lx + 392, y + 8, lx + lw, y + 148))
    cap = "Kyiv at dusk: strikes cut power nationwide."
    text_block(d, lx + 392, y + 154, cap, font(SANS, 13), GRAY, 212, 16)

    # --- right rail ----------------------------------------------------
    rx, rw = 668, RIGHT - 668
    ry = story(d, rx, 258, rw, "NORTH KOREA",
               "KIM ORDERS BIGGER NUCLEAR ARSENAL",
               "Kim Jong Un ordered an expansion of North Korea's nuclear "
               "programme, stressing tactical nuclear weapons, and called "
               "its nuclear status 'irreversible' after ignoring Mr "
               "Trump's offer to meet.",
               h_size=23, b_size=15, leading=19)
    story(d, rx, ry + 22, rw, "STRAIT OF HORMUZ",
          "BLASTS HIT 3 TANKERS IN HORMUZ",
          "A tanker struck a mine and exploded in the strait and two more "
          "were hit by projectiles. Iran's guards fired warning shots at "
          "a U.S. F-16, and a drone attack in Kuwait killed two Italians; "
          "oil neared $97.",
          h_size=23, b_size=15, leading=19)

    # --- bottom rule + grid ---------------------------------------------
    d.line([(MARGIN, 672), (RIGHT, 672)], fill=RULE, width=3)
    cols = [(MARGIN, "storm", "UNITED STATES — WEATHER",
             "STORM DISRUPTS THANKSGIVING",
             "A holiday storm cancelled some 400 flights, delayed 2,000 "
             "more and left 724,000 homes dark; the 100th Macy's parade "
             "was postponed to Saturday."),
            (360, "eu", "EUROPE",
             "EU FAILS TO AGREE €45BN UKRAINE LOAN",
             "EU leaders ended a Brussels summit without agreeing a €45bn "
             "loan for Ukraine's needs next year; 24 states backed it, "
             "but the deal stalled in a fight over the bloc's budget."),
            (684, "satellite", "SPACE",
             "SPACEX CLEARED FOR 1M SATELLITES",
             "U.S. regulators cleared SpaceX to deploy up to one million "
             "satellites as orbital data centres above Earth.")]
    for cx, key, kick, head, body in cols:
        PANELS[key](d, (cx, 684, cx + 304, 748))
        story(d, cx, 754, 304, kick, head, body, h_size=22, b_size=15,
              leading=18)

    # --- ticker ----------------------------------------------------------
    d.rectangle([MARGIN, 934, RIGHT, 982], fill=INK)
    tick = ("ALSO TODAY — TRUMP THREATENS IRAN NUCLEAR SITE · INDONESIA "
            "MINE FLOOD: 13 DEAD · CHESS: GAME 3 DRAWN")
    tf = fit_font(d, tick, SANS_B, 16, RIGHT - MARGIN - 28)
    tw = d.textlength(tick, font=tf)
    d.text(((W - tw) / 2, 949), tick, font=tf, fill=(250, 248, 240))

    foot = ("Compiled from reports by Reuters, AP, AFP, Dawn and The Japan "
            "Times on 27 November 2026 · Panels drawn by program; no "
            "photographs used")
    ff = fit_font(d, foot, SANS, 14, RIGHT - MARGIN)
    tw = d.textlength(foot, font=ff)
    d.text(((W - tw) / 2, 990), foot, font=ff, fill=GRAY)
    return img


def write_image(path):
    build().save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    write_image("entry.png")
