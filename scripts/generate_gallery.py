"""Genereer _render_review.html: alle 16 scenes, before (v2) vs after (v3/preview).
De after-img pollt: probeer FINAL_v3 -> REVIEW_PREVIEW -> (fallback) FINAL_v2.
"""
import os
ROOT = r"C:\Users\beike\Documents\Blender-blokhutten"
SC = [
 ("Camelia-250x300-300-zijwand/style-hot-tub-premium","camelia_buitenbad","Camelia Buitenbad"),
 ("Camelia-250x300-300-zijwand/style-mediterraan","camelia_wijnterras","Camelia Wijnterras"),
 ("Dahlia-250x250-300-zijwand/style-modern-urban-cottage","dahlia_tuinkantoor","Dahlia Tuinkantoor"),
 ("Dahlia-250x250-300-zijwand/style-scandi","dahlia_leeshoek","Dahlia Leeshoek"),
 ("Jasmijn-300x250-300-zijwand/style-klassiek-familie","jasmijn_familietuin","Jasmijn Familietuin"),
 ("Jasmijn-300x250-300-zijwand/style-japandi","jasmijn_theehuis","Jasmijn Theehuis"),
 ("Lavendel-400x300-400-zijwand/style-boerderij","lavendel_pluktuin","Lavendel Pluktuin"),
 ("Lavendel-400x300-400-zijwand/style-mediterraan","lavendel_lavendelveld","Lavendel Lavendelveld"),
 ("Lelie-400x250-300-zijwand/style-forest-wilderness","lelie_ochtendnevel","Lelie Ochtendnevel (af)"),
 ("Lelie-400x250-300-zijwand/style-modern","lelie_avondkubus","Lelie Avondkubus (af)"),
 ("Magnolia-300x200/style-eco-groendak","magnolia_groene_long","Magnolia Groene Long (overgeslagen)"),
 ("Magnolia-300x200/style-scandi","magnolia_wintertuin","Magnolia Wintertuin"),
 ("Roosmarijn-200x300-400-zijwand/style-japanese-zen","roosmarijn_zentuin","Roosmarijn Zentuin"),
 ("Roosmarijn-200x300-400-zijwand/style-mediterraan","roosmarijn_kruidenterras","Roosmarijn Kruidenterras"),
 ("Zonnebloem-300x300-300-zijwand/style-boerderij","zonnebloem_zomeravond","Zonnebloem Zomeravond"),
 ("Zonnebloem-300x300-300-zijwand/style-scandi","zonnebloem_ochtendhoek","Zonnebloem Ochtendhoek"),
]
def p(dir_, sc, suf): return f"pilots/{dir_}/{sc}_{suf}"
secs=[]
for i,(d,sc,disp) in enumerate(SC,1):
    before=p(d,sc,"FINAL_v2_2560x1440.png")
    fin=p(d,sc,"FINAL_v3_2560x1440.png"); prev=p(d,sc,"REVIEW_PREVIEW.png")
    secs.append(f'''<section class="scene">
  <h2>{i}. {disp}</h2>
  <div class="row">
    <div class="card"><div class="lbl"><span class="tag-before">BEFORE — v2</span><a class="full" href="{before}" target="_blank">open</a></div>
      <img src="{before}"></div>
    <div class="card"><div class="lbl"><span class="tag-after"><b>AFTER</b> <span class="pill" data-pill>…</span></span><a class="full" href="{fin}" target="_blank">open</a></div>
      <img data-after data-final="{fin}" data-preview="{prev}" data-fallback="{before}"></div>
  </div>
</section>''')
html=f'''<!doctype html><html lang="nl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Blokhut renders — review</title>
<style>:root{{color-scheme:dark}}body{{margin:0;background:#14161a;color:#e7e9ee;font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}}
header{{padding:16px 24px;border-bottom:1px solid #2a2d34;position:sticky;top:0;background:#14161a;z-index:2}}
h1{{margin:0;font-size:18px}}header p{{margin:4px 0 0;color:#9aa0ab;font-size:13px}}
.scene{{padding:16px 24px 4px}}.scene h2{{font-size:15px;margin:0 0 10px;color:#cdd2db;border-left:3px solid #6b9;padding-left:10px}}
.row{{display:flex;flex-wrap:wrap;gap:14px}}.card{{flex:1 1 440px;background:#1c1f25;border:1px solid #2a2d34;border-radius:10px;overflow:hidden}}
.card .lbl{{padding:7px 12px;font-size:12px;color:#aab0bb;border-bottom:1px solid #2a2d34;display:flex;justify-content:space-between;align-items:center}}
.card .lbl b{{color:#fff}}.card img{{width:100%;display:block;background:#000;min-height:60px}}
.tag-after{{color:#7fd6a6}}.tag-before{{color:#d6a17f}}a.full{{color:#7fb6ff;text-decoration:none;font-size:12px}}
.pill{{font-size:11px;padding:2px 7px;border-radius:10px;background:#33373f;color:#cfd4dd;margin-left:8px}}.pill.live{{background:#1f3a2a;color:#7fd6a6}}
footer{{padding:18px 24px;color:#7e848f;font-size:12px}}</style></head><body>
<header><h1>Blokhut renders — review (v2 → v3, grond-fix)</h1>
<p>Before = origineel v2 · After = na grond-fix (pad→steen, blobjes weg, gras groener). Pollt elke 15s; finales/previews verschijnen automatisch.</p></header>
{''.join(secs)}
<footer>python -m http.server 8765 · ververst zichzelf.</footer>
<script>
async function exists(u){{try{{const r=await fetch(u,{{method:'HEAD',cache:'no-store'}});return r.ok}}catch(e){{return false}}}}
async function tick(){{
 for(const img of document.querySelectorAll('img[data-after]')){{
  const fin=img.dataset.final,prev=img.dataset.preview,fb=img.dataset.fallback;
  const pill=img.closest('.card').querySelector('[data-pill]');const b='?t='+Date.now();
  if(await exists(fin)){{img.src=fin+b;if(pill){{pill.textContent='finale v3';pill.classList.add('live')}}}}
  else if(await exists(prev)){{img.src=prev+b;if(pill){{pill.textContent='preview v3';pill.classList.remove('live')}}}}
  else{{img.src=fb;if(pill){{pill.textContent='nog v2';pill.classList.remove('live')}}}}
 }}
}}
tick();setInterval(tick,15000);
</script></body></html>'''
open(os.path.join(ROOT,"_render_review.html"),"w",encoding="utf-8").write(html)
print("gallery generated:", len(SC), "scenes")
