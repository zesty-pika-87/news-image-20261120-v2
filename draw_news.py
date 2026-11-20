#!/usr/bin/env python3
"""Draw the Friday 20 November 2026 front page: 36 verified stories,
13 hand-drawn pictures, a UTC timeline, a numbers ribbon and a date check.

Build-time only. Renders entry.png (1024x1024, deterministic) from the
story list below; nothing here reads any other file. Run: python3 draw_news.py
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (250, 246, 236)
INK = (24, 24, 22)
MUTED = (96, 90, 80)
RULE = (24, 24, 22)
RED = (176, 32, 28)
BLUE = (28, 68, 140)
TEAL = (14, 110, 110)
GOLD = (176, 132, 24)
LIGHT = (232, 226, 214)
SKY = (30, 60, 110)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns list of lines."""
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


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap to max_lines lines; ellipsis-truncate the last line if needed."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    while lines and draw.textlength(lines[-1] + " ...", font=fnt) > max_w:
        lines[-1] = lines[-1][:-1]
    lines[-1] = (lines[-1] + " ...").strip()
    return lines


def centre(draw, x, y, w, text, fnt, fill=INK):
    tw = draw.textlength(text, font=fnt)
    draw.text((x + (w - tw) / 2, y), text, font=fnt, fill=fill)


def hline(draw, x0, x1, y, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- pictures
# Every picture below is drawn from scratch with PIL shapes: no photos,
# no copied art, no external files.

def pic_akvan(w, h):
    """Cyclone spiral over a stylised Bay of Bengal coast."""
    img = Image.new("RGB", (w, h), (196, 222, 232))
    d = ImageDraw.Draw(img)
    d.polygon([(0, h), (0, int(h * 0.42)), (int(w * 0.30), int(h * 0.30)),
               (int(w * 0.52), int(h * 0.52)), (int(w * 0.62), h)],
              fill=(214, 200, 158))
    d.polygon([(int(w * 0.62), h), (int(w * 0.52), int(h * 0.52)),
               (int(w * 0.78), int(h * 0.44)), (w, int(h * 0.55)), (w, h)],
              fill=(206, 190, 146))
    cx, cy = int(w * 0.44), int(h * 0.46)
    for k in range(1, 7):
        r = k * w // 22
        d.arc([cx - r, cy - r, cx + r, cy + r],
              start=40 + k * 55, end=40 + k * 55 + 250,
              fill=(14, 90, 130), width=3)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(176, 32, 28))
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], outline=(176, 32, 28), width=2)
    d.text((8, h - 18), "BAY OF BENGAL", font=font(SANS_B, 11), fill=(28, 68, 110))
    d.text((int(w * 0.60), int(h * 0.30)), "GOPALPUR",
           font=font(SANS_B, 11), fill=(176, 32, 28))
    return img


