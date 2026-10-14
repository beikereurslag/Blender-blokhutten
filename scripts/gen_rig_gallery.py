"""Bouw _rig_review.html: alle 15 A-E rig-renders + per-scene notitie (staat + resterend)."""
S = [
 ("Lelie Ochtendnevel","Lelie-400x250-300-zijwand/style-forest-wilderness/lelie_ochtendnevel","~8 · dageraadmist neutraal (roze weg), warm verlicht hout, weide+klaprozen. Rest: minors."),
 ("Lavendel Pluktuin","Lavendel-400x300-400-zijwand/style-boerderij/lavendel_pluktuin","~7.5 · zachte overcast, rijke border. Rest: overkapping-dressing."),
 ("Magnolia Wintertuin","Magnolia-300x200/style-scandi/magnolia_wintertuin","~7 · v5-basis (deck+potten), overcast+gras. Rest: subtiele warme key-light."),
 ("Dahlia Tuinkantoor","Dahlia-250x250-300-zijwand/style-modern-urban-cottage/dahlia_tuinkantoor","~7 · warme ochtend, verlichte overkapping, two-tone hout. Rest: bureau/kantoor-props (concept)."),
 ("Camelia Buitenbad","Camelia-250x300-300-zijwand/style-hot-tub-premium/camelia_buitenbad","~7 · blue-hour spa, warme bollards. Rest: hottub-water donker, lounge onder overkapping."),
 ("Jasmijn Familietuin","Jasmijn-300x250-300-zijwand/style-klassiek-familie/jasmijn_familietuin","~6.5 · gericht middaglicht+schaduwen, lush gras, hortensia's. Rest: zandbak-speelgoed (concept)."),
 ("Magnolia Groene Long","Magnolia-300x200/style-eco-groendak/magnolia_groene_long","~6.5 · warm helder, sedum groen, regenton. Rest: dakrand/zonnepaneel-detail nog iets los."),
 ("Zonnebloem Zomeravond","Zonnebloem-300x300-300-zijwand/style-boerderij/zonnebloem_zomeravond","~6.5 · sunset, festoon, geen natte-grasplas meer. Rest: tafel dekken (borden/glazen)."),
 ("Roosmarijn Kruidenterras","Roosmarijn-200x300-400-zijwand/style-mediterraan/roosmarijn_kruidenterras","~6.5 · v5-basis (festoon+shrubs+tafelset), warm namiddag, hout warmer. Rest: kruid-instances gronden, kook-props."),
 ("Camelia Wijnterras","Camelia-250x300-300-zijwand/style-mediterraan/camelia_wijnterras","~6 · warm namiddag, hout warmer (was wit). Rest: interieur onder afdak nog wat donker."),
 ("Jasmijn Theehuis","Jasmijn-300x250-300-zijwand/style-japandi/jasmijn_theehuis","~6 · warm ochtend, grind. Rest: theeset (concept), lantaarn-glas."),
 ("Dahlia Leeshoek","Dahlia-250x250-300-zijwand/style-scandi/dahlia_leeshoek","~6 · zachte ochtend, zwevende proxy-blobs weg. Rest: leeshoek-dressing warmer."),
 ("Lelie Avondkubus","Lelie-400x250-300-zijwand/style-modern/lelie_avondkubus","~6 · blue-hour, glas transparant + gloed door deur. Rest: kubus mag sterker gloeien (beacon)."),
 ("Zonnebloem Ochtendhoek","Zonnebloem-300x300-300-zijwand/style-scandi/zonnebloem_ochtendhoek","~6 · ochtend, loungeset, zwevende plaid-proxy weg. Rest: minors."),
 ("Lavendel Lavendelveld","Lavendel-400x300-400-zijwand/style-mediterraan/lavendel_lavendelveld","~6 · golden-hour, verborgen lavendel nu zichtbaar. Rest: lavendel meer als vol veld."),
]
def card(t, base, note):
    r = f"pilots/{base}_RIG_PREVIEW.png"
    return (f'<div class="card"><div class="lbl"><b>{t}</b><a class="full" href="{r}" target="_blank">open</a></div>'
            f'<img src="{r}"><div class="note">{note}</div></div>')
html = """<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Blokhut — rig-ronde (A-E)</title><style>:root{color-scheme:dark}body{margin:0;background:#14161a;color:#e7e9ee;font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}
header{padding:16px 24px;border-bottom:1px solid #2a2d34}h1{margin:0;font-size:18px}header p{margin:4px 0 0;color:#9aa0ab;font-size:13px}
.grid{display:flex;flex-wrap:wrap;gap:16px;padding:18px 24px}.card{flex:1 1 460px;max-width:640px;background:#1c1f25;border:1px solid #2a2d34;border-radius:10px;overflow:hidden}
.card .lbl{padding:8px 12px;display:flex;justify-content:space-between;color:#cdd2db}.card img{width:100%;display:block;background:#000}
.note{padding:8px 12px;color:#9aa0ab;font-size:12px}a.full{color:#7fb6ff;text-decoration:none;font-size:12px}footer{padding:18px 24px;color:#7e848f;font-size:12px}</style></head><body>
<header><h1>Blokhut-lijn — rig-ronde A–E (gesorteerd: sterkste bovenaan)</h1>
<p>Gedeelde rigs toegepast op 15 scenes (Zentuin = jouw eigen). A licht(+HDRI per moment)/B gras/C hout-nerf+warm/E overkapping-fill, daarna review + polish (junk weg, lavendelveld zichtbaar, magnolia dak, lelie glas). "Rest:" = wat ik bewust voor jouw oog liet. v3/v4/v5-bronnen intact; nieuw = _RIG.blend.</p></header>
<div class="grid">
""" + "\n".join(card(*x) for x in S) + """
</div><footer>Rig-functies in scripts/cabin_lib.py (setup_light/warm_wood_walls/overhang_fill) + grass_lib.py. Plan: docs/PLAN_rigs_implementation.md · voortgang: docs/AUTONOMOUS_PROGRESS.md</footer></body></html>"""
open(r"C:\Users\beike\Documents\Blender-blokhutten\_rig_review.html","w",encoding="utf-8").write(html)
print("rig-gallery geschreven:", len(S), "scenes")
