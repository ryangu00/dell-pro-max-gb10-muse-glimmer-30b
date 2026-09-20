#!/usr/bin/env python3
"""Draw the repo banner. Pure PIL, no generated imagery — house style.

Concept: Muse Glimmer 30B deployed in NVFP4 on one Dell Pro Max with GB10.
Left = wordmark. Right = three stacked tier slabs (WEIGHTS / DRAFT / KV POOL)
with 01/02/03 annotations, a dashed down-flow and a single orange up-arrow:
the DFlash draft path this cookbook measures.

Run: `pip install Pillow` then `python3 docs/make_banner.py`.
Note: the hardcoded font paths (/System/Library/Fonts/HelveticaNeue.ttc,
/System/Library/Fonts/Menlo.ttc) are macOS system fonts. On a host without
those exact fonts the loader below silently falls back to Pillow's default
bitmap font (ImageFont.load_default()), which does not preserve the requested
sizes; for a banner byte-for-byte identical to docs/assets/banner.png, run on a
host with those fonts, or substitute your own TrueType paths.
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 640
BG = (10, 10, 10)
WHITE = (245, 245, 245)
GREY = (140, 140, 140)
DIM = (70, 70, 70)
ORANGE = (255, 122, 26)
OUT = pathlib.Path(__file__).resolve().parents[1] / "docs/assets/banner.png"

HN = "/System/Library/Fonts/HelveticaNeue.ttc"
MENLO = "/System/Library/Fonts/Menlo.ttc"

def font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default()

f_title = font(HN, 88, 7)     # Light
f_tag = font(HN, 30, 7)
f_mono = font(MENLO, 17)
f_label = font(MENLO, 15)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# crosshair corners
for cx, cy in ((40, 40), (W - 40, H - 40)):
    d.line([(cx - 11, cy), (cx + 11, cy)], fill=DIM, width=1)
    d.line([(cx, cy - 11), (cx, cy + 11)], fill=DIM, width=1)

# 5x3 dot lattices
for ox, oy in ((72, 78), (1150, 536)):
    for r in range(3):
        for c in range(5):
            x, y = ox + c * 15, oy + r * 12
            d.ellipse([x, y, x + 1.6, y + 1.6], fill=DIM)

# wordmark
d.text((80, 196), "MUSE GLIMMER", font=f_title, fill=WHITE)
d.text((80, 288), "30B · NVFP4", font=f_title, fill=WHITE)
d.text((82, 414), "Muse Glimmer 30B in NVFP4 on one Dell Pro Max with GB10.", font=f_tag, fill=WHITE)
d.text((82, 462), "vLLM · DFLASH DRAFT k=15 · NEGATIVE RESULT · MEASURED ON DELL PRO MAX WITH GB10", font=f_mono, fill=GREY)

# right: three tiers as slabs (isometric-ish parallelograms), stacked
SX, SY = 860, 150
tiers = [("WEIGHTS  25.4 GB", "01"), ("DRAFT  5.1 GB", "02"), ("KV POOL  2.8M", "03")]
slab_w, slab_h, skew, gap = 260, 58, 42, 52
boxes = []
for i, (name, num) in enumerate(tiers):
    y = SY + i * (slab_h + gap)
    poly = [(SX + skew, y), (SX + skew + slab_w, y), (SX + slab_w, y + slab_h), (SX, y + slab_h)]
    d.polygon(poly, outline=(96, 96, 96), width=1)
    d.text((SX + skew + 14, y + 18), name, font=f_label, fill=GREY)
    d.text((SX + skew + slab_w + 16, y + 20), num, font=f_label, fill=DIM)
    boxes.append(y)

# dashed down-flow (offload) on the left edge of the stack
def dashed(p0, p1, dash=6, gap_=6, fill=DIM):
    x0, y0 = p0; x1, y1 = p1
    L = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    n = int(L // (dash + gap_))
    for k in range(n):
        t0 = k * (dash + gap_) / L; t1 = (k * (dash + gap_) + dash) / L
        d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0), (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)], fill=fill, width=1)

lx = SX + 20
dashed((lx, boxes[0] + slab_h), (lx, boxes[1]))
dashed((lx, boxes[1] + slab_h), (lx, boxes[2]))
d.text((lx - 70, boxes[1] - 30), "stack flow", font=f_label, fill=DIM)

# the single orange draft arrow: DFlash draft back up to the decode path
rx = SX + skew + slab_w - 30
top, bot = boxes[0] + slab_h + 6, boxes[2] - 6
d.line([(rx, bot), (rx, top)], fill=ORANGE, width=2)
d.polygon([(rx, top - 2), (rx - 6, top + 10), (rx + 6, top + 10)], fill=ORANGE)
d.ellipse([rx - 5, bot - 5, rx + 5, bot + 5], fill=ORANGE)
d.text((rx + 14, (top + bot) // 2 - 8), "DFLASH k=15", font=f_label, fill=ORANGE)

# footer rule + labels
d.line([(80, 560), (W - 80, 560)], fill=(40, 40, 40), width=1)
d.text((80, 576), "RYANAI LAB", font=f_label, fill=GREY)
d.text((W - 80 - 250, 576), "DELL PRO MAX WITH GB10", font=f_label, fill=GREY)

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT)
print("wrote", OUT)
