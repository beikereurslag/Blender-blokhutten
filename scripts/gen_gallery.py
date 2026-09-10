# scripts/gen_gallery.py — genereert index.html galerij van alle weekend-renders.
# Scant per scene op v1 / AgX-v2 / alt-hoek en bouwt een nette vergelijk-pagina.
import os
ROOT = r"C:\Users\beike\Documents\Blender-blokhutten"

SCENES = [
    (1, "Camelia Buitenbad", "spa · blue hour", "pilots/Camelia-250x300-300-zijwand/style-hot-tub-premium/camelia_buitenbad", "v2", ""),
    (2, "Camelia Wijnterras", "mediterraan", "pilots/Camelia-250x300-300-zijwand/style-mediterraan/camelia_wijnterras", "v2", ""),
    (3, "Dahlia Tuinkantoor", "modern", "pilots/Dahlia-250x250-300-zijwand/style-modern-urban-cottage/dahlia_tuinkantoor", "gelijk → v2", ""),
    (4, "Dahlia Leeshoek", "scandi", "pilots/Dahlia-250x250-300-zijwand/style-scandi/dahlia_leeshoek", "gelijk", ""),
    (5, "Jasmijn Familietuin", "klassiek", "pilots/Jasmijn-300x250-300-zijwand/style-klassiek-familie/jasmijn_familietuin", "v2", ""),
    (6, "Jasmijn Theehuis", "japandi", "pilots/Jasmijn-300x250-300-zijwand/style-japandi/jasmijn_theehuis", "v2", ""),
    (7, "Lavendel Lavendelveld", "mediterraan · golden hour", "pilots/Lavendel-400x300-400-zijwand/style-mediterraan/lavendel_lavendelveld", "v1", "AgX dempt de golden-hour-warmte → v1"),
    (8, "Lavendel Pluktuin", "boerderij", "pilots/Lavendel-400x300-400-zijwand/style-boerderij/lavendel_pluktuin", "gelijk → v2", ""),
    (9, "Lelie Ochtendnevel", "forest · mist", "pilots/Lelie-400x250-300-zijwand/style-forest-wilderness/lelie_ochtendnevel", "v2 (sterk)", ""),
    (10, "Lelie Avondkubus", "modern · blue hour", "pilots/Lelie-400x250-300-zijwand/style-modern/lelie_avondkubus", "v2", "alt-hoek zwak: voorgrond-struik blokkeert → gebruik hero"),
    (11, "Magnolia Groene Long", "eco-groendak", "pilots/Magnolia-300x200/style-eco-groendak/magnolia_groene_long", "gelijk → v2", "alt-hoek zwak: lage hoek toont sedum-dak niet → gebruik hero"),
    (12, "Magnolia Wintertuin", "scandi", "pilots/Magnolia-300x200/style-scandi/magnolia_wintertuin", "gelijk", ""),
    (13, "Roosmarijn Zentuin", "japanese-zen", "pilots/Roosmarijn-200x300-400-zijwand/style-japanese-zen/roosmarijn_zentuin", "v2", ""),
    (14, "Roosmarijn Kruidenterras", "mediterraan", "pilots/Roosmarijn-200x300-400-zijwand/style-mediterraan/roosmarijn_kruidenterras", "gelijk → v2", ""),
    (15, "Zonnebloem Zomeravond", "boerderij · sunset", "pilots/Zonnebloem-300x300-300-zijwand/style-boerderij/zonnebloem_zomeravond", "v2 (sterk)", ""),
    (16, "Zonnebloem Ochtendhoek", "scandi", "pilots/Zonnebloem-300x300-300-zijwand/style-scandi/zonnebloem_ochtendhoek", "gelijk → v2", ""),
]
VARIANTS = [("v1 — Filmic (hero)", "_FINAL_2560x1440.png"),
            ("v2 — AgX (hero)", "_FINAL_v2_2560x1440.png"),
            ("alt-hoek — lifestyle", "_ANGLE-lifestyle_2560x1440.png")]

