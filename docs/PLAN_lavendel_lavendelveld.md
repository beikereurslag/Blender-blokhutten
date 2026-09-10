# Plan — Lavendel 400x300+400+zijwand "Het Lavendelveld" (2026-06-12)

## 1. Concept & waarom dit origineel is
- Lavendel heeft de modern-strakke hero (zwart, architecturaal). Maar de lijn heet **Lavendel** en de inventory-stijlmatch is "Provence Lavender" — dat beeld bestaat nog niet.
- **Scene-idee dat nog nooit is gedaan: het lavendelveld zelf.** Geen border-met-wat-lavendel (dat had de oude Lavendel-modern als accent), maar **rijen lavendel als hoofdmotief** — het Provence-gevoel met de cabin als landelijk buitenverblijf erachter, gouden avondzon laag over de rijen. Persona: De Vakantieganger (stijlbijbel Mediterraan, 40-60, NL-Provence-vibe zonder vlucht).
- Onderscheid t.o.v. Roosmarijn-warm (al gedaan, mediterraan kruiden-terras): daar droeg het terras de scene; hier draagt het **veld met diagonale rijen** de compositie — een totaal ander beeld.
- Grootste model van de lijn (7.93 m) — kan een breed veld dragen zonder dat de cabin verzuipt.

## 2. Model-feiten (geprobed 12 jun, `pilots/base/Lavendel-400x300-400-zijwand.blend`)
- Footprint **7.93 × 3.41 m**, hoogte 2.37 m, plat dak (`flatroof-103-*`). Grootste cabin van de 8.
- Deur **+Y-voorzijde**, X 0.98..2.49; veranda links, pole-0 op (−3.69, 1.43), open naar +Y.
- GLB-camera aanwezig → weg in P1. Materialen leeg → `build_clean_wood`.

## 3. Stijl & materialen (alleen echte producttextures — géén stuc verzinnen)
Stijlbijbel Mediterraan vraagt stuc/terracotta, maar **wij gebruiken alleen echte Blokhutwinkel-producten** → de Provence-vertaling loopt via verweerd grijs hout (zoals een oude lavendelschuur) + warme props:
- Wanden: `assets/blokhutwinkel-textures/8192/luxehouse-grijs.jpg` (zacht verweerd grijs — leest zuid-Frans in goud licht)
- Balken/palen: `luxehouse-grijs-gedompeld.jpg`
- Deur: `hardhout-deuren-ramen.jpg`; luik-suggestie NIET toevoegen (niet in product)
- Dak: `epdm.jpg`, rand `staalpannen-antraciet.jpg`
- Terras: flagstones (`assets/sketchfab/path_stones/flagstone_floor_vl1iaf0lw_8k_ue_raw`) — natuursteen, mediterraan-correct
- Warmte komt uit terracotta-props + licht, niet uit verzonnen wandafwerking.

## 4. Scene-layout (coördinaten; cabin op origin, voorzijde +Y)
| Element | Positie | Detail |
|---|---|---|
| Grond | 34×34 m | gras gedempt droog-groen (`aerial_grass_rock` mix — zuidelijke look) |
| **Lavendelveld (focal)** | Y 4..12, X −8..6 | **6-7 rijen**, h.o.h. 1.1 m, rijen **diagonaal** richting cabin (leading lines), `assets/3daistudio/lavender` als cluster-donor, GN/array per rij met jitter |
| Maaipad door veld | 1 m breed, tussen rij 3 en 4, naar deur | beige split-gravel (`construction_gravel`, warm hertint) |
| Terras | X −3.7..0.5, Y 1.75..4.0 | flagstones |
| Bistroset | (−2.2, 2.8) | `bistrot_table_and_chair_gltf` — Frans! |
| Terracotta-cluster | 5 potten (3 maten) bij deur (3.2, 2.2) | `terracotta_pot` + `optimized_potted_plants` |
| Jacaranda als "olijf-silhouet" | (6.5, 0.5), 1 specimen | `jacaranda_tree_2k.blend` — paarse bloei rijmt met veld; GEEN palmen |
| Rozemarijn-heggetjes | 2 lage blokken langs terrasrand | GN shrub_03 laag (0.5 m), grijsgroen hertint |
| Heg perimeter | Y −6, X ±10 | GN shrub_03 1.6 m |
| Bomenringen | 3 ringen 15/19/25 m | pine-zwaar (cipres-gevoel), birch spaarzaam |

