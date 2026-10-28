# Plan — Roosmarijn 200x300+400+zijwand "De Zentuin" (2026-06-12)

## 1. Concept & waarom dit origineel is
- Roosmarijn heeft de mediterraan-warme hero. Het tweede gezicht: **het theehuis in een Japanse zentuin**.
- **Scene-idee dat nog nooit is gedaan: de volledige zen-tuin als ritueel.** Karesansui-grindvlak met harkpatroon, stapstenen, mospartijen, tsukubai-waterbak, een esdoorn als kleuraccent. Magnolia's hero was *modern-Japandi-architectuur* (strakke heggen, donker hout) — dit is het andere uiteinde: de **contemplatieve tuin zelf**, met harkringen en mos als hoofdmotief. Persona: De Rust-Zoeker / Wellness-Buyer (stijlbijbel Japandi, 45-65, theehuis/mindfulness).
- Roosmarijn 200×300 is het smalste, diepste model — intiem als theehuis. De zijwand-veranda wordt de **engawa** (overdekte zitrand), wat dit model uniek geschikt maakt.
- Lichtmoment: zacht bewolkt (overcast) — nog nooit gebruikt, en precies goed voor mos/grind (geen harde schaduwen, materiaal-eerlijk; stijlbijbel: snoei en textuur zíjn het ontwerp).

## 2. Model-feiten (geprobed 12 jun, `pilots/base/Roosmarijn-200x300-400-zijwand.blend`)
- Footprint **6.43 × 3.41 m**, hoogte 2.37 m, plat dak (`flatroof-19-*`).
- Deur **+Y-voorzijde**, X 1.23..2.74 — **verder naar rechts dan andere modellen** (gesloten deel rechts is smal); veranda links groot (pole-0 op (−2.94, 1.43)), open naar +Y.
- GLB-camera aanwezig → weg in P1. Materialen leeg → `build_clean_wood`.

## 3. Stijl & materialen (alleen echte producttextures)
Stijlbijbel Japandi vraagt shou-sugi-ban → echte productvertaling: **zwart fijnbezaagd hout**.
- Wanden: `assets/blokhutwinkel-textures/8192/kdi_rabat_fbz_zwart.jpg` (zwart fijnbezaagd ≈ yakisugi-look, echt product; roughness hoog 0.8, warm-zwart NIET koud)
- Balken/palen: `kdi_potdeksel_zwart.jpg`
- Deur: `hardhout-deuren-ramen.jpg` (warm hout in zwart vlak — japandi-correct contrast)
- Dak: `epdm.jpg`, rand `staalpannen-antraciet.jpg`
- Engawa-vloer (veranda): `douglas.jpg` glad, licht — contrast met zwarte wand

## 4. Scene-layout (coördinaten; cabin op origin, voorzijde +Y)
| Element | Positie | Detail |
|---|---|---|
| Grond | 30×30 m | gedempt groen + mos-zones (geen siergazon) |
| **Karesansui-grindvlak (focal)** | Y 2..7.5, X −3..2.5, niervorm | licht grind; **harkpatroon = proceduraal**: radial waves (displacement via wave/voronoi-mask) rond 2 mos-eilanden |
| Mos-eilanden in grind | (−1.2, 4.5) en (1.0, 5.8) | `boulder_01` + `stone_01` + `moss_01`-bekleding |
| Stapstenen-route | vanaf Y 9 → om grindvlak heen → deur (NIET door het grind!) | `mossy_stones_pack` onregelmatig, 0.5-0.6 m |
| **Tsukubai-zone** | bij engawa-rand (−2.2, 2.2) | waterbak = uitgeholde `boulder_01` + watervlakje; bamboe-lepel weglaten (geen asset) |
| Stenen lantaarn-sfeer | (1.8, 3.2) aan grindrand | `Lantern_01` (polyhaven, steen-hertint) — yukimi-doro-rol |
| **Esdoorn (kleuraccent)** | (4.2, 1.0), 1 specimen | `maple_tree_scan` — het enige warme kleuraccent |
| Lage snoeiwolken | 3× langs achterheg | GN shrub_03 op afgeplatte bol-donors (niwaki-suggestie, dicht scatter) |
| Zwarte-grassen-rand | langs engawa | `weed_plant_02` donker hertint (`Ophiopogon`-look) |
| Heg perimeter | Y −5.5, X ±8.5 | GN shrub_03 strak 1.8 m (besloten tuinkamer) |
| Bomenringen | 3 ringen 13/17/22 m | pine-zwaar (Japanse den-gevoel) + enkele maple |