def card(label, url, exists, weak):
    if not exists:
        return f'<div class="card missing"><div class="lab">{label}</div><div class="ph">— niet aanwezig —</div></div>'
    badge = '<span class="warn">⚠ zwak</span>' if weak else ''
    return (f'<figure class="card"><div class="lab">{label}{badge}</div>'
            f'<a href="{url}" target="_blank"><img loading="lazy" src="{url}" alt="{label}"></a></figure>')

rows = []
n_ok = 0
for num, title, style, base, advice, note in SCENES:
    cards = []
    for vi, (label, suffix) in enumerate(VARIANTS):
        rel = (base + suffix).replace("\\", "/")
        full = os.path.join(ROOT, rel.replace("/", os.sep))
        ex = os.path.exists(full)
        if ex: n_ok += 1
        weak = (vi == 2 and "alt-hoek zwak" in note)
        cards.append(card(label, rel, ex, weak))
    adv = f'<span class="adv adv-{"v1" if advice.startswith("v1") else "v2" if "v2" in advice else "eq"}">advies: {advice}</span>'
    notehtml = f'<div class="note">{note}</div>' if note else ''
    rows.append(f'''<section class="scene">
      <h2><span class="num">{num:02d}</span> {title} <span class="style">{style}</span> {adv}</h2>
      {notehtml}
      <div class="grid">{''.join(cards)}</div>
    </section>''')

html = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Blokhut-renders · weekend 20–23 jun</title>
<style>
:root{{--bg:#14161a;--card:#1e2228;--line:#2c313a;--txt:#e7e9ee;--mut:#9aa3b2;--v2:#4ea1ff;--v1:#ffb454;--eq:#7a8699;--warn:#ff6b6b}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--txt);font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}}
header{{padding:22px 26px;border-bottom:1px solid var(--line);position:sticky;top:0;background:rgba(20,22,26,.96);backdrop-filter:blur(6px);z-index:5}}
header h1{{margin:0 0 4px;font-size:20px}}
header p{{margin:0;color:var(--mut);font-size:13px}}
.legend{{margin-top:8px;display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--mut)}}
.legend b{{color:var(--txt)}}
main{{padding:18px 26px 80px;max-width:1500px;margin:0 auto}}
.scene{{margin:0 0 30px;border:1px solid var(--line);border-radius:12px;padding:14px 16px;background:var(--card)}}
.scene h2{{margin:0 0 4px;font-size:17px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}}
.num{{color:var(--mut);font-variant-numeric:tabular-nums}}
.style{{color:var(--mut);font-weight:400;font-size:13px}}
.adv{{margin-left:auto;font-size:12px;padding:3px 9px;border-radius:20px;font-weight:600}}
.adv-v2{{background:rgba(78,161,255,.16);color:var(--v2)}}
.adv-v1{{background:rgba(255,180,84,.16);color:var(--v1)}}
.adv-eq{{background:rgba(122,134,153,.18);color:var(--eq)}}
.note{{color:var(--warn);font-size:12.5px;margin:2px 0 10px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}
.card{{margin:0;background:#0e1014;border:1px solid var(--line);border-radius:9px;overflow:hidden}}
.card.missing{{opacity:.5}}
.lab{{padding:7px 10px;font-size:12.5px;color:var(--mut);border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center}}
.warn{{color:var(--warn);font-weight:700;font-size:11px}}
.card img{{display:block;width:100%;height:auto;cursor:zoom-in}}
.ph{{padding:40px 10px;text-align:center;color:var(--mut);font-size:12px}}
</style></head><body>
<header>
  <h1>Blokhut-renders — weekend 20–23 jun 2026</h1>
  <p>16 scenes · per scene: v1 (Filmic) · v2 (AgX) · alt-hoek (lifestyle). Klik een beeld voor volledige 2560×1440. {n_ok} renders gevonden.</p>
  <div class="legend">
    <span><b style="color:var(--v1)">advies v1</b> = Filmic warmer/beter</span>
    <span><b style="color:var(--v2)">advies v2</b> = AgX zachtere highlights</span>
    <span><b style="color:var(--eq)">gelijk</b> = beide prima</span>
    <span><b style="color:var(--warn)">⚠ zwak</b> = liever niet gebruiken</span>
  </div>
</header>
<main>{''.join(rows)}</main>
</body></html>'''

out = os.path.join(ROOT, "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(f"[gallery] {n_ok} renders -> {out}")
