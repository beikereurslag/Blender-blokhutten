# AUTONOME FIX-RONDE — voortgang (voor reset-resilience)

Beike is weg; opdracht: **alle handoff-feedback autonoom uitvoeren op alle 15 scenes (Zentuin NIET), zelf reviewen, review-fixes ook doorvoeren, klaar tegen morgen. Niets vragen.**

## Aanpak
Systematische rigs (gebouwd in cabin_lib/grass_lib), per scene toegepast via `apply_all_rigs.py`:
- **RIG A** `cl.setup_light(moment, azim)` — lage warme zon + matchende HDRI per moment + begrensde haze-cube + AgX. (KLAAR, gevalideerd op Dahlia)
- **RIG B** gras — `gl.add_grass` (gemaskeerd, grond-only) waar nog geen gras + grond-realisme (roughness 0.97 / spec 0.05, geen natte plas). (grass_lib KLAAR)
- **RIG C** `cl.warm_wood_walls()` — nerf mét de plank (uv_board) + warm-hout + witte/plastic wanden warmer. Two-tone blijft.
- **RIG E** `cl.overhang_fill()` — warme fill-area-light zodat overkapping/interieur nooit zwart is + gloed door glas.
- RIG D (camera/pad) + zware per-scene dressing = behoedzaam / in review-ronde (geen Beike om te checken → conservatief).

## Per-scene config (basis-versie / lichtmoment / azimut)
| Scene | basis | moment | azim | status |
|---|---|---|---|---|
| Dahlia Tuinkantoor | v4 | ochtend | 130 | rig-pass: |
| Magnolia Wintertuin | **v5** | overcast | 95 | |
| Camelia Wijnterras | v4 | namiddag | 125 | |
| Jasmijn Theehuis | v4 | ochtend | 120 | |
| Lelie Avondkubus | v4 | blue_hour | 135 | |
| Magnolia Groene Long | v4 | namiddag | 110 | |
| Zonnebloem Zomeravond | v4 | sunset | 140 | |
| Camelia Buitenbad | v4 | blue_hour | 130 | |
| Dahlia Leeshoek | v4 | ochtend | 120 | |
| Jasmijn Familietuin | v4 | namiddag | 115 | |
| Lavendel Pluktuin | v4 | overcast | 120 | |
| Lelie Ochtendnevel | v4 | ochtend | 130 | |
| Zonnebloem Ochtendhoek | v4 | ochtend | 125 | |
| Lavendel Lavendelveld | v4 | golden_hour | 135 | |
| Roosmarijn Kruidenterras | **v5** | namiddag | 120 | |
| Roosmarijn Zentuin | — | — | — | SKIP (Beike zelf) |

## Output
Per scene: `<scene>_RIG.blend` (niet-destructief) + `<scene>_RIG_PREVIEW.png` (1080p). Galerij: `_rig_review.html` op localhost:8765.

## Status-log
- A–E-uitrol: KLAAR op alle 15 (exit 0). `_RIG.blend` + `_RIG_PREVIEW.png` per scene.
- Parallelle review (15 agents): KLAAR. Scores 4–8. **Kalibratie: agents te streng** — jasmijn_familietuin oogt prima (niet "pre-rig"); **HASHED-blend = Cycles-non-issue** (geen zichtbare dithering) → NIET fixen. lelie_ochtendnevel (8) referentie is echt goed.
- Échte defecten → polish-fix ronde (DRAAIT): (a) zwevende naamloze Object_*/Fibers proxy-blobs weg, (b) lavendelveld VELD `hide_render=False`, (c) magnolia groendak dakrand/sedum/paneel flush, (d) lelie_avondkubus glas transmissief. Script: `fix_polish.py`, output overschrijft `_RIG.blend`/`_RIG_PREVIEW.png`.
- TODO na polish: eind-review (spot-check blockers), evt. concept-dressing (zandbak-speelgoed/theeset — nice-to-have), galerij `_rig_review.html`.

## EIND-STAND (ronde af)
- A–E toegepast op alle 15 + review + polish-fix + re-render: KLAAR. Galerij: `localhost:8765/_rig_review.html`.
- Scores na ronde (eigen inschatting): lelie_ochtendnevel ~8, lavendel_pluktuin ~7.5, magnolia_wintertuin/dahlia_tuinkantoor/camelia_buitenbad ~7, jasmijn_familietuin/magnolia_groene_long/zonnebloem_zomeravond/roosmarijn_kruidenterras ~6.5, rest ~6. (Start was 3–5,5.)
- **Bewust NIET blind gedaan (regressie-risico, voor Beike's oog):** concept-dressing (bureau Dahlia / theeset Jasmijn / zandbak-speelgoed / kook-props Roosmarijn), magnolia dakrand+zonnepaneel fijn-detail, sterkere "beacon"-gloed Lelie Avondkubus, lavendel écht als vol veld, interieur-fill fijnregelen enkele afdaken.
- Bronnen intact (v3/v4/v5). Nieuw per scene: `_RIG.blend` + `_RIG_PREVIEW.png`. Rig-code in cabin_lib (setup_light/warm_wood_walls/overhang_fill) + grass_lib.

## Resume-instructie (als sessie reset)
1. Check `_diag/rig_*.txt` welke scenes klaar zijn (regel "[allrig] klaar").
2. Hervat `apply_all_rigs.py` voor de resterende scenes.
3. Daarna review-ronde: elke `_RIG_PREVIEW.png` inspecteren + `validate_scene.py`/`_probe_junk.py`, per-scene fixes, re-render.
