# Renders 2.0 — fase 0: stand opgenomen (26-10-2026)

Invoer voor `docs/PLAN_renders2_2026-10.md`. Alleen gelezen, niets in de repo gewijzigd.

## Aanleiding

AI-omgevingsproef (`pilots/ai_omgeving_2026-10/VERSLAG.md`, `contactvel.png`): ComfyUI maakte bomen en haag
overtuigend (rechterbeeld = referentie voor hoe bomen en haag eruit moeten zien), maar het is beeldbewerking per
camera, dus onbruikbaar voor andere hoeken en film. Beike koos: "de scene zelf verbeteren. maar het hoeft niet echt
te verbeteren zijn, ze mogen bijna helemaal opnieuw." Het tuinconcept De Regentuinkamer (`docs/PLAN_astra_garden.md`,
goedgekeurd 10-09) blijft het ontwerp; de uitvoering gaat opnieuw.

## Git-stand (alleen gerapporteerd)

171 statusregels: 7 gewijzigde tracked bestanden (o.a. `stap2_dressing.py` +113 regels, `cabin_lib.py`,
`PLAN_astra_garden.md`, `result.json`) en 164 untracked items, samen ~1.740 bestanden en ~68,8 GB. Daarvan 61
.blend-bestanden (~68 GB: G1-versies, START_Jasmijn, zijwand-pilots, S1–S8, B10–B15), 1.233 PNG's (0,34 GB),
54 scripts, 137 logs, rescue-map `_drive_rescue_2026-09-11` (2,5 GB), `_tekentool_2026-10` (311 MB),
`source-glbs-new` (145 MB). Risico: een `git add .` zou 68 GB aan blends meenemen. Niets aangeraakt.

## Oude scène `regentuinkamer_G1_v20_zuid.blend`

| Categorie | Wat erin zit | Bron | Waarom het niet overtuigt |
|---|---|---|---|
| Hut | oud april-model uit `pilots/base/Jasmijn-300x250-250.blend`; Cabin_Root (10.263, 9.25, 0) rot 180°; envelop x 7.300–13.226, y 7.796–10.704 | `source-glbs/Jasmijn 300x250 + 250.glb` (april) | niet het tekentool-model; G1 is op 14-10 niet omgezet |
| Dennen | 263 stuks (RingPine 75, Zuid_Pine 188), 54 meshes per boom, alle LOD's tegelijk aan | `pine_tree_01_2k` via `cl.pine_rings` | dunne kruinen, roze lucht schijnt erdoor |
| Loofbomen | 5 coulissen + 7 zuidbomen, 1 berk buiten beeld | `island_tree_01/02/03` ×1,6–3,06 opgeschaald, BK `Birch_tree` | grote bladkaarten met gaten, kale tak linksboven |
| Haag | 5 tuinhagen + 8 veldhaagstukken | kubus + GN-scatter van één `shrub_03`-takje (density 650) | herhalend blaadjespatroon, geen geschoren haag |
| Gras/grond | Ground_Humus 46×44 m, Ground_Far 900 m, GN-gras met 3 laagpoly-pluimen | eigen noise-materialen, procedureel | egaal en laagpoly |
| Pad | lint 1,2 m, slate_floor_02 PBR, schort + kapvloer | `cl.ribbon_path` | vlak lint leest als plaat; alleen laatste 2,2 m recht |
| Borders | 12 geranium, 8 brandnetel, 15 maagdenpalm, 10 varens, 14 pollen, 12 mosstenen, 5 stapstenen | PH, BK, Sketchfab | in heldenbeeld nauwelijks zichtbaar; verspreid, geen drifts |
| Meubels | 2 teak-fauteuils (GLB Creator), side_table_01, schaal | GLB Creator, PH | echte assets; tafel is vervanger |
| Water | één vlak `Water_Plas_0` z −0,10 | eigen materiaal | zwarte schijf, geen rand of spiegeling |
| Lucht | `kiara_1_dawn_2k`, 0,7, mist-box 0,0018 | PH | roze dageraadlucht tussen dunne dennen |
| Zon | 5,0, 3500 K, 16° hoog, azimut 170° | `cl.setup_light` + handwerk | staat ~18° naast recht achter de HeroCam → vlakke voorgevel |
| Camera | HeroCam (8.0, 0.7, 1.55), rot (90, 0, −8), 33 mm, shift_y −0,03, f/5.6 focus 7,38 m; WalkCam 12 keys, 960 frames | | |
| Render | Cycles GPU, AgX Base Contrast, exposure 0,5 | | |

Probe-data: scratchpad `probe/g1_probe.json` en `g1_probe2.json` (sessie-scratchpad, niet in de repo).

## De juiste hut

Actuele tekentool-GLB: `source-glbs-new/2026-09-11/Jasmijn 300x250 + 250.glb` (meters). Bestaande omzetroute:
`scripts/swap_cabin_tekentool.py --glb <GLB> --draai180 --blend <uit>` (via `scripts/import_tekentool_glb.py`),
daarna `fix_cabin_boards.align_courses()` (planken 130 mm). De deur zit niet in de tekentool-GLB: `.DEURBASIC`,
greep en fundering komen uit de oude base.

## Assets op schijf (samenvatting)

- **Goed gevuld:** bomen (PH fir/pine/island/tree_small_02, BK berk ×2, olijf), heesters (PH shrub_01–04, BK
  beukenhaag-wall/-block, Sketchfab bloeiende struiken), borders (BK geranium, hortensia, lavendel, dahlia; PH varen,
  maagdenpalm, gazania), bestrating (PH slate, paving_stones_64, patio_tiles, cobblestone_07, gravel; ambientCG
  PavingStones125A; BK stapstenen), meubels (GLB Creator teak, BK lounge, PH), 26 HDRI's (o.a. eilenriede_park,
  cloudy_vondelpark, symmetrical_garden, kiara_7_late-afternoon, kloofendal_overcast).
- **Dun:** graszode-texturen (alleen PH leafy_grass, sparse_grass), haag-modellen (geen buxus/taxus/liguster/haagbeuk),
  fruitbomen, water/vijver/regenbekken.
- **Valkuilen:** `painted_grass` is een placeholder van 1 KB; meerdere Sketchfab-gltf's verwijzen naar lege
  texturemappen; mapnamen in `blenderkit/` kloppen soms niet (vloerkleed = steen, duingras = pijnboom).

## Kosten AI-3D (niets uitgegeven)

| Dienst | Saldo | Tarief | Licentie |
|---|---|---|---|
| 3D AI Studio | niet op te vragen: API-sleutel verlopen (`API_KEY_EXPIRED`), omgevingsvariabele leeg | 20–70 credits per model (Prism 3.1: 35); packs $0,011–0,017 per credit → ~$0,40–0,60 per model | output privé, commercieel toegestaan (FAQ) |
| GLB Creator (Meshy) | geen saldo-endpoint; ~2.800 op 16-07, minstens 270 verbruikt → vermoedelijk ruim 2.000 | 30 credits per model, retexture 10 → ~$0,40–0,60 | betaald plan: commercieel |
| PolyHaven | gratis | — | CC0 |
| ComfyUI (lokaal, SDXL) | gratis | ~30 s videokaart per beeld | CreativeML Open RAIL++-M |
