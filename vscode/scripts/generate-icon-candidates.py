"""Verdant Meadow Theme - icon candidates.

Generates 6 candidate marks (1024x1024, transparent), a light/dark contact
sheet and an inline strip. Code-drawn only (no AI images), fully re-runnable.

Run from the project root:  py -3 scripts/generate-icon-candidates.py
"""

import io
import math
import os

from PIL import Image, ImageDraw, ImageFont

S = 3                     # supersample factor
W = 1024                  # design canvas (and final size)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "logo-candidates")

INK = (108, 123, 90, 255)      # #6C7B5A  deep olive
MID = (144, 164, 121, 255)     # #90A479
SOFT = (197, 225, 165, 255)    # #C5E1A5
PALE = (228, 241, 214, 255)    # #E4F1D6
CREAM = (242, 247, 236, 255)

LIGHT_BG = (244, 246, 240, 255)
DARK_BG = (30, 36, 31, 255)
LIGHT_INK = (44, 51, 39, 255)
DARK_INK = (228, 241, 214, 255)

FONT_DIR = r"C:\Windows\Fonts"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except Exception:
        return ImageFont.load_default()


def scr(p):
    return (p[0] * S, p[1] * S)


def wd(v):
    return max(1, int(round(v * S)))


def canvas():
    return Image.new("RGBA", (W * S, W * S), (0, 0, 0, 0))


def finish(img):
    return img.resize((W, W), Image.LANCZOS)


def bez(p0, p1, p2, n=64):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1.0 - t
        pts.append((u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
                    u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]))
    return pts


def leaf_poly(base, tip, width, bend=0.0, n=64):
    bx, by = base
    tx, ty = tip
    dx, dy = tx - bx, ty - by
    length = math.hypot(dx, dy)
    nx, ny = -dy / length, dx / length
    cx = (bx + tx) / 2 + nx * bend
    cy = (by + ty) / 2 + ny * bend
    side_a = bez(base, (cx + nx * width, cy + ny * width), tip, n)
    side_b = bez(tip, (cx - nx * width, cy - ny * width), base, n)
    return side_a + side_b[1:]


def ribbon_poly(pts, widths):
    """Closed polygon for a tapered stroke along a centreline."""
    left, right = [], []
    n = len(pts)
    for i, (x, y) in enumerate(pts):
        if i == 0:
            dx, dy = pts[1][0] - x, pts[1][1] - y
        elif i == n - 1:
            dx, dy = x - pts[-2][0], y - pts[-2][1]
        else:
            dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        length = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / length, dx / length
        half = widths[i] / 2.0
        left.append((x + nx * half, y + ny * half))
        right.append((x - nx * half, y - ny * half))
    return left + right[::-1]


def poly(draw, pts, fill):
    draw.polygon([scr(p) for p in pts], fill=fill)


def disc(draw, center, r, fill):
    draw.ellipse([center[0] * S - r * S, center[1] * S - r * S,
                  center[0] * S + r * S, center[1] * S + r * S], fill=fill)


# ---------------------------------------------------------------- candidates

def cand_meadow_horizon():
    img = canvas()
    d = ImageDraw.Draw(img)

    disc(d, (630, 398), 118, MID)

    # far hill
    far = bez((150, 720), (330, 470), (520, 500)) + \
          bez((520, 500), (700, 530), (880, 700))
    poly(d, far + [(880, 800), (150, 800)], MID)

    # near hill
    near = bez((180, 780), (430, 560), (620, 600)) + \
           bez((620, 600), (790, 638), (900, 762))
    poly(d, near + [(900, 860), (180, 860)], INK)

    # two thin furrow strokes on the near hill
    for off in (28, 62):
        arc = bez((260, 800 - off), (520, 700 - off), (790, 800 - off))
        d.line([scr(p) for p in arc], fill=PALE, width=wd(9), joint="curve")

    return finish(img)