def pic_kyiv(w, h):
    """Night sky over Kyiv: missile streaks, burning rooftops."""
    img = Image.new("RGB", (w, h), (16, 24, 52))
    d = ImageDraw.Draw(img)
    d.ellipse([int(w * 0.82), 8, int(w * 0.82) + 26, 34], fill=(232, 228, 200))
    for i, (x0, y0, x1, y1) in enumerate([
            (20, 18, 90, 44), (120, 8, 200, 40), (230, 26, 300, 58)]):
        d.line([(x0, y0), (x1, y1)], fill=(255, 210, 90), width=3)
        d.ellipse([x1 - 3, y1 - 3, x1 + 3, y1 + 3], fill=(255, 230, 150))
    for bx, bh in [(0, 46), (52, 62), (118, 40), (172, 70), (238, 50), (292, 58)]:
        d.rectangle([bx, h - bh, bx + 46, h], fill=(8, 10, 26))
        for wy in range(h - bh + 8, h - 6, 14):
            d.rectangle([bx + 8, wy, bx + 14, wy + 7], fill=(255, 190, 80))
    for fx, fr in [(70, 12), (190, 15), (268, 10)]:
        d.ellipse([fx - fr, h - 34 - fr, fx + fr, h - 34 + fr],
                  fill=(255, 120, 30))
        d.ellipse([fx - fr // 2, h - 34 - fr // 2, fx + fr // 2, h - 34 + fr // 2],
                  fill=(255, 200, 60))
    return img


def pic_cop31(w, h):
    """COP31 final day: sun over hills, a row of flags, no deal yet."""
    img = Image.new("RGB", (w, h), (186, 214, 232))
    d = ImageDraw.Draw(img)
    d.ellipse([int(w * 0.45), 6, int(w * 0.45) + 44, 50], fill=(240, 190, 60))
    d.polygon([(0, h), (0, int(h * 0.62)), (int(w * 0.45), int(h * 0.42)),
               (w, int(h * 0.66)), (w, h)], fill=(96, 140, 78))
    d.polygon([(0, h), (0, int(h * 0.78)), (int(w * 0.55), int(h * 0.60)),
               (w, int(h * 0.80)), (w, h)], fill=(62, 110, 58))
    cols = [(176, 32, 28), (28, 68, 140), (14, 110, 110), (176, 132, 24),
            (90, 60, 140)]
    for i, c in enumerate(cols):
        x = 200 + i * 22
        d.line([(x, h - 30), (x, h - 58)], fill=(60, 50, 40), width=2)
        d.polygon([(x, h - 58), (x + 20, h - 53), (x, h - 48)], fill=c)
    d.text((10, 8), "FINAL DAY", font=font(SERIF_B, 17), fill=(24, 40, 60))
    d.text((10, 28), "NO DEAL YET", font=font(SANS_B, 12), fill=(24, 40, 60))
    return img


def mini_canvas(w, h, bg):
    img = Image.new("RGB", (w, h), bg)
    return img, ImageDraw.Draw(img)


def pic_candles(w, h):
    """Anthropic: candlesticks climbing to the $97.17 close."""
    img, d = mini_canvas(w, h, (238, 244, 238))
    base = h - 6
    pts = [(8, base - 2), (28, base - 6), (48, base - 4), (68, base - 14),
           (88, base - 12), (108, base - 22), (128, base - 20),
           (148, base - 30), (168, base - 28)]
    for i, (x, y) in enumerate(pts):
        up = i % 2 == 0
        c = (30, 140, 70) if up else (176, 32, 28)
        d.line([(x + 5, y - 5), (x + 5, y + 10)], fill=c, width=2)
        d.rectangle([x, y, x + 10, y + 7], fill=c)
    d.line([(4, h - 2), (w - 4, 4)], fill=(28, 68, 140), width=2)
    return img


def pic_falling(w, h):
    """US markets: a red line falling five days in a row."""
    img, d = mini_canvas(w, h, (248, 234, 232))
    pts = [(6, 6), (34, 10), (62, 9), (90, 16), (118, 19), (146, 25),
           (174, h - 6)]
    d.line(pts, fill=(176, 32, 28), width=3)
    for x, y in pts:
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(176, 32, 28))
    d.text((8, h - 16), "DAY 5 DOWN", font=font(SANS_B, 11), fill=(176, 32, 28))
    return img


def pic_gta(w, h):
    """GTA VI: sunset skyline with a big VI."""
    img, d = mini_canvas(w, h, (250, 170, 120))
    d.ellipse([int(w * 0.62), 4, int(w * 0.62) + 30, 34], fill=(255, 220, 120))
    for bx, bh in [(0, 30), (30, 44), (66, 26), (96, 52), (134, 34), (164, 46)]:
        d.rectangle([bx, h - bh, bx + 26, h], fill=(40, 24, 60))
    d.text((8, 4), "VI", font=font(SERIF_B, 30), fill=(255, 255, 255))
    d.text((52, h - 16), "99 METACRITIC", font=font(SANS_B, 11), fill=(255, 255, 255))
    return img


