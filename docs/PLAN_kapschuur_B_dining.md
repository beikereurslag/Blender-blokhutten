# PLAN — Kapschuur Scene B: "Tafelen onder het Zadeldak"

Concept: `kapschuren/SCENE_CONCEPTS.md` (scene B). Covered dining onder de zadeldak-kapschuur,
warme namiddag, gedekte tafel, doorkijk door de open kopgevel.

## Basis
- Model: `kapschuren/glb/Kapschuur zadeldak 600x400.glb` (cm → 0.01x, apply, dan gecentreerd:
  voetprint-center (3.0, 2.0) → wereld-origin). Structuur ≈ x −3.24..3.24, y −2.37..2.37, nok ~3.4 m.
- Palen op x ≈ ±2.905 / y ≈ ±1.93, muurplaat-top ~2.37, trekbalken ~2.2.
- **GLB heeft platte kleur-mats** (generator) → vervangen door échte producttextures:
  `douglas.jpg` met nerf-richting per onderdeel (palen verticaal via mapping-rotatie, balken/dek
  horizontaal), `kdi_potdeksel_zwart.jpg` op gevelbekleding. NIET uv_board_textures (geen UV-planken).

## Layout (wereld-coördinaten)
- Klinker-terras `cl.klinker_strip`: x −3.5..3.5, y −2.6..2.6, top 0.03 (floor_klinkers-warm).
- Eettafel-set (wooden_dining_table_set.glb) centraal onder de nok, iets naar −X.
- Bank (simple_wooden_bench) aan de camera-zijde van de tafel; stoelen set aan de andere kant.
- Dressoir (WoodenTable_03) tegen de achterste palenrij (+Y), potted_plant_01 x2 flankeert
  de open kopgevel (+X), kruidenpotten bij een paal.
- Tafel-styling: Lantern_01 + brass_candleholders + brass_goblets + carved_wooden_plate +
  bananas + water carafe; linnen loper = plane + rough_linen.
- Festoon langs de voorste muurplaat (y ≈ −1.93, z ≈ 2.3).

## Camera & licht
- Camera 35mm @ (~7.4, −6.4, 1.45) → target (−0.4, 0.4, 1.4): 3/4 die de gable-driehoek (+X-kop)
  én de lange open zijde toont; doorkijk door de kopgevel.
- `cl.setup_light('namiddag', azimuth −35)` (zon van voor-links → raking light op dak-onderkant),
  `cl.overhang_fill` @ (0,0,2.4) — onderdak mag geen zwart gat zijn. HDRI spaichingen (namiddag).
- Bomen: eigen spots — rug +Y (achter structuur vanuit camera), flanken −X en +X-ver, pines
  `tree_rings_clustered(full_only=True)` + maple-scan als featureboom links.

## Fases
| Fase | Script | Inhoud |
|---|---|---|
| p1 | build_kapschuur_b_p1.py | GLB import/schaal/center, douglas-materialen, gras, klinker-terras, licht-rig, camera → diag |
| p2 | build_kapschuur_b_p2.py | Bomenringen (sky dicht) + featureboom + gras-randen → diag |
| p3 | build_kapschuur_b_p3.py | Meubels: eetset, bank, dressoir, planters → diag + inspect-cams |
| p4 | build_kapschuur_b_p4.py | Tafel-styling + festoon + kruidenpotten → diag + inspect |
| p5 | build_kapschuur_b_p5.py | Audit + fixes + 1080p preview → **user-akkoord** |

Blend: `kapschuren/scenes/kapschuur_B_dining.blend`, diags in `kapschuren/scenes/diag/`.
Run: `& "C:\Program Files\Blender Foundation\Blender 4.1\blender.exe" -b --python <script>`
