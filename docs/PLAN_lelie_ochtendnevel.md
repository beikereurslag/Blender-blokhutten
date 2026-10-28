# Plan — Lelie 400x250+300+zijwand "De Ochtendnevel" (2026-06-12)

## 1. Concept & waarom dit origineel is
- Lelie heeft de Engelse-cottage-hero (weelderig, golden). Het tweede gezicht: **de natuurtuin bij dageraad**.
- **Scene-idee dat nog nooit is gedaan: ochtendmist over een wilde bloemenweide.** Vroege dageraad, laaghangende nevel tussen de bomen, een wildflower-meadow i.p.v. gemaaid gazon, een houten vlonderpad naar de deur. Stijl: forest-wilderness (bestaat als batch-categorie, nooit als hero). Persona: De Rust-Zoeker / natuurliefhebber.
- **Niemand heeft volumetrische mist gebruikt** — dit wordt het atmosferische beeld in de serie (MIR-achtig: painterly, low contrast). Ook de wildflower-meadow (klaprozen, paardenbloemen, heliophila los door hoog gras) is nieuw — alle eerdere tuinen waren aangelegd.
- Onderscheid t.o.v. Camelia scandi-forest: daar een nette scandi-tuin ín een bos; hier **de weide als rewilded tuin** met mist als hoofdrolspeler.

## 2. Model-feiten (geprobed 12 jun, `pilots/base/Lelie-400x250-300-zijwand.blend`)
- Footprint **7.43 × 2.91 m**, hoogte 2.34 m, plat dak (`flatroof-98-*`).
- Deur **+Y-voorzijde**, X 0.73..2.24; veranda links, pole-0 op (−3.44, 1.18), open naar +Y.
- GLB-camera aanwezig → weg in P1. Materialen leeg → `build_clean_wood`.

## 3. Stijl & materialen (alleen echte producttextures)
Forest-wilderness = eerlijk, naturel hout:
- Wanden: `assets/blokhutwinkel-textures/8192/douglas.jpg` (naturel)
- Balken/palen: `douglas-rabat.jpg`
- Deur: `hardhout-deuren-ramen.jpg`
- Dak: `epdm.jpg`, rand `staalpannen-antraciet.jpg`
- Vlonderpad: `douglas.jpg` vergrijzend getint (mix 0.2 naar `#8B8378`) — alsof het er al jaren ligt
- Mos-accenten op stenen (`moss_01`), NIET op het dak (product blijft schoon leesbaar).

## 4. Scene-layout (coördinaten; cabin op origin, voorzijde +Y)
| Element | Positie | Detail |
|---|---|---|
| Grond | 34×34 m | basis `forrest_ground_01` (polyhaven texture) gemixt met gras — geen golfbaan-groen |
| **Wildflower-meadow (focal-veld)** | Y 3..12, X −9..8 | hoog gras (weed_plant_02) + klaprozen (`field_poppy`) + `dandelion_01` + `flower_heliophila` — losse drifts, GEEN rijen (contrast met Lavendel-veld) |
| Vlonderpad | 0.9 m breed, Y 10 → deur, licht slingerend | douglas-planken dwars, 5 cm boven maaiveld |
| Veranda | bank + plaid | `painted_wooden_bench_2k` + plaid-plane |
| Boulder-groep | (4.5, 5.5) 3 stenen + mos | `boulder_01`, `stone_01`, `moss_01` |
| Vogelvoeder op paal | (−4.5, 4) | `small_wooden_bird_feeder_gltf` |
| Berkengroep | (6, −1) 3-stam + (−6.5, 2) 2-stam | birch pack |
| **Mist-volume** | box X −15..15, Y −5..18, Z 0..2.2 | principled volume, density 0.008-0.02, hoogte-gradient (dichter bij grond) |
| Bosrand | 3 ringen 12/16/22 m — DICHTER dan andere scenes | pine + birch + maple; mist heeft bomen nodig om tegen af te tekenen |
| Heg | géén strakke heg — bosrand IS de grens | wel lage shrub-drifts (shrub_01/02/04) tussen weide en bos |

