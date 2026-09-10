# Plan — Camelia 250x300+300+zijwand "Het Buitenbad" (2026-06-12)

## 1. Concept & waarom dit origineel is
- Camelia's bestaande hero is **scandi-forest overdag** — sterk, maar de lijn mist een tweede beeld dat het premium-recreatie-gevoel verkoopt.
- **Scene-idee dat nog nooit is gedaan: wellness/spa-tuin op blue hour.** Een houten dompelbad naast de veranda, handdoeken, lantaarns, stoom boven het water. Persona: De Sauna-Liefhebber (stijlbijbel Scandi, 30-50, premium recreatie).
- Onderscheid t.o.v. Jasmijn hygge-avond (al gedaan): daar was **vuur** het hart, hier is **water + stoom** het hart; ander palet (koel blauw + warm lamplicht i.p.v. oranje vuurgloed).
- Lichtmoment blue hour is nog maar één keer gebruikt (Jasmijn) en nooit met waterreflectie — het glas, chroom en natte hout-look verkopen de avond.

## 2. Model-feiten (geprobed 12 jun, `pilots/base/Camelia-250x300-300-zijwand.blend`)
- Footprint **5.93 × 3.41 m**, hoogte 2.37 m, plat dak (`flatroof-40-*`).
- Deur **+Y-voorzijde**, X 0.73..2.24 (gesloten deel rechts), glas + chroom aanwezig.
- Open veranda links: pole-0 op (−2.69, 1.43), canopy-wanden aan −X-zijde; open naar +Y.
- GLB-camera "camera" aanwezig → verwijderen in P1.
- Materialen leeg (`basetexture-firstLayer-*`) → `build_clean_wood` BOX-mapping aanpak.

## 3. Stijl & materialen (alleen echte producttextures)
Stijlbijbel: **Scandi/Nordic** — optie (a) verweerd zilvergrijs.
- Wanden: `assets/blokhutwinkel-textures/8192/luxehouse-grijs-gedompeld.jpg` (zilvergrijs, scandi-correct)
- Balken/palen: `luxehouse-grijs.jpg` (iets lichter contrast)
- Deur: `hardhout-deuren-ramen.jpg`
- Dak: `epdm.jpg` + dakrand `staalpannen-antraciet.jpg`
- Vlonder: `douglas.jpg` licht geschuurd (whitewash-tint via ColorMix 0.15 naar `#E6E0D6`)
- **Verboden** (stijlbijbel): true black, glans, messing, terracotta, felle kleuren.

## 4. Scene-layout (coördinaten; cabin op origin, voorzijde +Y)
| Element | Positie | Maat |
|---|---|---|
| Grasgrond | (0,0,0) | 30×30 m, `assets/sketchfab/ground_grass` |
| Vlonder-terras | X −3.2..1.0, Y 1.7..6.0 | doorlopend vanaf veranda |
| **Dompelbad (focal)** | (−1.2, 4.2), Ø 1.9 m, h 0.95 m | proceduraal: douglas-duigen cilinder + 2 stalen banden + watervlak op z 0.82 |
| Trapje + handdoekrek | naast bad (−2.4, 4.0) | 2 treden douglas; rek = 2 staanders + ligger |
| Houtstapel (netjes!) | tegen −X-wand, (−3.1, 0.5) | berken-stammetjes rij, scandi-anchor |
| Pad | stapstenen Y 6..10 → vlonder | `mossy_stones_pack` flagstones in gras |
| Heg (GN shrub_03) | U-vorm op Y −6 en X ±9 | h 1.6 m, vóór schutting |
| Bomenringen | 3 ringen op 14/18/24 m | pine + birch mix, sky occluderen |
| Berkencluster | (5.5, −2), 3 multi-stam | stijlbijbel: NOOIT solitaire berk |

## 5. Compositie & camera
- 35 mm, hoogte 1.60 m, **3/4 vanaf voor-rechts (7.5, 9.5, 1.6)**, target (−0.3, 0.5, 1.2).
- Let op asrichting: vanaf (+X,+Y) is wereld +X = **links** in beeld → gesloten deel links, veranda + bad rechts-diep in beeld; bad op rechter power point.
- Horizon onderste derde; rotation_x = 0, shift_y voor framing; deurglas (verlicht interieur) op linker power point.
- Driedubbele diepte: voorgrond out-of-focus grassen (f/5.6), midden cabin+bad, achter boomwand.

