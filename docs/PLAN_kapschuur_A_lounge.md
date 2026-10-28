# PLAN — Kapschuur Scene A: "Avondgloed Loungekamer" (vlaggenschip)

**STATUS (3 jul 2026, ~10:55): AKKOORD van Beike — FINALE rendert** (p7-preview met Beike's
eigen GUI-tweaks: camera dichterbij/frontaler). Feedbackronde p6/p6b/p6c/p7 verwerkt:
structuur 180° gedraaid (hoge open zijde voor), fauteuils naar voren, vuurschaal weg,
lage heg rondom, tafel/stoelen naar rechts, écht sprietgras (grass_lib, mask cell 0.22,
drempel 0.95 + kill-zone om pad). Les: gras-mask drempel 0.5 laat randcellen door →
0.85-0.95 + expliciete kill-zone om hardscape.
Fixes onderweg: p1b klinker-texturemap zit in submap `\textures` + schort als vlak; p2b
understory -X dekt Venice-straat af, HDRI rot 150; p3b Sofa_01 = antieke salonbank →
2x modern_arm_chair_01, egg chair-positie, lantaarn uit B-blend (4k-blend = Blender 5.0);
p5b waterig gras → M_PBR_GrassRock rough 0.93/spec 0.08. Fog: To Min 0.0016, aniso 0.35.
NB: BlenderKit is er nu — bij Beike-feedback op meubels eerst daar zoeken.

Concept: `kapschuren/SCENE_CONCEPTS.md` (scene A). Overdekte lounge-tuinkamer onder het
asymmetrische dak, golden-hour zomeravond, godralen tussen de palen, vuurschaal gloeit op.

## Basis
- Model: `kapschuren/glb/Kapschuur asymmetrisch 600x300.glb` (cm → 0.01x, apply, center:
  voetprint (3.0, 1.5) → origin). Deel-namen + open/dichte zijden proben in p1 (asymmetrisch
  dak: oriëntatie eerst vaststellen op de p1-diag!).
- Materialen als scene B: douglas.jpg 8K per onderdeel (palen verticaal via mapping-rot,
  balken/dek horizontaal), douglas-rabat.jpg op gevelbekleding. Terras-mat les: naam checken.

## Verankering VANAF p2 (lessen scene B — zie memory feedback-scene-verankering-lessen)
- **Recht pad** (vlak + klinker-texture, GEEN losse steentjes) loodrecht op de entree-opening
  tussen twee palen; nooit op een paal aan laten lopen; ingang ~1m+ breed.
- Borderhagen (0.42) rond het klinker-schort met gat bij pad-mond en doorloop; rughaag 1.75m
  dicht achter de structuur; grasranden knippen waar het pad kruist.
- Entreepot flankeert, nooit in camera-verlengde van het pad. Verhaal-props: mand, plaid.
- GEEN kandelaar. Kruiwagen verworpen.

## Layout (wereld)
- Vlonder `cl.plank_deck` onder het dak (x −3.05..3.05, y −1.55..1.55, top 0.05).
- Klinker-schort (échte klinker_strip-steentjes, vol in beeld = ok) als 4 randstroken
  rondom de vlonder tot ±(3.8, 2.4), top 0.03.
- Lounge: Sofa_01 rug naar +Y, coffee_table_round centraal, relax chair links,
  stone_fire_pit voor de sofa richting open zijde, lantaarn/boek/mok/plaid.
- Festoon langs de open (hoge) zijde.

## Camera & licht
- Camera 35mm @ ~(7.2, −5.6, 1.4) → (−0.5, 0.3, 1.35); nabije hoekpaal rechts als frame,
  diagonaal door de open vakken. DoF f8.
- `cl.setup_light('sunset', azimuth −55)` = venice_sunset HDRI + lage 3000K zon →
  strijklicht onder het dakvlak door; `cl.overhang_fill` warm; godralen via Mist_Rig
  (density p5 tunen, fog-les B: To Min ~0.0008-niveau, anisotropy 0.35).
- Backdrop: 3+ boomringen, hemel dicht, doorkijk-vak links (−X) voor avondlucht.

## Fases
| Fase | Script | Inhoud |
|---|---|---|
| p1 | build_kapschuur_a_p1.py | GLB+douglas, vlonder, klinker-schort, licht, camera → diag (oriëntatie-check!) |
| p2 | build_kapschuur_a_p2.py | Verankering: pad/borders/rughaag/grasranden + boomringen + doorkijk → diag |
| p3 | build_kapschuur_a_p3.py | Lounge-meubels + inspects |
| p4 | build_kapschuur_a_p4.py | Aankleding + festoon + inspects |
| p5 | build_kapschuur_a_p5.py | Audit + godralen-tuning + 1080p preview → **Beike-akkoord** → finale |

Blend: `kapschuren/scenes/kapschuur_A_lounge.blend`, diags in `kapschuren/scenes/diag/`.
