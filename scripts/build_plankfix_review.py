r"""Build a review page for the plank repair.

Two sections:
  VERVANGEN - the finals that were replaced. Before = the backup, after = what
              is now in ALLE_FINALS. Only the walls should differ.
  R4-STIJLEN - comparison only. Left is the approved final, right is the R4 blend
              with the repair. These blends moved on after the final was made, so
              the whole picture differs, not just the planks. Nothing replaced.

Click an image to flip between before and after.

  python scripts/build_plankfix_review.py
"""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(ROOT, "_plankfix_review")
WEB = os.path.join(REVIEW, "_web")
BACKUP = os.path.join(ROOT, "ALLE_FINALS", "_pre_plankfix_backup")
CATS = ["blokhutten-tuinscenes", "blokhutten-stijlen"]
THUMB_W = 1100

os.makedirs(WEB, exist_ok=True)


def thumb(src, tag):
    out = os.path.join(WEB, f"{tag}.jpg")
    if not os.path.exists(out):
        im = Image.open(src).convert("RGB")
        h = int(THUMB_W * im.height / im.width)
        im.resize((THUMB_W, h), Image.LANCZOS).save(out, quality=88)
    return f"_web/{tag}.jpg"


def find_final(name):
    for c in CATS:
        p = os.path.join(ROOT, "ALLE_FINALS", c, name + ".png")
        if os.path.exists(p):
            return p
    return None


pairs = []          # (section, name, before_src, after_src)

for fn in sorted(os.listdir(BACKUP)) if os.path.isdir(BACKUP) else []:
    if not fn.endswith(".png"):
        continue
    name = fn[:-4]
    after = find_final(name)
    if after:
        pairs.append(("vervangen", name, os.path.join(BACKUP, fn), after))

r4dir = os.path.join(REVIEW, "_r4")
if os.path.isdir(r4dir):
    for fn in sorted(os.listdir(r4dir)):
        if not fn.endswith(".png"):
            continue
        name = fn[:-4]
        before = find_final(name)
        if before:
            pairs.append(("r4", name, before, os.path.join(r4dir, fn)))

cards = {"vervangen": [], "r4": []}
for section, name, before, after in pairs:
    b = thumb(before, f"{section}_{name}_a")
    a = thumb(after, f"{section}_{name}_b")
    cards[section].append(
        f'<figure class="card"><figcaption>{name}</figcaption>'
        f'<div class="cmp" onclick="this.classList.toggle(\'on\')">'
        f'<img class="a" src="{b}" loading="lazy">'
        f'<img class="b" src="{a}" loading="lazy">'
        f'<span class="tag">klik om te wisselen</span></div></figure>'
    )

html = f"""<!doctype html><meta charset="utf-8">
<title>Plankfix review</title>
<style>
 body{{font:15px/1.5 system-ui,sans-serif;margin:0;background:#14150f;color:#e9e9e2}}
 header{{padding:22px 28px;background:#3d4a1c}}
 h1{{margin:0 0 4px;font-size:20px}} h2{{margin:32px 28px 8px;font-size:17px}}
 p.note{{margin:4px 28px 0;color:#c9c9b8;max-width:70ch}}
 .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(520px,1fr));gap:18px;padding:16px 28px 40px}}
 .card{{margin:0;background:#1e1f18;border-radius:8px;overflow:hidden}}
 figcaption{{padding:9px 12px;font-weight:600;background:#262719}}
 .cmp{{position:relative;cursor:pointer;line-height:0}}
 .cmp img{{width:100%;display:block}}
 .cmp .b{{position:absolute;inset:0;opacity:0;transition:opacity .12s}}
 .cmp.on .b{{opacity:1}}
 .tag{{position:absolute;left:10px;bottom:10px;background:rgba(0,0,0,.66);
       padding:3px 9px;border-radius:4px;font-size:12px;line-height:1.5}}
 .cmp.on .tag::after{{content:" - NA FIX"}}
 .cmp .tag::after{{content:" - NU"}}
</style>
<header>
 <h1>Plankfix review</h1>
 <div>Wandplanken uitgelijnd op een raster + plankgroef. Klik op een beeld om te wisselen.</div>
</header>

<h2>Vervangen in ALLE_FINALS ({len(cards['vervangen'])})</h2>
<p class="note">Links het oude beeld (staat als backup in
 <code>ALLE_FINALS/_pre_plankfix_backup/</code>), rechts wat er nu staat.
 Uitsnede en licht zijn identiek - alleen de wanden veranderen.</p>
<div class="grid">{''.join(cards['vervangen'])}</div>

<h2>R4-stijlen - alleen ter vergelijking ({len(cards['r4'])})</h2>
<p class="note">Deze blends zijn ná de goedgekeurde final doorgeschoven, dus hier
 verandert het hele beeld en niet alleen de planken. Er is niets vervangen -
 links staat nog steeds de goedgekeurde final.</p>
<div class="grid">{''.join(cards['r4'])}</div>
"""

out = os.path.join(REVIEW, "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(f"wrote {out}")
print(f"  vervangen: {len(cards['vervangen'])}   r4: {len(cards['r4'])}")