def cand_grass_fan():
    img = canvas()
    d = ImageDraw.Draw(img)

    base = (512, 812)
    specs = [(-44, 360, -0.22, INK),
             (-22, 425, -0.10, INK),
             (0, 462, 0.0, MID),
             (22, 425, 0.10, INK),
             (44, 360, 0.22, INK)]

    for angle, length, bend, color in specs:
        rad = math.radians(angle)
        tip = (base[0] + math.sin(rad) * length,
               base[1] - math.cos(rad) * length)
        poly(d, leaf_poly(base, tip, 78, bend * 120), color)

    # ground arc
    ground = bez((232, 806), (512, 862), (792, 806))
    d.line([scr(p) for p in ground], fill=INK, width=wd(30), joint="curve")

    return finish(img)


def cand_butterfly():
    img = canvas()
    d = ImageDraw.Draw(img)

    # upper wings
    poly(d, leaf_poly((512, 512), (268, 300), 150, bend=-26), INK)
    poly(d, leaf_poly((512, 512), (756, 300), 150, bend=26), INK)
    # lower wings
    poly(d, leaf_poly((512, 536), (330, 774), 128, bend=-18), MID)
    poly(d, leaf_poly((512, 536), (694, 774), 128, bend=18), MID)

    # body
    disc(d, (512, 496), 34, INK)
    body = leaf_poly((512, 500), (512, 782), 30, bend=0)
    poly(d, body, INK)

    # antennae
    left = bez((500, 476), (466, 404), (438, 368))
    right = bez((524, 476), (558, 404), (586, 368))
    d.line([scr(p) for p in left], fill=INK, width=wd(16), joint="curve")
    d.line([scr(p) for p in right], fill=INK, width=wd(16), joint="curve")
    disc(d, (438, 364), 20, INK)
    disc(d, (586, 364), 20, INK)

    return finish(img)


def cand_dew_drop():
    img = canvas()
    d = ImageDraw.Draw(img)

    poly(d, leaf_poly((300, 832), (676, 330), 200, bend=92), INK)

    # droplet resting on the leaf tip
    disc(d, (712, 268), 112, MID)
    disc(d, (676, 228), 32, CREAM)

    # small satellite droplet
    disc(d, (596, 486), 26, SOFT)

    return finish(img)


def cand_fern_curl():
    img = canvas()
    d = ImageDraw.Draw(img)

    cx, cy = 572, 448
    steps = 300
    turns = 1.85
    r_out = 268
    ang0 = math.radians(108)
    pts, widths = [], []
    for i in range(steps + 1):
        t = i / steps
        r = r_out * (1 - t) ** 1.15 + 30
        ang = ang0 - t * turns * 2 * math.pi
        pts.append((cx + math.cos(ang) * r, cy + math.sin(ang) * r))
        widths.append(96 * (1 - t) ** 0.8 + 26)

    poly(d, ribbon_poly(pts, widths), INK)

    # short stem from the outer tip down to the baseline
    outer = pts[0]
    stem = bez(outer, (452, 790), (404, 856))
    d.line([scr(p) for p in stem], fill=INK, width=wd(66), joint="curve")

    # a small frond on the stem
    poly(d, leaf_poly((470, 762), (664, 700), 66, bend=16), MID)

    return finish(img)


def cand_dandelion():
    img = canvas()
    d = ImageDraw.Draw(img)

    cx, cy = 512, 424
    rays = 22
    for i in range(rays):
        ang = 2 * math.pi * i / rays
        length = 292 if i % 2 == 0 else 250
        tip = (cx + math.cos(ang) * length, cy + math.sin(ang) * length)
        if tip[1] > cy + 250:
            continue
        d.line([scr((cx + math.cos(ang) * 70, cy + math.sin(ang) * 70)), scr(tip)],
               fill=MID, width=wd(15), joint="curve")
        disc(d, tip, 19, SOFT)

    disc(d, (cx, cy), 62, INK)
    disc(d, (cx, cy), 26, PALE)

    # stem
    stem = bez((cx, cy + 62), (556, 700), (588, 856))
    d.line([scr(p) for p in stem], fill=INK, width=wd(30), joint="curve")

    return finish(img)


CANDIDATES = [
    ("01", "meadow-horizon", cand_meadow_horizon),
    ("02", "grass-fan", cand_grass_fan),
    ("03", "butterfly", cand_butterfly),
    ("04", "dew-drop", cand_dew_drop),
    ("05", "fern-curl", cand_fern_curl),
    ("06", "dandelion", cand_dandelion),
]


