r"""Check every repaired render against the final it is meant to replace.

A good repair changes the cabin walls and nothing else. So for each pair we
report the best-fit alignment shift (must be 0,0 -- anything else means the
framing moved) and how much of the frame actually changed (a few percent; a
large number means the scene itself drifted, not just the planks).

Writes a side-by-side into _plankfix_review/_cmp_<name>.png for eyeballing.

  python scripts/qc_plankfix.py
"""
import os

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(ROOT, "_plankfix_review")
CATS = ["blokhutten-tuinscenes", "blokhutten-stijlen"]


def find_final(name):
    for c in CATS:
        p = os.path.join(ROOT, "ALLE_FINALS", c, name + ".png")
        if os.path.exists(p):
            return p
    return None


def best_shift(a, b, rad=3, step=4):
    A = a[::step, ::step]
    B = b[::step, ::step]
    best = None
    for dy in range(-rad, rad + 1):
        for dx in range(-rad, rad + 1):
            Bs = np.roll(np.roll(B, dy, 0), dx, 1)
            m = np.abs(A[8:-8, 8:-8] - Bs[8:-8, 8:-8]).mean()
            if best is None or m < best[0]:
                best = (m, dy * step, dx * step)
    return best


rows = []
for fn in sorted(os.listdir(REVIEW)):
    if not fn.endswith(".png") or fn.startswith("_"):
        continue
    name = fn[:-4]
    final = find_final(name)
    if not final:
        rows.append((name, "NO FINAL TO COMPARE", "", ""))
        continue

    fi = Image.open(final).convert("RGB")
    ne = Image.open(os.path.join(REVIEW, fn)).convert("RGB")
    if fi.size != ne.size:
        rows.append((name, f"SIZE MISMATCH {fi.size} vs {ne.size}", "", ""))
        continue

    a = np.asarray(fi.convert("L"), dtype=np.float32)
    b = np.asarray(ne.convert("L"), dtype=np.float32)
    resid, dy, dx = best_shift(a, b)
    changed = (np.abs(a - b) > 12).mean() * 100

    if (dy, dx) != (0, 0):
        status = f"FRAMING MOVED dy={dy} dx={dx}"
    elif changed > 12:
        status = f"TOO MUCH CHANGED ({changed:.1f}%)"
    else:
        status = "ok"
    rows.append((name, status, f"{changed:.1f}%", f"dy={dy} dx={dx}"))

    # side by side for the eye
    W = 820
    H = int(W * fi.height / fi.width)
    left = fi.resize((W, H), Image.LANCZOS)
    right = ne.resize((W, H), Image.LANCZOS)
    pad, top = 12, 26
    out = Image.new("RGB", (W * 2 + pad * 3, H + top + pad), (250, 250, 250))
    d = ImageDraw.Draw(out)
    out.paste(left, (pad, top))
    d.text((pad + 4, 7), "NU (huidige final)", fill=(15, 15, 15))
    out.paste(right, (pad * 2 + W, top))
    d.text((pad * 2 + W + 4, 7), "NA FIX", fill=(15, 15, 15))
    out.save(os.path.join(REVIEW, f"_cmp_{name}.png"))

print(f"\n{'scene':30s} {'status':28s} {'changed':>8s}  shift")
print("-" * 80)
bad = 0
for name, status, changed, shift in rows:
    if status != "ok":
        bad += 1
    print(f"{name:30s} {status:28s} {changed:>8s}  {shift}")
print("-" * 80)
print(f"{len(rows)} renders, {bad} need a look")