def pic_children(w, h):
    """World Children's Day: a globe ringed by small figures."""
    img, d = mini_canvas(w, h, (226, 238, 246))
    cx, cy, r = w // 2, h // 2 + 1, 14
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 160, 210))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(28, 68, 140), width=2)
    d.arc([cx - r, cy - 6, cx + r, cy + 6], 0, 360, fill=(40, 140, 70), width=3)
    for i, fx in enumerate([14, 52, 96, 134, 168]):
        c = [(176, 32, 28), (28, 68, 140), (14, 110, 110), (176, 132, 24),
             (90, 60, 140)][i]
        d.ellipse([fx, h - 18, fx + 8, h - 10], fill=c)
        d.rectangle([fx + 1, h - 10, fx + 7, h - 2], fill=c)
    return img


def pic_flags(w, h):
    """UK-EU summit: Union Jack beside the EU circle of stars."""
    img, d = mini_canvas(w, h, (238, 238, 232))
    d.rectangle([8, 4, 88, 32], fill=(28, 68, 140))
    d.rectangle([8, 16, 88, 21], fill=(255, 255, 255))
    d.rectangle([44, 4, 52, 32], fill=(255, 255, 255))
    d.rectangle([8, 18, 88, 20], fill=(176, 32, 28))
    d.rectangle([46, 4, 50, 32], fill=(176, 32, 28))
    d.rectangle([104, 4, 184, 32], fill=(28, 68, 140))
    for k in range(12):
        a = math.pi * 2 * k / 12 - math.pi / 2
        sx = 144 + int(10 * math.cos(a))
        sy = 18 + int(10 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 210, 60))
    return img


def pic_cricket(w, h):
    """Phillips 118: stumps, bat and ball on a green strip."""
    img, d = mini_canvas(w, h, (232, 242, 220))
    d.rectangle([0, h - 16, w, h], fill=(120, 170, 90))
    d.rectangle([w - 46, 8, w - 8, h - 16], fill=(210, 190, 140))
    for sx in [w - 40, w - 32, w - 24]:
        d.line([(sx, 10), (sx, 20)], fill=(240, 200, 60), width=3)
    d.rectangle([w - 42, 8, w - 22, 11], fill=(240, 200, 60))
    d.line([(30, 32), (62, 12)], fill=(150, 100, 50), width=7)
    d.rectangle([56, 4, 74, 16], fill=(150, 100, 50))
    d.ellipse([84, 26, 94, 36], fill=(176, 32, 28))
    d.text((8, 4), "118", font=font(SERIF_B, 20), fill=(28, 68, 140))
    return img


