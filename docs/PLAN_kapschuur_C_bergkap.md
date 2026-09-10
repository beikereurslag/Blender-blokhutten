# PLAN — Kapschuur Scene C: "De Bergkap" (carport & berging, warme ochtend)

**STATUS (3 jul 2026): AKKOORD Beike op p4g-preview — FINALE gerenderd.** Trio compleet.
Beike-rondes verwerkt: fiets weg, oost-heggen weg + brede oprit 3.8m (auto kan de tuin
uit), zuidborder ingekort (neus vrij), vergeten p2-Border_oost verwijderd (stond dwars
over de oprit). Sedan-saga: witte "boog op dak" bleek het beugel-fietsenrek erachter
(parallax!) — camera-ray-methode staat in memory. Sedan 2x herimporteerd (trim-schade),
lak = schone zilvergrijze Principled op alle Car Paint-varianten. Dak = EPDM.

Concept: `kapschuren/SCENE_CONCEPTS.md` (scene C). Carport annex nette buitenberging —
auto droog, modern/urban, warm douglas als eerlijk alternatief voor zwart aluminium.
Sfeer (BESLIST): zachte warme ochtend met lichte nevel, AgX Base Contrast.

## Basis
- Model: `kapschuren/glb/Kapschuur platdak 500x300.glb` (cm → 0.01x, center voetprint → origin).
  Oriëntatie/deel-namen proben in p1 (welke zijden dicht).
- Douglas 8K per onderdeel als A/B (palen verticaal, balken horizontaal, gevel douglas-rabat).

## Verankering vanaf het begin (memory-lessen A+B)
- **Rechte oprit** (vlak + klinker-texture, GEEN losse steentjes in laag licht) loodrecht
  op de open beuk; breed genoeg voor de auto (~2.4m). Nooit op een paal aan laten lopen.
- Lage heg helemaal rondom (les A-feedback!) met opening voor de oprit; bomenwal achter
  (crisp platte daklijn tegen vol groen), rughaag dichtbij.
- Écht sprietgras via grass_lib (mask cell 0.22, drempel 0.95, kill-zone om oprit;
  Mist_Rig verbergen tijdens raycast).
- Grond mat (rough 0.93 / spec 0.08) tegen glans in laag ochtendlicht.

## Vloer & props
- Vloer: grootformaat betontegels strak — vlak met `square_concrete_pavers` (polyhaven).
- Hero: **generic_sedan_car** (v2.93-blend, leesbaar) in de beuk; bike_rack_7 (FBX) rechts.
- **BlenderKit-lijst voor Beike** (niet op schijf): fiets, regenton, gieter(s),
  gereedschaps-wandrek/pegboard, deurmat + laarzen, evt. opbergkast.
- GEEN kandelaar; groene cc0-kruiwagen blijft verworpen.

## Camera & licht
- Camera 35mm, laag ~1.3 m, ~45°: (6.6, −5.2, 1.3) → (−0.4, 0.2, 1.15); voorste paal +
  auto als foreground-anker.
- `cl.setup_light('ochtend', azimuth −40)` (kiara dawn HDRI, 4500K elev 10, AgX Base
  Contrast), `cl.overhang_fill` zacht; haze laag (fog-les: To Min ~0.0012, aniso 0.35).

## Fases
| Fase | Script | Inhoud |
|---|---|---|
| p1 | build_kapschuur_c_p1.py | GLB+douglas, betonvloer, oprit, gras-grond, licht, camera → diag |
| p2 | build_kapschuur_c_p2.py | Bomenwal + heg rondom + sprietgras + grasranden → diag |
| p3 | build_kapschuur_c_p3.py | Sedan + bike rack + schijf-props → inspects; BlenderKit-lijst |
| p4/p5 | build_kapschuur_c_p4/5.py | Styling + audit + preview → **Beike-akkoord** → finale |

Blend: `kapschuren/scenes/kapschuur_C_bergkap.blend`, diags in `kapschuren/scenes/diag/`.
