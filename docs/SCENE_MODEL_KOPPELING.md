# Scene -> cabin-model

Welke final hoort bij welke blend, en welk model daarin staat. Afgeleid door de
cabin-bbox in elke blend te meten en te combineren met de familie + hutmaat uit
de mapnaam. De totale bbox alleen is niet genoeg: `Roosmarijn 200x300 + 400` en
`Zonnebloem 300x300 + 300` zijn allebei 642,6 cm breed.

Drie finals heten anders dan hun scene; die zijn gevonden door de final te
vergelijken met de renders in de pilot-mappen (beeldgelijkenis 1.000):

- `roosmarijn_buitenbioscoop` -> de S5-tuinwerkzaterdag-scene
- `jasmijn_vinylmiddag` -> de B10-speelhuismiddag-scene
- `lavendel_tuinfeest` -> de S8-goudenuur-scene

`lavendel_lavendelveld` en `lavendel_pluktuin` gebruiken een luifel van **350**,
niet 400. De oude bestandsnaam `Lavendel 400x300 + 400` klopte niet met de
geometrie. Daarvoor is een aparte export `Lavendel 400x300 + 350 + zijwand`
gemaakt, zodat die scenes alleen planken wisselen.

`roosmarijn_modern` staat niet in de lijst: dat is Beikes eigen Zentuin-werk.

| final | bronblend | model |
|---|---|---|
| `camelia_buitenbad` | `pilots/Camelia-250x300-300-zijwand/style-hot-tub-premium/camelia_buitenbad_R4_PLANKFIX.blend` | Camelia 250x300 + 300 + zijwand |
| `camelia_leesplek` | `pilots/S7-leesplek-Camelia250x300/camelia_leesplek_S7_PLANKFIX.blend` | Camelia 250x300 + 300 + zijwand |
| `camelia_wijnterras` | `pilots/Camelia-250x300-300-zijwand/style-mediterraan/camelia_wijnterras_R4_PLANKFIX.blend` | Camelia 250x300 + 300 + zijwand |
| `dahlia_leeshoek` | `pilots/Dahlia-250x250-300-zijwand/style-scandi/dahlia_leeshoek_R4_PLANKFIX.blend` | Dahlia 250x250 + 300 + zijwand |
| `dahlia_ochtendkoffie` | `pilots/S6-ochtendkoffie-Dahlia250x250/dahlia_ochtendkoffie_S6_PLANKFIX.blend` | Dahlia 250x250 + 300 + zijwand |
| `dahlia_tuinkantoor` | `pilots/Dahlia-250x250-300-zijwand/style-modern-urban-cottage/dahlia_tuinkantoor_R4_PLANKFIX.blend` | Dahlia 250x250 + 300 + zijwand |
| `jasmijn_familiemiddag` | `pilots/S1-familiemiddag-Jasmijn300x250/jasmijn_familiemiddag_S1_PLANKFIX.blend` | Jasmijn 300x250 + 300 + zijwand |
| `jasmijn_vinylmiddag` | `pilots/B10-speelhuismiddag-Jasmijn300x250/jasmijn_speelhuismiddag_B10_PLANKFIX_HOEKFIX.blend` | Jasmijn 300x250 + 250 |
| `jasmijn_vlindertuin` | `pilots/B12-vlindertuin-Jasmijn300x250/jasmijn_vlindertuin_B12_PLANKFIX_HOEKFIX.blend` | Jasmijn 300x250 + 250 |
| `lavendel_buitenbioscoop` | `pilots/B14-buitenbioscoop-Lavendel400x300/lavendel_bioscoop_B14_PLANKFIX_HOEKFIX.blend` | Lavendel 400x300 + 300 |
| `lavendel_lavendelveld` | `pilots/Lavendel-400x300-400-zijwand/style-mediterraan/lavendel_lavendelveld_R4_PLANKFIX.blend` | Lavendel 400x300 + 350 + zijwand |
| `lavendel_pluktuin` | `pilots/Lavendel-400x300-400-zijwand/style-boerderij/lavendel_pluktuin_R4_PLANKFIX.blend` | Lavendel 400x300 + 350 + zijwand |
| `lavendel_tuinfeest` | `pilots/S8-goudenuur-Lavendel400x300/lavendel_goudenuur_S8_PLANKFIX.blend` | Lavendel 400x300 + 300 + zijwand |
| `lelie_avondkubus` | `pilots/Lelie-400x250-300-zijwand/style-modern/lelie_avondkubus_R4_PLANKFIX.blend` | Lelie 400x250 + 300 + zijwand |
| `lelie_goudenborrel` | `pilots/S2-goudenborrel-Lelie400x250/lelie_goudenborrel_S2_PLANKFIX.blend` | Lelie 400x250 + 300 + zijwand |
| `lelie_ochtendnevel` | `pilots/Lelie-400x250-300-zijwand/style-forest-wilderness/lelie_ochtendnevel_R4_PLANKFIX.blend` | Lelie 400x250 + 300 + zijwand |
| `magnolia_atelier` | `pilots/S3-atelier-Magnolia300x200/magnolia_atelier_S3_PLANKFIX.blend` | Magnolia 300x200 |
| `roosmarijn_buitenbioscoop` | `pilots/S5-tuinwerkzaterdag-Roosmarijn200x300/roosmarijn_tuinwerkzaterdag_S5_PLANKFIX.blend` | Roosmarijn 200x300 + 400 + zijwand |
| `roosmarijn_schaakavond` | `pilots/B13-schaakavond-Roosmarijn200x300/roosmarijn_schaakavond_B13_PLANKFIX_HOEKFIX.blend` | Roosmarijn 200x300 + 400 |
| `roosmarijn_uitslaapochtend` | `pilots/B11-uitslaapochtend-Roosmarijn200x300/roosmarijn_uitslaapochtend_B11_PLANKFIX_HOEKFIX.blend` | Roosmarijn 200x300 + 400 |
| `zonnebloem_modern` | `pilots/Zonnebloem-300x300-300-zijwand/style-modern/zonnebloem_modern_PLANKFIX.blend` | Zonnebloem 300x300 + 300 + zijwand |
| `zonnebloem_zomerselunch` | `pilots/S4-zomerselunch-Zonnebloem300x300/zonnebloem_zomerselunch_S4_PLANKFIX.blend` | Zonnebloem 300x300 + 300 + zijwand |
| `zonnebloem_zonnegroet` | `pilots/B15-zonnegroet-Zonnebloem300x300/zonnebloem_zonnegroet_B15_PLANKFIX_HOEKFIX.blend` | Zonnebloem 300x300 + 300 |