## 5. Compositie & camera
- 35 mm, 1.60 m, vanaf voor-rechts **(9.0, 11.0, 1.6)**, target (−0.5, 0.5, 1.25) — verder weg vanwege 8 m gevel.
- Vanaf (+X,+Y): cabin links-boven-derde, lavendelrijen lopen diagonaal van rechts-onder (voorgrond, onscherp) naar de cabin — **de rijen zijn de leading lines**, het maaipad eindigt bij de deur.
- Horizon onderste derde; deur op power point; veranda-diepte rechts.
- Voorgrond: eerste lavendelrij gedeeltelijk in onscherpte onderin (f/5.6) — paarse parallax.

## 6. Licht & sfeer (golden hour avond ~19:30)
- HDRI: `assets/polyhaven/hdri/qwantani_dusk_2_2k.hdr` (of `spaichingen_hill` als backup), strength 1.0, Z-rotatie: zon laag **achter-rechts van camera**, strijkt dwars over de rijen → elke rij krijgt een gouden rand en eigen schaduwband.
- Zon: 4000K warm, energie 3.0, elevatie 12-15° — lager dan Dahlia-hero, het veld vraagt strijklicht.
- Filmic, Medium High Contrast, exposure 0.3; paars NIET laten clippen (crop-check op veld!).

## 7. Props & asset-paden
- Lavendel: `assets/3daistudio/lavender/` — **cluster-donor fix verplicht** (de bekende _duplicate_collection_at variant-bug); dichtheid per rij hoog genoeg dat rijen vol lezen
- Bistroset: `assets/sketchfab/furniture/bistrot_table_and_chair_gltf`
- Terracotta: `assets/sketchfab/decor/terracotta_pot` + `optimized_potted_plants_gltf`
- Rieten mand met lavendelbosjes op terras: `old_wicker_basket_ukqpfhsaw_gltf_raw` + 3 lavendel-clusters erin (oogst-knipoog, klein houden)
- Lantaarn op tafel: `assets/sketchfab/lighting/old_lantern_gltf` (uit, het is nog licht)
- Jacaranda: `assets/polyhaven/models/jacaranda_tree_2k.blend` (append per object, NIET libraries.load)
- GN-heg: shrub_03; bomen: pine trio + birch pack

## 8. Bouwfases (headless, per fase script + save + diag 1280×720/64)
| Fase | Script | Inhoud |
|---|---|---|
| P1 | `build_lavendel_veld_p1.py` | GLB-cam weg, grijs-verweerde materialen, grond, HDRI+zon, camera |
| P2 | `build_lavendel_veld_p2.py` | Perimeter-heg + bomenringen + jacaranda |
| P3 | `build_lavendel_veld_p3.py` | Terras flagstones + maaipad + **lavendelrijen** (de kern — apart proben!) |
| P3b | veld-check | full-res crops: rij-dichtheid, kleur, schaduwbanden |
| P4 | `build_lavendel_veld_p4.py` | Bistroset, terracotta, mand, lantaarn, rozemarijn-randen |
| P4b | inspectiecams | close-ups: terras, deurzone, veldrand, focal-rij |
| P5 | `build_lavendel_veld_p5.py` | validate + audit + 1080p preview |
| P6+ | fixes na feedback → finale | |

## 9. Risico's & fallbacks
- **Lavendel-asset-kwaliteit onbekend op veld-schaal** → P3b verplicht: één rij eerst, crop, dan pas 7 rijen. Te zwaar (VRAM)? → instancing via GN op curve per rij + texture_limit; nog te zwaar → 5 rijen en achterste rijen als low-detail clusters.
- **Paars kan neon worden** in golden hour → albedo dempen, saturatie via ColorMix; crop-check.
- **Rijen te perfect** = CG-tell → jitter in positie/schaal/rotatie per cluster (±10%).
- Jacaranda te dominant/bloei te fel → hertint richting grijsgroen of vervang door pine-silhouet.
- Veld eet de cabin op → cabin-derde bewaken in framing; desnoods veld 1 rij smaller.

## 10. Validatie & render-trap
- Audit per fase; anti-empty checklist (pad→deur geldt: het maaipad is de route).
- Let op compositieregel "asymmetrie": veld rechts dicht, links bij veranda lucht.
- Preview 1080p/160 → user-akkoord → finale 2560×1440/240 (playbook).

## Output
`pilots/Lavendel-400x300-400-zijwand/style-mediterraan/lavendel_lavendelveld.blend` (nieuwe stijlmap) + diag PNGs.