## 6. Licht & sfeer (blue hour)
- HDRI: `assets/polyhaven/hdri/kloppenheim_06_puresky_2k.hdr`, strength 0.35-0.5.
- Zon uit; in plaats daarvan: 2× area light warm (2700K) in cabin-interieur achter deurglas, 3× `wooden_lantern_01` (polyhaven) met emission op vlonder/badrand, 1 wandlamp bij deur.
- **Stoom**: smalle volume-cone boven watervlak (principled volume, density 0.02-0.05) — alleen als het in diag-render overtuigt, anders weglaten.
- Water: glossy/glass mix, roughness 0.05, subtiele wave-bump; reflecteert lantaarns.
- Filmic, Medium High Contrast, exposure +0.1 (donkerder mag).

## 7. Props & asset-paden
- Lantaarns: `assets/polyhaven/models/wooden_lantern_01/`, `Lantern_01`
- Handdoeken: simpele subdivided planes met cloth-achtige solidify, off-white `#E6E0D6`, over badrand + rek
- Bank veranda: `assets/polyhaven/models/painted_wooden_bench_2k.blend` (grijs hertinten)
- Schapenvacht op bank: plane + hair-achtig fuzz of gewoon dikke witte mat — alleen als close-up cam het goedkeurt
- Potplanten bij deur: `potted_plant_02/04` (geen calathea/anthurium buiten!)
- GN-heg: blaadjes uit `assets/polyhaven/models/shrub_03_2k.blend` (bewezen methode, Distribute outward normals)
- Bomen: `assets/sketchfab/trees/five_birch_trees_pack_lowpoly_lods_gltf` + `pine_tree_trio_free_download_gltf` — NOOIT USD-bomen

## 8. Bouwfases (headless, per fase script + save + diag-render 1280×720/64)
| Fase | Script | Inhoud |
|---|---|---|
| P1 | `build_camelia_bad_p1.py` | GLB-cam weg, materialen (build_clean_wood), grasgrond, HDRI, hero-camera |
| P2 | `build_camelia_bad_p2.py` | GN-heggen + 3 bomenringen + berkencluster |
| P3 | `build_camelia_bad_p3.py` | Vlonder, **dompelbad proceduraal**, trapje, stapstenen-pad |
| P4 | `build_camelia_bad_p4.py` | Lantaarns + interieurlicht + handdoeken + bank + houtstapel + potten |
| P4b | inspectiecams | 4 close-ups: bad, deurzone, veranda, vlonder — GLTF-props checken |
| P5 | `build_camelia_bad_p5.py` | Stoom-volume test, validate_scene + audit, 1080p preview |
| P6+ | fixes na feedback | daarna pas finale 2560×1440 |

Run: `& "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" -b --python build_camelia_bad_pN.py`

## 9. Risico's & fallbacks
- **Dompelbad proceduraal** is het grootste risico → eerst los testen in P3-diag met close-up; duigen = array van gebogen planken rond cilinder, banden = torus geschaald. Fallback: rechthoekige houten "soaking tub" (simpeler) of focus verleggen naar vuurkorf (`stone_fire_pit`) + lantaarns.
- **Stoom/volume** kan render duur of vlekkerig maken → density laag, en bij twijfel WEGLATEN (verwijderen mag, playbook).
- **Blue hour te donker** → exposure/HDRI-sterkte proben per crop, lantaarn-emissie opvoeren i.p.v. HDRI.
- Handdoeken/vacht lelijk in close-up → weglaten, bad + licht dragen de scene.

## 10. Validatie & render-trap
- Na elke fase: full-res crops van verdachte zones (thumbnail bedriegt — donkere scene!).
- `scripts/validate_scene.py` + audit (niets in cabin-bbox, niets >12 m).
- Anti-empty checklist (pad→deur, heg zichtbaar, boomwand boven heg, meubel zichtbaar, glas+chroom leesbaar).
- Preview 1920×1080/160 → **user-akkoord afwachten** → finale 2560×1440/240, adaptive 0.008, OIDN, texture_limit 2048, 16-bit PNG.

## Output
`pilots/Camelia-250x300-300-zijwand/style-hot-tub-premium/camelia_buitenbad.blend` + diag PNGs in dezelfde map.
