# Self-review — 16 nieuwe scenes (2026-06-13)

Kritische review per scene tegen de anti-empty checklist + compositieregels + amateur-tells.
Verdict: ✅ goed / 🔧 gerichte fix toegepast.

## Primaire scenes (8)
| # | Scene | Verdict | Opmerking / fix |
|---|---|---|---|
| 1 | Zonnebloem Zomeravond | ✅ | User-goedgekeurd, finale 2560×1440 al gerenderd. Niet aangeraakt. |
| 2 | Dahlia Tuinkantoor | ✅ | Fiets+bureau-doorkijk+cor-ten; bomen via cluster-donors, glas-reflectie getemd. |
| 3 | Jasmijn Familietuin | ✅ | Picknicktafel rechtop, vogelbad 1 variant, borders hoog-laag. |
| 4 | Lavendel Lavendelveld | ✅ | Diagonale lavendelrijen als leading lines, bistro rechtop, terracotta. |
| 5 | Roosmarijn Zentuin | ✅ | Karesansui met deterministische harkringen (vertex-z), mos-eilanden, acer. |
| 6 | Camelia Buitenbad | ✅ | Proceduraal dompelbad+water, lantaarns, kale bomen vervangen (vert-count). |
| 7 | Magnolia Groene Long | ✅ | Sedum-dak GN-scatter, paneel proceduraal, regenton+pijp, verhoogde cam. |
| 8 | Lelie Ochtendnevel | ✅ | Volumetrische mist (density 0.03 + height-falloff), dauw-god-rays — sfeer-topper. |

## Alternatieve scenes (8)
| # | Scene | Stijl | Verdict | Opmerking / fix |
|---|---|---|---|---|
| 9 | Camelia Wijnterras | Mediterraan | ✅ | Travertine, terracotta+olijf, bistro+wijn, festoon; heg grijs-groen gefixt. |
| 10 | Dahlia Leeshoek | Scandi | 🔧 | Voorgrond-weeds te grof (lazen als kamerplanten) → vervangen door lavendel-drift. |
| 11 | Jasmijn Theehuis | Japandi | ✅ | Engawa, simpel grindvlak (distinct van Roosmarijn-karesansui), acer, niwaki. |
| 12 | Lavendel Pluktuin | Boerderij | ✅ | Weelderige dichte border, rozenboog + klimrozen, klinkerpad. |
| 13 | Lelie Avondkubus | Modern | ✅ | Zwart blok + interieur-gloed, beuken-blokken, cor-ten, bollards, blue hour. |
| 14 | Magnolia Wintertuin | Scandi | ✅ | Pale wash, schoon plat dak, witte bank (scandi-correct), berken-trio. |
| 15 | Roosmarijn Kruidenterras | Mediterraan | ✅ | Verhoogde kruidenbakken, travertine, olijf-pot; kruiden magenta→groen gefixt. |
| 16 | Zonnebloem Ochtendhoek | Scandi | 🔧 | Idem #10: grove voorgrond-weeds → lavendel-drift. |

## Systematische bevindingen (in cabin_lib gebakken)
- **`full_tree_donors`/`tree_rings_clustered(full_only=True)`** — nooit meer kale-skelet-dennen (was: Camelia/Magnolia handmatig vervangen).
- **`load_asset_clusters` met `all_objects`** — planten in sub-collecties laden nu wél (was: gras-count 0 bij Lelie).
- **`fix_broken_image_materials`** — sorrel/periwinkle/weed/rooibos zonder disk-textures → procedureel groen i.p.v. magenta.
- **`auto_upright` + `keep_one_xy_cluster`** — GLTF-props (picknicktafel, potten, vogelbad) rechtop + 1 variant.
- **weed_plant_02 is een GROVE breedbladige "weed"**, geen fijn siergras. Goed als losse pol in mid-ground; in nette scandi-voorgrond te dominant → liever 3daistudio-lavendel of weglaten.

## Toegepaste review-fixes
- #10 Dahlia Leeshoek: voorgrond-weeds weg, lavendel-drift (3daistudio OBJ) + preview opnieuw.
- #16 Zonnebloem Ochtendhoek: idem.
