# Plan — Magnolia 300x200 "De Groene Long" (2026-06-12)

## 1. Concept & waarom dit origineel is
- Magnolia heeft de modern-Japandi-hero. Maar Magnolia is het **enige platte-dak-model in de hele line-up** — en dat unieke dak is nog nooit het verhaal geweest.
- **Scene-idee dat nog nooit is gedaan: de duurzame tuin.** Sedum-groendak óp de cabin, zonnepaneel, regenton aan de regenpijp, grind-wadi, inheemse beplanting. Persona: de bewuste koper (30-45, wil subsidie-proof verduurzamen, tuinkantoor/berging met eco-statement).
- Geen enkele eerdere scene heeft een dak-feature, een nadrukkelijk duurzaamheidsverhaal of het frisse heldere "eerlijke" lichtmoment dat daarbij hoort.
- Marketing-hook is concreet en echt: plat dak + EPDM is het bestaande product; sedum en panelen zijn gangbare opties op precies dit dak — geen verzonnen claims nodig, het beeld toont alleen wat kan.

## 2. Model-feiten (geprobed 12 jun, `pilots/base/Magnolia-300x200.blend`)
- Footprint **3.46 × 2.41 m**, hoogte 2.31 m — kleinste model. Plat dak `flatroof-14-*`.
- **Geen veranda, geen palen** (9 materialen, geen canopyWall/poles) — compact blok.
- Deur **gecentreerd** op +Y (X −0.75..0.75), glas + chroom.
- GLB-camera aanwezig → weg in P1. Materialen leeg → `build_clean_wood`.
- Klein model = camera dichterbij; de scene moet intiem blijven (kleine stadse achtertuin), anders verdrinkt het blok.

## 3. Stijl & materialen (alleen echte producttextures)
Naturel-modern, eerlijk:
- Wanden: `assets/blokhutwinkel-textures/8192/kdi_rabat.jpg` (naturel kdi — warm, onbewerkt, past bij eco)
- Deur: `hardhout-deuren-ramen.jpg`
- Dakrand/trim: `staalpannen-antraciet.jpg`
- Dak: `epdm.jpg` als basis, **sedum-laag erbovenop** (apart vlak 6 cm boven dakvlak, 15 cm binnen de rand — EPDM-rand blijft zichtbaar = product blijft leesbaar!)
- Terras: flagstones licht (`flagstone_floor`) klein gehouden, rest halfverharding