def pic_senate(w, h):
    """Senate vote: a dome over the 51-48 tally."""
    img, d = mini_canvas(w, h, (238, 238, 244))
    d.rectangle([20, 26, w - 20, 29], fill=(90, 90, 100))
    for cx in range(30, w - 24, 18):
        d.rectangle([cx, 30, cx + 6, h - 4], fill=(90, 90, 100))
    d.pieslice([w // 2 - 30, 0, w // 2 + 30, 30], 180, 360, fill=(120, 120, 135))
    d.rectangle([w // 2 - 3, 0, w // 2 + 3, 5], fill=(120, 120, 135))
    d.text((6, 4), "51-48", font=font(SANS_B, 12), fill=(176, 32, 28))
    return img


def pic_boat(w, h):
    """Migrant boat off Senegal: a small hull on heavy waves."""
    img, d = mini_canvas(w, h, (210, 228, 242))
    d.polygon([(60, 20), (128, 20), (118, 30), (70, 30)], fill=(120, 70, 40))
    d.polygon([(92, 20), (92, 6), (114, 20)], fill=(250, 246, 236))
    d.line([(92, 6), (92, 20)], fill=(60, 50, 40), width=2)
    for wy in [30, 34]:
        for x in range(0, w, 24):
            d.arc([x, wy, x + 24, wy + 8], 0, 180, fill=(28, 68, 140), width=2)
    return img


def pic_strike(w, h):
    """Italy general strike: a red banner across the piazza."""
    img, d = mini_canvas(w, h, (244, 238, 232))
    d.line([(14, 8), (14, h - 6)], fill=(90, 70, 50), width=3)
    d.line([(w - 14, 8), (w - 14, h - 6)], fill=(90, 70, 50), width=3)
    d.rectangle([14, 12, w - 14, 34], fill=(176, 32, 28))
    d.text((20, 16), "SCIOPERO 24H", font=font(SANS_B, 13), fill=(255, 255, 255))
    for i, x in enumerate([30, 80, 130, 170]):
        d.ellipse([x, h - 22, x + 10, h - 12], fill=(40, 40, 44))
        d.rectangle([x + 1, h - 12, x + 9, h - 4], fill=(40, 40, 44))
    return img


def pic_rates(w, h):
    """China rates: a flat line at 3.0% for an 18th month."""
    img, d = mini_canvas(w, h, (238, 244, 238))
    pts = [(8, 26), (40, 26), (72, 26), (104, 26), (136, 26), (168, 26)]
    d.line(pts, fill=(28, 68, 140), width=3)
    for x, y in pts:
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(28, 68, 140))
    d.text((8, 4), "3.0%", font=font(SANS_B, 13), fill=(28, 68, 140))
    d.text((w - 58, 4), "18TH MO.", font=font(SANS_B, 11), fill=(96, 90, 80))
    return img


# ------------------------------------------------------------------- map
# Rough continent outlines in lon/lat; plotted equirectangularly.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 71), (-95, 80), (-80, 73), (-65, 60),
     (-55, 52), (-60, 45), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-117, 32), (-125, 40), (-124, 48), (-135, 58),
     (-155, 58), (-165, 60)],
    [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
     (-58, -38), (-65, -45), (-70, -52), (-73, -40), (-70, -20), (-80, -5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 70),
     (15, 70), (10, 64), (5, 60), (0, 54), (-5, 50), (-9, 43), (-10, 36)],
    [(-6, 35), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12), (51, 10),
     (48, 0), (40, -10), (35, -18), (32, -28), (26, -34), (18, -32),
     (12, -18), (8, -2), (-8, 5), (-15, 10), (-17, 15), (-10, 30)],
    [(30, 62), (40, 68), (60, 70), (80, 73), (100, 77), (120, 73),
     (140, 72), (160, 70), (178, 66), (170, 60), (160, 55), (142, 50),
     (140, 40), (130, 33), (122, 30), (110, 20), (105, 10), (100, 8),
     (95, 15), (90, 22), (85, 19), (80, 10), (75, 8), (70, 20), (60, 25),
     (50, 28), (45, 30), (40, 35), (35, 36), (30, 36)],
    [(114, -22), (114, -32), (124, -33), (135, -35), (140, -38),
     (147, -39), (153, -32), (153, -27), (146, -19), (142, -11),
     (136, -12), (132, -12), (126, -14), (122, -17), (114, -22)],
]

# Story number -> (lon, lat) for the 13 numbered map pins.
PINS = {1: (85, 19), 2: (30, 50), 3: (30, 37), 4: (-122, 37), 5: (-74, 41),
        6: (-80, 26), 7: (6, 46), 8: (4, 51), 9: (175, -41), 10: (-77, 39),
        11: (-17, 15), 12: (12, 42), 13: (116, 40)}
# Small nudges (lon, lat degrees) so clustered pins do not pile up.
NUDGE = {2: (4, 4), 3: (-4, -4), 5: (5, 4), 6: (-5, -3), 8: (-4, 4),
         10: (-4, -4), 12: (3, -3)}


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(196, 222, 236))
    for poly in CONTINENTS:
        pts = [(x0 + (lon + 180) / 360 * w,
                y0 + (90 - lat) / 150 * h) for lon, lat in poly]
        d.polygon(pts, fill=(214, 200, 158), outline=(150, 138, 110))
    for n, (lon, lat) in sorted(PINS.items()):
        dlon, dlat = NUDGE.get(n, (0, 0))
        px = x0 + (lon + dlon + 180) / 360 * w
        py = y0 + (90 - lat - dlat) / 150 * h
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(176, 32, 28),
                  outline=(255, 255, 255), width=1)
        pf = font(SANS_B, 9)
        tw = d.textlength(str(n), font=pf)
        d.text((px - tw / 2, py - 5), str(n), font=pf, fill=(255, 255, 255))


