r"""Scene-registry voor de clips-v2 (plankfix-herrender van de blokhut-filmpjes, 3 sep 2026).

Per scène: de blend die de goedgekeurde final oplevert (PLANKFIX / HOEKFIX), de runtime-tweaks
die bij de R4-fixronde NIET in de blend zijn opgeslagen (zie HANDOFF_plankfix.md, 3 sep 11:29),
en de clipnaam in ALLE_FINALS/filmpjes. Kapschuren/overkappingen staan er ook in (geen plankfix
nodig, wel dezelfde hoek-klacht) maar krijgen prioriteit 2.
"""
import os

ROOT = r"D:\Blender-blokhutten"
OLD = r"C:\Users\beike\Documents\Blender-blokhutten_OLD\pilots"
P = os.path.join(ROOT, "pilots")

SCENES = {
    # ---- tuinscenes S/B-reeks (15) -> blokhutten-tuinscenes ------------------------------------
    "jasmijn_familiemiddag":      dict(blend=P + r"\S1-familiemiddag-Jasmijn300x250\jasmijn_familiemiddag_S1_PLANKFIX.blend", clip="jasmijn-familiemiddag"),
    "lelie_goudenborrel":         dict(blend=P + r"\S2-goudenborrel-Lelie400x250\lelie_goudenborrel_S2_PLANKFIX.blend", clip="lelie-goudenborrel"),
    "magnolia_atelier":           dict(blend=P + r"\S3-atelier-Magnolia300x200\magnolia_atelier_S3_PLANKFIX.blend", clip="magnolia-atelier"),
    "zonnebloem_zomerselunch":    dict(blend=P + r"\S4-zomerselunch-Zonnebloem300x300\zonnebloem_zomerselunch_S4_PLANKFIX.blend", clip="zonnebloem-zomerselunch"),
    "roosmarijn_tuinwerkzaterdag": dict(blend=P + r"\S5-tuinwerkzaterdag-Roosmarijn200x300\roosmarijn_tuinwerkzaterdag_S5_PLANKFIX.blend", clip="roosmarijn-tuinwerkzaterdag"),
    "dahlia_ochtendkoffie":       dict(blend=P + r"\S6-ochtendkoffie-Dahlia250x250\dahlia_ochtendkoffie_S6_PLANKFIX.blend", clip="dahlia-ochtendkoffie"),
    "camelia_leesplek":           dict(blend=P + r"\S7-leesplek-Camelia250x300\camelia_leesplek_S7_PLANKFIX.blend", clip="camelia-leesplek"),
    "lavendel_goudenuur":         dict(blend=P + r"\S8-goudenuur-Lavendel400x300\lavendel_goudenuur_S8_PLANKFIX.blend", clip="lavendel-goudenuur"),
    "jasmijn_vinylmiddag":        dict(blend=P + r"\B10-speelhuismiddag-Jasmijn300x250\jasmijn_speelhuismiddag_B10_PLANKFIX_HOEKFIX.blend", clip="jasmijn-vinylmiddag"),
    "roosmarijn_uitslaapochtend": dict(blend=P + r"\B11-uitslaapochtend-Roosmarijn200x300\roosmarijn_uitslaapochtend_B11_PLANKFIX_HOEKFIX.blend", clip="roosmarijn-uitslaapochtend"),
    "jasmijn_vlindertuin":        dict(blend=P + r"\B12-vlindertuin-Jasmijn300x250\jasmijn_vlindertuin_B12_PLANKFIX_HOEKFIX.blend", clip="jasmijn-vlindertuin"),
    "roosmarijn_schaakavond":     dict(blend=P + r"\B13-schaakavond-Roosmarijn200x300\roosmarijn_schaakavond_B13_PLANKFIX_HOEKFIX.blend", clip="roosmarijn-schaakavond"),
    "lavendel_buitenbioscoop":    dict(blend=P + r"\B14-buitenbioscoop-Lavendel400x300\lavendel_bioscoop_B14_PLANKFIX_HOEKFIX.blend", clip="lavendel-buitenbioscoop"),
    "zonnebloem_zonnegroet":      dict(blend=P + r"\B15-zonnegroet-Zonnebloem300x300\zonnebloem_zonnegroet_B15_PLANKFIX_HOEKFIX.blend", clip="zonnebloem-zonnegroet"),
    "zonnebloem_modern":          dict(blend=P + r"\Zonnebloem-300x300-300-zijwand\style-modern\zonnebloem_modern_PLANKFIX.blend", clip="zonnebloem-modern"),
    # ---- R4-stijlen (8) -> blokhutten-stijlen; bron = _OLD-kopie + fixronde-tweaks (niet in blend) ----
    "camelia_buitenbad":     dict(blend=OLD + r"\Camelia-250x300-300-zijwand\style-hot-tub-premium\camelia_buitenbad_v2_PLANKFIX.blend", clip="camelia-buitenbad"),
    "camelia_wijnterras":    dict(blend=OLD + r"\Camelia-250x300-300-zijwand\style-mediterraan\camelia_wijnterras_v2_PLANKFIX.blend", clip="camelia-wijnterras",
                                  tweaks={"exposure": -0.3}),
    "dahlia_leeshoek":       dict(blend=OLD + r"\Dahlia-250x250-300-zijwand\style-scandi\dahlia_leeshoek_v2_PLANKFIX_HOEKFIX2.blend", clip="dahlia-leeshoek",
                                  tweaks={"fill_canopy": {"energy": 60, "size": 2.5}}),
    "dahlia_tuinkantoor":    dict(blend=OLD + r"\Dahlia-250x250-300-zijwand\style-modern-urban-cottage\dahlia_tuinkantoor_v2_PLANKFIX.blend", clip="dahlia-tuinkantoor",
                                  tweaks={"mats": {"firstLayer-wall": {"Roughness": 0.9, "Specular IOR Level": 0.25}}}),
    "lavendel_lavendelveld": dict(blend=OLD + r"\Lavendel-400x300-400-zijwand\style-mediterraan\lavendel_lavendelveld_v2_PLANKFIX.blend", clip="lavendel-lavendelveld"),
    "lavendel_pluktuin":     dict(blend=OLD + r"\Lavendel-400x300-400-zijwand\style-boerderij\lavendel_pluktuin_v2_PLANKFIX.blend", clip="lavendel-pluktuin"),
    "lelie_avondkubus":      dict(blend=OLD + r"\Lelie-400x250-300-zijwand\style-modern\lelie_avondkubus_v3_PLANKFIX.blend", clip="lelie-avondkubus"),
    "lelie_ochtendnevel":    dict(blend=OLD + r"\Lelie-400x250-300-zijwand\style-forest-wilderness\lelie_ochtendnevel_v3_PLANKFIX.blend", clip="lelie-ochtendnevel",
                                  tweaks={"sun_angle": 6.0, "world_strength": 1.25}),
}