## 5. Compositie & camera
- 35 mm, 1.55 m (iets lager — door het hoge gras kijken), vanaf voor-rechts **(8.5, 10.5, 1.55)**, target (−0.4, 0.6, 1.3).
- Vanaf (+X,+Y): cabin links in de mist-laag, vlonderpad start rechts-onder in frame en slingert naar de deur.
- Drie lagen diepte is hier ALLES: voorgrond scherp gras/klaprozen → midden cabin half in nevel → achter boomwand die in mist vervaagt. Geen harde skyline nodig: de mist sluit het beeld.
- Zon laag ACHTER de bomen rechts → god-rays door de stammen (volumetrie vangt het licht).

## 6. Licht & sfeer (dageraad ~06:15)
- HDRI: `assets/polyhaven/hdri/kiara_1_dawn_2k.hdr`, strength 0.7.
- Zon: 3500K erg warm, energie 2.5, elevatie **6-9°**, van rechts-achter door de bomenring → lichtschachten in de mist.
- Mist: principled volume in box (zie layout); density laag beginnen (0.008) en in crops opbouwen — te dik = grijze soep, te dun = onzichtbaar. Anisotropy 0.3 (forward scatter voor de god-rays).
- Filmic, **Medium Contrast** (lager dan standaard — painterly), exposure 0.4.

## 7. Props & asset-paden
- Klaprozen: `assets/sketchfab/flowering_bushes/field_poppy_vmcobd0ja_ue_raw`
- Hoog gras: `assets/polyhaven/models/weed_plant_02_2k.blend` (cluster-donor fix!)
- Paardenbloemen: `dandelion_01_2k.blend`; heliophila: `flower_gazania`/`flower_heliophila`
- Lage shrubs bosrand: `shrub_01/02/04_2k.blend`
- Bank: `painted_wooden_bench_2k.blend` (vergrijzen)
- Stenen + mos: `boulder_01`, `stone_01_2k.blend`, `moss_01_2k.blend`
- Voederhuisje: `small_wooden_bird_feeder_gltf`
- Bomen: `five_birch_trees_pack` + `pine_tree_trio` + `maple_tree_scan` — NOOIT USD

## 8. Bouwfases (headless, per fase script + save + diag 1280×720/64)
| Fase | Script | Inhoud |
|---|---|---|
| P1 | `build_lelie_nevel_p1.py` | GLB-cam weg, douglas-materialen, grond-mix, HDRI+zon laag, camera |
| P2 | `build_lelie_nevel_p2.py` | Dichte bosrand (3 ringen) + berkengroepen + shrub-drifts |
| P3 | `build_lelie_nevel_p3.py` | Vlonderpad + boulder-groep + meadow-scatter (gras eerst, dan bloemen-drifts) |
| P3b | meadow-check | crops: dichtheid, kleurbalans klaprozen, pad-leesbaarheid |
| P4 | `build_lelie_nevel_p4.py` | Bank + plaid + voederhuisje + **mist-volume + god-ray-tuning** |
| P4b | mist-trap | 3 diag-renders met density 0.008 / 0.014 / 0.02 → beste kiezen |
| P5 | `build_lelie_nevel_p5.py` | validate + audit + 1080p preview |
| P6+ | fixes na feedback → finale | |

## 9. Risico's & fallbacks
- **Volumetrie + 8GB VRAM**: volume-box klein houden (niet de hele 34 m), tile-size checken, texture_limit 1024 in diags. Crasht/te traag → mist faken met 2-3 semi-transparante gradient-planes tussen boomlagen (oude matte-painting-truc) — beslis in P4b.
- **Mist dempt alles** → cabin moet leesbaar blijven: density-gradient zo dat gevel boven 1 m relatief vrij is; deurglas mag zwak warm licht krijgen (1 area light binnen) als anker.
- **Meadow-scatter VRAM**: drifts in zones i.p.v. full-field scatter; achterste weide alleen hoog gras zonder bloemen.
- **Klaproos-rood clipt** in warm licht → albedo dempen, crop-check.
- Pad slingert te veel → max 2 zachte bochten, anders leest de route niet (anti-empty checklist eist pad→deur).

## 10. Validatie & render-trap
- Audit per fase; bekende false-positives benoemen (ground-naam, gltf "floating" delen).
- Anti-empty checklist — uitzondering gemotiveerd: geen strakke heg (bosrand is de erfgrens), wél continue groene wand.
- Preview 1080p/160 → user-akkoord → finale 2560×1440/240; bij finale extra crops op mist-banding (16-bit PNG helpt).

## Output
`pilots/Lelie-400x250-300-zijwand/style-forest-wilderness/lelie_ochtendnevel.blend` + diag PNGs.