## 5. Compositie & camera
- 35 mm, 1.55 m, vanaf voor-rechts **(7.5, 9.0, 1.55)**, target (−0.3, 0.8, 1.2).
- Vanaf (+X,+Y): zwarte gevel + deur links (deur zit toch al rechts op de gevel = dicht bij beeldcentrum), engawa/veranda rechts-diep, karesansui-vlak vult het middenvlak vóór de cabin.
- Harkpatroon moet leesbaar zijn: camera laag genoeg dat strijklicht… nee — overcast: leesbaarheid komt uit **displacement-schaduwwerking + glanzende grind-roughness-variatie**; crop-check verplicht.
- Asymmetrie (stijlbijbel: introduceer één curve): de niervorm van het grindvlak is de curve in een verder rechte compositie.
- Veel negatieve ruimte bewust laten — leegte is onderdeel van de stijl (anti-empty checklist geldt, maar "vol" is hier fout; elke zone moet wél intentioneel zijn).

## 6. Licht & sfeer (zacht bewolkt, tijdloos ~11:00)
- HDRI: `assets/polyhaven/hdri/kloofendal_overcast_puresky_1k.hdr`, strength 1.1.
- Zon: zwak (energie 1.0-1.5, 5800K) alleen als shaping-licht 30° off-axis — overcast mag niet plat worden.
- Filmic, **Medium Contrast**, exposure 0.35; palet bewaken: charcoal / warm hout / jade-mos / grijswit grind — niets verzadigd.

## 7. Props & asset-paden
- Stenen/boulders: `assets/polyhaven/models/boulder_01/`, `stone_01_2k.blend`
- Mos: `moss_01_2k.blend` (scatter op stenen + eilanden)
- Stapstenen: `assets/sketchfab/path_stones/mossy_stones_pack_tliiadmva_gltf_high` + `japanese_mossy_stone_wall_ulldfby_gltf_raw` (lage muur-fragmenten evt. als rand bij engawa)
- Lantaarn: `assets/polyhaven/models/Lantern_01/` steen-hertint; brandend = uit (daglicht)
- Esdoorn: `assets/sketchfab/trees/maple_tree_scan_trunk_4_lod_gltf`
- Lage bank op engawa: `wooden_bench_low_poly_gltf` laag gezaagd (40 cm zithoogte, japandi) of proceduraal hinoki-latje-bankje
- Theeset op engawa: 2 kommen = simpele cilinders keramiek-wit `#E8E2D5` — klein, alleen als close-up overtuigt
- GN-heg + bomen: shrub_03, pine trio, maple, birch spaarzaam

## 8. Bouwfases (headless, per fase script + save + diag 1280×720/64)
| Fase | Script | Inhoud |
|---|---|---|
| P1 | `build_roosmarijn_zen_p1.py` | GLB-cam weg, zwart-fbz materialen + douglas engawa, grond, HDRI, camera |
| P2 | `build_roosmarijn_zen_p2.py` | Perimeter-heg + bomenringen + esdoorn + snoeiwolken |
| P3 | `build_roosmarijn_zen_p3.py` | **Karesansui-vlak + harkpatroon-displacement** + mos-eilanden + stapstenen |
| P3b | grind-check | full-res crops: leest het harkpatroon? displacement-schaal proben (3 varianten) |
| P4 | `build_roosmarijn_zen_p4.py` | Tsukubai, lantaarn, bank + theeset, zwarte grassen |
| P4b | inspectiecams | close-ups: tsukubai, lantaarn, engawa, grindrand |
| P5 | `build_roosmarijn_zen_p5.py` | validate + audit + 1080p preview |
| P6+ | fixes na feedback → finale | |

## 9. Risico's & fallbacks
- **Harkpatroon** is het technische hart → P3b met 3 displacement-schalen; werkt micro-displacement niet binnen VRAM, dan normal-map-aanpak (wave-texture → bump) — visueel bijna gelijkwaardig op deze afstand.
- **Overcast = plat risico** → zwakke zon erbij + roughness-variatie; desnoods `kloofendal_48d_partly_cloudy` als half-bewolkt alternatief proben in P5.
- **Tsukubai uithollen** (boolean op boulder) kan lelijke shading geven → fallback: ondiepe komvormige cilinder met steen-materiaal naast de boulder.
- **Leegte vs. kaalheid**: na P4 de anti-empty-lijst bewust langslopen — elke lege zone moet een rand/textuur-overgang hebben (gras→mos→grind), anders leest het als onaf.
- Theeset/snoeiwolken lelijk in crop → weglaten (verwijderen mag).

## 10. Validatie & render-trap
- Audit per fase; stapstenen NIET door het grindvlak (anti-pattern: stepping stones boven grind) — route loopt over mos/gras erlangs.
- Preview 1080p/160 → user-akkoord → finale 2560×1440/240 (playbook).

## Output
`pilots/Roosmarijn-200x300-400-zijwand/style-japanese-zen/roosmarijn_zentuin.blend` + diag PNGs.