# prioriteit 2: geen plankfix, maar dezelfde hoek-klacht geldt
SCENES_P2 = {
    "kapschuur_A_lounge":  dict(blend=ROOT + r"\kapschuren\scenes\kapschuur_A_lounge.blend", clip="kapschuur-A-lounge"),
    "kapschuur_B_dining":  dict(blend=ROOT + r"\kapschuren\scenes\kapschuur_B_dining.blend", clip="kapschuur-B-dining"),
    "kapschuur_C_bergkap": dict(blend=ROOT + r"\kapschuren\scenes\kapschuur_C_bergkap.blend", clip="kapschuur-C-bergkap"),
    "overkapping_wellness":  dict(blend=ROOT + r"\overkappingen-website\scenes\tuinWellness-douglas-600x300-stap2.blend", clip="overkapping-wellness-hottub"),
    "overkapping_keuken":    dict(blend=ROOT + r"\overkappingen-website\scenes\tuinKeuken-douglas-1000x400-stap2.blend", clip="overkapping-buitenkeuken"),
    "overkapping_vuurtafel": dict(blend=ROOT + r"\overkappingen-website\scenes\tuinVuurtafel-douglas-600x300-stap2.blend", clip="overkapping-vuurtafel"),
    "overkapping_zwembad":   dict(blend=ROOT + r"\overkappingen-website\scenes\tuinZwembad-douglas-700x400-stap2.blend", clip="overkapping-zwembadtuin"),
}


def alle():
    d = dict(SCENES)
    d.update(SCENES_P2)
    return d


if __name__ == "__main__":
    ontbreekt = [k for k, v in alle().items() if not os.path.exists(v["blend"])]
    print(f"{len(SCENES)} prio-1 + {len(SCENES_P2)} prio-2 scenes; ontbrekende blends: {ontbreekt or 'geen'}")
