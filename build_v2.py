#!/usr/bin/env python3
"""Build v2 newspaper front page for make.fun news-image-20261123.

Fresh generator, written in-session for the v2 entry. Deterministic:
no time, no randomness. PIL only. Output 1024x1024, entry.png + entry.jpg.
All 35 stories are Monday 23 November 2026 (UTC) stories or Monday
follow-ups dated in their decks; weekend developments are never
presented as if they happened on the 23rd.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
V1 = os.path.expanduser("~/workspace/makefun/news-image-20261123/thumbs-ai")

W = H = 1024
NAVY = (16, 28, 58)
RED = (207, 31, 38)
CREAM = (247, 242, 234)
INK = (25, 25, 25)
GREY = (96, 96, 96)
GREEN = (46, 139, 87)
GOLD = (176, 132, 24)
OLIVE = (148, 138, 88)
TAB_COLORS = [(207, 31, 38), (36, 84, 160), (176, 132, 24), (34, 120, 74),
              (110, 62, 150), (20, 130, 138), (16, 28, 58)]

F = "/usr/share/fonts/truetype/liberation/"
SERIF_B = F + "LiberationSerif-Bold.ttf"
SERIF_R = F + "LiberationSerif-Regular.ttf"
SERIF_I = F + "LiberationSerif-Italic.ttf"
SANS_B = F + "LiberationSans-Bold.ttf"
SANS_R = F + "LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, int(size))


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, path, size, max_w, max_lines, min_size=8):
    """Shrink font until text wraps to <= max_lines. Returns (font, lines)."""
    s = size
    while s > min_size:
        fnt = font(path, s)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        s -= 1
    fnt = font(path, min_size)
    return fnt, wrap(draw, text, fnt, max_w)[:max_lines]


def fit_single(draw, text, path, size, max_w, min_size=7):
    """Shrink font until text fits on one line. Returns font."""
    s = size
    while s > min_size:
        fnt = font(path, s)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        s -= 0.5
    return font(path, min_size)


def cover(img, w, h):
    """Cover-crop image to w x h."""
    iw, ih = img.size
    s = max(w / iw, h / ih)
    nw, nh = int(iw * s + 0.5), int(ih * s + 0.5)
    im = img.resize((nw, nh), Image.LANCZOS)
    x, y = (nw - w) // 2, (nh - h) // 2
    return im.crop((x, y, x + w, y + h))


def load_thumb(name):
    if name.startswith("thumb"):
        p = os.path.join(V1, name)
    elif name.startswith("flat"):
        p = os.path.join(HERE, "thumbs2d", name)
    else:
        p = os.path.join(HERE, name)
    return Image.open(p).convert("RGB")


# ---------------------------------------------------------------- data
TICKER = ("HORMUZ: Iran vows all means  \u00b7  KYIV: 12 killed  \u00b7  "
          "WASHINGTON: talks may run to year's end  \u00b7  "
          "ANTALYA: world reacts to COP31 collapse  \u00b7  "
          "GULF: blockade grinds on")

STATS = [("12", "killed in Ukraine strikes"),
         ("22", "shipping attacks in Nov"),
         ("$92.57", "Brent crude"),
         ("24", "dead as Nigeria boat sinks"),
         ("14", "tankers to run US blockade"),
         ("7", "provinces in BMKG rain warning")]

TABS = ["MIDDLE EAST 5", "EUROPE 5", "SE ASIA 5", "EAST ASIA 5",
        "AMERICAS 5", "AFRICA 5", "WORLD 5"]

HEROES = [
    dict(bar="HORMUZ: BLOCKADE DEFIED", badge="23 NOV", badge_c=GREEN,
         tag="2 TANKERS", img="flat01_hormuz.png",
         caption="Tankers ablaze near Hormuz",
         loc="1 HORMUZ \u00b7 MIDDLE EAST \u00b7 WAR",
         head="Iran vows all means to break US blockade",
         deck=("Tehran says it will use every means against US aggression, "
               "after a weekend of tanker hits and drone claims in the Strait.")),
    dict(bar="UKRAINE: STRIKES KILL 12", badge="12 KILLED", badge_c=GREEN,
         tag="CONFIRMED", img="flat02_dymer.png",
         caption="Apartment block hit in Dymer",
         loc="2 DYMER & SLOVIANSK \u00b7 EUROPE \u00b7 WAR",
         head="Russian strikes kill 12 in Kyiv region and Donetsk",
         deck=("Drones and missiles hit an apartment block in Dymer and "
               "Sloviansk; at least 12 dead, dozens hurt.")),
    dict(bar="WASHINGTON: TALKS SIGNAL", badge="23 NOV", badge_c=GOLD,
         tag="REPORTED", img="flat03_whitehouse.png",
         caption="White House, Washington",
         loc="3 WASHINGTON \u00b7 AMERICAS \u00b7 DIPLOMACY",
         head="Trump: Iran talks may run to year's end",
         deck=("President signals talks with Iran could continue until the end "
               "of the year; the war has cost $48.3bn, the Pentagon said last week.")),
]

CARDS = [
    dict(bar="ANTALYA: COP31 FALLOUT", img="flat04_cop31.png",
         loc="ANTALYA, WORLD \u00b7 CLIMATE",
         head="World reacts to COP31 collapse",
         deck=("Talks closed on Sunday with no fossil-fuel deal; capitals trade "
               "blame and look to COP32 in Ethiopia.")),
    dict(bar="RIYADH: AFTER THE STRIKE", img="flat05_piftower.png",
         loc="RIYADH, MIDDLE EAST \u00b7 WAR",
         head="Riyadh counts cost of PIF Tower hit",
         deck=("Thursday's strike blew out windows across eight floors of the "
               "80-storey tower; investors told to leave as the district stays shut.")),
    dict(bar="WASHINGTON: WAR POWERS", img="flat06_senate.png",
         loc="WASHINGTON, AMERICAS \u00b7 POLITICS",
         head="Senate's Iran vote still reverberates",
         deck=("Last Thursday's 51\u201348 rejection of a war-powers curb leaves "
               "Trump free to fight on; Democrats vow to return to it.")),
    dict(bar="THE HAGUE: ICJ FALLOUT", img="flat07_icj.png",
         loc="THE HAGUE, WORLD \u00b7 JUSTICE",
         head="Rohingya press for ICJ ruling to bite",
         deck=("After last Thursday's verdict that Myanmar committed genocide, "
               "survivors and states demand enforcement and returns.")),
    dict(bar="NEW DELHI: VOTER PURGE", img="flat08_ballot.png",
         loc="NEW DELHI, EAST ASIA \u00b7 POLITICS",
         head="Voter-list purge sparks detention fears in India",
         deck=("Muslim residents face detention and deportation threats to "
               "Bangladesh after names vanish from the rolls; youth protests spread.")),
    dict(bar="NIGERIA: BOAT SINKS", img="flat09_boat.png",
         loc="NIGERIA, AFRICA \u00b7 DISASTER",
         head="Funeral boat sinks in Nigeria, 24 dead",
         deck="Vessel carrying a funeral party goes down; at least 24 killed."),
    dict(bar="BRUSSELS: NATO READINESS", img="flat10_nato.png",
         loc="BRUSSELS, EUROPE \u00b7 DEFENCE",
         head="NATO allies lift emergency readiness",
         deck=("Alliance lifts emergency readiness as the Gulf war and Baltic "
               "incidents stretch its forces.")),
    dict(bar="BALTIC: SHIP BURNS", img="flat11_baltic.png",
         loc="BALTIC SEA, EUROPE \u00b7 WAR",
         head="Russian cargo ship burns in the Baltic",
         deck=("Fire engulfs a Russian cargo vessel; cause unclear as Baltic "
               "tensions rise.")),
    dict(bar="WASHINGTON: AI CHIPS", img="flat12_chip.png",
         loc="WASHINGTON, AMERICAS \u00b7 TECH",
         head="US spy chief: China got advanced AI chips",
         deck=("Intelligence says advanced chips reached China despite export "
               "curbs, raising security alarms.")),
    dict(bar="HAITI: HUNGER", img="flat13_haiti.png",
         loc="PORT-AU-PRINCE, AMERICAS \u00b7 AID",
         head="UN warns millions in Haiti face acute hunger",
         deck=("Aid agencies warn millions face acute hunger as gangs choke "
               "food supplies.")),
]

ALSO = [
    (14, "Iran lines up 14 tankers to run US blockade", "Reuters"),
    (15, "Bahrain denies Iran hit US Patriot radars", "Reuters"),
    (16, "Likud\u2013Yashar talks end with no deal", "Reuters"),
    (17, "Berlin youth march against conscription", "dpa"),
    (18, "Indonesian culture fills Nagoya festival", "AP"),
    (19, "Democrats lock in big House majority", "AP"),
    (20, "Mexico catches fugitive Meza Flores; 11 dead", "Reuters"),
    (21, "Russian ship hit by drone at Benghazi port", "Reuters"),
    (22, "Pressure mounts in Sudan to end civil war", "Reuters"),
    (23, "Africa blasts rich nations on energy funding", "AP"),
    (24, "Lagos push for early cleft-lip surgery", "AP"),
    (25, "2026 on track to be one of hottest years", "Reuters"),
    (26, "World silver deficit seen near 35m ounces", "Reuters"),
    (27, "Brent $92.57, WTI $83.41, down 3rd straight week", "Reuters"),
    (28, "Turkey denies hosting 10,000 Rohingya", "Reuters"),
    (29, "BMKG warns of heavy rain in 7 provinces", "AP"),
    (30, "UN OCHA urges MUI to boost disaster funding", "AP"),
    (31, "Singapore, Thailand join supply-chain push", "AP"),
    (32, "Shenzhen trilateral: leaders weigh follow-up", "Reuters"),
    (33, "Verstappen's Vegas win shakes title race", "Reuters"),
    (34, "Pope Leo XIV hosts 100 cycling champions", "Reuters"),
    (35, "Pro-Hasina protests rock Bangladesh again", "Reuters"),
]

# lon, lat, (dx, dy) nudge in px for the map pins
# nudges keep the crowded clusters readable: Washington x3, Hague/Brussels,
# Baltic/Dymer, and the Hormuz/Riyadh/Delhi triangle.
PINS = [(56.5, 26.5, 10, -12), (30.5, 50.8, 14, -2), (-77.0, 38.9, 0, -4),
        (30.7, 36.9, 0, 0), (46.7, 24.7, -10, 10), (-77.0, 38.9, -18, 14),
        (4.3, 52.1, -16, -12), (77.2, 28.6, 14, 10), (6.5, 9.5, 0, 0),
        (4.35, 50.85, -16, 10), (19.0, 57.0, 12, -12), (-77.0, 38.9, 17, 14),
        (-72.3, 18.5, 0, 6)]

DATE_CHECK = ("Every main story on this page happened, or was first reported, "
              "on Monday 23 November 2026 (UTC). Weekend developments appear "
              "only as Monday follow-ups, dated in their decks. Figures are as "
              "reported by the wires at press time; developing stories may "
              "since have moved on.")

# Rough continent polygons (lon, lat) for the dotted world map.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80), (-85, 70),
     (-75, 62), (-65, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 25),
     (-85, 20), (-90, 15), (-95, 18), (-105, 20), (-110, 23), (-120, 32),
     (-125, 40), (-130, 55), (-150, 60)],
    # South America
    [(-80, 10), (-75, 5), (-60, 0), (-50, 0), (-40, -5), (-35, -10),
     (-40, -20), (-48, -28), (-55, -35), (-65, -40), (-70, -50),
     (-73, -40), (-72, -20), (-78, -5)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 70), (40, 68),
     (45, 60), (40, 50), (35, 45), (30, 42), (28, 40), (23, 36),
     (19, 40), (15, 38), (12, 44), (8, 44), (3, 43), (-2, 37)],
    # Africa
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
     (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20),
     (32, -28), (25, -34), (18, -35), (15, -27), (12, -18), (9, -1),
     (9, 4), (-8, 4), (-13, 8)],
    # Asia
    [(30, 70), (40, 68), (55, 70), (70, 72), (90, 75), (110, 74),
     (130, 72), (150, 70), (170, 66), (178, 65), (162, 60), (158, 52),
     (142, 50), (140, 40), (135, 35), (127, 33), (122, 38), (120, 30),
     (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20),
     (80, 8), (77, 8), (72, 20), (66, 25), (60, 25), (55, 28),
     (50, 30), (48, 30), (43, 35), (36, 36), (30, 42)],
    # SE Asia islands
    [(95, 5), (105, 0), (110, -5), (115, -8), (120, -10), (130, -5),
     (135, 0), (140, -5), (140, 2), (130, 5), (120, 8), (105, 10)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32),
     (137, -35), (140, -38), (145, -38), (150, -37), (153, -27),
     (150, -22), (146, -19), (142, -11), (136, -12), (132, -11),
     (126, -14), (122, -17), (118, -20)],
    # New Zealand
    [(167, -45), (170, -42), (174, -39), (178, -38), (175, -41),
     (172, -43), (168, -47)],
]


def point_in_poly(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > lat) != (yj > lat)):
            xint = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < xint:
                inside = not inside
        j = i
    return inside


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---- top navy bar
    d.rectangle([0, 0, W, 27], fill=NAVY)
    f = font(SANS_B, 13)
    d.text((14, 6), "THE WORLD IN ONE DAY", font=f, fill="white")
    f2 = font(SANS_B, 9)
    right = "35 STORIES \u00b7 7 REGIONS \u00b7 ALL FROM THIS ONE DAY \u00b7 PRESS TIME 09:45 UTC"
    d.text((W - 14 - d.textlength(right, font=f2), 8), right, font=f2, fill="white")

    # ---- masthead
    f = font(SERIF_B, 54)
    t = "Monday 23 November 2026"
    d.text(((W - d.textlength(t, font=f)) / 2, 30), t, font=f, fill=NAVY)

    # ---- ticker (fit to the page width, never clipped)
    tf = fit_single(d, TICKER, SERIF_I, 15, W - 28)
    d.text(((W - d.textlength(TICKER, font=tf)) / 2, 88), TICKER, font=tf, fill=RED)

    # ---- stats row
    d.line([14, 106, W - 14, 106], fill=(200, 190, 175), width=1)
    d.line([14, 140, W - 14, 140], fill=(200, 190, 175), width=1)
    cw = 996 / 6
    for i, (num, lab) in enumerate(STATS):
        cx = 14 + cw * i + cw / 2
        f = font(SERIF_B, 23)
        d.text((cx - d.textlength(num, font=f) / 2, 108), num, font=f, fill=RED)
        f2 = font(SANS_R, 9)
        d.text((cx - d.textlength(lab, font=f2) / 2, 131), lab, font=f2, fill=GREY)
        if i:
            x = 14 + cw * i
            d.line([x, 110, x, 136], fill=(200, 190, 175), width=1)

    # ---- region tabs
    tw = 996 / 7
    for i, tab in enumerate(TABS):
        x0 = 14 + tw * i
        d.rectangle([x0, 142, x0 + tw - 2, 158], fill=TAB_COLORS[i])
        f = font(SANS_B, 10)
        d.text((x0 + (tw - 2) / 2 - d.textlength(tab, font=f) / 2, 145),
               tab, font=f, fill="white")

    # ---- heroes
    hx = [14, 350, 686]
    HW = 324
    for col, h in enumerate(HEROES):
        x = hx[col]
        # red bar
        d.rectangle([x, 160, x + HW, 176], fill=RED)
        f = font(SANS_B, 11)
        d.text((x + 8, 163), h["bar"], font=f, fill="white")
        # image
        im = cover(load_thumb(h["img"]), HW, 130)
        img.paste(im, (x, 176))
        # badge + tag pills, top-right stacked
        for j, (txt, colr) in enumerate([(h["badge"], h["badge_c"]),
                                         (h["tag"], NAVY)]):
            pf = font(SANS_B, 9)
            twd = d.textlength(txt, font=pf) + 12
            px = x + HW - 6 - twd
            py = 180 + j * 20
            d.rounded_rectangle([px, py, px + twd, py + 15], radius=7, fill=colr)
            d.text((px + 6, py + 2), txt, font=pf, fill="white")
        # caption
        f = font(SERIF_I, 11)
        d.text((x, 308), h["caption"], font=f, fill=GREY)
        # location
        f = font(SANS_B, 10)
        d.text((x, 322), h["loc"], font=f, fill=RED)
        # headline (serif bold, up to 3 lines)
        hf, lines = fit_lines(d, h["head"], SERIF_B, 19, HW, 3)
        y = 336
        for ln in lines:
            d.text((x, y), ln, font=hf, fill=INK)
            y += int(hf.size * 1.08)
        # deck
        df, dlines = fit_lines(d, h["deck"], SANS_R, 11, HW, 3)
        y = max(y + 2, 372)
        for ln in dlines:
            d.text((x, y), ln, font=df, fill=INK)
            y += 13

    # ---- small cards, two rows of five (164 px tall so 3-line decks fit)
    rows_y = [408, 578]
    CARD_H = 164
    CW2 = 192
    for ri, y0 in enumerate(rows_y):
        for ci in range(5):
            c = CARDS[ri * 5 + ci]
            x = 14 + ci * 201
            im = cover(load_thumb(c["img"]), CW2, 56)
            img.paste(im, (x, y0))
            d.rectangle([x, y0 + 56, x + CW2, y0 + 71], fill=RED)
            bf = fit_single(d, c["bar"], SANS_B, 8.5, CW2 - 8)
            d.text((x + 4, y0 + 59), c["bar"], font=bf, fill="white")
            lf = fit_single(d, c["loc"], SANS_B, 7.5, CW2)
            d.text((x, y0 + 74), c["loc"], font=lf, fill=RED)
            hf, lines = fit_lines(d, c["head"], SERIF_B, 13, CW2, 3)
            y = y0 + 86
            for ln in lines:
                d.text((x, y), ln, font=hf, fill=INK)
                y += 15
            # deck: 3 lines when the headline took 2, else 2 lines;
            # font shrinks (never below 8) so no sentence is cut mid-way
            max_dl = 3 if len(lines) <= 2 else 2
            df, dlines = fit_lines(d, c["deck"], SANS_R, 9.5, CW2, max_dl)
            for ln in dlines:
                d.text((x, y), ln, font=df, fill=INK)
                y += 12
            assert y <= y0 + CARD_H + 1, (c["bar"], y - y0)

    # ---- bottom: map + also list
    d.text((14, 748), "WHERE IT HAPPENED", font=font(SANS_B, 11), fill=INK)
    f = font(SERIF_I, 9)
    d.text((150, 750), "pins match story numbers", font=f, fill=GREY)
    d.text((340, 748), "22 MORE STORIES \u00b7 MONDAY 23 NOVEMBER",
           font=font(SANS_B, 12), fill=INK)
    d.line([14, 764, W - 14, 764], fill=INK, width=1)

    # dotted map, x 14..330, y 768..920
    mx0, my0, mx1, my1 = 14, 768, 330, 920
    mw, mh = mx1 - mx0, my1 - my0
    step = 6
    for gy in range(my0, my1, step):
        for gx in range(mx0, mx1, step):
            lon = (gx - mx0) / mw * 360 - 180
            lat = 84 - (gy - my0) / mh * 142
            if any(point_in_poly(lon, lat, p) for p in CONTINENTS):
                d.ellipse([gx - 1.6, gy - 1.6, gx + 1.6, gy + 1.6], fill=OLIVE)
    # pins
    nf = font(SANS_B, 8)
    for i, (lon, lat, dx, dy) in enumerate(PINS, start=1):
        px = mx0 + (lon + 180) / 360 * mw + dx
        py = my0 + (84 - lat) / 142 * mh + dy
        px = min(max(px, mx0 + 9), mx1 - 9)
        py = min(max(py, my0 + 9), my1 - 9)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline="white", width=1)
        s = str(i)
        d.text((px - d.textlength(s, font=nf) / 2, py - 6), s,
               font=nf, fill="white")

    # also list, two columns of 11
    lf = font(SANS_R, 9)
    bf = font(SANS_B, 9)
    gf = font(SANS_R, 9)
    for k, (num, txt, src) in enumerate(ALSO):
        col = k // 11
        row = k % 11
        x = 340 + col * 340
        y = 768 + row * 13.8
        ns = str(num) + "."
        d.text((x, y), ns, font=bf, fill=RED)
        tx = x + d.textlength(ns, font=bf) + 4
        full = txt + " "
        # shrink only if needed to keep one line
        tf = lf
        while d.textlength(full + src, font=tf) > (1010 if col else 670) - tx and tf.size > 7:
            tf = font(SANS_R, tf.size - 0.5)
        d.text((tx, y), full, font=tf, fill=INK)
        sx = tx + d.textlength(full, font=tf)
        d.text((sx, y), src, font=gf, fill=GREY)

    # ---- date check box
    d.rectangle([14, 926, W - 14, 968], outline=RED, width=2)
    d.text((24, 936), "DATE CHECK", font=font(SANS_B, 13), fill=RED)
    tf = font(SANS_R, 10.5)
    lines = wrap(d, DATE_CHECK, tf, W - 14 - 150)
    y = 930
    for ln in lines:
        d.text((150, y), ln, font=tf, fill=INK)
        y += 13

    # ---- sources line
    d.text((14, 972), "Sources: Reuters, AP, AFP.",
           font=font(SANS_R, 9), fill=GREY)
    rt = "Scenes are drawn illustrations \u00b7 wires read to 09:45 UTC"
    f = font(SANS_R, 9)
    d.text((W - 14 - d.textlength(rt, font=f), 972), rt, font=f, fill=GREY)

    # ---- footer bar
    d.rectangle([0, 992, W, H], fill=NAVY)
    d.text((14, 1002), "THE WORLD IN ONE DAY", font=font(SANS_B, 11), fill="white")
    rt = "MONDAY 23 NOVEMBER 2026 \u00b7 ONE PAGE"
    f = font(SANS_B, 9)
    d.text((W - 14 - d.textlength(rt, font=f), 1004), rt, font=f, fill="white")

    return img


def main():
    img = build()
    png_path = os.path.join(HERE, "entry.png")
    jpg_path = os.path.join(HERE, "entry.jpg")
    img.save(png_path, optimize=True, compress_level=9)
    img.save(jpg_path, quality=88, optimize=True)
    print("png", os.path.getsize(png_path))
    print("jpg", os.path.getsize(jpg_path))


if __name__ == "__main__":
    main()