# ------------------------------------------------------------------- data
# One truth table: every figure below is used identically wherever it
# repeats on the page (ribbon, features, grid, map).

FEATURES = [
    ("1", "CYCLONE AKVAN", "Cyclone Akvan strikes the Odisha coast",
     "Landfall near Gopalpur 07:30-08:30 IST; winds 70-80, gusting 90. "
     "Over 300,000 evacuated to 9,341 shelters. (IMD)",
     pic_akvan),
    ("2", "KYIV UNDER FIRE", "Missiles rain on Kyiv overnight",
     "39 missiles, 120+ drones; 3 Dnipro bridges hit. Fires in Obolonskyi, "
     "Podilskyi, Holosiivskyi; blackouts. (Reuters)",
     pic_kyiv),
    ("3", "COP31", "COP31 ends its final day with no deal",
     "Draft: 80 paragraphs, down from 144 - no 'fossil', no $120bn. Africa "
     "wants $120bn/yr by 2035; adaptation $305bn. (Reuters)",
     pic_cop31),
]

MID = [
    ("4", "ANTHROPIC", "Anthropic closes day one up 17%",
     "Close $97.17, reported Friday; opened $111.50.",
     pic_candles),
    ("5", "MARKETS", "US stocks fall for a fifth straight day",
     "S&P -2.02%, Dow -2.19%, Nasdaq -2.25%.",
     pic_falling),
    ("6", "GTA VI", "GTA VI: 24.6m copies on day one",
     "Sensor Tower: ~$2.36bn; Metacritic 99.",
     pic_gta),
    ("7", "CHILDREN", "1 in 4 children now lives in a war zone",
     "589m children in conflict - most since 1990.",
     pic_children),
    ("8", "UK-EU SUMMIT", "Burnham's first UK-EU summit",
     "Food deal £5.1bn/yr; carbon pact £6.5bn.",
     pic_flags),
    ("9", "CRICKET", "Phillips' 118 stuns India in Wellington",
     "NZ 368 all out; Nicholls 175*; Bumrah takes 4.",
     pic_cricket),
    ("10", "SENATE", "Senate rejects Iran war-powers bid",
     "Thu-night vote; reported Friday.",
     pic_senate),
    ("11", "SENEGAL", "Migrant boat sinks off Senegal",
     "4 bodies found; boat carried 50-100 people.",
     pic_boat),
    ("12", "ITALY", "Italy in 24-hour general strike",
     "CGIL protests Meloni's 2027 budget in Rome.",
     pic_strike),
    ("13", "CHINA", "China holds rates for an 18th month",
     "1-year LPR 3.0%, 5-year 3.50%; no change.",
     pic_rates),
]

ALSO_ON = [
    (14, "Genoa airport shut over a drone."),
    (15, "Kharkiv drone hits hospital; 4 hurt."),
    (16, "Houthi missile hits Riyadh PIF tower."),
    (17, "Hormuz: 4 attacks in 96 hours."),
    (18, "Gaza: Israel ends one-day operation."),
    (19, "Europe offers Russia talks on Ukraine."),
    (20, "US sanctions Comancheros."),
    (21, "Trump pardons Pete Rose."),
    (22, "Hippo Fiona dies aged 9 in Cincinnati."),
    (23, "California probes Nvidia on AI chips."),
    (24, "880,000 AI chips cleared for China."),
    (25, "Pochettino takes over Man Utd."),
    (26, "Rakshitha, 19, stuns Chen Yufei."),
    (27, "Jepchirchir banned 3 years over EPO."),
    (28, "Bavuma out; Markram captains."),
    (29, "Quebecor bids C$31bn for Telus."),
    (30, "Japan core inflation hits 2.2%."),
    (31, "Samsung names Choi to lead mobile."),
    (32, "Google adds Mac controls to Gemini."),
    (33, "Broadcom patches vCenter flaw."),
    (34, "Harris meets Macron in Paris."),
    (35, "Dutch summon Russia envoy."),
    (36, "Tonga declares drought emergency."),
]