# ---------------------------------------------------------------- sheet bits

def centered_text(d, center, text, fnt, fill):
    b = d.textbbox((0, 0), text, font=fnt)
    x = center[0] - (b[2] - b[0]) / 2 - b[0]
    y = center[1] - (b[3] - b[1]) / 2 - b[1]
    d.text((x, y), text, font=fnt, fill=fill)


def contact_sheet(icons, bg, ink, path):
    cell_w, cell_h = 420, 540
    margin, gap = 40, 26
    head = 118
    sheet_w = margin * 2 + cell_w * 3 + gap * 2
    sheet_h = margin + head + cell_h * 2 + gap + margin

    sheet = Image.new("RGBA", (sheet_w, sheet_h), bg)
    d = ImageDraw.Draw(sheet)

    f_title = font("segoeuib.ttf", 40)
    f_num = font("segoeuib.ttf", 30)
    f_name = font("segoeui.ttf", 26)
    f_small = font("segoeui.ttf", 20)

    centered_text(d, (sheet_w / 2, margin + 34), "VERDANT MEADOW THEME", f_title, ink)
    centered_text(d, (sheet_w / 2, margin + 82), "icon candidates", f_small, ink)

    for idx, (num, name, icon) in enumerate(icons):
        row, col = divmod(idx, 3)
        gx = margin + col * (cell_w + gap)
        gy = margin + head + row * (cell_h + gap)

        big = icon.resize((260, 260), Image.LANCZOS)
        sheet.alpha_composite(big, (gx + (cell_w - 260) // 2, gy + 30))

        centered_text(d, (gx + cell_w / 2, gy + 330), num, f_num, ink)
        centered_text(d, (gx + cell_w / 2, gy + 372), name, f_name, ink)
        centered_text(d, (gx + cell_w / 2, gy + 404), "1024 x 1024  PNG", f_small, ink)

        thumb = icon.resize((32, 32), Image.LANCZOS)
        tx, ty = gx + cell_w - 32 - 22, gy + cell_h - 32 - 22
        d.rectangle([tx - 10, ty - 10, tx + 42, ty + 42],
                    outline=(ink[0], ink[1], ink[2], 70), width=1)
        sheet.alpha_composite(thumb, (tx, ty))

    save_png(sheet.convert("RGB"), path)


def inline_strip(icons, path):
    size, gap, margin = 150, 18, 30
    strip_w = margin * 2 + size * len(icons) + gap * (len(icons) - 1)
    strip_h = margin * 2 + size + 34
    strip = Image.new("RGBA", (strip_w, strip_h), LIGHT_BG)
    d = ImageDraw.Draw(strip)
    f_num = font("segoeuib.ttf", 20)

    for idx, (num, _name, icon) in enumerate(icons):
        x = margin + idx * (size + gap)
        strip.alpha_composite(icon.resize((size, size), Image.LANCZOS), (x, margin))
        centered_text(d, (x + size / 2, margin + size + 16), num, f_num, LIGHT_INK)

    save_png(strip.convert("RGB"), path)


def save_png(img, path):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(buf.getvalue())


def main():
    os.makedirs(OUT, exist_ok=True)

    icons = []
    for num, name, fn in CANDIDATES:
        icon = fn()

        box = icon.getbbox()
        if box is None:
            raise AssertionError("%s rendered empty" % name)
        left, top, right, bottom = box
        lo, hi = 70, 954
        if left < lo or top < lo or right > hi or bottom > hi:
            raise AssertionError("%s out of safe area: %s" % (name, box))

        path = os.path.join(OUT, "%s-%s.png" % (num, name))
        save_png(icon, path)
        print("wrote", os.path.relpath(path, ROOT), box)
        icons.append((num, name, icon))

    contact_sheet(icons, LIGHT_BG, LIGHT_INK, os.path.join(OUT, "contact-light.png"))
    contact_sheet(icons, DARK_BG, DARK_INK, os.path.join(OUT, "contact-dark.png"))
    inline_strip(icons, os.path.join(OUT, "inline-strip.png"))
    print("wrote contact-light.png / contact-dark.png / inline-strip.png")


if __name__ == "__main__":
    main()