## 4. Scene-layout (coördinaten; cabin op origin, voorzijde +Y; kleine stadstuin ~10×12 m)
| Element | Positie | Detail |
|---|---|---|
| Tuinkamer-grond | 22×22 m zichtbaar, maar erfgrens dichtbij | gemengd: gras + grindzones |
| **Sedum-dak (focal #1)** | dakvlak, Z ~2.34 | GN-scatter: moss_01-plukken + shrub_03-blaadjes laag + her en der `flower_heliophila` (bloeiend sedum-effect), op groene basis-mat |
| Zonnepaneel | achterhelft dak, 10° schuin opgesteld | `assets/sketchfab/lighting/solar_panel_gltf` — NIET het hele dak: 1 paneel, suggestie |
| **Regenton (focal #2)** | rechterhoek gevel (1.9, 1.0) | proceduraal: cilinder Ø0.6 h0.9, donkergroen/antraciet, houten deksel; regenpijp = cilinder langs trim naar ton |
| Wadi/grindstrook | langs gevelvoet Y 1.3..1.9, X −1.8..1.8 | `construction_gravel` licht; vangt "regenwater" op — echte bouwpraktijk |
| Stapstenen | Y 2..7 naar deur | `rocky_stone_path_scan` in gras (NIET boven grind — anti-pattern!) |
| Inheemse border | links (−3.5, 3), rechts (3, 4.5) | butterfly bush + spiraea + weed/dandelion mix — bijenvriendelijk-look |
| Insectenboom | multi-stam berk (3.5, −1) | birch pack |
| Heg perimeter | dichtbij: Y −3.5, X ±5.5 | GN shrub_03, 1.7 m — kleine ommuurde stadstuin |
| Bomenringen | 2 ringen 9/14 m (compact!) + vulring 20 m | buurt-groen boven de heg |

## 5. Compositie & camera
- **Verhoogd standpunt is hier de uitzondering**: het dak is het verhaal. Camera 35 mm op **2.6 m hoogte** (bovenkant trap/talud-perspectief), vanaf (4.5, 6.0, 2.6), target (0, 0.3, 1.6) — net genoeg om het sedum-dak als groen vlak te zien ZONDER drone-flyover te worden (regel: eye-level — bewust en gemotiveerd gebroken, max +1 m).
- Alternatief frame in P5 ook renderen: klassiek eye-level (4.5, 6.5, 1.6) — user kiest.
- Vanaf (+X,+Y): regenton + regenpijp links leesbaar, deur centraal-rechts, dakvlak loopt naar rechtsboven.
- Compact frame: cabin vult ~55% breedte (klein model, dichtbij).

## 6. Licht & sfeer (heldere voorjaarsochtend ~10:00, "eerlijk" licht)
- HDRI: `assets/polyhaven/hdri/kloofendal_48d_partly_cloudy_puresky_2k.hdr`, strength 1.0 — fris, documentair.
- Zon: 5500K neutraal, energie 3.5, elevatie ~35°, 40° off-axis — sedum-textuur moet reliëf tonen.
- Filmic, Medium High Contrast, exposure 0.3. Dit is de meest "catalogus-eerlijke" scene van de acht — bewust.

## 7. Props & asset-paden
- Zonnepaneel: `assets/sketchfab/lighting/solar_panel_gltf` (schaal/oriëntatie checken — P4b!)
- Sedum-scatter: `moss_01_2k.blend` + `shrub_03_2k.blend` blaadjes + `flower_heliophila_2k.blend` spaarzaam
- Regenton + pijp: proceduraal (cilinders + deksel), mat antraciet `#2A2D2E` roughness 0.7
- Stapstenen: `assets/sketchfab/path_stones/rocky_stone_path_scan_gltf`
- Grind: `construction_gravel_vl0mfbllw_8k_ue_raw`
- Borders: `multi_color_butterfly_bush_gltf`, `goldmound_spiraea_red_flowering_gltf`, `dandelion_01`
- Fiets NIET hier (die is van Dahlia-kantoor) — evt. gieter weglaten (geen asset, niet verzinnen)

## 8. Bouwfases (headless, per fase script + save + diag 1280×720/64)
| Fase | Script | Inhoud |
|---|---|---|
| P1 | `build_magnolia_eco_p1.py` | GLB-cam weg, kdi-naturel materialen, grond, HDRI+zon, camera (verhoogd standpunt) |
| P2 | `build_magnolia_eco_p2.py` | Heg dichtbij + 2+1 bomenringen + berk |
| P3 | `build_magnolia_eco_p3.py` | **Sedum-dak** (basisvlak + GN-scatter) + zonnepaneel + regenton/pijp + wadi |
| P3b | dak-check | crops van dakvlak vanaf hero-cam én een steile checkcam — dekt het sedum, blijft EPDM-rand leesbaar? |
| P4 | `build_magnolia_eco_p4.py` | Stapstenen, borders, eventuele potten bij deur |
| P4b | inspectiecams | close-ups: regenton+pijp, paneel, deurzone, border |
| P5 | `build_magnolia_eco_p5.py` | validate + audit + 1080p preview (beide cam-standpunten) |
| P6+ | fixes na feedback → finale | |

## 9. Risico's & fallbacks
- **Sedum-dak leest als ruis** → grotere kleurplukken (3-4 groentinten in patches via voronoi-mask) i.p.v. uniforme scatter; werkt het niet, dan strakke sedum-mat (textuur-vlak met bump) als fallback.
- **Verhoogde camera wordt drone-look** → max 2.6 m, verticalen recht houden (rotation_x ≈ 0 + shift_y); eye-level-variant is de verzekering.
- **Zonnepaneel-GLB** onbekend → P4b; lelijk = weglaten, sedum + ton dragen het verhaal ook alleen.
- **Regenpijp-aansluiting** moet kloppen op de trim (geometrie-validatieregel: fysiek laten samenwerken, niet zweven) — numeriek positioneren op trim-bbox.
- Klein model + dichte heg = snel vol → max 2 borders, lucht laten.

## 10. Validatie & render-trap
- Audit per fase; let op: sedum-scatter mag NIET buiten dakrand steken (bbox-check op dak-zone).
- Anti-empty checklist; stapstenen in gras (niet op grind).
- Preview 1080p/160 in 2 standpunten → user kiest + akkoord → finale 2560×1440/240 (playbook).

## Output
`pilots/Magnolia-300x200/style-eco-groendak/magnolia_groene_long.blend` (nieuwe stijlmap) + diag PNGs.
