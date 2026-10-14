"""Vul _grass_review.html met kaarten voor alle gras-scenes."""
DONE = [
 ("Camelia Buitenbad", "Camelia-250x300-300-zijwand/style-hot-tub-premium/camelia_buitenbad"),
 ("Camelia Wijnterras", "Camelia-250x300-300-zijwand/style-mediterraan/camelia_wijnterras"),
 ("Dahlia Tuinkantoor", "Dahlia-250x250-300-zijwand/style-modern-urban-cottage/dahlia_tuinkantoor"),
 ("Dahlia Leeshoek", "Dahlia-250x250-300-zijwand/style-scandi/dahlia_leeshoek"),
 ("Jasmijn Familietuin", "Jasmijn-300x250-300-zijwand/style-klassiek-familie/jasmijn_familietuin"),
 ("Jasmijn Theehuis", "Jasmijn-300x250-300-zijwand/style-japandi/jasmijn_theehuis"),
 ("Lavendel Pluktuin", "Lavendel-400x300-400-zijwand/style-boerderij/lavendel_pluktuin"),
 ("Lelie Avondkubus", "Lelie-400x250-300-zijwand/style-modern/lelie_avondkubus"),
 ("Magnolia Wintertuin", "Magnolia-300x200/style-scandi/magnolia_wintertuin"),
 ("Magnolia Groene Long", "Magnolia-300x200/style-eco-groendak/magnolia_groene_long"),
 ("Roosmarijn Zentuin", "Roosmarijn-200x300-400-zijwand/style-japanese-zen/roosmarijn_zentuin"),
 ("Roosmarijn Kruidenterras", "Roosmarijn-200x300-400-zijwand/style-mediterraan/roosmarijn_kruidenterras"),
 ("Zonnebloem Zomeravond", "Zonnebloem-300x300-300-zijwand/style-boerderij/zonnebloem_zomeravond"),
 ("Zonnebloem Ochtendhoek", "Zonnebloem-300x300-300-zijwand/style-scandi/zonnebloem_ochtendhoek"),
]
SPECIAL = [
 ("Lelie Ochtendnevel (weide)", "Lelie-400x250-300-zijwand/style-forest-wilderness/lelie_ochtendnevel"),
 ("Lavendel Lavendelveld (veld)", "Lavendel-400x300-400-zijwand/style-mediterraan/lavendel_lavendelveld"),
]
def card(title, base):
    png = f"pilots/{base}_R2_PREVIEW.png"
    return (f'<div class="card"><div class="lbl"><span>{title}</span>'
            f'<a class="full" href="{png}" target="_blank">open</a></div>'
            f'<img src="{png}"></div>')
html = open(r"C:\Users\beike\Documents\Blender-blokhutten\_grass_review.html", encoding="utf-8").read()
html = html.replace("CARDS", "\n".join(card(t, b) for t, b in DONE))
html = html.replace("SPECIAL", "\n".join(card(t, b) for t, b in SPECIAL))
open(r"C:\Users\beike\Documents\Blender-blokhutten\_grass_review.html", "w", encoding="utf-8").write(html)
print("gallery geschreven:", len(DONE), "done +", len(SPECIAL), "special")