NUMBERS = [
    ("300,000", "EVACUATED - AKVAN"),
    ("$97.17", "ANTHROPIC CLOSE"),
    ("118", "PHILLIPS CENTURY"),
    ("51-48", "SENATE VOTE"),
    ("$120bn", "CLIMATE DEMAND"),
    ("99", "GTA VI SCORE"),
]

TIMELINE = [
    ("00:16", "Genoa airport closed over a drone"),
    ("00:22", "Phillips century; NZ 317-6 at lunch"),
    ("01:25", "First blasts in Kyiv; missiles inbound"),
    ("02:00-03:00", "Akvan crosses coast near Gopalpur"),
    ("04:22", "Drone hits Kharkiv hospital; 4 hurt"),
    ("05:09", "Genoa flights resume; airport reopens"),
]

DATE_CHECK = [
    "ICJ: Myanmar guilty of genocide, 9-6",
    "Trump-Xi-Putin trilateral, Shenzhen",
    "Anthropic IPO priced at $83",
    "GTA VI midnight unlock",
    "Drone strike on Kyiv embassies",
    "Fiji drought disaster declared",
    "Ex-PM Han Duck-soo acquittal",
    "Crimean Bridge attack",
    "Houthi strike on Riyadh PIF tower",
    "Voyager 1 passes one light-day (18 Nov)",
    "Van Gogh sells for $190.4m",
    "EU's proposed €45bn Ukraine loan",
]

REGIONS = ("EUROPE 9  ·  AMERICAS 11  ·  ASIA-PACIFIC 5  ·  MIDDLE EAST 3  ·  "
           "AFRICA 3  ·  OCEANIA 2  ·  WORLD 3  =  36 STORIES")


# ------------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 18  # side margin

    # Masthead
    centre(d, 0, 2, W, "THE WORLD TODAY", font(SERIF_B, 44))
    centre(d, 0, 48, W, "FRIDAY 20 NOVEMBER 2026", font(SANS_B, 18))
    hline(d, MX, W - MX, 70, width=2)
    centre(d, 0, 74, W, REGIONS, font(SANS_B, 14), fill=MUTED)

    # Numbers ribbon
    y0, y1 = 92, 144
    d.rectangle([MX, y0, W - MX, y1], fill=(24, 24, 22))
    cw = (W - 2 * MX) / 6
    for i, (num, lab) in enumerate(NUMBERS):
        x = MX + i * cw
        centre(d, x, y0 + 3, cw, num, font(SERIF_B, 24), fill=(250, 246, 236))
        centre(d, x, y0 + 33, cw, lab, font(SANS_B, 13),
               fill=(200, 192, 176))
        if i:
            d.line([(x, y0 + 6), (x, y1 - 6)], fill=(90, 86, 76), width=1)

    # Timeline strip
    d.text((MX, 150), "THE DAY IN UTC", font=font(SANS_B, 14), fill=RED)
    hline(d, MX, W - MX, 168, width=1)
    tw = (W - 2 * MX) / 6
    for i, (t, txt) in enumerate(TIMELINE):
        x = MX + i * tw
        d.text((x + 2, 172), t, font=font(SANS_B, 13), fill=RED)
        for j, ln in enumerate(fit_lines(d, txt, font(SANS, 13), tw - 8, 2)):
            d.text((x + 2, 188 + j * 15), ln, font=font(SANS, 13), fill=INK)
    hline(d, MX, W - MX, 220, width=1)

    # Features: 3 columns
    fy = 228
    fw = (W - 2 * MX - 2 * 10) / 3
    for i, (num, kick, head, facts, picfn) in enumerate(FEATURES):
        x = MX + i * (fw + 10)
        d.text((x, fy), num + "  " + kick, font=font(SANS_B, 13), fill=RED)
        img.paste(picfn(int(fw), 76), (int(x), fy + 18))
        hy = fy + 98
        for j, ln in enumerate(fit_lines(d, head, font(SERIF_B, 22), fw, 2)):
            d.text((x, hy + j * 25), ln, font=font(SERIF_B, 22), fill=INK)
        ly = hy + 52
        for ln in fit_lines(d, facts, font(SANS, 15), fw, 3):
            d.text((x, ly), ln, font=font(SANS, 15), fill=INK)
            ly += 17
        if i < 2:
            d.line([(x + fw + 5, fy), (x + fw + 5, fy + 200)],
                   fill=(200, 192, 176), width=1)

    # Mid grid: 5 columns x 2 rows
    gy = 436
    gw = (W - 2 * MX - 4 * 8) / 5
    gh = 140
    for idx, (num, kick, head, fact, picfn) in enumerate(MID):
        r, c = divmod(idx, 5)
        x = MX + c * (gw + 8)
        y = gy + r * gh
        d.text((x, y), num + "  " + kick, font=font(SANS_B, 12), fill=RED)
        img.paste(picfn(int(gw), 36), (int(x), y + 16))
        hy = y + 56
        for j, ln in enumerate(fit_lines(d, head, font(SANS_B, 17), gw, 2)):
            d.text((x, hy + j * 20), ln, font=font(SANS_B, 17), fill=INK)
        ly = hy + 42
        for ln in fit_lines(d, fact, font(SANS, 15), gw, 2):
            d.text((x, ly), ln, font=font(SANS, 15), fill=MUTED)
            ly += 17
        if r == 0:
            hline(d, x, x + gw, y + gh - 6, fill=(200, 192, 176))
    hline(d, MX, W - MX, gy + 2 * gh - 2, width=1)

    # ALSO ON: 3 columns x 8 rows
    ay = 722
    d.text((MX, ay), "ALSO ON", font=font(SANS_B, 14), fill=RED)
    d.text((W - MX - 260, ay), "STORIES 14-36 IN BRIEF", font=font(SANS_B, 12),
           fill=MUTED)
    hline(d, MX, W - MX, ay + 20, width=1)
    aw = (W - 2 * MX - 2 * 16) / 3
    for idx, (num, txt) in enumerate(ALSO_ON):
        c, r = divmod(idx, 8)
        x = MX + c * (aw + 16)
        y = ay + 28 + r * 19
        line = str(num) + ". " + txt
        lines = fit_lines(d, line, font(SANS, 15), aw, 1)
        d.text((x, y), lines[0], font=font(SANS, 15), fill=INK)

    # Bottom row: map + date check
    by = 906
    hline(d, MX, W - MX, by - 4, width=1)
    d.text((MX, by), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill=RED)
    d.text((MX + 316, by), "DATE CHECK - LEFT OUT (FIRST REPORTED 19 NOV)",
           font=font(SANS_B, 13), fill=RED)
    draw_map(d, MX, by + 20, 300, 82)
    dw = (W - MX - (MX + 316)) / 2
    for idx, item in enumerate(DATE_CHECK):
        c, r = divmod(idx, 6)
        x = MX + 316 + c * dw
        y = by + 20 + r * 14
        lines = fit_lines(d, "· " + item, font(SANS, 13), dw - 6, 1)
        d.text((x, y), lines[0], font=font(SANS, 13), fill=INK)

    # Footer
    hline(d, MX, W - MX, 1012, width=1)
    d.text((MX, 1014),
           "Sources: Reuters · IMD · Barron's · Save the Children · The Guardian · "
           "Al Jazeera · PBOC · CGIL · Sensor Tower · Metacritic · AP · AFP",
           font=font(SANS, 10), fill=MUTED)

    img.save(OUT, optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
