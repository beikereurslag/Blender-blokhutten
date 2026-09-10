# Blender Blokhutten — Vault Compendium

*Alle vault-kennis over Blender-archviz én 3D-print van de tuinhuizen/blokhutten, geëxtraheerd uit ~90 wiki-notities op 2026-07-01. Samengevoegd door 14 thema-agents + synthese.*

Bron-vault: `C:/Users/beike/Desktop/Icloud/iCloudDrive/Vault/Claude/wiki/`

## Inhoud

- [TL;DR — Golden rules & huidige status](#tldr--golden-rules)
- [1. Build workflow & playbooks](#1)
- [2. Scene composition & dressing](#2)
- [3. Camera & composition](#3)
- [4. Lighting & atmosphere](#4)
- [5. Materials & shaders](#5)
- [6. Vegetation & scattering](#6)
- [7. Render optimization & batch pipeline](#7)
- [8. Compositing & color grading](#8)
- [9. Photorealism / anti-uncanny-valley principles](#9)
- [10. MCP, Python automation & plugin stack](#10)
- [11. Assets, inventory & garden styles](#11)
- [12. Project builds, lessons & garden-style research](#12)
- [13. 3D-print blokhutten (Blender to FDM)](#13)
- [14. Current project state (hot list & recent sessions)](#14)

---

My task is to write the TOP of a master reference — Markdown only, starting directly with the "## TL;DR — Golden rules" heading. This is a utilitarian document (a reference compendium header), so I'll deliver polished Markdown with real hierarchy, not an editorial web page. The task explicitly asks for Markdown output returned as my response, not an Artifact deployment.

Let me synthesize the three required sections from the 14 provided JSON theme sections.

## TL;DR — Golden rules

- **Headless CLI for every real render, never MCP** — save the `.blend` to disk first (`wm.save_as_mainfile`), use an absolute `-o` path, and set `scene.use_nodes = False` (an active compositor silently renders all-black); heavy scenes crash through MCP. [§7][§12]
- **Never World Volume Scatter on exteriors** — density 0.002 turns the whole Cycles 5.1 exterior pitch-black with no error; use a bounded volume box for fog instead. [§4][§7][§12]
- **Cycles hero settings are fixed**: 256 samples / adaptive 0.005, OpenImageDenoise with `RGB_ALBEDO_NORMAL` (omit and detail blurs), `texture_limit_render='2048'` and `use_persistent_data=False` to stay inside 8 GB VRAM on the RTX 3070 (~60–90 s at 1080p). [§7]
- **AgX, not Filmic** — default view transform `AgX` + look `Medium High Contrast`, exposure ~0.3; Filmic is the superseded 4.x-era default. [§4][§7][§8]
- **Blokhutwinkel GLB comes in cm** — apply 0.01× via `bpy.ops.transform.resize` with `INDIVIDUAL_ORIGINS` (ops respects hierarchy), then `transform_apply`; delete the embedded GLB camera. [§1][§11]
- **Fix wall grain direction with `cl.uv_board_textures()`** — GLB box-projection puts potdeksel/rabat nerf 90° wrong; re-map to mesh UV + FLAT so grain runs with the plank. Applies to every scene. [§5][§12]
- **Material source priority: real Blokhutwinkel 8K texture → Polyhaven/Sketchfab → procedural** — read the asset inventory before building any shader. [§5][§11]
- **Glass = Transmission 1.0, IOR 1.45, `transmission_bounces = 12`**; chrome Metallic 1.0 / Roughness 0.25; unhide the 13 hidden GLB door/glass/pot elements before rendering. [§5][§11]
- **Hedges = GN Poisson scatter (~500/m²) of a real Polyhaven shrub sprig**, instances aligned to the Distribute-Points `Rotation` output (outward normals, no donor-sphere); AI leaf-cards are deprecated. [§6][§12]
- **Scatter rules**: Poisson (not Random) distribution, random Z-rotation only, scale 0.7–1.3 (never 0), keep everything instanced — never Realize (200k grass ≈ 1.3 GB instanced vs 6 GB+ realized crash). [§6][§7]
- **Validate before "done" via code, never a thumbnail** — run `scripts/validate_scene.py` + the in-cabin/zombie-dim audit; probe numerically (bbox, view-layer, image `os.path.exists`) instead of guessing; thumbnails hide thin objects and off-frame trees. [§1][§7]
- **Watch the shared-data transform trap** — if `obj.data.users > 1`, `transform_apply()` corrupts all instances (700 m+ zombie meshes → black Cycles); move via `bpy.ops.transform.translate`, a parent empty, or `.data.copy()` first. [§7][§10]
- **Anti-uncanny non-negotiables**: cabin touches ground (dirt skirt), every plant sunk −2 cm with a dirt ring, grass intersects the plinth, AO contact under every prop, per-instance hue/scale variation, and a human-scale prop. [§9]
- **Camera hero recipe**: 35 mm, eye-level 1.5–1.65 m, 3/4 angle, cabin on a vertical third filling 50–65% of width, verticals kept plumb with `shift_y` (never tilt). [§2][§3]
- **Three-layer depth always** — foreground (0–4 m, soft), midground (cabin), background tree-line that occludes the sky; a horizon of sky-meets-bare-lawn is the "flying island" tell. [§2][§9]
- **Renders ship pure Blender Cycles — no AI upscaling/img2img in the gallery** (EU AI Act disclosure); log any AI-generated asset to provenance. Photoshop color/exposure/sharpen is fine. [§1][§9][§10]
- **Per new scene, invent an original concept** — follow the Cabin Hero Build Playbook (Fase 0 read-in → probe base blend → phased `build_<cabin>_pN.py` → inspect after every phase), don't replay a recipe. [§1]
- **3D-print: parametric route is current** (crisp rabat/large models) over voxel-remesh (small/dense, exact texture); ship `_printready.stl`, print Bambu P2S / PLA / 0.20 mm / 0% infill; dovetail gap 0.15 mm (measured). [§13]

## Current state snapshot

*(as of 2026-07-01, branch `weekend-renders`)*

- **All 16 hero scenes exist** at REALISM_PREVIEW level (8 primary + 8 alt-style), completed **20 jun 2026**; index at `docs/INDEX_scenes.md`. Final **2560×1440** renders are still to be selected. [§14]
- **Realism overhaul complete** — hand-built boxes replaced with real Polyhaven/Sketchfab props via `swap_lib.py` + per-scene `swap_*.py`. [§14]
- **Render-fix round 2 (24 jun)** in progress: 16 renders reviewed (v3 blends, gallery on `localhost:8765`); paths/blobs removed. Lighting overhaul plan = `docs/PLAN_lighting_overhaul.md`; PDF 12–16 feedback = `docs/ROUND2_feedback.md`. **Currently active on branch `weekend-renders`**: in-progress edits to Camelia scandi, Lelie cottage, Magnolia modern `.blend` files, Lavendel Pluktuin iterations, and `scripts/cabin_lib.py`. [§14]
- **Pending goal (do AFTER per-scene fixes)**: roll the Lelie Ochtendnevel "light-comes-through" look (volumetric haze + low warm sun + AgX) across all scenes. [§14]
- **One reference-quality FINAL exists**: `roosmarijn_modern_FINAL.png` (2560×1440, 512 samples, ~1:46 on RTX 3070) — the canonical render recipe. Roosmarijn Zentuin (#13) is Beike's own separate work — **do not touch**. [§14]
- **Cabin catalogue**: 8 product lines × 33 pilot variants (Camelia, Dahlia, Jasmijn, Lavendel, Lelie, Magnolia [only flat-roof], Roosmarijn, Zonnebloem); 3 full hero pilots + 30 batch; ~132 renders in the gallery. Magnolia is the modern Japandi flat-roof flagship. [§11][§14]
- **3D-print pipeline live on the PC** (since 25 jun): PC runs voxel-remesh/parametric build → `_printready.stl` **and** slices/prints itself (Bambu Studio + P2S); workdir `C:\Users\beike\blokhut-print\`. **All 75 door/window GLBs converted** (242 MB ASCII-OBJ → 8.3 MB binary, 0 errors, 25 jun); real DD-18-0050 door in `parametric_blokhut.py` — Camelia done, 7 cabins to go. [§13][§14]

## How the pieces fit — quick map

The end-to-end path from empty Blender to delivered asset:

1. **Concept + build** — invent an original per-cabin concept, then run the phased Cabin Hero Build Playbook: read-in → probe the `pilots/base/<Cabin>.blend` → one `build_<cabin>_pN.py` per phase, inspecting after each *(§1 Build workflow & playbooks)*.
2. **Import + dress** — bring in the GLB (0.01× scale, camera deleted), apply real Blokhutwinkel textures with the correct UV/Object coord per material *(§5 Materials, §11 Assets)*, then compose the camera and dress the garden per style *(§2 Scene composition, §3 Camera, §11 Garden styles)*.
3. **Populate** — scatter vegetation and hedges as instances via Geometry Nodes *(§6 Vegetation & scattering)*, driven live or headless through the MCP/Python control plane *(§10 MCP & automation)*.
4. **Light + atmosphere** — HDRI + synced sun + bounded volumetric haze under AgX *(§4 Lighting & atmosphere)*.
5. **Validate → render → grade** — code-audit the scene, headless-render in Cycles per the fixed recipe *(§7 Render optimization)*, then grade in the compositor *(§8 Compositing & color grading)* — always cross-checked against the anti-uncanny-valley checklist *(§9 Photorealism principles)*.
6. **Deliver two ways** — marketing renders/reviews *(§7, §8)*, or the parallel Blender→FDM print pipeline that turns the same cabin into a printable model *(§13 3D-print blokhutten)*.

---

Note: the MCP connectors listed in the system reminder (brand-voice, design, marketing plugins) require authorization and are unavailable in this non-interactive session — but none were needed for this task. The deliverable above is the compendium TOP as requested; it was not published as an Artifact since the request was for Markdown returned directly.


---

<a id="1"></a>
# §1. Build workflow & playbooks

### Two competing/complementary workflow models (know which applies)
- **Foundation-First** (2026-05-21, status: current) — build all cabins as base templates first, then dress per style. Base work is one-time-per-cabin, reused across all style renders (Foundation-First).
- **Cabin Hero Build Playbook** (2026-06-12, status: **critical — read ALWAYS first**) — the proven phased headless build for a single hero scene; validated on Dahlia "De Oogsttuin" (first zero-to-approved-hero in one session). Supersedes ad-hoc per-render building (Cabin Hero Build Playbook).
- **Production Checklist Cabin Render** (2026-05-21, status: critical) — strict step-by-step recipe with an AUDIT after every step, to avoid the "19-iteration chaos". Validated on Lavendel rebuild (Production Checklist).
- **Jasmijn Hygge Build Runbook (HOE)** (2026-06-10, status: ready-to-build) — the live-MCP execution HOW (per-step code + DoD gates), companion to the Jasmijn scene plan (Jasmijn Runbook).
- **Site-Specific Cabin Placement Workflow** (2026-05-22, critical) — render customer's cabin in their real garden from address+photos, inquiry-to-delivery 24h (Site-Specific).
- **Customer Render Review Workflow** (2026-05-22, critical) — structured feedback for 165-render delivery (Review Workflow).

### Cabin Hero Build Playbook — phase sequence (the proven flow)
- **Fase 0 Inlezen (mandatory before anything):** read skill `blender-archviz` (critical rules + audit script); vault: this playbook + Lavendel Build Lessons Learned + Cabin Hero Render Composition Rules + Garden Style Bible 5 Core Styles; explore repo `pilots/*/style-*` (most-recent root build-scripts = current patterns to reuse) + `assets/`; pick an **original concept** per Blokhutten Cabin Inventory — never reuse a recipe (Cabin Hero Build Playbook).
- **Fase 0b Probe the base-blend (never skip):** headless probe on `pilots/base/<Cabin>.blend` → bbox whole model + per material-group (closed part vs open veranda/canopy); door objects (`.DEURBASIC` etc.) → which side is front (door-Y/X = camera side); poles (`pole-*`), canopyWall users → open side; leftover GLB-camera (delete in p1); material names always `basetexture-firstLayer-*`. Dahlia example: closed part right (X 0.13..2.83), door +Y, veranda open +Y. **Axis warning:** camera from (+X,+Y) → world +X = LEFT in frame; check axis before concluding "off screen" (Cabin Hero Build Playbook).
- Write plan to `docs/PLAN_<scene>.md` (concept, layout coords, phase table). One script `build_<cabin>_pN.py` per phase that: opens scene-blend (p1 = base-blend) → builds one bounded thing → saves to same blend → diag-render 960×540 or 1280×720, 64 samples (Cabin Hero Build Playbook).
- Run: `& "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" -b --python build_X.py`

| Phase | Content (Cabin Hero Build Playbook) |
|---|---|
| p1 | GLB-camera removed; cabin materials (`build_clean_wood` BOX-mapping, real product textures); grass ground; HDRI+sun; hero camera |
| p2 | GN-hedges (real shrub_03 leaves) + tree rings (3 rings, occlude sky) + statement tree |
| p3 | Hardscape: path to door, terrace/deck, style-specific structures (grow-beds etc.) |
| p4 | Props + borders (gltf imports, flowering drifts) |
| p5 | Fixes + validation + preview render 1080p |
| p6+ | Fix-phases after user feedback, then final hero |

- **Crash-safe scripts:** save only at end → mid-crash leaves blend untouched, script restartable. Delete-loops: collect names first, then delete per name (else `StructRNA removed`) (Cabin Hero Build Playbook).

### The inspection loop (the real secret — after EVERY phase render)
1. **Thumbnails lie** — Read view is ~240px; thin/dark objects (trees! arch!) vanish. Make full-res crop (PowerShell `System.Drawing` rectangle-crop) of suspect region (Cabin Hero Build Playbook).
2. **Looks wrong → probe numerically, don't guess.** Small probe script: world-bbox, hide_render/viewport, view-layer membership, depsgraph instances, material images (`os.path.exists` on abspath, `packed_file`). Found this way: trees fine but outside frame; magenta = corrupt 94-byte file; "purple flowers" = missing texture (Cabin Hero Build Playbook).
3. **Verify props with close-up inspection cams** before "done": 4 temp cameras on prop zones (veranda, door zone, garden, focal), 800×600 / 48 samples. Caught: picnic table upside-down, spade as white stick, tilted bird-feeder. GLTF props often import upside-down — bbox numbers still look normal, only a render reveals it (Cabin Hero Build Playbook).
4. **Deleting is allowed** — dropping a broken prop beats a half-baked fix.

### Render trap / render-step ladder (Cabin Hero Build Playbook — current for hero)
1. Diag per phase: 960×540–1280×720, 64 samples.
2. Preview after p5: **1920×1080, 160 samples** → show user, await feedback.
3. Final hero (only after explicit OK): **2560×1440, 240 samples, adaptive 0.008, OIDN RGB_ALBEDO_NORMAL, texture_limit 2048, persistent_data off, 16-bit PNG, ~4 min on RTX 3070**.
4. After final: crop again on detail zones — the black-strip bug (wedge gap between flat wall-top and sloped roof, patched with wedge-plank `GableFiller` in wall material) only showed on the 1440p.

### Reusable code patterns (repo-root, Dahlia scripts) (Cabin Hero Build Playbook)
- `build_clean_wood()` — cabin material BOX/Object-mapping + bump (p1)
- GN-hedge node-group + `add_hedge()` (p2, originated in jasmijn-p2)
- **Cluster-donor fix** for polyhaven multi-variant blends (p2b) — NEVER `_duplicate_collection_at` directly on a tree/plant collection
- `import_gltf()` with cm-scale normalization via bbox-height + grounding on min-z (p4b/p6)
- `pbr_from_folder()` — polyhaven texture-map → Principled (p3)
- Procedural leaf-green (noise+ramp) for plants with missing textures (p8)
- Wedge `GableFiller` for roof-slope gap (p9)
- Prop-inspection cams (`probe_props.py`); full-res crop via PowerShell `System.Drawing`

### Foundation-First — base template contents (per cabin .blend)
- **IN base:** GLB geometry imported, scaled 0.01x (blokhutwinkel); cabin centered origin (0,0,0), base z=0; 6-8 cabin materials with blokhutwinkel textures; glass **transmission 1.0, IOR 1.45**, clean; chrome **metallic 1.0, R 0.25 brushed, anisotropic 0.6**; anthracite **M 0.85, R 0.45**; 13 hidden door elements unhidden (glass panels, handle, hinges, trims, pot plants) (Foundation-First).
- **NOT in base:** garden assets, ground/grass, HDRI world, sun, camera, render settings (Foundation-First).
- Material map: wall = luxehouse-onbehandeld OR luxehouse-grijs-gedompeld; door = hardhout-deuren-ramen (UV); roofBeam/board = douglas (UV); roofPlate = shingles-zwart OR epdm (UV); foundationBeam = beton (Object); poles = douglas (UV) (Foundation-First).

### Foundation-First — wall color per style
| Style | Wall texture | Reason |
|---|---|---|
| Scandi modern | luxehouse-grijs-gedompeld | dark grey-blue (Camelia signature) |
| Modern Japandi | luxehouse-grijs-gedompeld OR kdi_rabat_fbz_zwart | black accent |
| Cottage/English | luxehouse-onbehandeld | natural light |
| Forest/Boerderij | kdi_rabat | verduurzaamd warm brown |
| Mediterranean | luxehouse-onbehandeld + warm HSV tint | sun-bleached |
(Default luxehouse-onbehandeld) (Foundation-First).

### Foundation-First — folder structure & tracking
- `pilots/base/<Cabin>.blend` (33 base templates, all 33 source-GLBs mapped) exists = base done.
- `pilots/<Cabin>/style-<x>/<cabin>_<style>.blend` exists = style overlay done.
- `pilots/<Cabin>/style-<x>/<cabin>_<style>_hero.png` exists = hero done (Foundation-First).
- Base build: `pilots/base/build_base_templates.py` runs headless, builds all 33; ~5-10s/cabin (no render), ~3-5 min total. Per-cabin override: `CABIN_NAME=Magnolia`. Quick base-validation render: 64 samples, 512×288 ≈ 5s (Foundation-First).
- **Base quality gate:** proper blokhutwinkel texture (not raw GLB `lugarde-onbehandeld`); glass transmission=1.0; chrome metallic=1.0; door panels UV-mapped hardhout-deuren-ramen; 13 hidden door elements unhidden; centered origin z=0; no `_scaled` compound-scale issues (Foundation-First).

### Foundation-First — GLB scale (Blender 5.1) — CURRENT fix supersedes historic
- **Current (works):** after import select top-level (parent is None, EMPTY/MESH); `transform_pivot_point='INDIVIDUAL_ORIGINS'`; `bpy.ops.transform.resize(value=(0.01,0.01,0.01))`; then `transform_apply(scale=True)` on all. KEY: use `bpy.ops.transform.resize()` with INDIVIDUAL_ORIGINS, NOT `obj.scale=(0.01,...)` — ops handles hierarchy (Foundation-First).
- **Historic bug (superseded):** nested `parentBoard-*-scaled` children have own scale matrix; top-level 0.01x + transform_apply doesn't propagate (symptom: bbox 758m×380m×2.3m, X/Y ×100 but Z correct). Fallback in `build_base_templates.py`: sanity-check width >50 → force-scale each mesh individually ×0.01 (location too) + transform_apply. Triggers on wide cabins (Lavendel 400, Camelia +400+zijwand); result 7.38m×3.98m×2.31m (Foundation-First).

### Production Checklist — build sequence (ALWAYS this order, AUDIT after each)
- **Pre-flight:** base exists in `pilots/base/<Cabin>.blend`; cabin scale checked (~8m×3.4m×2.4m); geometry-name whitelist for cleanup: parentboard-X, wall-X, roof-X, deur, pole-X (Production Checklist).
1. **Walls texture** — two-tone: kdi_potdeksel_zwart on walls + luxehouse-onbehandeld on canopyWall.
2. **Ground plane** — `primitive_plane_add(size=30, location=(0,0,-0.005))`, name "ground_grass", grass PBR (basecolor+normal); audit: no extra plane.
3. **Schutting U-shape** — import single GLTF panel (native 0.05×3.29×6.14, long-in-Y); use `bpy.ops.transform.rotate()` NOT `rotation_euler=` (only ops respects hierarchy); back panels rotate 90° Z, first at x=-5.5 y=-3.0, duplicate-linked 3 more; wings rotate -90° back to native. Name `schutting_back_panel_1..4`, `schutting_wing_left/right`. Audit: back covers x=-7..+7, wings y=-3..0.3.
4. **Hedge in front of schutting** — Hetz_Midget GLTF scaled 1.6m, first at (-6,-2.5,0) in front of back wall (y=-3.0), duplicate-linked spacing 0.85m; wings x=±5.0; ~18-20 balls U-shape; audit: none inside cabin bbox, wraps 3 sides.
5. **Foundation planting drift** — use `wm.append(filepath=blend+"/Object/"+variant)` for SINGLE object, NOT libraries.load (junk). 9 lavender front y=+1.85, x=-3..+3, scale 0.35m; optional 2nd row y=1.95. Audit: all y>1.7, single objects, named lavender_0..9.
6. **Border drifts** — 3 hydrangea LEFT (x=-5, y=-0.3..1.3), 3 RIGHT (x=+5). Use `import_gltf_only_main` (finds biggest mesh by bbox_volume, hides variants).
7. **Door boxwoods** — 2 Hetz_Midget at (0.7,2.0) & (2.7,2.0), scale 0.45m, named door_boxwood_0/1.
8. **Wooden deck** — plane 4.0×5.2m at (-2,0.9); spans x=-4..0, y=-1.7..+3.5; douglas texture; Z=0.005-0.015 anti-z-fight.
9. **Furniture** — Sofa (Polyhaven Sofa_01) at (-2,-0.8,deck), target_h 0.75m; Bench (sketchfab wooden_bench_low_poly) at (-1.5,2.8), target_h 0.5m; Coffee table (Polyhaven coffee_table_round) at (-2.7,2.6), target_h 0.42m.
10. **Path** — straight diagonal gate(5,7)→door(1.7,1.7); plane length 6.2m × width 1.0m; rotate `atan2(dir.y,dir.x)`; material paving_stones_64, HSV value 0.55 (anthracite); Z=0.005.
11. **Lamps** — 3 bollards (target_h 0.7m) at 15/50/85% path length + 1 entry post (target_h 1.4m) at gate; all offset 0.7m perpendicular RIGHT.
12. **Statement tree** — ONE cherry (Yoshino USD) at (6,-1,0), height 5.5m; HIDE all `Yoshino_Cherry_Branch_*` prototypes not under main.
13. **Camera** — lens 35mm, sensor 36mm, shift_y 0.05; DOF focus_distance 12, aperture f/8; position (9,9,1.7); target (-0.5,0,1.2); verify rotation_x=0 (no tilt).
14. **HDRI + Sun** — HDRI `kloofendal_43d_clear_2k` rotation 50° (sun front-right), strength 1.1; Sun energy 3.5, color (1.0,0.94,0.85), angle 2°, rotation (55°,0°,45°).
15. **Render settings** — samples 256, adaptive_threshold 0.005, denoiser OPENIMAGEDENOISE, input_passes RGB_ALBEDO_NORMAL, max_bounces 6, transmission_bounces 12, sample_clamp_indirect 5.0, blur_glossy 1.0, view_transform Filmic, look Medium High Contrast, exposure 0.3, 1920×1080 (Production Checklist).

### Production Checklist — final audit + rules
- FINAL AUDIT script (`audit_scene()`): flags objects inside cabin (0<cx<4, -1.7<cy<1.7, max z>0.1), HUGE objects (dim>10m excl ground/path), schutting <6 panels, hedge <15 balls, missing statement_cherry, no scene camera (Production Checklist).
- File naming: `pilots/base/<Cabin>.blend`; WIP `..._REBUILD_v<N>.blend`; pre-render `..._REBUILD_FINAL.blend`; renders `..._HERO_v<N>.png`. Save vN each major step for rollback.
- **6 critical rules:** always `wm.append("Object")` for polyhaven plants; always `transform.rotate()` ops for fences; always NAME everything descriptively; always AUDIT after each step; always SAVE vN; never render without audit passing (Production Checklist).
- Lavendel reference stats (2026-05-21): 149 cabin meshes, 19 hedge balls, 6 schutting panels, 10 lavender, 6 hydrangea, 2 door boxwoods, 1 cherry, sofa+bench+coffee table, 1 path, 4 lamps, ground+deck; 200 named visible meshes (~420 with GLTF children); **0 objects inside closed cabin** (Production Checklist).

### Jasmijn Hygge Runbook — live-MCP execution model
- **Cabin:** Jasmijn-300x250-300-zijwand, style-scandi. Build live via `mcp__Blender__execute_blender_code` in shared session; render NO own screenshots (token cost) — **user is the eyes for aesthetics, code validates correctness** (bbox, NDC, audit). Headless only for base-measure + final hero (Jasmijn Runbook).
- Validation-gate + explicit **Definition of Done (DoD)** after every step; reuse proven functions (`scripts/extend_scene_real.py` = `esr`, `scripts/validate_scene.py`) — don't improvise (Jasmijn Runbook).
- Load helpers once: `sys.path.insert(0, r"C:\Users\beike\Documents\Blender-blokhutten\scripts")`; `esr._load_blend_as_collection` (source hidden at (1000,1000,0)), `_duplicate_collection_at` (linked copies), `_get_collection_bbox_height` (auto-scale-to-target), `remap_broken_image_paths()` (magenta .jpg↔.png fix), `scale_heavy_textures(max_size=2048)` (VRAM). Universal helpers: `world_bbox_cm`, `aim_at` (Vector.to_track_quat('-Z','Y')), `import_gltf_scaled` (parent-empty, scale-to-target, no transform_apply on shared data) (Jasmijn Runbook).
- **Step 0:** open base `pilots\base\Jasmijn-300x250-300-zijwand.blend`, Save-As `...\style-scandi\jasmijn_hygge_v1.blend`. DoD: filepath correct; summary 151 meshes + material `flatroof-71-board-mat`. WARNING: opening base disturbs live Roosmarijn session — only after user "go".
- **Materials:** texture root `assets\blokhutwinkel-textures\8192`; **image cache bug fix — `img.reload(); _=img.pixels[0]` to FORCE load** (else stays black). wall=luxehouse-grijs-gedompeld BOX rough 0.6; canopyWall=same + HueSat Value 1.08 (lounge readable); roof/beam/foundation/poles=douglas BOX; door=hardhout-deuren-ramen **UV**; roofPlate=staalpannen-antraciet BOX; flatroof=epdm BOX; glass transmission 1.0 IOR 1.45 roughness 0.05 + dirt-noise; chrome metallic 1.0 roughness 0.25. Don't touch trim-1/2/3 (chrome) or fascia-roofboards (Jasmijn Runbook).
- **Camera before props (framing-lock):** lens 35mm sensor 36mm, location (-1.50,8.20,1.58), aim (30,30,118), shift_y 0.04, DOF f/4. Verify via `world_to_camera_view` NDC (in-frame = x/y∈0-1, depth>0): door~(0.62,0.46), carport-open-L~(0.20,0.45), deck-front y~0.12, dakrand y~0.72, den_R~(0.9,0.85). Adjust NOW, not after props (Jasmijn Runbook).
- Ground: deck-top exactly z+5cm=0.05m; deck material douglas BOX scale(0.4,7.14,1)=14cm planks + Voronoi DIST_TO_EDGE seams + bump 1.0/0.008; tile-band z0; base-plane 200×200m z-2. Deck-apron must reach gevel y+125 (no gap) (Jasmijn Runbook).
- **Lighting (golden hour):** Sun energy 4.5, color (1.0,0.78,0.55), angle 2.5°, dir (-0.45,-0.78,-0.22); HDRI `qwantani_dusk_2_2k.hdr` strength 0.55, Z-rot synced to sun; AREA fills use_shadow=False (Fill_Carport 300×200 @50W warm, Fill_BackWall 180×130 @25W); glows: Interior_Glow POINT @22W (1.0,0.66,0.36), Fire_Glow POINT @18W (1.0,0.42,0.14) + emissive mesh, lantern @4W. No compositor, no World Volume Scatter (Jasmijn Runbook).
- **Final hero:** audit `validate_scene.print_report(run())` all CRITICAL/HIGH=0 + zombie-dim-scan (no object >15m except base-plane) + `remap_broken_image_paths()`=0; `scale_heavy_textures(2048)` (→1024 on OOM); save before headless; render via `render_final_clean.py` **AgX Base Contrast, exposure 0.25, 2560×1440, 256 samples**; 4 critical rules: `use_nodes=False`, save-before-headless, absolute `-o` path, no Volume Scatter; DoD PNG 2560×1440 16-bit non-black, <~90s → rename `jasmijn_scandi_FINAL.png` (Jasmijn Runbook).

### Jasmijn Runbook — failure-mode → guard table
| Symptom | Cause | Guard |
|---|---|---|
| Render all-black | compositor on / zombie-mesh occluder | `use_nodes=False` + zombie-dim-scan |
| Magenta on plants | broken image-path .jpg↔.png | `remap_broken_image_paths()` after each asset step |
| Material black after swap | image not in RAM | `img.reload(); _=img.pixels[0]` |
| Object floats/sunken | wrong z / shared-data shift | `validate_scene.run()` floating/underground flags |
| Asset 100× wrong | source cm vs m | `import_gltf_scaled` measures bbox + scales to target |
| Instances jump on move | transform_apply on shared mesh-data | parent-empty + move the empty |
| GN-instances far off scatter-mesh | Object Info `transform_space='RELATIVE'` + sprig on offset | `transform_space='ORIGINAL'` |
| OOM 8GB VRAM | 8K textures | `scale_heavy_textures(2048)` →1024 |
(Jasmijn Runbook)

### Validation gate (pre-preview)
- `scripts/validate_scene.py` (`print_report`) + custom audit (objects in closed cabin volume, >12m objects). Known false-positives to name but not blind-fix: `Ground_Grass` (name matches plant keyword), gltf sub-parts "floating" (tabletop), applied boxes "origin_at_zero". Run Anti-empty checklist from Cabin Hero Render Composition Rules (Cabin Hero Build Playbook).

### Cabin Render Reference Standard — target quality (2026-05-21 user refs)
- Two refs: (1) Modern Japandi flat-roof (Magnolia) — floor-to-ceiling glass ~80% facade, light natural wood, flat roof, concrete 3-step stairs, horizontal-slat fence backdrop, trees behind, visible interior (desk+chair, bed+grey cushion, wall map, plant, wall lamp). (2) Wide modern + carport — 5-6m wide, natural light wood, black-framed industrial windows ~70%, red car in carport, anonymous person (no face), mature oak/cypress, klinker paving (Reference Standard).
- Common musts: glass >60% facade, visible interior (NOT empty), light natural wood (cedar/larch warm, not dark stained), lush garden depth (fg+mid+bg), mature trees behind fence/hedge, soft natural light, flowering fg accent, premium materials (Reference Standard).
- **NO AI-enhanced renders** (user 2026-05-21: "NIET de bedoeling dat ze met ai verbeterd worden"): no AI upscaling (Topaz/Magnific), no img2img, no style transfer, no `_AI_FINAL` suffix. Allowed: pure Blender Cycles + standard compositor (glare, vignette, color grade in Blender). Worktree `*_AI_FINAL.png`/`*_V2_FINAL.png` = experimental, keep OUT of production gallery (Reference Standard).
- Interior assets in `assets/polyhaven/models/`: coffee_table_round_01_2k, painted_wooden_bench_2k, Sofa_01_2k, modern_arm_chair_01_2k, outdoor_table_chair_set_01_2k, anthurium_botany_01_2k, calathea_orbifolia_01_2k, pachira_aquatica_01_2k, potted_plant_01/02/04_2k. In `assets/sketchfab/furniture/`: dining_set, outdoor_relax_chair, adirondack_chair_photogrammetry, bistrot_table_and_chair, pergola (Reference Standard).
- Production template steps: import GLB from `source-glbs/{cabin}.glb`, scale 0.01x; apply blokhutwinkel textures (wall Object (4,4,4) rough 0.85; door hardhout-deuren-ramen UV (1,1,1) rough 0.55); unhide door/window elements; hardware mats (glass transmission 1.0 IOR 1.45 + dirt; chrome metallic 1.0 R 0.25; pot_anthracite M 0.85); interior assets sink -0.02 for grounding; garden per style; spruce_fence backdrop at y=-5; camera 35mm at (3.5,7.5,1.6); HDRI kloofendal_43d_clear OR qwantani_dusk_2 (golden), sun strength 3.5; render 1080p 256sa OIDN Filmic Medium High Contrast (Reference Standard).
- **Phased rollout** (33 pilots × ~30min setup + 1min render = 16+h): Phase 1 top-3 heroes (Camelia/Lelie/Magnolia) DONE; Phase 2 widest-glass 5 (Lavendel-400x300-400-zijwand, Lelie-400x250-300-zijwand, Jasmijn-300x250-300-zijwand, Camelia-250x300-400-zijwand, Zonnebloem-300x300-400-zijwand); Phase 3 rest (Roosmarijn done `roosmarijn_modern_FINAL.png` 2560×1440, 10 jun 2026); Phase 4 style variations. Foundation-First phase plan adds: Phase 5 AI upscale 1080p→4K for print/marketing (note: conflicts with Reference Standard "no AI in gallery" — upscale is for print only, not gallery) (Reference Standard, Foundation-First).

### Site-Specific placement workflow (customer-garden renders)
- **Intake:** postcode+huisnummer (only ID for all PDOK lookups), 4 GPS-tagged phone photos (N/S/E/W), garden dims, schutting type+height (standard 1.8-2.0m), sun ref photo 12-14h, preferred location sketch, neighbour context; optional Polycam/KIRI scan (Site-Specific).
- **Geo:** address→RD New EPSG:28992 via PDOK Locatieserver `/free?q=...` `fl=centroide_rd`; terrain AHN4/5/6 0.5m DTM 500×500m via Blender Hoogtedata Addon (Thomas Kole, fetches AHN3/AHN4 DSM+DTM); aerial PDOK Luchtfoto WMTS (25cm RGB, CC BY); buildings 3D BAG CityJSON LoD 2.2 (roof silhouettes only, no windows — privacy); perceelgrens PDOK Kadastrale Kaart WFS (Site-Specific).
- **Blender:** AHN metric (1m=1BU); schutting at perceelgrens −1m setback (national), windows facing neighbour = 2m setback; hide neighbour behind schutting silhouettes. Photogrammetry: KIRI Engine (free GLB, ≤150 photos) preferred over Polycam; decimate <50K tris (0.1-0.2 ratio); reference only, DELETE scan within 14 days (GDPR 5(1)(e)). No-Polycam: fSpy + Blender importer for camera match (Site-Specific).
- **Lighting:** Sun Position addon (bundled), lat/long from RD address, date=delivery month; render 4 variants 08h/12h/16h/20h (16-18h best hero, NOAA algo <1° accurate) (Site-Specific).
- **Output:** hero 1080p/2K 16:9 at 16-17h; day+evening A/B; optional before/after slider, AR-ready GLB (USDZ). Render pricing €150-300/scene (bundle 1 free with orders >€3.000). Conversion lift 5-8% → 25-40%. Headless RTX 3070 1080p/256sa ~60s, SLA 24h. Disclaimer footer on every render (indicatief, AHN/BAG open data) (Site-Specific).

### Customer Render Review workflow (165-render delivery)
- Build thin self-hosted Django/React `renders_review/` (magic-link `/review/<token>`, 7-day TTL, react-image-annotate MIT); Postgres tables Render/RenderVersion/ReviewSession/Annotation/ThreadMessage/Approval/MagicLink; ~600 LOC MVP. Week-1 fallback Notion gallery. Consider 2-day Kitsu (CGWire) POC first (Review Workflow).
- **Canonical feedback JSON** (§5) is the single most important artifact: `<cabin>_<style>_hero_v03_feedback.json` next to PNG; annotations with x/y normalized [0,1], fixed-vocab tags, severity minor|major|blocker, thread, overall_decision, sla_target. Meta file per render: parent, manifest_hash, cabin_lib_version, blender_version, render_settings {samples 256, resolution 2560x1440, cycles}, compute_time_sec (Review Workflow).
- Strict naming `<cabin>_<style>_<shot>_v<NN>.png`. Fixed tag vocabulary: lighting, materials, composition, props, weather, vegetation, color_grade, branding, geometry (Review Workflow).
- **Deferred grading = the productivity lever:** every Cycles render → multi-layer EXR (Combined, Diffuse Direct/Indirect/Color, Glossy, Emission, Environment, Z-depth, Mist, Cryptomatte). color_grade/atmosphere/branding tags = compositor-only 80% of time (~5s vs 60s Cycles). Full re-render all 165 = 2.75h; compositor re-grade all = 14 min; single-shot rebuild ~50min; cabin geometry change (cascade 5 styles × ~5 shots) ~4-6h (Review Workflow).
- Vague→concrete translation table for agent: "warmer"=sun 5500K→3500K +exp0.1; "too dark"=exp+0.3 key×1.2; "trees too dense"=density 0.8→0.5 + autumn pack; "cabin small"=35mm→24mm or dolly 1.5m; "sky boring"=swap clear_sky_2k→partly_cloudy_4k; "no human scale"=add bench/firewood. Agent must FLAG vague feedback, not silently guess (Review Workflow).
- **SLA per severity:** color-grade <1h same-day; lighting same-day; prop/camera next-day; composition 2-3 days; cabin/geometry 3-5 days; vague >2 days = auto-archive+ping (Review Workflow).
- Artist anti-patterns: **max 3 changes/iteration**; close every pin (no rotting minors); always run `validate_scene.py` before re-render; don't re-render when compositor works; always bump manifest version; all replies in thread not email (Review Workflow).

### Afronden (both playbooks)
- New pitfalls → append Lavendel Build Lessons Learned; update memory (project-memory + MEMORY.md index); leave probe/build scripts in place (no auto-cleanup) (Cabin Hero Build Playbook).


---

<a id="2"></a>
# §2. Scene composition & dressing

### Camera setup (hero render)
| Setting | Value | Reason |
|---|---|---|
| Angle | 3/4 (~45°, cabin 30-40° off facade-axis) | Shows facade + carport depth + roof; best for asymmetric 8m cabin (Cabin Hero Composition Rules; Landscape Architecture Rules) |
| Focal length | **35mm hero, 50mm product/close-up** | <30mm distorts ("wide-angle = #1 amateur tell"); 24mm vervormt cabin (Cabin Hero Composition Rules; Landscape Architecture Rules) |
| Camera height | **1.5-1.6m eye-level** (Houzz/IKEA/Wayfair conv.) | Drone/estate-agent flyover = amateur (Cabin Hero Composition Rules; Landscape Architecture Rules; Scene Composition Workflow says 1.6m tilted up ~5° for hero feel) |
| Distance | 12-18m at 35mm → 8m cabin fills ~60% frame width | (Cabin Hero Composition Rules) |
| Aperture | f/8 (Blender DoF f/5.6-8) — cabin sharp, FG/BG slightly soft | (Cabin Hero Composition Rules) |
| Vertical lock | rotation_x = 0; use shift_y to adjust, never tilt walls | Tilted verticals = amateur (Cabin Hero Composition Rules) |
- Rule: open carport side TOWARD camera reveals interior depth (Cabin Hero Composition Rules).
- Conflict note: Scene Composition Workflow (30 apr, older) says "cabin 1/3, 35/50mm, 1.6m tilt up 5°"; Cabin Hero Composition Rules (21 mei) and Landscape Architecture Rules give the precise current numbers — treat those two as current, and note 35mm on 1.5m camera warned against as wide-angle distortion (Landscape Architecture Rules) whereas Cabin Hero explicitly endorses 35mm@1.5-1.6m — Cabin Hero (newer, status:critical) is the operative recipe.

### Rule of thirds / framing
- Cabin mass on vertical LEFT or RIGHT third — NEVER centered (Cabin Hero; Scene Dressing).
- Horizon on lower third (1/3 ground, 2/3 above); roofline aligned to upper horizontal third; door/focal point on a power point (Cabin Hero).
- Cabin-deur on vertical 1/3 line; cabin fills **50-65%** of width, not more (Landscape Architecture Rules; also 60% at 35mm per Cabin Hero).
- Foreground props on opposite 1/3 from cabin; path leads diagonally to door (leading line) (Scene Dressing).
- Framing devices: overhanging branches in upper corners (from tree behind cabin), hedge-mass "wall" behind cabin, low blurry FG plant-cluster as depth-anchor (Scene Dressing).
- Background check: watch for junk in background (Scene Dressing / Keefomatic).

### Three-layer depth
| Layer | Distance | Contents |
|---|---|---|
| Foreground | 0-4m | Out-of-focus planting, stepping stone, ornamental grass, lavender bush → parallax (Cabin Hero) |
| Midground | 5-20m | Cabin + terrace/lawn + 1-2 garden features (Cabin Hero) |
| Background | 20m+ | Tree-line occluding sky (anti-flying-island), neighbour greenery (Cabin Hero) |
- NEVER: sky meets bare lawn at horizon = "flying-island" (Cabin Hero; Scene Dressing).

### Negative space ratios
- ~30% sky, ~50% midground (cabin+garden), ~20% foreground/lawn (Cabin Hero).
- Landscape Architecture Rules variant: sky/background 25-35% of frame; foreground 1.5-2.5m empty gravel/lawn with 1 staffage element; min 2m gravel/lawn visible before facade.
- Asymmetric planting: one side dense (closed-wall side), other breathing (carport-open side) (Cabin Hero).
- Pure empty lawn = dead zone → break with shadow / mowing pattern / path (Cabin Hero).

### Time of day (see theme "lighting" for full detail)
- Overcast (Dutch default): material accuracy, catalogue/spec, honest (Cabin Hero).
- Golden hour (sun ~15° altitude, behind camera 30-45° off-axis): hero/lifestyle, best emotional sell (Cabin Hero).
- Blue hour: only with interior lights ON visible (Cabin Hero).
- ❌ Noon sun: flat, hard shadows, ugly black void under flat roof (Cabin Hero).
- 10-16h optimal for natural daylight; golden hour = 15-30 min before sunset (Scene Dressing).

### The 4 laws of scene dressing (Scene Dressing, researched 30 apr 2026 after too-bare pilot)
**1. Layering — min 3 plant heights per frame:**
- Foreground 0-40cm: groundcover, sedum, creeping thyme, buxus bollen.
- Midground 40-120cm: ornamental grasses (Pennisetum, Miscanthus), lavendel, salvia, daylilies.
- Background 120cm+: tall panicle grasses, hedge-mass, framing trees.
- Min **5-7 plant-clusters** in FG+MG, not 2-3 loose pieces.

**2. Material zoning — 3-5 different surfaces per frame:**
| Zone | Material | Purpose |
|---|---|---|
| Deck | Hardwood vlonder (ipe/teak/composite) | sit/lounge |
| Path | Concrete tiles or gravel | leading line to door |
| Bed | Mulch/bark/split | under planting, low-maintenance |
| Gravel | Light-grey 10-20mm | architectural fill |
| Lawn | Grass, border only | soft edge, not dominant |
- Modern minimalist = gravel + deck + 1 plant-bed; NOT all-grass.

**3. Lifestyle props — min 4-5 per scene:**
- 1× outdoor seating (Adirondack/lounge/rattan), 1× side table, 2-3× plant pots in **odd numbers (3,5,7)** (pairs feel formal), 1× textile (throw/cushion), 1× mug/book/lantern.
- Empty deck = "showroom"; populated = "home".
- Modern minimalist props: Acapulco/B&B Italia rattan chair; black-steel or concrete cylinder table; 3 black-concrete pots (agave/buxus/succulent); black-steel solar lantern w/ frosted glass. NOT bright cushions, mixed flower pots, colourful textile.

**4. Composition + framing:** (folded into rule-of-thirds above).

### Plant-mix per style (Scene Dressing)
- Modern Minimalist: grasses Pennisetum alopecuroides; structurals agave/yucca/ophiopogon (black grass) + 1 sierboom (Acer/Betula); palette greens/whites/silvers/neutrals; repeat same plant 3-5× per cluster.
- English Cottage: borders hollyhocks (back), delphiniums+lupins (mid), foxgloves+lavendel (mid-front), peony+dianthus (front); climbers Rosa 'Graham Thomas' + kamperfoelie; density HIGH, no gaps.
- Scandinavian: Betula pendula (3-5 as birch clump); underplant ferns/moss/blueberry/heather; hardscape birch-plank path + boulders w/ moss.

### 6 Garden styles — full spec (Garden Styles + Cabin Interior Reference, status:critical)
- **MODERN (Dutch contemporary)**: Hakonechloa macra, Buxus sempervirens cubes, Carex morrowii, Miscanthus 'Gracillimus', Hydrangea paniculata 'Limelight', single Cornus kousa. Hardscape: anthracite Ardenne/basalt tiles 60×60, corten edging, black-stained ipe vlonder. Palette anthracite/black/warm wood/sage/off-white. Furniture low teak/concrete lounge, geometric L-bench. Lighting linear LED, black bollard lamps, 2700K.
- **KLASSIEK (Dutch formal)**: Buxus hedges, Taxus baccata topiary, Rosa 'Bonica', Hydrangea macrophylla, Lavandula 'Hidcote'. Hardscape red-brown waaltjes halfsteens-verband, beige gravel path, white picket. Palette brick-red/cream/soft-green/lavender. White iron bench, terracotta pots.
- **BOERDERIJ (farmhouse)**: Malus domestica, Hydrangea 'Annabelle', Echinacea, Rudbeckia, Helianthus, kitchen herbs (rozemarijn/tijm). Hardscape reclaimed klinkers wild-verband, wooden gate, oak vlonder. Palette warm brick/weathered oak/white-cream/soft yellow-pink. Rough oak picnic bench, zinc planters, kruiwagen as planter.
- **MEDITERRANEAN**: Olea europaea, Lavandula, Rosmarinus, Cistus, Festuca glauca, potted Agave, Stipa tenuissima. Hardscape buff/tan gravel + travertine slabs, terracotta pots, dry-stone wall. Palette ochre/terracotta/blue-grey/white. Rattan chairs, teak table, terracotta urns. Lighting warm 2200K lanterns.
- **JAPANDI**: Acer palmatum dissectum, clumping Phyllostachys bamboo, moss, Carex 'Ice Dance', Pinus mugo, Hakonechloa. Hardscape irregular flat-basalt stepping stones in raked gravel, shou-sugi-ban charred screen, oiled iroko vlonder. Palette black/sand/deep-green/oak. Low platform bench, single ceramic stool.
- **ENGLISH COTTAGE**: climbing Rosa, Delphinium, Digitalis purpurea, Lupinus, Geranium 'Rozanne', Alchemilla mollis, Nepeta. Hardscape York-stone stepping path, soft-brick edging, white picket / arched arbour. Palette soft-pink/lilac/cream/mid-green. Weathered teak bench, watering can, vintage birdbath.

### Garden zone layout (8m-wide cabin) (Garden Styles Reference)
| Zone | Min size | Note |
|---|---|---|
| Terras | 3×3m | off carport, table+4 chairs |
| Vlonder bridge | 60-80cm wide | between door and lawn |
| Gazon | 4×4m | rect, never wider than border zone |
| Border depth | 1m min, 1.5-2m std | Dutch border |
| Sierhoekje | 1.5×1.5m | corner accent: statement tree or boulder+lantern |
| Path width | 80-100cm | main path |
| Stepping spacing | 60cm center-to-center | standard pace |
- Sight-line rule: focal point (tree/sculpture/lantern) on axis from cabin window/door at 4-6m distance.
- Zone separation: hedge 60-100cm, raised border 30cm, or paving-material change.
- Hierarchical zones: terras (hard) → border (soft) → gazon (open) → sierhoekje (accent) → tuinhuis (destination).

### Piet Oudolf planting rules (Garden Styles Reference)
1. 70% structure / 30% bloom (grasses + seed-heads dominate).
2. Drifts: 3-7 plant groups per species, irregular brushstroke (never rows/circles).
3. Repeat 3-5 species across border at 2-4m intervals for rhythm.
4. Vertical accents every 2-3m: Veronicastrum, Eremurus, Stipa gigantea, Verbascum, Digitalis.
5. Texture mix fine (Stipa, Deschampsia) vs bold (Rodgersia, Hosta, Ligularia) within 50cm.
6. Form variety: spike + button + plume + umbel + screen — each drift different silhouette.
7. Winter interest: 60%+ plants with seedheads/structure.

### Landscape-architecture numeric rules (Landscape Architecture Rules)
**Plant ecology / gravel:** nothing grows in loose gravel (decorative 4-6cm top-layer on weeddoek); plants go in soil UNDER gravel. Drought-tolerant OK in gravel-bed (mediterranean): Lavandula angustifolia, Stipa tenuifolia, Festuca glauca, Sedum, Euphorbia, Verbena bonariensis, Allium, Yucca, Agave. NOT in gravel: Hosta, ferns, hortensia, buxus-ball, Calathea, Anthurium, plain grass.
- Anti-pattern from pilots 1+2: tropical plants (Calathea/Anthurium/succulent) on gravel; random grass-tufts on gravel ("flying grass"). Fix: plants only in defined bed-zones with mulch/soil.

**Zone transitions (mandatory — no transition = fake):**
| Transition | How |
|---|---|
| Gravel↔Lawn | steel edging 2-4mm thick, height 75-100mm |
| Gravel↔Deck | deck 20-40mm above gravel + corten rand or concrete band 100×100mm |
| Mulch-bed↔Lawn | mowing strip 200-300mm brick/concrete, flush with grass |
| Mulch-bed↔Gravel | light plinth 50-80mm or edging |

**Plant-bed dimensions:** border vs cabin/schutting 80cm min (120-150cm); border along path 40cm min (60cm); mass-planting island 150cm min (200-300cm). 3-layer: back 120-180cm (taxus, Hydrangea paniculata, tall grasses), mid 60-90cm (lavendel, Salvia, low hortensia), front 20-40cm (sedum, thyme, Festuca).

**Plant spacing h.o.h.:** Pennisetum 40-50cm; lavendel 40cm; Hydrangea paniculata 100-120cm; buxus-bol Ø30 = 50cm; perennials 30-35cm; solitary tree (Acer/Amelanchier) min 200cm from facade.

**Hedge design:** modern cabin = almost never hedge-wall directly behind; use vertical wooden schutting (cedar/larch slats, 180-200cm) + 80-100cm in front 1 ornamental tree (Amelanchier lamarckii, Cornus kousa, multi-stem birch) + underlayer ornamental grass mass (5-15× same species). Never hedge against cabin. Hedge species/height: Buxus 60-100cm/40cm deep; Taxus baccata 120-180cm/60-80cm; Beuk 150-200cm/60cm; Liguster 150-180cm/50cm. Clipped hedge = clean rectangle, not row of balls (that's topiary).

**Hardscape paths:** main path 90-120cm wide (two people); secondary 60-75cm; stepping path 40cm tile-width. Stepping stones: tile 400×400 or 600×400mm, thickness 40-60mm; step spacing h.o.h. 60-65cm; stones flush with gravel (Z-offset = -0.4 × stone_size, half-buried); logical A→B line, no decorative S-curve. Cottage = straight path to door OK; modern = curve or path ends beside door (door is "discovery").

**Object placement:**
- Adirondack chair: corner of deck, 30-50cm from both edges, rotated 15-25° off cabin wall (view to garden). Two chairs 80-100cm apart w/ side table between. Specs: 75cm high × 76cm wide × 88cm deep, seat 35cm front / 28cm rear, slats 7cm with 1cm gap.
- Plant pots at door: 1 or 2 (asymmetric 1, symmetric 2) — NEVER 3-in-row for modern (3 = cottage cluster). Pot Ø40-50cm, height 50-60cm, matte anthracite OR terracotta (not both), 1 species per pot (olive/buxus-ball/Pennisetum/Phormium), 20-30cm from wall, 40-60cm from door frame.
- Side table: Ø40-50cm, height 45-55cm, next to chair armrest, not deck-center unless coffee table w/ 2 chairs.
- Lantern: floor-lantern on deck 40-60cm; path-lantern 90-120cm; wall lamp by door 150-170cm centerline. ❌ 180cm standing lantern by cabin over-scales.
- Staffage density: max 3 object categories in frame (chair+pots+lantern); more = clutter. Pilot 2 mistake: chair + side table + 3 pots + lantern + scattered plants = too busy.

### Interior dressing (carport visible) (Garden Styles Reference)
- Living/lounge: linen 2-seater sofa (sand/oat) + wool throw (rust/charcoal) + 2 cushions; round oak coffee table 70cm Ø + ceramic bowl + 2 stacked books; floor lamp 1.4m arc + table lamp 30cm (2700-3000K); wool/jute rug 160×230 w/ 30% floor margin; one large Strelitzia/Monstera in terracotta or matte-black pot.
- Office: solid oak desk 140×60, slim black task lamp, single 27" monitor; walnut bookshelf, 1 framed art; Eames-style walnut/leather chair, small Ficus lyrata corner.
- Sauna/wellness: cedar bench, rolled white linen towel, single black ceramic vase, hanging eucalyptus bundle, salt-stone lamp (2200K).
- Storage: open pine shelving + rattan baskets, hand-tools on pegboard, galvanised watering can, seagrass basket.
- Common: pendant 1.7m above table (matte-black or rattan dome); side table 50cm w/ single object; linen off-white curtain, bronzed-black hardware.
- Match exterior: cedar two-tone → oak/walnut/rattan furniture; blackwall → repeat in lamp bases/frames/hardware.
- Visible-from-outside: 1 anchor at frame center (sofa/desk/large plant); 3-depth layering (rug-edge/lamp FG, hero MG, wall-art BG); interior 3000K warm vs exterior 5500-6500K cool for depth + lived-in glow; decor at eye-level 1.2-1.6m; slight asymmetry.

### Dutch-specific signatures (Garden Styles Reference)
- Vlonder: hardwood (bangkirai/ipe), 14×2cm planks, 5mm gap, anthracite/natural oil.
- Klinker patterns: halfsteens-verband (running bond), keperverband (herringbone), wildverband (random) — waal-format 5×10×20cm.
- Beukenheg: Fagus sylvatica 120-180cm tall, 40-60cm deep, copper-bronze winter leaf retention.
- Buxus: cubes 40×40×40cm at terras corners/door flanks (buxusmot → substitute Ilex crenata if modern).
- Hortensia drift: H. paniculata 'Limelight' north border, 3-5 specimens 1.5m apart.
- Geveltuintje: narrow planter strip along foundation (20-30cm) — Hedera or Heuchera.
- Schuttingen: anthracite/black wood or hardwood slatted (50mm slat, 10mm gap).

### Build order for Blender scene (Garden Styles Reference — current build sequence)
1. Cabin → vlonder strip → terras hardscape (size by style).
2. Border zone 1.5m deep, min 2 sides, drift placement 3-7 clumps.
3. Hedge/fence backdrop (beukenheg or shou-sugi-ban).
4. Statement tree at sight-line axis from window.
5. Lawn (gazon) fill with 5-10% bare-patch variation.
6. Interior: sofa+rug+lamp anchor → coffee table → plant → wall art.
7. Two-light setup: 6500K HDRI sun + 3000K interior pendants.
8. Desaturate materials 15-20% in compositor.
- Older workflow (Scene Composition Workflow, 30 apr): Ground+Sky → major landscape (3-7 big elements, triangle composition, not symmetric) → foliage scatter (GN, density-mask paths=0, beds=high) → hardscape+props → lighting → camera+render. Superseded on ordering by the Garden Styles Reference build order but the two are consistent.

### MCP scene-build loop & output org (Scene Composition Workflow)
- Iteration checks after every step: get_viewport_screenshot() → user go/no-go → adjust → don't proceed without approval (user watches live).
- Blokhut import: no dedicated tool, use execute_blender_code (bpy.ops.import_scene.fbx global_scale=1.0, or wm.append). Then get_scene_info / get_object_info: check scale (meters!) + orientation; move to origin, voorgevel → +Y.
- Render-batch per blokhut: 1 cabin → 3-4 styles → 2 angles = 6-8 finals.
- Output: ~/Documents/event-branding/blokhutten/<product>/ with style-modern/, style-cottage/, style-scandi/ (PNGs) + _source.blend per style. (NOTE: current project actually uses pilots/<Name-dims>/style-*/ per git status — path convention has since moved.)

### HDRI selection (Cabin Hero Composition Rules — current)
| Mood | HDRI |
|---|---|
| Overcast Dutch daylight (flagship) | kloofendal_overcast_puresky (24K) |
| Soft daylight variant | qwantani_puresky, kiara_1_dawn |
| Golden hour | qwantani_dusk_2_puresky, belfast_sunset_puresky, spaichingen_hill |
| Blue hour | dikhololo_night, kloppenheim_06_puresky (low intensity) |
- Always use *_puresky variants (clean sky, no rocks/buildings in reflections); strength 0.8-1.2; rotate Z to control sun direction (30-45° off-camera for golden hour).
- Older shortlist (Scene Dressing): symmetrical_garden_02 (modern formal midday), studio_garden (cottage midday), qwantani_dusk_2 (golden hour overlay). Landscape Architecture Rules: HDRI overcast 10000K for product-clarity.

### Polyhaven asset shortlist (Scene Dressing)
| Category | Asset ID | Use |
|---|---|---|
| Tree | tree_small_02 | sierboom focal 4.5m (137K dl) |
| Tree | jacaranda_tree | sierlijker (130K dl) |
| Tree (forest) | pine_tree_01, fir_tree_01 | background mass scandi/forest |
| Grass | grass_medium_02 | scatter-friendly clump |
| Plant | flower_heliophila | small flower accent |
| Texture | aerial_grass_rock | grass-with-stones tussenkleur |
| Texture | coast_sand_rocks_02 | gravel-look |
- Also referenced in workflow: oak_tree_01, tree_small_02, grass_medium_02.

### Sketchfab licensing (Scene Dressing)
- Commercial marketing = only CC0 or CC BY (no NC, no ND).
- NC-trap models to avoid: all xfrog plant models (CC BY-NC-ND) — Acer, Pinus, etc.
- First place to look: Thomas Flynn CC0 collection (nebulousflynn). For problem plants, Polyhaven is safe default.

### Anti-patterns / "looks AI-generated"
- Scene Dressing: 1 tree + 1 plant + empty space; same grass over whole 30×30m ground (tiled); empty planters ("random blocks"); symmetric pairs (formal); single-colour-texture ground (TV-set).
- Cabin Hero amateur checklist: wide-angle <28mm; cabin dead-centered + symmetric; identical-height bushes in row; no human-scale cue; floating cabin (no ground shadow, no grass intersecting plinth); tilted verticals; sky→bare-lawn horizon; single plant species cloned everywhere; over-saturated grass green; all trees same height/type.
- Landscape Architecture Rules: flying grass on gravel (no snap-to-ground); UV-sphere boxwoods; solid green hedge wall (no silhouette break); ad-hoc scatter without bed boundaries; stepping stones above gravel; bad chair proportions; too many staffage categories.
- Interior/dressing mistakes (Garden Styles Reference): symmetry/staging (rotate items 2-8°, offset cushions); oversaturated textures (drop HSV saturation 15-25%); anachronism (no MacBook + farmhouse); scale errors (pillows 45×45 not 30×30, sofa cushions 60cm thick); sterile (add open book/mug/tossed throw/crooked frame); too much (rule of 3 per surface max); wrong plant scale (indoor Monstera leaves ~30cm not 10cm); no wear (rugs need wrinkles, wood grain variation, fabric micro-displacement).

### Anti-empty verification checklists (run BEFORE accepting render)
- Cabin Hero (11 checks): path starts FG-bottom + leads to door; schutting visible (back wall + ≥1 side wing); hedge in front of schutting continuous; foundation planting at cabin base; ≥1 statement tree; furniture in chill area/deck; no object inside cabin bbox; no object >10m visible randomly; sky doesn't meet bare lawn (tree-line above hedge); cabin walls dark (two-tone); door+window glass + chrome handle visible.
- Scene Dressing "vol genoeg" checklist (≤4 ticks = too bare, keep building): ≥3 plant heights; ≥2 ground-zones; ≥1 lifestyle prop; ≥1 framing element; cabin not centered; leading line to door; no empty planters; background not bare.

### Compositing essentials (Cabin Hero + Garden Styles Reference)
- Slight vignette (corner darkening) to draw eye to cabin; S-curve on RGB for contrast pop; subtle warm tint in shadows (color balance); 0.5-1px chromatic aberration on edges; optional very-subtle film grain; desaturate materials 15-20%.

### Tested Lavendel settings (Cabin Hero — concrete reference values)
- Camera (8, 9.5, 1.6), target (0, 0, 1.3), 35mm.
- HDRI kloofendal_43d_clear_2k rotated 1.2 rad (sun front-right of cabin).
- Sun 4500K (1.0, 0.93, 0.82), energy 3.0, elevation 55°.
- View transform Filmic + Medium High Contrast; Exposure 0.3.

### NL building-code constraints that shape composition (NL Building Code + Real Terrain)
| Reg | Visual impact |
|---|---|
| 3m goothoogte | ≈ 1× eye-height at 1.5m cam → roof ~2m above camera level |
| 5m nokhoogte | cabin top just above avg schutting (2m) |
| 30m² footprint | max ≈5.5×5.5m — rarely >6m wide in frame |
| Schutting 2m + setback | cabin ≥30cm behind schutting → backdrop = schutting + green + roof-edge + sky |
| 5m brandafstand | in house-visible renders keep ≥5m gap cabin↔house |
| Voortuin verboden | NEVER show cabin in front yard (legally impossible → unbelievable) |
| Mantelzorg 100m² | ≈10×10m, own front door + BAG house-number sign for authenticity |
- Schutting max vergunningsvrij: 2m behind voorgevelrooilijn, 1m in front (voortuin).

### Dutch backdrop + terrain authenticity (NL Building Code + Real Terrain)
- Backdrop patterns: rijtjeshuizen on distance 5-6m wide, 2-3 storeys, saddle roof, shared side-walls, visible 30-200m in almost any backyard render (10/17M NL'ers live in rijtjeshuis); polder-horizon 90% sky/10% land + kerktoren 1-5km as compositional anchor; knotwilgen row parallel to sloot rhythmic 8-12m; schutting 1.8-2m + beuk/liguster/taxushaag behind = majority of plot boundaries.
- Sky/weather (KNMI 1991-2020): cloud cover ~67% (⅔ time >5/8 covered); ~1700 sun-hours/yr → render-budget 60-70% overcast diffuse HDRI (6500-7500K), 30-40% blue sky+sun; fog 40-80h/yr (oct-mar) → subtle volumetric fog density 0.01-0.02; stratus/altostratus dominate (flat grey), stacked cumulus summer only; rain 7% of time → "just-dried, moist sheen" on paving/tiles = authentic detail.
- Region topography/planting: Polder (<1m NAP, flat, sloten talud 1:3, knotwilgen; native Salix alba/zwarte els/populier/meidoorn-hagen); Veluwe (zandgrond 25-110m NAP, terrain modulation midground; grove den/zomereik/ruwe berk/jeneverbes/struikheide/blauwe bes); Zuid-Limburg (löss to 322m, holle wegen/graften, beuk on hilltop; beuk/haagbeuk/hazelaar/mispel/oude fruitrassen); Kust/duinen (5-30m, sharp relief within 50m, AHN 0.5m essential; duindoorn/meidoorn/kruipwilg/helmgras); Randstad urban (plataan/linde/robinia). Avoid rhododendron-mass, palms, olive trees in NL context (reads unbelievable).
- Real-terrain pipeline (site-specific, client gives address): address → BAG geocoder (PDOK/QGIS) → RD coord; bbox 500×500m; Blender Hoogtedata Addon (Thomas Kole, gitlab.com/thomaskole/blender-hoogtedata-addon) = go-to for NL, pulls AHN3 DSM+DTM + 3D BAG in one click (raw heightmap / clean maaiveld / 3D buildings); PDOK luchtfoto 25cm as maaiveld texture for distance shots; kadastrale kaart (PDOK WMS kadastralekaartv4) overlay → perceelgrens → schutting placement; place cabin asset georeferenced within plot. AHN = RD New EPSG:28992 → reproject 3857/4326 for Blender GIS. Alt tooling: BlenderGIS (domlysz), QGIS 3.40+ → glTF/OBJ.

### Files
- All six target files read in full; none missing or empty.


---

<a id="3"></a>
# §3. Camera & composition

Sources (short names): **Adv-Camera** = "Advanced Camera Composition Archviz" (status: critical, 2026-05-22); **Cam-Marketing** = "Camera and Composition for Cabin Marketing Visuals" (status: current, 2026-05-08); **Preset-Lib-32** = "Camera Composition Preset Library 32" (status: critical, 2026-05-22). Preset-Lib-32 is the most concrete/current for exact coordinates; the two others give the reasoning.

### Focal length (mm) — combined table
| Lens | FOV | Effect / use | Source |
|---|---|---|---|
| 24mm | 84° | Whole garden+cabin wide / establishing; distortion creeps in; avoid for product (Adv-Camera). "Hele tuin + blokhut wide" (Cam-Marketing) | both |
| 28mm | 75° | Wide hero "in z'n tuin" context; context shot (cabin small in landscape) | both |
| **35mm ⭐** | 63° | **Default hero** — documentary/environmental "I am standing there"; all-purpose natural perspective; use 28-35mm 80% of the time | both |
| 40mm | 53° | Tight hero on cabin + immediate surroundings | Cam-Marketing |
| 50mm | 46° | Product/natural eye, no distortion; material close-ups, interiors, veranda close-up | both |
| 70mm | 32° | Compressed depth — brings back closer | Cam-Marketing |
| 85mm | — | Portrait/isolating — detail shots (door hardware, joinery, log-joint) | Adv-Camera |
| 100mm | 23° | NOT for archviz exterior — flattens too much | Cam-Marketing |

- Rule: use **28–35mm for 80%** of blokhut marketing; avoid <30mm unless wide-context (Cam-Marketing). NEVER lens <20mm (barrel distortion, fish-eye creep) (Preset-Lib-32 anti-patterns).
- Blender code: `cam.lens = 35.0`, `cam.sensor_width = 36.0` (full-frame) (Cam-Marketing).

### Two-point perspective / vertical correction (CRITICAL — all three notes)
- Keep verticals plumb via `camera.shift_y`, **NOT tilt/rotation**. Tilted camera = "cabin falling backward" amateur / Dutch-angle = art not sale (Adv-Camera, Cam-Marketing).
- Recipe: camera at eye height, **level (rotation_x = 90°)**, positive `shift_y` to include roof → mimics tilt-shift lens, two vanishing points (horizontal L/R), no vertical vanishing point (Adv-Camera, Cam-Marketing).
- Code: `cam.shift_x = 0.0`; `cam.shift_y = 0.15` (example; positive = look higher without rotating) (Cam-Marketing). Preset-Lib-32 uses smaller shift_y values (+0.02 to +0.10, see presets).
- Always use `shift_y` (e.g. +0.05) to put roofline on upper-1/3 instead of physically tilting; wall lines parallel = "premium" (Preset-Lib-32 §40). Camera roll must = 0.

### Camera height
| Height | Effect | Source |
|---|---|---|
| 0.1m worm's-eye | Dramatic social-media standout | Cam-Marketing |
| 0.4m sit-height | Japanese Zen pavilion (lower) | Cam-Marketing |
| 0.5m knee | Heroic, object feels bigger, better FG context — **marketing hero standard 0.5–0.8m** | Cam-Marketing |
| 0.8m heroic low-angle | Cabin towers — dramatic-sky promo | Adv-Camera |
| **1.6m / 1.65m eye-level ⭐** | Buyer's POV "imagining myself there"; canonical eye level = **1.65m** in Preset-Lib-32 | all |
| 2.0m slight elevation | Comprehensive, roof + surroundings | Adv-Camera |
| 2.2m | "Catalogue" high bracket | Preset-Lib-32 |
| 5–15m drone | Show-the-grounds only, NEVER for hero (unless selling plot not cabin) | both |
- Anti-patterns (Preset-Lib-32 §39): Z < 1.0 = kid POV (looks up door's nostril); Z > 5.0 without justification = unhuman; 90° top-down kills perceived value 40%+; 0° dead-center front = CAD/technical drawing.

### DoF / f-stop conventions (Preset-Lib-32)
- DoF enabled per preset; `dof.aperture_fstop` per table; `dof.focus_distance = (loc − target).length` (units = meters).
- f-stop range seen: f/2.8 (persona/interior blur, macro BG melt), f/4.0 (hero/lifestyle default), f/5.6 (garden context), f/8.0 (editorial/wide/reflections), f/11.0 (drone). FG frame out-of-focus at f/4–f/5.6 so it reads as context not subject (Adv-Camera).
- CGarchitect ranking: **35mm + slight elevation + f/5.6–8** = #1 for "real-estate plus premium feel" (Preset-Lib-32 sources).

### The 32 named presets (Preset-Lib-32) — coordinate convention
Cabin centered at world origin; +Y = front (door side), −Y = back wall, +X = right, +Z = up; eye level 1.65m; positions in meters. Track-to rig: `TRACK_NEGATIVE_Z` + `UP_Y` (Blender standard look-at).

**Hero (1–8):** 1 3Q Eye Level Hero (6.5,−7.0,1.65)→(0,0,1.6) 35mm 16:9 f4 shiftY+0.05, all styles, sun side-back 45°; 2 3Q High Drone-Adj (5,−8,5)→(0,0,1.8) 35mm f5.6, modern/japandi; 3 Wide Establishing (8,−12,2.2) 24mm 16:9 f8 shiftY+0.08 back-lit, scandi/boerderij; 4 Tight Hero Front-On (0,−8.5,1.65) 50mm 4:3 f4, modern, side 90°; 5 Door-First Approach (3.5,−5.5,1.55)→(−0.5,0,1.4) 35mm 4:5 f4, scandi/boerderij; 6 Garden-First (4,−9.5,1.50)→(0,0,1.8) 28mm 16:9 f5.6; 7 Side-Profile Arch (10,0,1.80) 85mm 16:9 f8, japandi/modern side 90°; 8 Catalogue Hero (5.5,−7.5,2.20) 35mm 16:9 f5.6, real-estate, all.

**Detail (9–16):** 9 Door Close-Up (0,−1.8,1.40) 50mm 4:5 f4; 10 Cedar Wall Texture (3,0,1.45)→(1.5,0,1.45) 85mm 1:1 f5.6 (grazing light for grain); 11 Klinker Path Detail (1.5,−3.5,1.20)→(0.5,−2.5,0) 35mm 4:5 f5.6 (45° down, FG plant blur); 12 Roof Eave Corner (3.5,−3.5,1.40)→(2,−2,2.6) 35mm 4:5 f5.6; 13 Window Reveal (2.2,0,1.55)→(1,0,1.55) 35mm 1:1 f5.6; 14 Plant+Wall (1.8,−1.5,1.10) 50mm 4:5 f2.8; 15 Handle+Lock (0,−1.2,1.05)→(0,−0.85,1.05) 100mm 1:1 f4 (macro, true f/4 BG melt); 16 Trim Profile (2.8,0.2,2.40) 85mm 16:9 f8.

**Interior (17–22):** 17 Sitting Hub (−1.2,0.8,1.40) 24mm 16:9 f4; 18 Reading Nook (−1.5,1.0,1.20) 28mm 4:5 f2.8; 19 Kitchen/Bar (0.5,1.4,1.55) 35mm 16:9 f4; 20 Sleeping Hub (1.3,1.3,1.10) 32mm 4:5 f2.8; 21 Bathroom Mirror (−1.4,1.5,1.55) 24mm 4:5 f4 (mirror reflects window+garden); 22 Door Threshold (0,−1.0,1.50)→(0,0.5,1.4) 28mm 4:5 f5.6.

**Garden context (23–28):** 23 Pergola Frame (5.5,−6.5,1.55) 28mm 16:9 f5.6, mediterraan (beam shadows); 24 Tree Frame (4.5,−8.0,1.65) 35mm 16:9 f4 (trunks L+R, branches top); 25 Schutting Reveal (6,−3.5,1.60)→(−1.5,0,1.6) 35mm 4:5 f5.6; 26 Hedge Path Leading (1.5,−10,1.55) 50mm 4:5 f5.6 (hedges = vanishing lines); 27 Pond Reflection (3.5,−9.0,0.45)→(0,0,2.0) 35mm 16:9 f8 shiftY+0.10 (low cam, water mirror lower 1/3); 28 Patio Looking Back (−5,−7.5,1.30) 50mm 16:9 f4 (persona chair FG).

**Drone / over-shoulder (29–32):** 29 Drone Adj 8m (5,−8,8) 50mm f8 (~15° tilt down); 30 Drone Adj 12m (7,−10,12) 50mm f11 catalog; 31 Over-Shoulder Persona (5.8,−6.5,1.65) 35mm 4:5 f2.8 (persona blurry FG, cabin sharp BG); 32 Reverse Drone (−3,−16,14)→(0,0,1.0) 70mm 16:9 f11 (cabin tiny, garden fills FG).

- Full drop-in `CAMERA_PRESETS` dict + `apply_camera(preset_name, scene)` function in Preset-Lib-32 §33: sets loc, creates/uses `CAM_TARGET` empty (PLAIN_AXES), TRACK_TO constraint, lens, DoF (fstop + focus_distance), shift_x/shift_y, custom prop `["preset_name"]`, and resolution = `aspect × 240`.

### Camera library structure (Preset-Lib-32 §34)
- Master file: `lib/cameras/preset_library.blend` — one `bpy.types.Camera` per preset, named `CAM_<preset_name>`, custom prop `["preset_name"]`.
- Mark each as Asset (`obj.asset_mark()`), add preview render, tag with style + cabin-size + mood.
- Asset library folder `lib/cameras/` registered via Preferences → File Paths → Asset Libraries → **"BlokhutCameras"**; drag into scene → handler reads `preset_name` → `apply_camera()`.

### Per-style camera defaults (Preset-Lib-32 §35)
| Style | Preferred lens | Presets | Avoid |
|---|---|---|---|
| Modern | 50mm (architectural honesty) | 4, 7, 8, 13, 29 | wide <28mm distortion |
| Scandi | 35mm (warm, lifestyle) | 1, 5, 6, 24, 28 | telephoto >85mm |
| Japandi | 50–85mm (calm) | 7, 10, 16, 18, 26 | dutch tilt, over-shoulder |
| Boerderij | 35mm + persona | 5, 6, 17, 19, 28 | drone-high, clinical front-on |
| Mediterraan | 28–35mm pergola-framed | 6, 23, 24, 28 | overcast HDRI, side-profile cold |

### Per-style hero recipes (Cam-Marketing — camera + composition + time)
- **Modern Minimalist office**: 35mm, eye-level, three-quarter (45° to façade); cabin L/R, 60% garden/sky, leading line via decking path; midday sharp shadows or blue-hour warmth-vs-cool.
- **English Cottage pavilion**: 28mm, knee-height, frontal+flank; flower chaos front, pavilion center, tree behind; overcast or golden hour.
- **Scandinavian sauna**: 35mm, knee-height, three-quarter; birch trunks flank left, sauna right, hot-tub FG; golden-hour low-angle = signature Scandi.
- **Forest cabin / pipowagen**: 28mm, eye-level, deep fern FG; through trees, dappled light; golden hour 30 min after sunrise (mist still low).
- **Mediterranean veranda**: 35mm, eye-level, axial frontal under pergola; pergola top-frame, long table center, grapevine top; late afternoon long shadows.
- **Japanese Zen pavilion**: 50mm, **lower sit-height 0.4m**, frontal; minimalist asymmetric (pavilion right, rocks+gravel left); soft morning/overcast, NO golden hour.
- **Boerderij kapschuur**: 24–28mm wide "complete erf"; barn central, chickens scatter, wheelbarrow FG; midday Dutch, no hot spots.
- **Tropical/Bali**: 35mm, eye-level, angled through canopy; pavilion center, palms flanking, floating candles FG; midday diffuse or blue-hour lit.
- **Coastal/dunes**: 28mm, lower-than-eye, dune-grass front; cabin center, marram grass FG, sunset behind; golden hour or overcast wind shot.
- **Industrial/Urban Jungle**: 35mm, eye-level, square-on; corten+glass front, climbing plant breaks straight lines; evening with lamps on.
- **Prairie (Oudolf)**: **28mm wide essential** (masses need width); waving grasses 40% of frame, cabin small center; low-angle golden hour for grass-spike glow.
- **French Provence**: 35mm, knee-height, lavender row FG as leading line to pavilion; midday warm or golden-hour lavender glow.
- **Alpine**: 28mm wide for mountain context; chalet center, alpine meadow FG, mountains back; morning crisp or golden hour.

### Composition rules (all three notes)
- **Rule of thirds**: place cabin on lower-left or lower-right intersection, not centered; door/front-left corner on left 1/3 vertical, roofline on upper 1/3 horizontal (use `shift_y +0.05`, not tilt). Blender: Camera Properties → Viewport Display → Composition Guides → Thirds.
- **Leading lines** ("compositional rails" — Brickvisual; diagonals > horizontals): garden path bottom-left→front door (archetypal); side-wall log courses converge on doorway; hedge row/fence/paver edges/decking joints/rooflines; klinker path + schutting top edge + hedge row anchor in lower corner, terminate at door.
- **Frame within frame**: tree canopy upper-third + centered cabin = +30% perceived depth; branches top-L+top-R, pergola beam top, schutting corner right (presets 23,24,25); FG frame out-of-focus at f/4–5.6.
- **Reflections**: window glass reflecting forest, pond doubling silhouette, wet decking. Works only when (a) doubles visual mass or (b) reveals off-frame content; DON'T reflect a busy background.
- **Depth 3-plane stack (mandatory)**: FG ~2m from cam (grass tufts/low plants, out-of-focus OK) → MG = cabin (sharp) → BG 20m+ (tree-line + atmospheric haze). Empty FG = "floating cabin"; no BG = no scale reference. Add 5–15% volumetric mist in deep BG; back trees desaturate ~40% (MIR signature), blues shift cooler.
- **Negative space**: hero = 40–50% sky; dramatic/moody = 15–25% sky; detail = 0% sky. Mediterranean/Japanese let ground/sky breathe; Dutch cottage = fuller, less negative space.
- **S-curve**: path winds left-right-left FG→door.
- **Visual weight see-saw**: heavy dark cabin (right third) balanced by small bright at distance (tall tree / person silhouette / bright cloud) in left third.
- **Color triangle**: three brand-color accents at far-left, center, far-right = eye-loop.
- **Color theory (magic hour)**: complementary orange interior glow 2700K + blue dusk sky 8000K; or interior 3200K bulbs vs exterior twilight 6500K; AVOID mono-temperature (reads flat).

### Storytelling shot types & multi-shot series
- Shot types (Adv-Camera): Hero (35mm,1.6m,twilight); Lifestyle (50mm, partial person boots/hand, daytime); Product detail (85mm macro — log-joint/hinge/seal); Context (28mm wide, cabin small); Interior story (35mm from inside looking out).
- **5-shot series per cabin** (Adv-Camera §12): 1 Context wide (28mm, 2.0m) → 2 Hero exterior (35mm, eye-level, twilight) → 3 Lifestyle (50mm, partial person, day) → 4 Detail (85mm, log corner/hardware) → 5 Interior-outward (35mm). Mirrors buyer journey: "where am I → what is it → I could live here → well-built → this is my view."
- Brick Visual per-project standard: **1 hero + 4–6 details + 2–3 lifestyle** (Preset-Lib-32 sources).
- **Multi-shot versatility trick** (Cam-Marketing): for one cabin with 3–4 styles, shoot from a **fixed camera position** with only scene-dressing changing → shows product versatility without implying a different product; plus optionally 1 hero per style from a different camera for variety.

### Bracketing strategy (Preset-Lib-32 §37)
- Bracket **camera Z** at 3 heights per hero: Low 1.40 (intimate), Center 1.65 (canonical), High 2.20 (catalogue).
- Render all three at **1080p preview, 256 samples, ~60s each**; pick winner on Lightroom contact-sheet; re-render winner at full 4K → saves 60–80% of re-render cycles.
- Optional 2nd-axis bracket = lens (28/35/50) only when composition unproven.
- "Bracket the camera, never the sun" (Brick Visual).

### Cabin-centric camera math (Preset-Lib-32 §38)
For cabin width W, depth D (m), `MAX_DIM = max(W,D)`:
- `three_q_distance = MAX_DIM*1.5 + 3.0`
- `wide_context_distance = MAX_DIM*2.5 + 5.0`
- `drone_height = MAX_DIM*1.5`
- `detail_distance = 1.5`; `interior_offset = 1.2` (back-from-wall for 24mm interior); `eye_z = 1.65`
- Worked pilots: **Camelia 2.5×3.0** → 3Q 7.5 / wide 12.5 / drone Z 4.5; **Magnolia 3.0×2.0** → 7.5 / 12.5 / 4.5; **Lavendel 4.0×3.0** → 9.0 / 15.0 / 6.0; **Lelie 4.0×2.5** → 9.0 / 15.0 / 6.0.
- Scaling rule: multiply preset `loc` X/Y by `MAX_DIM_actual / 4.0` (4m = canonical).

### Aspect ratios / output dimensions
- Master strategy: render at 16:9 (or 4:5) master and **crop/recompose derivatives, don't re-render** (Adv-Camera). Render larger, downscale per channel in post (Photoshop "Save for Web" or `magick convert -resize`) (Preset-Lib-32).
- Preset-Lib-32 §36 dimension table: Website hero 16:9 = 3840×2160 (web-OK 2560×1440); Pinterest pin 2:3 = 3000×4500 (2000×3000); Pinterest tall 9:16 = 3000×5333 (1080×1920); IG square 1:1 = 3000×3000 (1080×1080); IG portrait 4:5 = 3000×3750 (1080×1350); TikTok/Reels 9:16 = 3000×5333 (1080×1920); Print A4 portrait = 2480×3508 @300 DPI; A4 landscape = 3508×2480; Trade banner 2:1 = 4000×2000 (2000×1000).
- Also cited (Adv-Camera / Cam-Marketing): 3:2 = 3000×2000 print brochure; 2.39:1 = 2560×1072 cinematic banner; 2400×3000 4:5 print catalog @300 DPI.

### Anti-patterns — NEVER USE (Preset-Lib-32 §39 + Cam-Marketing "Vermijden")
- 0° front elevation dead-center (CAD/technical); 90° top-down (Zillow/real-estate drone, −40% value); Z<1.0 kid POV; Z>5.0 unjustified; lens <20mm (barrel/bow/fish-eye); fish-eye/panoramic; dead-flat horizon centered (offset via shift_y); camera roll ≠ 0 (Dutch tilt = action-movie cue); looking *down the path away* from cabin (loses subject); tight crop hiding/cropping roof (cabin looks incomplete). Also: centered subject without reason; wide-lens distortion stretching plants; no foreground (flat); symmetry everywhere (boring — except Japanese Zen where asymmetry is the rule).

### Reference galleries / sources named in notes
MIR (mir.no — atmospheric depth, twilight color; 3Q hero 35–50mm plumb verticals = canonical); Brickvisual/Brick Academy (leading lines, lifestyle storytelling, bracket camera not sun); Methanoia (frame-within-frame, restraint); Ronen Bekerman (photographic approach; warns against <20mm lenses & top-down drones residential); The Boundary (luxury exterior hero); Beauty and the Bit (85mm material detail); Chaos Blog, D5 Render, Property Render, Fabrice Bourrelly (fix vertical tilt-shift), GarageFarm, Studiobinder (aspect ratios), PhotoPills (FOV/DoF calc), CGarchitect. Blender docs: `shift_x/shift_y` keep verticals; `dof.focus_distance` units = meters; TRACK_TO + TRACK_NEGATIVE_Z + UP_Y = standard look-at rig.


---

<a id="4"></a>
# §4. Lighting & atmosphere

### Source hierarchy / currency
- **Lighting Recipes Catalog 25** (status: critical, 2026-05-22) is the CURRENT authoritative recipe set — 25 named recipes + drop-in Python. It uses **AgX + "Medium High Contrast"** as default view transform and W/m² sun-strength convention. It supersedes the older **Lighting Recipes for Cabin Archviz** (status: current, 2026-05-08) which still recommends **Filmic Log Encoding** and lower sun-strength ranges — treat Filmic advice there as outdated; Catalog 25 / ACES-OCIO note both use AgX or ACES, not Filmic.
- **Outdoor Archviz Lighting Setups** (critical, 2026-05-22) = professional setup workflow (three-point, practicals, portals). **ACES OCIO + Atmospherics Advanced** (critical, 2026-05-22) = colour pipeline + physically-based volumetrics. **Atmospheric Effects for Garden Scenes** (current, 2026-05-08) = mist/fog/god-ray techniques. **HDRMaps** (source, confidence medium) = mix-shader + IES.

### NL solar / climate constraints (Lighting Recipes Catalog 25)
- NL ≈ 52°N. Sun max altitude ≈ **61°** (summer solstice noon), ≈ **14°** (winter solstice noon). KNMI 1991-2020: **1,774 sunshine h/yr**; December sun only **18%** of daylight; fog frequent Oct-Feb.
- **Sun altitude clamp**: Dec/Jan max alt ≈14°; never use alt >20° for "winter midday" or it looks Mediterranean.
- **NL realism mix**: 60% of marketing renders should use overcast/dappled/hazy recipes (#4, #7, #8, #11-13) — Dutch climate overcast-dominant, but archviz sells better in golden hour.

### Sun-strength conventions (conflict — Catalog 25 is current)
- **Catalog 25 (current)**: Cycles SUN `energy` in W/m². Real clear noon ≈1000 W/m² → `strength ≈ 4-6` with HDRI strength 1.0. Diffuse/overcast: 0.5-2 (HDRI does the lifting).
- **Outdoor Archviz Setups**: Overcast 3.0-4.0; Bright daylight 5.0-7.0; Golden hour 3.5-5.0 (3500K); Hazy 2.5-3.5.
- **ACES-OCIO note**: default 1.0 is too low for ACEScg; clear day 5-10 W/m², golden-hour backlit 3-5.
- **Old note (2026-05-08, HDRI-mode)**: sun strength 2-5 (3-5 clear, 1-2 overcast) — lower because it assumed Filmic + HDRI-primary. Prefer Catalog 25 numbers.

### Sun angle = shadow softness (angular diameter, °)
- Real-world sun = **0.526°**. Archviz slightly-soft default 1.5-2°. Hazy 5-10°. Heavy overcast 15-25° (basically skylight). Crisp golden hour 0.5-0.8° (Catalog 25).

### View transform / colour management (ACES OCIO note — current)
- Default for **90% of Dutch blokhut archviz = AgX** (zero-config, better highlight rolloff than Filmic). Catalog 25 default look = "Medium High Contrast"; per-recipe looks vary (Base / Medium / Medium High / High Contrast).
- **Blender 5.0+** ships ACES 1.3 + ACES 2.0. **Use ACES 2.0**, not 1.x (1.x desaturates blues/yellows, "skin reds" issue; 2.0 fixes warm wood/terracotta/golden skies, HDR Rec.2100-PQ ready). Only use 1.3 if client demands 1.x compat.
- Bundled config: `cg-config-v4.0.0_aces-v2.0_ocio-v2.5.ocio` (OpenColorIO 2.5.0+). **Blender 4.4 had a bug breaking OCIOv2 ACES configs — fixed 4.5+, stay on 5.x.**
- Custom OCIO install: download config → place `D:\OCIO\aces-2.0\config.ocio` → set Windows env var **`OCIO`** = full path → restart Blender → verify View Transform lists `ACES 2.0 - SDR Video` and `ACES 2.0 - HDR Video (Rec.2100 PQ 1000 nits)`.
- **Switch AgX→ACES only when**: client is film/VFX studio, HDR (Rec.2100-PQ) required, multi-DCC pipeline (Substance→Blender→Nuke/Fusion), or serious LUT grading downstream.
- Working space = **ACEScg** (AP1, linear). Client SDR: View `ACES 2.0 - SDR Video`, Display `sRGB`. HDR master: View `ACES 2.0 - HDR Video`, Display `Rec.2100-PQ`.
- Colour-space per texture: Albedo/base color = `Utility - sRGB - Texture`; Normal/Roughness/Metallic/AO/Displacement/Height = `Utility - Raw` (Non-Color); HDRI .exr/.hdr = `Utility - Linear - sRGB`.
- **Most common mistake**: normal/data map left as sRGB → re-linearised → soft surfaces. Always flip non-color maps to Non-Color/Raw. If everything "milky/washed out" → check albedo colour spaces first.
- HDRIs from Poly Haven are linear EXR/HDR — do NOT gamma, do NOT pipe through Gamma node; adjust via World strength + Color Balance compositor node.
- **Output master**: OpenEXR MultiLayer, ZIP codec, Float 32-bit, colour space ACEScg → re-gradeable. Client gets 8-bit PNG/JPG via `ACES 2.0 - SDR Video` + sRGB. Never deliver EXR to client. PNG can't hold ACEScg gamut → EXR master only.
- Photoshop 25+ (CC 2025): OCIO plugin bundled, set same `OCIO` env var. Affinity Photo 2.4+: native OCIO.
- Exposure adjustment via Render → Color Management. **Never combine `view_settings.exposure > +0.5` with HDRI strength > 1.2** — AgX clips warm channels.

### 25 named lighting recipes (Lighting Recipes Catalog 25) — HDRI / RotZ° / Str / SunK / SunW·m⁻² / Alt° / Az° / Angle° / VolDens / Aniso / Look / Exp
| # | Name | HDRI (Polyhaven) | Rot | Str | K | W | Alt | Az | Ang | Vol | Aniso | Look | Exp |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|1|Dawn Polder Mist|kloppenheim_07_puresky|80|0.8|7500|0.6|4|85|4.0|0.015|0.4|High Contrast|-0.2|
|2|Crisp Morning Summer|spruit_sunrise|110|1.0|5200|3.5|18|95|1.5|0.003|0.5|Med High|+0.1|
|3|Foggy Autumn Morning|kiara_1_dawn|70|0.6|6500|1.2|8|100|3.0|0.025|0.6|Med High|-0.3|
|4|Overcast Soft Diffuse|kloofendal_overcast_puresky|200|1.0|6500|0.0|–|–|–|0.001|0.3|Base|0.0|
|5|Clear Blue Summer Noon|kloofendal_43d_clear|180|1.0|5500|5.5|58|180|0.526|0.0008|0.5|Med High|0.0|
|6|Diffuse Winter Midday|winter_sky|160|0.9|7000|1.8|14|175|1.5|0.004|0.4|Med|-0.1|
|7|Partly Cloudy Dappled|kloofendal_48d_partly_cloudy_puresky|140|1.0|5400|4.0|48|170|0.9|0.002|0.5|Med High|+0.1|
|8|Hazy Summer Afternoon|kloppenheim_05|240|1.0|4800|3.2|35|240|1.2|0.005|0.6|Med High|+0.15|
|9|Crisp Autumn Afternoon|kloofendal_43d_clear|250|0.9|4500|3.0|22|245|0.8|0.003|0.5|High Contrast|+0.1|
|10|Stormy Afternoon Mood|qwantani_puresky|260|0.6|6000|2.5|20|255|1.5|0.012|0.5|High Contrast|-0.4|
|11|Front-lit Golden|spaichingen_hill|90|0.9|3400|4.5|6|95|0.6|0.006|0.6|Med High|+0.2|
|12|Backlit Golden|kloppenheim_06_puresky|270|1.2|3200|5.5|5|265|0.5|0.008|0.7|High Contrast|-0.1|
|13|Side-lit Golden|venice_sunset|200|1.0|3500|4.0|7|215|0.7|0.006|0.6|Med High|+0.15|
|14|Blue Hour After Sunset|the_sky_is_on_fire|300|0.7|9500|0.2|-3|280|1.0|0.018|0.4|Med|-0.5|
|15|Civil Twilight|spiaggia_di_mondello|290|0.5|8500|0.4|-2|285|1.5|0.014|0.4|Med High|-0.4|
|16|Night Practical Lights|dikhololo_night|0|0.4|12000|0.0|–|–|–|0.020|0.5|Med|-1.0|
|17|Moonlit Night|kloppenheim_02_puresky|220|0.8|11000|0.15|25|200|0.526|0.022|0.5|High Contrast|-1.2|
|18|Light Rain|cloudy|180|0.9|6800|0.0|–|–|–|0.008|0.3|Med|-0.2|
|19|Snow Afternoon|snowy_field|200|1.1|6500|2.5|16|210|1.0|0.005|0.4|Med High|+0.2|
|20|Frost Morning|winter_river|95|1.0|7200|2.8|10|100|0.8|0.010|0.5|High Contrast|-0.1|
|21|Magazine Cinematic|kloppenheim_06_puresky|260|0.8|4200|3.5|12|250|1.0|0.009|0.6|High Contrast|-0.3|
|22|Pinterest Dreamy|spruit_sunrise|120|1.2|5500|2.5|15|110|2.5|0.004|0.7|Base|+0.4|
|23|Real Estate Clean|kloofendal_overcast_puresky|180|1.1|6000|1.5|45|175|1.5|0.0005|0.3|Base|+0.1|
|24|Spring Bloom Pastel|kiara_1_dawn|130|1.0|5800|2.8|30|130|1.0|0.003|0.6|Med High|+0.25|
|25|Indian Summer Late|venice_sunset|225|1.1|3800|3.8|12|230|0.7|0.005|0.6|High Contrast|+0.15|
- All recipes use `view="AgX"`. A drop-in Python `RECIPES` dict + `apply_recipe(name)` function exists (uses `kelvin_to_rgb` Tannenbaum approx, `HDRI_DIR="//hdris/"`, loads `{hdri}_4k.hdr`, sets SUN energy/angle/color/rotation_euler `(radians(90-alt),0,radians(az))`, sets view_settings view/look/exposure, gamma=1.0). Ground-fog recipes (#1,#3,#10,#14,#16,#18,#20): add optional cube volume density 0.05, height 1.5m.

### HDRI + Sun sync workflow (Outdoor Archviz Setups; Lighting Recipes note; HDRMaps)
- Enable built-in **Sun Position** addon (Preferences > Add-ons). Modes: "Sun + Sky Texture" (procedural, no HDRI) or **"Sun + HDR texture"** (photoreal). In viewport preview click **"Sync Sun to Texture"**, click brightest spot on HDRI to lock direction → Sun placed at that exact angle.
- **HDRI strength**: BG default 1.0; camera-visible BG 1.5-2.0; lighting-only HDRI (separated via Is Camera Ray) 0.2-0.5 to avoid double-lighting.
- **HDRI rotation-Z convention**: 0°=north (also "sun behind camera"), 90°=east, 180°=south, 270°=west (default Map UV). Rotate Z 90-135° = sun camera-right/back → rim light on cabin.
- Use `_puresky` HDRI variants for cabin hero shots (avoids HDRI's baked terrain conflicting with foreground).
- Setup choice: Sun-only + procedural Nishita Sky = hero golden hour/animations (flat reflections); HDRI-only = overcast/blue hour/product (mushy shadows); **HDRI + Sun = industry default (90% archviz)**.

### Three-point exterior (Outdoor Archviz Setups)
- **Key = Sun**: 5.0 W/m², 5500K, Angle 1° → facade + long shadows.
- **Fill = HDRI**: strength 0.3-0.5 sky-only, MIS ON.
- **Rim/back**: secondary Sun OR Area light behind cabin — 50-150 W, 4-6 m² area, 4500K, 25-40% of key; put in Light Group "rim" to dial in compositor.

### Mix-shader trick (HDRMaps; old Lighting note)
- For "nice sky, wrong lighting" (or vice versa): two Environment Textures (A cosmetic/soft background, B technical/sharp for lighting+reflections) → **Mix Shader** with Factor = `Light Path > Is Camera Ray` → World Output. Camera sees A; shading/reflections use B. Gold standard when sky must look right but lighting must be steered.

### Color temperature (Kelvin)
- Time-of-day (old Lighting note): Pre-dawn/blue-hour morning 9000-10000K; golden hour 3200-3500K; mid-morning/afternoon 5000-5500K; midday 5800-6500K (avoid, hard shadows); overcast 6500-7500K; twilight evening blue hour 8500K.
- **Blackbody node** reference (Outdoor note, physically accurate light color): 1800K candle #ff8b14; 2200K sodium #ffa757; 2700K warm LED #ffb16e; 3200K tungsten #ffc18d; 4000K neutral #ffd6ae; **5500K daylight #fff2e0**; 6500K overcast #ffffff; 10000K blue-hour #c9d9ff.

### Practical / interior lights (Outdoor Archviz Setups)
- Real-world LED W in Cycles: Path bollards 8-12W/2700K/0.05m point; Wall lantern (door) 25-40W/2700K/0.08m spot; Pendant over deck 40-60W/3000K/0.25m area; String light per bulb 3-5W/2400K tiny point; Tree up-lighter 15-25W spot/4000K/blend 0.3.
- Cycles enforces inverse-square → keep light **Size > 0 (0.02-0.1m)** to avoid fireflies; Light Falloff > Quadratic if custom emission.
- **Interior visible through window/carport**: exterior key 5500K/5 W/m² + interior Area 0.6×0.4m, 30-60W, 2700-3000K facing outward. Ratios: noon interior 1.5-2 EV below exterior; blue hour interior +0.5 EV brighter. Use Light Path > Is Glossy Ray to cut caustic blowout on glass; **Glass IOR 1.45**; add **Light Portal** in window frame for clean sampling.

### Volumetric atmosphere — Volume Scatter density (m⁻¹) & anisotropy (ACES-OCIO note + Atmospheric note)
| Condition | Density (m⁻¹) | Anisotropy |
|---|---|---|
| Crystal clear (30km vis) | 0.0002-0.0005 | 0.3 |
| Light haze (10km vis) | 0.002-0.005 | 0.4 |
| Hazy afternoon | 0.01-0.02 | 0.5 |
| Morning mist | 0.03-0.08 | 0.6 |
| Heavy fog (50m vis) | 0.1-0.3 | 0.7 |
| Dense Dutch polder fog | 0.4-0.8 | 0.75 |
- Anisotropy: 0=isotropic; real fog forward-scatters → 0.5-0.75 natural; 0.85+ exaggerates god-rays.
- Older Atmospheric-note ranges (World Volume Scatter): subtle haze 0.005-0.015 (aniso 0.4); morning mist bounded cube 50×50×3m density 0.025 (aniso 0.3); heavy fog 0.1-0.3 (~3× perf). Keep world-volume density VERY low (0.001-0.005) or scene becomes "soup".
- **World volume** = scene-wide haze/distance fog (cheap). **Empty Cube + Volume material** = localised ground fog / interior beams / pond mist (Shade Smooth off, no UVs, drive density via noise/gradient).
- **Dutch polder fog = both**: World volume density 0.05 + flat cube 5m tall on grass, density 0.3-0.4, gradient mask dense-at-ground fading by ~3m (1.0 base → 0 top), aniso 0.7.

### Aerial perspective / god-rays (ACES-OCIO + Atmospheric)
- **A. Procedural Mist/Z-pass (zero render cost)**: View Layer→Passes enable Mist; World→Mist Pass Start 20m, Depth 200m, Falloff Quadratic; Compositor Mix, factor=Mist, color `#a8b8c4` atmospheric blue. Covers 95% of exterior stills.
- **B. Full volumetric (+30-60% render time)**: World Volume Scatter captures god-rays through trees; use when low sun + tree backdrop.
- **Hybrid (recommended)**: World volume very low density 0.001 for sun shafts + compositor mist on top for distance blue.
- **God-rays trick** (Atmospheric note): World Volume Scatter density 0.005 + aniso 0.5; **Sun strength 8-10** (high, to punch through volume); camera looks toward sun behind trees; trees must be real shadow-casting geometry (cards fail); render 256+ samples.
- **Real vs fake god-rays** (ACES note): real = Cycles World volume + Sun Angle 3-5°, Volumes Step Rate Render 0.2-0.5, Max Steps 256 (needed when shafts pass between objects — forest/pergola slats). Fake = compositor Sun Beams node, 1000× cheaper, OK for flat-roof modern cabins with no occluders, useless for cottage-through-trees.
- **Sun-scatter coupling (make-or-break)**: clear day Sun 5-10 W/m² + scatter 0.002; golden-hour backlit = double scatter (0.01) + warm sun 2800K str 3-5. **Diagnosis: fog looks grey/flat → need MORE sun energy, not more density.**
- **EEVEE Next volumetrics** (animation walkthroughs): World→Volumetrics Tile Size 4px, Samples 128, Start 0.1, End 200 (approximate but real-time; Cycles for final stills).

### Mist Pass compositor pipeline (Atmospheric note — cheap depth fade)
- Camera Properties > Mist enable; World Properties > Mist Pass Start (e.g. 10m) / Depth (e.g. 50m) / Falloff (Linear/Quadratic/Inverse Quadratic); Render Properties > Passes > Mist.
- Compositor: `Render Layers Mist → ColorRamp → Mix(Add) → subtle white/atmosphere-color tint, factor 0.15-0.4`. Cool tint `#B5C8D9`, warm `#FFF5E0`/cream. Avoid hard cutoff (use Falloff).

### Steam / smoke / fire (Atmospheric note)
- Hottub steam (still): Volume Cube above water, low Density Noise + upward gradient; white emission. Chimney smoke: Volume Cube density-noise vertical gradient + 4D noise, OR smoke-texture billboards. Fire pit/bbq: light orange-red 1500-2000K str 0.5-2 + local volume scatter above fire for heat-haze. Don't emit steam from cold objects.

### Render / sampling settings for lighting quality
- **Cycles** required for photoreal finals (GI, soft shadows); Eevee Next only for preview (misses accurate HDRI GI on complex foliage) (HDRMaps, old Lighting note).
- Sampling (old note): Adaptive 256, Noise threshold 0.01, Min 64. Denoising ON (OpenImageDenoise; OptiX on NVIDIA).
- Light Paths defaults: Diffuse 4 / Glossy 4 / Transmission 12 / Volume 2 (boost transmission for glass-sauna).
- Volumes: Step Rate Render **0.5** (default 1.0 doubles cost), Max Steps 128 stills / 64 anim. Persistent Data ON for anim, OFF for single still. Light Tree ON (4.x+). World-level volumes cheaper than object-bounded. Volume samples default 8 → drop to 4 for previews; Volume bounces 1; Light Threshold 0.01.
- **8GB VRAM / RTX 3070 volumetric cost** (ACES note): World volume +20-40% time (negligible VRAM); localised cube +30-60% time (~200MB); VDB smoke 500MB-2GB (skip for archviz).
- **Anti-flicker** (Outdoor note): Stills → Clamp Indirect 10.0, Clamp Direct 0/off, Adaptive 0.01, 1024-2048 samples, OptiX denoise OK. Animations → Clamp Indirect 5.0, Min Samples 64, Adaptive 0.005, Persistent Data ON, same denoiser per frame (OptiX-Temporal 4.x+), lock seed, disable Light Tree for anims <2 min.
- Adaptive sampling saves 30-50% render time (HDRMaps).

### Compositor grade hints (Lighting Recipes Catalog 25) — Lift / Gamma / Gain
| Recipe class | Lift | Gamma | Gain |
|---|---|---|---|
| Wellness/Real Estate | (0,0,0) | 1.00 | (1,1,1) neutral |
| Lifestyle warm | (+0.01,+0.005,−0.005) | 0.95 | (1.02,1.00,0.98) warm shadows, cool highs |
| Editorial moody | (+0.02,+0.01,+0.03) | 1.10 | (0.95,0.97,1.02) lifted blue shadows |
| Premium golden | (−0.005,0,+0.005) | 0.92 | (1.05,1.00,0.93) crushed teal-orange |
| Night/Blue hour | (+0.03,+0.02,+0.05) | 1.15 | (0.90,0.95,1.10) strong blue lift |
| Snow/Frost | (+0.01,+0.015,+0.02) | 1.00 | (1.00,1.02,1.05) cool highlights |
- Studio references: Brick Visual = Filmic→AgX migration + low-contrast LUT + post grade; MIR = real chromatic aberration + atmospheric haze cube; Bloomimages = AgX Base + subtle warm shadows.

### Physically-based recipes (ACES-OCIO note, hex = volume color)
- **Crystal clear summer (NL)**: Sun Angle 0.5°, Str 8, 5500K, Elev 60°; World vol density 0.0003 aniso 0.4 `#c8d8e8`; compositor mist Start 100m Depth 500m quadratic.
- **Light hazy afternoon**: Sun Angle 1.5°, Str 4, 4500K, Elev 35°; vol 0.008 aniso 0.55 `#d8d4c8`; no compositor mist.
- **Golden-hour backlit haze**: Sun Angle 2°, Str 5, 2800K, Elev 8°; vol 0.015 aniso 0.75; HDRI sun BEHIND cabin.
- **Foggy Dutch polder morning**: Sun Angle 4°, Str 1.5, 4000K, Elev 12°; World vol 0.08 aniso 0.6 `#c0c4c8`; ground cube 5m tall × scene-sized density 0.4 gradient (1.0→0) aniso 0.7; compositor subtle blue shadow lift + gentle black crush.
- **Blue hour mist over pond**: Sun off/very low (Str 0.3, 8000K); HDRI "blue_hour"/`dikhololo_night` EXR strength 1.5; World vol 0.02 `#a0b0c8`; pond cube density 0.5 animated noise; 1-2 interior area lights 3000K 50W for window glow on mist.

### HDRI catalog (old Lighting note, all Polyhaven CC0)
- Garden: studio_garden_4k, symmetrical_garden_4k, tiergarten_16k (autumn overcast), soliltude_22k. Forest: kloofendal_43d_clear_puresky_4k, kloofendal_overcast_puresky_4k, forest_slope_4k, mossy_forest_4k. Golden/sunset: qwantani_dusk_2_4k, qwantani_noon_4k, gem_2_4k, dikhololo_night_4k. Overcast/cool: kloppenheim_03_4k, belfast_sunset_puresky_4k, industrial_sunset_02_puresky_4k. Open: stadium_exterior_29k, christmas_photo_studio_03_4k.
- HDRMaps table: golden hour `qwantani_dusk_2`/`the_sky_is_on_fire` sun 2.0-3.0, cam −0.5 EV; overcast `rural_landscape_4k` sun 0 (HDRI has sun), 0 EV; blue hour `kloppenheim_03` sun 1.0 warm, −0.3 EV; night dark HDRI + window emission sun 0.1, +0.7 EV. IES profiles for evening spot/lamp accent alongside HDRI.

### Per-style lighting recipes (old Lighting note, Filmic-era — cross-check strengths with Catalog 25)
- Modern Minimalist: symmetrical_garden_4k / kiara_1_dawn; sun midday str 3.0, 5500K, sharp shadows OK.
- English Cottage: tiergarten_16k / soliltude_22k; low/no sun, diffuse, warm 5800K.
- Scandinavian sauna: qwantani_dusk_2_4k / kloppenheim_03; sun 15-20° warm 3300K, str 4.0 side-light.
- Forest/wilderness: mossy_forest_4k / forest_slope_4k; sun 30-45° dappled, Volume Scatter god-rays, str 5.0.
- Mediterranean: gem_2_4k / qwantani_noon; sun 60-70° str 4-5 warm 3800K, harsh shadows OK; vol 0.001 heat-haze.
- Japanese Zen: kloofendal_overcast_puresky; low/no sun, diffuse; avoid golden hour; HEAVY mist Pass depth 5m factor 0.7 + vol 0.005.
- Boerderij: soliltude_22k / belfast_sunset_puresky; sun 40-50° str 3.5 warm 4500K "Hollandse middag"; light vol 0.001 + subtle mist depth 50m factor 0.15.
- Alpine: snow/mountain overcast; sun high cold 6000K str 5+; no volume (clear air), crisp.
- Coastal/duinen: dikhololo_night / qwantani_dusk_2; low golden sun; mist depth 50m factor 0.5.

### Common mistakes (lighting) — old Lighting note + ACES note
- HDRI strength too high → sky overpowers, flat shadows (default 1.0). Sun direction not synced to HDRI → double/crossed shadows = fake. No sun on clear HDRI → mushy shadows. Excess bloom/glare → looks like render not photo. Cool-blue sun on cozy/cottage = context mismatch. Double colour transform (never screenshot viewport — render through File Output node). Linear HDRI gamma'd → sky blown out.


---

<a id="5"></a>
# §5. Materials & shaders

Blender 4.2+/5.x, Cycles, Principled BSDF. Hex = sRGB. Priority order for cabin surfaces: **blokhutwinkel-textures FIRST → polyhaven/sketchfab → procedural** (Blokhutwinkel Real Product Textures).

### 5.1 Blokhutwinkel real-product textures (PRIMARY source)
- Path: `~/Documents/Blender-blokhutten/assets/blokhutwinkel-textures/` (Blokhutwinkel Real Product Textures). Absolute in code: `C:\Users\beike\Documents\Blender-blokhutten\assets\blokhutwinkel-textures\8192`.
- Structure: `8192/` = 16 JPG @ 8K (primary); `8192-complete/` = full PBR set for `luxehouse-onbehandeld` (COLOR/NRM/DISP/OCC/SPEC PNG); `origineel/` = `.psd` source of luxehouse-grijs-gedompeld.

**Wall/accent textures**
| File | Size | Colour | Best for |
|---|---|---|---|
| `luxehouse-grijs-gedompeld.jpg` | 2.4MB | charcoal grey-blue | Scandi modern walls (Camelia signature) |
| `luxehouse-grijs.jpg` | 2.5MB | medium grey | lighter wall alt, terras |
| `luxehouse-onbehandeld.jpg` | 2.7MB | warm cream-beige | natural wall (Cottage/Boerderij) |
| `kdi_rabat.jpg` | 9.6MB | warm light brown | standard cabin wall (Lelie?) |
| `kdi_potdeksel_zwart.jpg` | 8.0MB | pure black | modern minimalist accent |
| `kdi_rabat_fbz_zwart.jpg` | 8.9MB | pure black w/ grain | modern zwart wall (alt to Shou Sugi Ban) |

**Trim/beam/door**: `hardhout-deuren-ramen.jpg` (12MB, warm cedar tan → **door+raam frame**); `hardhout.jpg` (25MB, golden hardwood → trim); `douglas.jpg` (9.8MB → roofBeam/roofboard/poles, NL standard); `douglas-rabat.jpg` (11MB → wall as Douglas planken).
**Roof**: `shingles-zwart.jpg` (5.1MB → roofPlate schuin dak Lelie/Camelia); `staalpannen-antraciet.jpg` (2.8MB → metal roof); `epdm.jpg` (2.2MB → flatroof Magnolia/Modern plat dak).
**Foundation**: `beton.jpg` (4.2MB → foundationBeam all pilots); `muur-diff.jpg`+`muur-disp.jpg` (baksteen diffuse+displacement pair).

**Style combination matrix**
| Style | Wall | Door/trim | Roof | Foundation |
|---|---|---|---|---|
| Scandi modern (Camelia) | luxehouse-grijs-gedompeld | hardhout-deuren-ramen | shingles-zwart | beton |
| Modern Japandi (Magnolia) | luxehouse-grijs-gedompeld / kdi_rabat_fbz_zwart | hardhout-deuren-ramen | epdm | beton |
| Cottage (Lelie) | luxehouse-onbehandeld | hardhout-deuren-ramen | shingles-zwart | beton |
| Boerderij | kdi_rabat | hardhout-deuren-ramen | staalpannen-antraciet | beton |
| Modern minimalist zwart | kdi_rabat_fbz_zwart / kdi_potdeksel_zwart | hardhout-deuren-ramen | epdm | beton |
| Natural cedar | douglas-rabat | hardhout-deuren-ramen | shingles-zwart | beton |

- Open gaps: no Shou Sugi Ban/charred texture (use procedural recipe below), no weathered-grey (luxehouse-grijs closest but dipped not weathered), no seasonal variants (Blokhutwinkel Real Product Textures).
- Why not polyhaven `dark_planks`: generic dark wood, no luxehouse/kdi branding, not 8K, no marketing-consistency with product photos (Blokhutwinkel Real Product Textures).

### 5.2 Camelia node-graph pattern (PROVEN, verified 2026-05-21)
Per-material graph, applied to GLB cabins: `TexCoord → Mapping(scale 4,4,4)→ImageTexture A`; second `Mapping2(scale 5.5,5.5,5.5, rotation Z=1.3 rad ≈75°)→ImageTexture B (same image)`; `Noise(scale 1.5, detail 2)→ColorRamp(sharp 0.35–0.65)→Mix.Fac`; Mix(MIX, A/B)→BSDF Base Color. BSDF **Specular IOR Level 0.3**; Roughness 0.85 wood / 0.55 hardhout / 0.9 shingles (Blokhutwinkel Real Product Textures).
- 2 mappings @ different scale+rotation break visible tiling; works via **Object coords** on GLB meshes without UV; anti-tile also works with UV coords (both mappings take `tc.outputs['UV']`).
- Helper fn `apply_camelia_texture(mat_name, texture_filename, roughness=0.85, coord_mode='UV', scale=(1,1,1))` clears all nodes then rebuilds; `img.extension='REPEAT'`; `bpy.data.images.load(..., check_existing=True)` (Blokhutwinkel Real Product Textures).
- Verified 2026-05-21 (`2026-05-21-magnolia-garden-build`): 6 materials → two-tone Scandi look on Magnolia.

**Tile scale**: 4x = 1 tile / 25cm. Wide cabin (4m+): Map1 scale 4 (25cm) + Map2 scale 5.5 (18cm). Close-up (<3m camera): try scale 6+8 for finer plank pattern (Blokhutwinkel Real Product Textures).

### 5.3 UV vs Object coords — critical per-material rule
Camelia blokhut-GLBs have proper UV unwrap on door+roof+beams — USE it or you get tile-pattern on door instead of real panel look (Blokhutwinkel Real Product Textures).
| Material | Coord | Reason |
|---|---|---|
| `basetexture-firstLayer-door` | **UV** | door UV-mapped panels (1536 verts, 600 polys); Object=generic tile=wrong |
| `basetexture-firstLayer-roofBeam` | **UV** | grain along length |
| `basetexture-firstLayer-roofboard` | **UV** | board UVs mapped |
| `basetexture-firstLayer-roofPlate` | **UV** | EPDM/shingles UV mapped |
| `basetexture-firstLayer-fasciaboard` | **UV** | fascia |
| `basetexture-firstLayer-poles` | **UV** | vertical, UV along length |
| `basetexture-firstLayer-wall` | **Object** | large wall; UV stretch distorts annual rings; Object=consistent plank pattern |
| `basetexture-firstLayer-foundationBeam` | **Object** | beton tile, no UV needed |

- **Texture-direction fix (superseding)**: GLB puts cladding on BOX projection → potdeksel grain 90° wrong. Fix = mesh-UVMap + FLAT via `cl.uv_board_textures()` so grain follows the plank (Blokhutwinkel Real Product Textures → Blokhut Render-Fix Lessons). This is the current guidance for wall grain direction.

### 5.4 Hardware materials (verified 2026-05-21, Magnolia M26)
- **Glass**: Base (1,1,1), Metallic 0, Roughness 0 (or dirt noise), **IOR 1.45**, **Transmission Weight 1.0** (essential), Alpha 1.0; dirt = Noise(scale 50, detail 2)→ColorRamp(0.4–0.6→0..0.08)→Roughness. Set `scene.cycles.transmission_bounces = 12` (default 8 too few for clean glass) (Blokhutwinkel Real Product Textures).
- **Chrome/brushed steel** (handle/hinges/trim): Base (0.72,0.72,0.72), Metallic 1.0, Roughness 0.25 (brushed, NOT 0=mirror), Anisotropic 0.6.
- **Anthracite metal** (door posts/accents): Base (0.06,0.06,0.07), Metallic 0.85, Roughness 0.45 (coated matte).
- **Hidden GLB elements** to unhide for full renders (default off): `.DEURBASIC.DEURBASIC` (glass panels), `.doorhandle`, `.scharnier-hinge`, `.scharnier-0-1/0-2/1-0/1-1/1-2`, `trim-1/2/3`, `door_pot`, `door_pot_R`, `pot_plant_L/L_b/R/R_b`.

**NOTE — glass IOR conflict**: Blokhutwinkel note uses **IOR 1.45** (verified Magnolia); Advanced Material Recipes specifies **IOR 1.52** (soda-lime float, "NOT 1.45") plus Transmission Roughness 0.0, Dispersion 0.05–0.15 (Cycles 4.1+), and a green-cyan tint `#F4F8F5`. Advanced recipe is the more detailed/newer (2026-05-22) hero spec; Blokhutwinkel 1.45 is the proven quick default.

### 5.5 Twelve production Cycles recipes (Advanced Material Recipes Archviz)
- **1 Cabin window glass**: Base `#F4F8F5`, Metallic 0, Roughness 0 (+0.005–0.02 via dirt), **IOR 1.52**, Transmission 1.0, Transmission Roughness 0.0, **Dispersion 0.05–0.15**, Alpha 1.0. Dirt=Noise(200)→ColorRamp(0.55–0.7); water spots=Noise(800)→Bump 0.02. PRO: disable Refractive Caustics; Light Path>Is Shadow Ray → Transparent BSDF for shadows = render −30–40%.
- **2 Weathered cedar/larch facade**: TexCoord(Object)→Mapping(x4,y40,z4); Wave(Bands,X,scale2,distortion1.5,detail8)=grain; Noise(15)=plank hue mix; Object Info>Random→ColorRamp→HSV Hue ±0.03/Value ±0.15; Bevel(radius 0.002, samples 4)→Normal. Base random `#B8956A`→`#8B6F4E`; Roughness dark grain 0.85 / light 0.65; Specular IOR Level 0.35; Bump 0.08. Fresh red cedar `#C68D5A` R0.55; silver-grey `#9C9489` R0.9 Sheen 0.1. PRO: UV along ONE axis (Y) w/ 40x stretch; weather look = Bevel + AO multiplied into Roughness.
- **3 Shou Sugi Ban**: 2 Voronoi — `Voronoi(F1,scale30)→ColorRamp(0/0.08/0.15)`=cracks + `Voronoi(scale120)`=micro-flakes; `Wave(scale4,distortion2)`=grain. Base gradient `#1A1715`→`#2E2A26`→`#4A3E2E`; Roughness cracks 0.95 / flat 0.55; **Sheen Weight 0.15, Sheen Roughness 0.4, Sheen Tint `#3A3A3A`** (signature satin glint); Bump Voronoi 0.5 + grain 0.1. Modern matte black (Zwarthout): kill sheen, R0.85 uniform. PRO: expose grey grain via Wave→ColorRamp clipped 0.7–0.85 as `#5C4F3E` at fac 0.08.
- **4 Wicker/rattan**: TexCoord(UV)→Mapping(40,40,1); 2 Wave (Bands) rotated 90°→Math Multiply→ColorRamp; Checker=top strand; Noise(600) anisotropic. Base `#C49968` ±0.08 hue; Roughness 0.55 / gaps 0.85; **Subsurface Weight 0.05, Radius (0.3,0.2,0.1), Color `#F0C088`**; Bump 0.3 (80% of look). Poly-rattan: kill SSS, R0.7, `#8B7A65`.
- **5 Linen fabric**: 2 perpendicular Voronoi(F1,scale400) multiplied → **Displacement output** (scale 0.0005, midlevel 0), Surface>Displacement = Displacement and Bump, Adaptive Subdivision dicing 1.0. Base sage `#A8B098`/oat `#D8CFB8`/off-white `#EFE7D3`; Roughness 0.75–0.85; **Sheen Weight 0.5** (key), Sheen Roughness 0.25, Sheen Tint `#F0EBE0`; SSS 0.1 (pillows) Radius (0.4,0.3,0.2); Specular IOR Level 0.4. Velvet Sheen 1.0 R0.6. PRO: use new Sheen lobe (4.0+), NOT Fresnel-mix hack (old Layer Weight tutorials obsolete).
- **6 Vegetation leaf**: Image alpha→Alpha; Blend Mode Alpha Clip Threshold 0.5, Shadow Mode Alpha Clip; Geometry>Backfacing→Mix Shader→Translucent BSDF `#88B070` fac 0.4 (or 4.1+ Thin Walled toggle + SSS). Front Base→`#5C8A3A`; Roughness clamped 0.4–0.6 (waxy); **SSS Weight 0.2 Color `#A8C870` Radius (0.5,0.3,0.15)**; Specular IOR Level 0.6; **IOR 1.42** (cuticle, NOT 1.5); Normal 0.7. Hydrangea translucency 0.5; conifer needles kill SSS R0.7. PRO: disable shadow casting on translucent mix via Light Path>Is Shadow Ray (prevents black foliage voids).
- **7 Wet cobblestone**: Voronoi(Smooth F1,scale12,randomness0.8)+Brick(mortar); wet mask=Geometry>Pointiness→ColorRamp(0.4–0.55); moss=Noise(8)→ColorRamp(0.6–0.7)×Z-mask. Stone `#3E3833` R0.7 Spec IOR 0.5; wet R0.08 base×0.5; moss `#4A6034` R0.8 SSS0.05; Normal cobble 0.5 + micro-pebble(scale500,0.05). PRO: drive Roughness with Layer Weight>Facing (low at glancing only); water fills cracks first (Pointiness).
- **8 Anthracite klinker (Dutch paving)**: Brick(scale10,mortar0.02,brick_width0.6,row_height0.3); per-tile via Voronoi F1 Cells (preferred over Brick). Base `#2A2826`/`#34302C`/`#3E3A36`; Roughness 0.78±0.05; Spec IOR Level 0.45; Bump micro-noise(scale1000,0.02)+mortar grooves 1.0. PRO: never uniform; Brightness/Contrast boost on random 5% (fresh tiles).
- **9 Lawn grass (hair/GN)**: Hair Info>Intercept→ColorRamp root `#3A5028`/mid `#6B8C3F`/tip `#A4B85C`; Object Info>Random hue ±0.06; Noise(scale2) field. Roughness 0.6–0.7 tips 0.5; **SSS Weight 0.15 Color `#9CB050` Radius (0.4,0.3,0.1)**; Spec IOR Level 0.45; optional Sheen 0.1 dewy. Dry `#9C9050` kill SSS; wet Sheen 0.3 R0.4. PRO: root darkness NON-NEGOTIABLE; randomize blade scale (Hair Info>Random) into clumps.
- **10 Weathered concrete**: Noise(scale3,detail16)+Voronoi(80) aggregate; stains Noise(1.5,detail2)→clipped ColorRamp→`#3A352F`; rain streaks Mapping Z=5x low-distortion fac 0.1. Base `#A8A29A`; Roughness 0.82 (stains 0.65); Spec IOR Level 0.5; Bump aggregate 0.15 + undulation 0.3. PRO: **vertical tear streaks below edges** via Gradient(Linear,Z) masked under overhangs = #1 selling detail.
- **11 Chrome/brushed alu**: brushed = Tangent(Radial,Z)→Anisotropy Direction, Noise(2000) stretched Y=0.01→Bump 0.05; Base `#C8C9CB`, Metallic 1.0, Roughness 0.35, **Anisotropic 0.7** Rotation 0, IOR 1.39. Polished chrome: Base `#DBE2E9`, Metallic 1.0, Roughness 0.05, Coat Weight 0.3 Coat Roughness 0.0, no aniso. PRO: Tangent(Radial) for cylindrical handles.
- **12 Brass/bronze patina**: patina mask=Pointiness→ColorRamp(0.45–0.55 inverted)×Gradient(Z). Brass polished Base `#B5904A` Metallic 1.0 R0.25. Verdigris Base `#5A8A7C`, **Metallic 0.2** (oxide semi-dielectric!), R0.75, SSS0.05. Bronze `#8A5A30` patina `#4A6850`. PRO: Metallic MUST drop to ~0.2 in oxidized areas or you get "green chrome".
- **Python helper** `make_principled(name, base_hex, metallic=0.0, roughness=0.5, ior=1.45, **kw)` — converts hex→RGB, sets Base Color/Metallic/Roughness/IOR + any BSDF input via kwargs.

### 5.6 Wood recipes & weathering (Wood Material Recipes for Cabin Visuals)
- **Two approaches**: PBR scan (max photoreal, tiling repeats on big surfaces) vs procedural (infinite variation, no UV-stretch). For cabins: **mix** — PBR for close/hero detail (door, deurpost), procedural for large wall planes.
- **PBR sources (CC0/free)**: Polyhaven `bark_brown_02`, `pine_bark`, `weathered_planks`, `wood_planks_*`, `rough_wood`, `wood_table_001`, `cedar_bark`, `oak_veneer_01`. freepbr.com: Scorched Wood Charcoal, Rough Plank Wood, Painted Wood. textures.com: "3D Scanned Charred Wood Planks - Shou Sugi Ban 06x06m" (best SSB on web). BlenderKit free: "Wood03 PBR" (Peter Berghold).
- **10-node procedural basis** (Samuel Sullins): TexCoord(Object)→Mapping(scale Z=10)→Noise(scale5,detail16,distortion0.5)→ColorRamp(sharp, 2 tones)→Mix(w/ Voronoi knots)→Principled(roughness 0.4, specular 0.5). Bump=same Noise→Bump strength 0.05. Knots=Voronoi(Distance to Edge)→ColorRamp dark. End-grain=Object Z direction.

**Per-species**
| Species | Base range | Roughness | Notes |
|---|---|---|---|
| Cedar (Scandi/premium) | `#A86B3D`→`#C49B6F` | 0.5–0.7 | reddish, oxidizes orange-grey |
| Larch | `#7E5C3A`→`#A0856B` | 0.55–0.7 | yellower, harder grain |
| Pine (standard tuinhuis) | `#D4A874`→`#EAC893` | 0.5 | golden, light knots |
| Douglas (NL standard) | `#B0793E`→`#D69960` | 0.5–0.6 | dark late-wood lines; impregneerd → +0.05 specular |
| Oak (luxury) | `#7B5A3C`→`#A07B58` | 0.4 polished → 0.7 rough-sawn | open pores via Voronoi |
| Shou Sugi Ban | `#1A1714`→`#2D2520` (NOT pure black) | 0.6–0.85 | HIGH bump (Voronoi+Noise, strength 0.15), low specular, unburnt edge accents |
| Weathered grey | `#9C968D`→`#B8B0A4` | 0.7–0.9 | heavy bump, vertical drip streaks essential |
| Painted cottage white | `#F5F0E5` | 0.5 | chipping via pointiness → wood beneath |
| Painted boerderij green | `#3F5C3A` (RAL 6009) | 0.4 | pointiness chipping |

- **Weathering**: pointiness dirt/wear = Geometry(Pointiness)→ColorRamp(0.4–0.6)→mix (lighter convex=bleached, darker concave=dirt); Bevel-shader edge wear → Roughness/color shift; drip stains = Generated Z-component → vertical Noise(scale2) → ColorRamp dark streaks in upper area.
- **Anti-tile Mix-Generated-UV**: UV Mapping(scale1)→ImageA + Generated Mapping(scale1.7, rotated)→ImageB, mix by large Noise→ColorRamp.
- **Macro zone-variation (validated 10 jun)**: per-plank Object Info Random alone still reads flat over 3m+. Add meso Noise: `Scale 1.2, Detail 3.0, Roughness 0.5` → ColorRamp(elements at 0.87 & 1.0) → MixRGB MULTIPLY, **Fac 0.06 (max 0.08)** into base color = ~1m tonal zones.
- **Voronoi plank-seam bump (validated 10 jun)**: Voronoi `feature=DISTANCE_TO_EDGE, Scale 8.0, Randomness 0.0` (0 = regular seams) → Bump `Strength 0.4, Distance 0.016` (16mm), chained onto existing bump.
- **Bump limits**: keep Distance ≤ 0.02 for grain, 0.016 for seams (higher = rubber look).
- **Mistakes**: pure-black SSB=plastic; roughness <0.4 only for polished furniture; missing edge-wear=always-new; identical per-plank material=tiling; micro-only (no macro)=flat wall; no vertical drip=fake; bump too high=rubber.

### 5.7 Procedural Shou Sugi Ban recipe (tested 8 mei 2026) — CURRENT for charred, since no product texture exists
Use for: Modern Urban Pavilion black, Scandi sauna dark char, dark boerderij bijgebouw. NOT for pine/cedar or painted white.
- **Key insight**: base color `#1A1714`→`#2D2520`, NEVER (0,0,0) — pure black reads as plastic.
- **Coords**: TexCoord(Object)→Mapping(1,1,1) — Object (not UV), works on GLB without unwrap.
- **Plank seams**: Mapping→Separate XYZ, swap so Z→Combine.Y (brick rows vertical = horizontal planks); Brick Texture: **Mortar Size 0.012 (12mm), Row Height 0.18 (18cm plank)**, Color1/Color2/Mortar = white/black masks. 18cm×1.2cm seam optimal at 5–15m; closer → 12cm/0.5cm.
- **Alligator cracks (2-layer Voronoi, Distance to Edge)**: Layer1 Scale 18 Randomness 1.0 (drying cracks); Layer2 Scale 35 Randomness 1.0 (micro); each → ColorRamp(sharp 0.0–0.10, pos0=white=crack); combine via Math MAXIMUM. Multiply by brick.Color so cracks don't cross seams.
- **Grain (Wave)**: Type Bands, Direction X, Profile Saw, Scale 5, Distortion 8, Detail 4, Detail Scale 1.5, Detail Roughness 0.7.
- **Per-plank brightness hash**: Position.Z → Multiply ×(1/0.18=5.56) → Floor → White Noise(1D, W) → ColorRamp(0.55–1.0).
- **Colour mix (3-layer)**: base `#1A1714`(0.012,0.012,0.014) ←crack fac→ warm `#3D281A`(0.18,0.10,0.05); ←wave×0.25→ char grain `#0A0605`(0.04,0.025,0.02); ×plank_var (multiply fac 0.6); ×brick.Color (multiply fac 1.0, seams pure black).
- **Bump (3-layer chained)**: crack→Bump(Strength 1.0, Distance 0.025); grain wave→Bump(0.4, 0.001); seam brick→Bump(0.6, 0.005).
- **Roughness**: crack→ColorRamp pos0=0.75 (char subtle sheen) / pos1=0.95 (cracks matte). **Specular IOR Level 0.4**.
- **Distance tuning table**:
| Camera | Row Height | Voronoi S1 | Voronoi S2 | Bump Dist |
|---|---|---|---|---|
| Close-up <3m | 0.10 | 6 | 18 | 0.015 |
| Mid 5-10m | 0.15 | 10 | 25 | 0.020 |
| **Hero 10-20m** | **0.18** | **6** | **18** | **0.025** |
| Wide >20m | 0.22 | 4 | 12 | 0.030 |
- **Pitfalls**: pure black=plastic; use Distance to Edge (not Distance); Blender 5.1 `bands_direction` enum changed → swap X/Z for horizontal planks; Random Value FLOAT_VECTOR use `outputs[0]` not `outputs[1]`; Object coord beats Generated for GLB; 12cm planks vanish at hero distance (18cm sweet spot); bump strength 1.0 on cracks essential (<0.5 = flat).
- **Render quality**: 96 samples + OptiX = preview; **256 samples + adaptive sampling 0.01 = standard hero**; 512 + adaptive subdiv on walls = hyperreal close-up. Render time (M4 MacBook Pro): no shader 5–7 min/frame; +procedural SSB (256) +1 min; +adaptive subdiv micro-displacement +5–8 min.
- **Combine**: close-up add adaptive subdivision + micro-displacement; hyperreal add SSS (subsurface weight 0.05 warm glow); weathering pointiness ColorRamp reveals wood on edges; mud splash = vertical Z gradient bottom + Voronoi.

### 5.8 Substance Painter + baking pipeline (for the ~15% hero materials only; status critical)
- **Use Painter ONLY for**: brand-recognizable surface (custom cedar matched to sample), close-up hero (<1m), branded pattern that can't tile from one repeat, decals/text on curves. **Never first-pass**; upgrade only after composition lock. Budget: **2–3 materials/cabin** get Painter; everything else Polyhaven/ambientCG (anything <100px on final render).
- **Licensing (May 2026)**: recommend **Substance Painter perpetual Steam $199.99** (owns v2026 forever, no Adobe lock-in). Subs: Texturing $24.99/mo or $249.88/yr; Collection $59.99/mo or $599.88/yr. Alternatives: ArmorPaint ~$16 OSS MIT (recommended free Painter alt, real-time raytraced, Vulkan 1.3); 3D Coat Textura $180.54/yr or $380.13 floating; Material Maker free (Designer replacement, Godot, v1.6 Apr 2026, ~200 nodes); Quixel Mixer free.
- **Bake workflow**: Blender high-poly (subdiv+bevels+sculpt) → decimate low-poly (~5–15K tris) → UV-unwrap (seams on board ends/panel breaks, one UDIM per hero board) → Apply scale (Ctrl+A) → Shade Auto Smooth 30° + Edge Split on seams → export `low.fbx`+`high.fbx` separate (Selected only, Apply Modifiers OFF on high, Smoothing=Face, +Y up); optional cage inflated 0.01m.
- **Painter**: New Project → **Document Resolution 4K → Normal Map Format OpenGL** (critical — Cycles/EEVEE Next default GL tangent). Bake Normal(GL), World-Space Normal, AO (128 samples hero / 32 prototype), Curvature(Per Vertex), Position, Thickness. Export template **PBR Metallic Roughness**, Padding 16px, PNG 16-bit for normal/height + 8-bit for basecolor/roughness/metallic, naming `{mesh}_{channel}.png`.
- **Channel conventions**: Base Color=sRGB; Normal(GL)=Non-Color→Normal Map node (Tangent,+Y); Roughness/Metallic/Height/AO=Non-Color. Height→Displacement on **Material Output** (not Principled). AO=Multiply w/ Base Color (Mix RGB factor 0.3–0.5, optional). Metallic **binary** for archviz (0 or 1, no greyscale). If normal bumps read as valleys → exported DirectX; re-export GL or invert Green channel.
- **Custom cedar**: ≥4 photos/board (face-on, 45°, raking, macro), perpendicular sun 10–11h/14–15h, shoot RAW ETTR no clipping. Start "Wood Stained Modern" smart material; Edge Wear generator intensity 0.3 + Dirt (Curvature) opacity 0.2; per-board dup 4× tweak hue ±5° / roughness ±0.1 / grain ±15%. UDIM per board 1001–1004.
- **Branded klinker**: source Vandersanden/Wienerberger NL/ARGEX brand sheets; project as stencil (Shift-S); 3-tone gradient (base `#8B4A3A`, Curvature concave +20% darker, Position-Y top +10% lighter); joint material on UDIM 1002 (Concrete Rough, roughness 0.85, `#B5A693`).
- **Branded textile**: 1:1 macro (2+ repeats) → **Substance Sampler "Image to Material (AI Powered)"** = single photo → Normal/Height/Roughness in <2 min w/ built-in delight. (This ML delight is **allowed** per project rule — input is real photo; StableGen/generative diffusion textures banned.)
- **UDIMs in Blender 5.x**: unwrap into tile grid (1001 main, 1002 right, 1011 up); Image Texture Source: Tiled, load `cedar.<UDIM>.png`. **VRAM math**: 4K×10 tiles×5 channels ≈ 800MB/material set; 8GB RTX 3070 borderline → **Texture Limit Render = 2048** (Render>Performance>Simplify) halves VRAM. Addons: Ucupaint v2.4.6 (free), Paint System 2.1.1 (free), SimpleBake (~$25, pick over Bake Wrangler for 5.x), DECALmachine v2.16.1 (~$30, Blender 4.3–5.1) for branded stickers/house numbers (or free GN decal projector).
- **Live Link** (Kambari, Blender 5.1+ ↔ Painter 12): persistent socket, bi-directional, saves ~1h/material; add once >5 hero materials/month.
- **File org**: one `.spp` per category, version in filename (`_v01`), Git LFS for `.spp`/`.sbsar`/large PNG.

### 5.9 Replicate flux-schnell AI textures (status current) — supplement only
- Model `black-forest-labs/flux-schnell`; ~1 sec/image, **~$0.003 each**; PNG, 16:9 or 1:1, `megapixels:"1"`; output `replicate.delivery` URL valid **24h** — download immediately. Full archviz set (8–12) = $0.04–0.06; 100 textures ≈ $0.30.
- **Use for**: things with no real-product counterpart — hedges, gravel, brick pavers, leaf-sprigs.
- **NOT for**: detail-critical cabin wood (keep real Blokhutwinkel photos); direct normal/roughness maps (flux = COLOR only, bump-from-color OK for low-detail, not metal/glass); guaranteed-seamless tiling (edge-match variable → post-process boundary-blend).
- **Prompt patterns**: tileable surface = "seamless tileable [material] texture, [details], photorealistic, flat front orthographic view, even flat lighting, no shadows, no perspective, high detail, repeating pattern, 4K"; isolated sprig = "single sprig of [plant], ... isolated on pure white background, studio product photo, top-down view, sharp focus, no shadows".
- **Blender wiring (box-projected)**: Mapping Scale (1.5,1.5,1.5) = 1.5 tiles/m; `tex.image.colorspace_settings.name='sRGB'`; `tex.projection='BOX'`, `projection_blend=0.3` (works on cube without UV); Color→Bump `Strength 0.65`→Normal.
- **Alpha-cutout from white-BG sprig**: TEX.Color→SeparateXYZ→Math Min(R,G)→Min(,B)→ColorRamp [0.75=white, 0.88=black]→BSDF.Alpha; `mat.blend_method='HASHED'` and `shadow_method='HASHED'` (NOT 'CLIP' — edges too binary).
- **Examples**: Roosmarijn 2026-06-05 boxwood/beech/yew hedge + boxwood leaf sprig ($0.003 each); earlier Zonnebloem PATINA (herringbone parquet, William Morris wallpaper) 4 textures $0.012.

### 5.10 Cross-cutting numeric anchors
- Standard cabin BSDF: Specular IOR Level **0.3** (Camelia pattern) / 0.4 (SSB charcoal) / 0.35–0.5 (weathered wood/stone).
- Glass IOR: **1.45** (proven quick) vs **1.52** (detailed hero, Advanced recipe). Leaf cuticle IOR **1.42**. Brushed alu IOR 1.39.
- `transmission_bounces = 12` for clean glass (default 8).
- Bump distance ceilings: grain ≤0.02, plank seams 0.016.
- Texture Limit Render 2048 to stay in 8GB VRAM (RTX 3070) with UDIM/8K sets.


---

<a id="6"></a>
# §6. Vegetation & scattering

### Core GN scatter node-pattern (default, free, all Blender 3.0+)
- Base graph: `Distribute Points on Faces → Instance on Points (Object/Collection Info) → [Set Material] → Output` (Geometry Nodes Scattering; Vegetation Scattering Recipes).
- **Distribute Points on Faces: use Poisson Disk, NOT Random** — less clumping (Vegetation Scattering Recipes). Poisson `Distance Min: 0.3` controls spacing (Blender Garden Archviz Scattering).
- Rotate Instances: **random Z-axis ONLY** (0 to 6.283 = tau). Random rotation on all axes = leaves stand crooked (Blender Garden Archviz Scattering; Vegetation Scattering Recipes).
- Scale Instances: random **0.7–1.3** (Recipes) / **0.8–1.2** (Recipes node-essentials) / min **0.7** — **never 0**, zero-scale still renders (Blender Garden Archviz Scattering).
- **Realize Instances: avoid** unless per-instance editing / exporting to another tool. Instancing cheap, realization expensive (all notes).

### Density figures (per m²)
| Target | Density | Source |
|---|---|---|
| Grass | 50–200 | Vegetation Scattering Recipes |
| Ground cover (ferns/weeds/shrubs), Poisson | Density Max 5, Distance Min 0.3 | Blender Garden Archviz Scattering |
| Bushes/trees | 0.1–2 | Vegetation Scattering Recipes |
| Cottage garden floor | 80 | Vegetation Scattering Recipes |
| Hedge sprigs (GN, real leaf) | ~500/m² Poisson | Hedge Creation |
| Hedge leaf-cards (legacy particle) | 80–150/m² (default 50 too sparse), ~100/m² baseline | Hedge Creation |
| Forest floor: dead-leaves 200 / ferns 5 / mushroom cluster 0.3 / stones 1 | layered | Vegetation Scattering Recipes |
| Mediterranean gravel: stones 500 (micro-rotation) | no grass | Vegetation Scattering Recipes |
| Alpine wiese: grasses 200 / edelweiss+gentian 0.5 / stones 2 | layered | Vegetation Scattering Recipes |

### Density masking techniques (do NOT scatter uniformly)
- **Vertex group / weight paint**: new vertex group "density" on ground plane, paint 1.0 where plants go / 0.0 on path; in GN read via Named Attribute "density" → multiply into Distribute density input (Geometry Nodes Scattering; Recipes).
- **Texture-driven**: Noise Texture → Density input = patchy fill (Geometry Nodes Scattering).
- **Slope mask**: `Normal → Dot with UP (0,0,1) → Compare >0.7 (flatter) → boolean density` — no grass on steep faces (Recipes; Geometry Nodes Scattering).
- **Boundary/proximity mask**: distance-from-object/curve; near object = density 0, far = 1. Stops grass poking through cabin foundation / walls / paths (Recipes; Geometry Nodes Scattering).
- Ground plane subdivision: **200×200 verts for 40×40m plane** (Geometry Nodes Scattering); subdivision 50+ for weight-paint resolution (Recipes).

### Style-specific scatter recipes
| Style | Approach | Source |
|---|---|---|
| Modern minimalist | Low-density grass + loose ornamental-grass blocks placed manually | Geometry Nodes Scattering |
| Cottage | High-density flower chaos, 5–7 plant types in one instance collection; density 80, 10 wildflower variants, slope <30°, camera-cull ON, wind subtle 0.05 | Geometry Nodes Scattering; Recipes |
| Scandinavian | Medium grass + moss patches + ferns scattered under trees | Geometry Nodes Scattering |
| Forest/wildernis | Layered: big trees manual (5–10), mid shrubs medium-density scatter, small grass+ferns high density | Geometry Nodes Scattering |
| Japanese-Zen | NO scatter on gravel — everything hand-placed (composed asymmetry); optional moss-patches with precisely painted density mask | Geometry Nodes Scattering; Recipes |
| Boerderij | Vegetable beds = row/grid pattern, NOT random scatter | Geometry Nodes Scattering |
| Mediterranean gravel | No grass; small stones density 500 micro-rotation; solitaire olive/lavender blocks manual; boundary mask off walls | Recipes |

### Piet Oudolf drift planting (5-7 grouping) (Blender Garden Archviz Scattering)
- One species per drift; irregular kidney-shape outline via vertex paint on separate patch mesh.
- **Odd numbers only**: 3/5/7/11 per drift (even reads "designed", odd = "natural").
- Repeat same species in 2–3 separated drifts = rhythm. Structural anchor plants (grass plume, allium) every ~3m.
- 3-layer composition: Foreground low+textured (heuchera, lambs ear) / Mid structural (echinacea, salvia) / Back grasses (calamagrostis, miscanthus).
- Vary Density Max per drift via separate modifiers = non-uniform = natural.

### Continuous hedge — GN scatter on curve (Blender Garden Archviz Scattering)
- ❌ NOT array modifier (visible tiling), NOT curve-array combo (jittery), NOT particle systems (deprecated).
- ✅ `Curve to Points → Instance on Points`, Instance = Collection Info ("hedge_balls", Separate Children=ON, Reset Children=ON), Pick Instance=ON, Rotation=Random Z 0–6.283, Scale=Random 0.9–1.1.
- Pro technique: low-poly "loaf" silhouette mesh, scatter 3–5 ball variants on TOP surface via Poisson (min dist 30cm). Add base mesh with leaf material underneath so gaps don't show through.

### Hedge — CURRENT method (GN scatter of real scanned leaf sprig, update 10 jun 2026) (Hedge Creation)
- **Supersedes the legacy AI-leaf-card method below.** Roosmarijn/Jasmijn review: flux-schnell AI sprigs = baked fake lighting, dirty alpha edges, "fuzzy green noise" — root cause was the AI texture source, not the scatter technique.
- Harvest a **real scanned leaf sprig from a Polyhaven shrub** (`shrub_01..04`, 12–36 twig clusters, real photo diff+alpha+normal+rough).
- Recipe: rounded box hedge-volume, shade-smooth (smooth outward normals) → `Distribute Points on Faces` (Poisson ~500/m², outputs Points·Normal·Rotation) → `Instance on Points` (Instance = Object Info(sprig, As Instance); **Rotation = Distribute.Rotation** so sprigs fan outward along surface normal; Scale = Random 0.8–1.3) → `Rotate Instances` random Z → `Set Material` (real shrub texture + Subsurface 0.12 + HSV sat 0.68 / val 0.76).
- **KEY: Distribute Points on Faces `Rotation` output already aligns instances to surface normal** → the old sphere-normal-donor + Data-Transfer hack is NO LONGER NEEDED (no black backfaces, fewer modifiers, robust).
- Hedge-volume shape defines the sharp trimmed outline; give volume dark-green `MAT_HedgeCore` so gaps read as shadow. Full build recipe: [[Jasmijn Hygge Build Runbook (HOE)]] §5.

### Hedge — LEGACY AI-leaf-card / particle method (DEPRECATED, reference only) (Hedge Creation)
- Base cube ~0.5m wide → subdivide + Displace (cloud tex strength 0.05–0.10) for organic top → `HedgeLeaf_Card` quad ~0.15×0.15m alpha boxwood sprig → Particle Hair, render_type='OBJECT', count = surface_area_m2 × 100 → Data Transfer of custom split normals from smooth icosphere (1.2× hedge bbox, hidden) to give leaf-cards volumetric outward normals.
- Particle settings: `type='HAIR'`, `use_advanced_hair=True`, `render_type='OBJECT'`, `size_random=0.5`, `use_rotations=True`, `rotation_mode='NOR'`, `phase_factor_random=1.5`, `use_rotation_instance=True`, `particle_size=1.4` (default 1.0), `display_percentage=100` (default 50 too sparse).
- Leaf-card alpha from white-bg: `TEX.Color → SeparateXYZ → Min(R,G) → Min(,B) → ColorRamp (e0@0.75 opaque, e1@0.88 transparent) → BSDF.Alpha`. `blend_method='HASHED'` (NOT 'CLIP' — too binary), `shadow_method='HASHED'`, Subsurface Weight 0.15.
- Sphere-normal-trick (icosphere subdivisions=4, scale 1.2× bbox, shade_smooth, hidden WIRE): Data Transfer modifier at TOP of stack, `use_loop_data=True`, `data_types_loops={'CUSTOM_NORMAL'}`, `loop_mapping='POLYINTERP_LNORPROJ'`.
- Roosmarijn 2026-06-05 example: Hedge_Main 13.6×0.5×1.85m → 6195 cards; Hedge_East 0.4×7×1.85m → 3181; Hedge_West → 3183; total 12,559 instances. Modifier stack: CopyNormals (Data Transfer) → Hedge_Bumps (Displace cloud strength 0.10) → ParticleSystem. Library collection `Hedge_Unit_Library` (hidden), `HedgeLeaf_Card` asset-marked.
- Pitfalls: flat wall = particles off in render (`show_instancer_for_render=True`, `display_percentage=100`); black side leaves = no sphere-normal transfer; magenta = broken image path (`.jpg` vs `_2k.png`); hard alpha edges = 'CLIP' → 'HASHED'; viewport blank = shading is MATERIAL not RENDERED.

### Tree generation tools (Tree Generation and Wind Animation)
| Tool | Cost | Note |
|---|---|---|
| Sapling Tree Gen (built-in) | free | Add>Curve>Sapling Tree; F6 tweak; bake to mesh; replace leaf-card mat with Polyhaven `leaf_*`. Leaves are cards — weaker close-up. Best for mid-distance filler |
| Modular Tree (addon) | free | Node-based (own system), L-system growth, 8 botanical shapes, procedural Superformula leaves. Best for stylized/close-up |
| The Grove 3D | €136 | Photoreal, built-in physical wind sim, twigs/deadwood. Hero close-ups only, not 50+ background |
- Asset-library alternatives: Polyhaven trees (CC0 scanned), Botaniq Lite (paid, 28 biomes), BlenderKit free, Sketchfab CC0 (Thomas Flynn, filter CC0).
- **Recommended blokhutwinkel stack**: hero close-up = Polyhaven scanned (Acer/Oak/Birch CC0); mid-distance = Sapling (5 variants baked); far background = card billboards with tree-silhouette textures.

### Photoreal tree pitfalls (Tree Generation and Wind Animation)
- Add **Translucent BSDF** on leaf shader, mix factor **0.3** with Principled — sunlight-through-leaf glow is the signature.
- Sub-canopy variation: top leaves paler than inside — drive via Geometry→Pointiness.
- Never identical copies: scale 0.85–1.15 + random Z rotation 0–360° minimum.
- Add dead branches/twigs (~5% bare, via The Grove or manual).
- Vary leaf colour pale-to-deep green via per-instance random colour shift.

### Wind animation — GN pattern (no simulation) (Tree Generation; Vegetation Animation Wind Effects)
- Pattern: `Position → Add(Time × Speed vec) → Noise Texture (4D, W=scene time × speed) → scalar[0..1] → × wind-direction × strength → Add to position (leaves only via vertex-group tip mask)`. Animate via driver `#frame*0.05`.
- **Critical for scattered instances: animate the deformation BEFORE `Instance on Points`** so all instances share it; for 1000+ plants animate the SOURCE object, not per-instance fields (Vegetation Animation Wind Effects).
- Per-instance phase variance: `Capture Instance Index → ×0.37 (irrational seed) → + Scene Time/24 → sin() → × tip-mask VG → displace along normal` (Vegetation Animation).
- Wind strength/speed/scale per scene-type (Tree Generation):
  - Cottage calm: strength 0.02, speed 0.5, scale 1.5
  - Coastal/dune windy: strength 0.15, speed 2.0, scale 0.8
  - Forest mid-breeze: strength 0.06, speed 1.0, scale 1.2
  - Japanese Zen: strength 0.005 or off (motion breaks the calm)
- Grass wind (GN layered noise): scatter 50k blades; animate base mesh with TWO noise textures — large scale 5.0 strength 0.02 + small scale 30.0 strength 0.005; Z-displace via root-to-tip vertex group (Vegetation Animation).
- Individual-plant quick wind: Wave modifier (Z axis, speed 0.5, height 0.005, width 1.5, narrowness 1.5) + tip-weighted vertex group. Stiff plants (succulents/ferns): shape keys driven by `#sin(frame*0.1)*0.05`. AVOID legacy Wind force field (Vegetation Animation).
- Tree wind, 3 valid: Botaniq 7.1 baked (breeze/wind/storm presets, bake to Alembic — best for hero stills) / hierarchical bones (noise on rotation Euler, strength 0.5→2.0→5.0 up the levels) / procedural Displace (Mtree built-in or Displace + animated Empty tex-coord + root=0/tips=1 weight) (Vegetation Animation).
- Motion blur for stills: Cycles Motion Blur ON, Shutter **0.2–0.3** (NOT default 0.5), Position=Center on Frame; **shutter 0.15 = barely-there hero blur, ~20% render-time cost**; animate vegetation 2 frames before/after target, render middle frame (Vegetation Animation).

### Scattering-tool decision (8GB RTX 3070 archviz) (Blender Scattering Tools Decision Guide)
- **FINAL recommendation, install in order:** (1) **BagaPie Modifier (FREE)** — daily driver, modifier-based so trivially scriptable (`modifier["Input_X"]=0.5`), handles ~80% of cabin-garden needs; (2) **Native Geometry Nodes** — build reusable `scatter_archviz.blend` GN library appended to every pilot, zero addon dependency for CI rendering; (3) **Botaniq Free Sample (38 assets) + engon (free)** — Polygoniq quality without $129.
- BagaPie: v11 (May 2026), Blender 4.2+ Extensions "Bagapie"; modifier free, assets $39 Lite / $93 Full; outputs instances; `obj.modifiers["BagaPie_Scatter"]["Input_2"]=0.5`.
- Geo-Scatter (was Scatter5): v5.6.3 (March 2026); $99 Indie / $1299 Studio; multilayer masks (slope/altitude/proximity/density-paint), collision-avoidance, native instances; `bpy.ops.scatter5.*`. **SKIP for now** until pipeline outgrows BagaPie.
- Note the Geo-Scatter source note lists paid price as **$67** and 170+ biomes (Geo-Scatter Plugin) — conflicts with the $99/$1299 in the Decision Guide; Decision Guide (2026-05-22) is newer than the source note (2026-05-08), treat Decision Guide pricing as current.
- Scatter5 legacy free = DEAD (rebranded, old v5.0–5.2 broken on 4.2+). GScatter (Graswald free) = ABANDONED (no updates since 2023, no biome stack) — SKIP. Grassblade > QuickGrassPro for the "Real Grass" niche.
- Botaniq + engon: 700+ trees/plants + 50+ scatter presets; engon free; Botaniq $129 Full / $49 Lite / **$1.99 Starter**; geo-filter by world-region (good for Dutch), seasonal/hue sliders, baked wind, snap-to-ground, curve-placement (7.1+).
- iMeshh hedges: $5–15 per asset, GN curve-driven — best for boundary hedges along property lines, buy per-need only.
- Comparison matrix (Density / Layers / Output / Memory / Auto-script): BagaPie = slider-per-mod / modifier stack / instances / low / easy. Native GN = manual / one graph / both / lowest / easiest.

### GScatter (free) / Geo-Scatter / Plant-Library (Geo-Scatter Plugin; Recipes)
- GScatter free: Scatter Systems, Effect Layers (Distribution/Proximity/Scale/Rotation), masks (Slope/Altitude/Curvature/Camera-distance/Proximity), wind without sim; first results in 30 sec. Install `gscatter-X.X.zip` from geoscatter.com/download.
- GScatter performance features: viewport proxies (lo-poly viewport / hi-poly render), viewport-vs-render density, camera culling (hide instances outside frustum), distance LODs.
- Via MCP: GScatter UI not directly reachable; `bpy.ops.scatter.add_system(asset_type='COLLECTION', collection_name='grass_clumps')` — or skip UI and build GN scatter directly in Python.
- **Plant-Library (free, bd3d.gumroad.com/l/plant-library)**: 170+ HQ nature assets, 1.5 GB, Cycles+Eevee. It's an asset SOURCE not auto-scatter.
- Geo-Scatter (paid) biomes: forest floor, meadow, beach, alpine, desert, garden, urban; cloud-database.

### Polyhaven plant import — correct flow (Blender Garden Archviz Scattering)
- ❌ NOT `bpy.data.libraries.load()` directly (brings ALL variant junk); ❌ NOT multiple `wm.append` calls (creates `.001/.002` duplicates).
- ✅ Polyhaven Blender add-on (ahujasid MCP has it enabled) → drag-drop individual variants as lightweight collection instances.
- ✅ Or `bpy.ops.wm.append(filepath=f"{blend_path}/Collection/{name}", directory=f"{blend_path}/Collection/", filename=name, link=False)` — appends one collection, internal variants grouped.
- ✅ Or after libraries.load hide all non-primary variants (names ending `_b`.._h` → `hide_viewport/hide_render=True`).

### Memory / performance rules
- **Everything = INSTANCES until final render; NEVER Realize Instances** until per-vertex shading needed (Blender Garden Archviz Scattering; Decision Guide).
- 200k grass instances ≈ **1.3 GB VRAM**; realized = **6+ GB and crashes** (Decision Guide).
- Heavy scatter modifier viewport display = **Bounds** while modeling; switch to Textured only for previews (Blender Garden Archviz Scattering).
- Grass-wind viewport at 25%, full at render; **`use_persistent_data=False`** (RTX 3070 VRAM spike) (Vegetation Animation).
- Distance LOD via `Switch by Distance` / camera-distance culling; keep high-poly for close-ups only (Geometry Nodes Scattering; Recipes). Use linked collections for source objects (no memory duplicates) (Recipes).

### Common scatter mistakes (Vegetation Scattering Recipes)
- Too-uniform density = artificial → always weight-paint variation.
- Grass on 90° slopes / against walls → slope + boundary masks essential.
- One grass species en masse → minimum 3–5 variants in the source collection.
- Random rotation on all axes → limit to Z only.
- Too much detail near camera, too little far → camera-distance LOD/culling.

### Asset library architecture (33 cabins × 5 styles) (GN Asset Library Architecture 33×5)
- One `.blend` per asset grouped by category (NOT a mega-file — mega blocks parallel git-LFS pulls and collides catalog UUIDs). Vegetation split: `vegetation/trees/{birch,oak,pine,cherry,magnolia}/`, `hedges/{boxwood,beech}.blend`, `grasses/meadow_drift.blend`, `lavender/lavender.blend`, `hydrangea/`, `ferns/fern_male.blend`, `moss/moss_carpet.blend`. Textures in sibling `textures/`, relative paths only (`//textures/...`).
- Naming: `{prefix}-{category}_{type}_{variant}_{lod}_v{NN}` — prefixes `GN- MAT- OB- CO- IM- WO-`; e.g. `GN-tree_birch_a_lod0_v03`, `GN-plant_lavender_drift_v02`. LOD suffix `_lod0` hero / `_lod1` mid / `_lod2` silhouette; variant single letter `_a/_b/_c`.
- Catalogs in `lib/blender_assets.cats.txt` (VERSION 1); tag vegetation on axes style / climate (nl/mediterranean/nordic) / season (summer/autumn/winter/evergreen) / prop_category (tree/shrub/...) / dutch_native (bool) / lod.
- **Trees, plants, hedges = link + override** (updated weekly, propagate to all 33 scenes); materials/HDRI = link; one-off pilot props = append.
- Override exposures — Tree: scale_jitter, hue_jitter, season_blend, lod_select. Hedge: length, height, density, trim_top. Lavender drift: bounds_object, density, hue_jitter. Keep <10 overrides/asset.
- Reference: Blender Studio **Sprite Fright** `geometry-nodes-moss` = canonical moss scatter pattern; Sprite Fright Bush-library = GN-instances-on-compound-geom reference (closest to vegetation needs).
- 256² PNG thumbnail gen via `lib/_tools/gen_thumbnails.py` (Eevee Next, film_transparent, `bpy.ops.ed.lib_id_generate_preview()`).

### Resources / assets cited
- Poliigon "Environment Scattering with Geometry Nodes"; Blender Studio "Geometry Nodes from Scratch" (Simon Thommes); BlenderArtists BushDraw GN tool; Poly Haven Blender add-on docs; iMeshh hedge GN models (Blender Garden Archviz Scattering).
- BlenderArtists "Creating a hedge in Blender" (origin of sphere-normal-trick, user Vanek); Replicate flux-schnell (leaf-sprig gen — now deprecated for hedges) (Hedge Creation).
- Windy Grass GN system, Stylized Grass idle wind, Camera Shakify (EatTheFuture, "Handheld 1" influence 0.05–0.15), HDRMAPS free 300-frame timelapse pack, Mtree wind (Vegetation Animation).


---

<a id="7"></a>
# §7. Render optimization & batch pipeline

Sources distilled: Cycles Optimization for 8GB Archviz; Ultimate 1080p Cycles Render Recipe; Cycles vs Eevee Next for ArchViz; Cycles Zombie Mesh Debug Pattern; Render Manifest Schema + Batch Orchestrator; Flamenco Render Farm Self-Hosted Setup; Multi-Season Variant Pipeline; Style Overlay Production System.

### Canonical Cycles hero settings (RTX 3070, 8GB)
Current default per (Ultimate 1080p Recipe, updated 2026-06-10) — supersedes the Filmic-based settings in the older (Cycles vs Eevee, 2026-04-30):
- Engine: Cycles GPU, `compute_device_type = 'OPTIX'` (or CUDA), `feature_set='SUPPORTED'`
- Resolution: 1920×1080 @ 100% (web) / 2560×1440 (high-res+print) / 3840×2160 (master)
- Samples: **256 adaptive**, `adaptive_threshold=0.005`, `adaptive_min_samples=64` (Ultimate). (Cycles-8GB note gives min_samples=32, max 1024 cap.)
- Denoiser: OpenImageDenoise, `denoising_input_passes='RGB_ALBEDO_NORMAL'` (ESSENTIAL — omitting blurs fine detail), `denoising_prefilter='ACCURATE'` (~15% slower, cleaner), `denoising_use_gpu=True` on 4.1+
- OIDN > OptiX for STILLS (sharper detail on grass/foliage + emissive accuracy); OptiX = fast viewport preview only
- `tile_size=256` (GPU) / 32 (CPU)
- `texture_limit_render='2048'` (forces 8K→2K, saves 60-70% VRAM on 4K assets); use `'1024'` when many 8K loaded (35-50% faster); `'4096'` for hero
- `use_persistent_data=False` for single stills (persistent wastes 200-500MB VRAM needed for vegetation; only ON for animations, 10-30% faster via BVH cache)

### Sample/threshold table (Ultimate)
| Scene type | Samples | Threshold |
|---|---|---|
| Test/iteration | 32-64 | 0.05 |
| Preview | 128 | 0.01 |
| **Production hero (default)** | **256** | **0.005** |
| Hyperreal close-up | 512-1024 | 0.001 |
| Complex interior + caustics | 1024-2048 | 0.001 |

Noise-threshold guidance (Cycles-8GB): 0.01 = production default (20-40% faster than 0.005, no perceptible diff w/ denoise); 0.005 = hero; 0.001 = print only. min_samples=0 leaks noise into tree-canopy shadows. Always calibrate a reference frame at 0.005 then check if 0.01 matches.

### Light paths (exterior cabin + garden + glass)
Ultimate values: `max_bounces=6, diffuse=3, glossy=4, transmission=8, volume=2, transparent_max=8`. Cycles-8GB variant: max 8, transmission **12** (window panes stack 4-6 hits), transparent 8 (alpha-clipped leaves).
- Per scene: Exterior max 4-6 / diff 2-3 / glossy 2-4; Interior max 8-12, transmission 12+; Caustic-heavy max 12+, filter_glossy 0.0
- Anti-firefly: `sample_clamp_direct=0` (off; only on for hot-light fireflies), `sample_clamp_indirect=5` (drop to 3-5 if fireflies on glossy leaves/wet stones). `blur_glossy=1.0` (0.5-1.0 sweet spot, anti-caustic-noise). MIS ON for world+sun.
- Transmission too low → glass renders black.

### Color management (AgX, Blender 4.0+)
- `view_transform='AgX'` replaces Filmic; rolls bright sky/window highlights to white like real camera (16.5 stops)
- Look: **AgX - Medium High Contrast** = hero default; Punchy = marketing; High Contrast = dramatic dusk; Medium Low = cottage/soft; None/Base Contrast = catalog/flat
- Khronos PBR Neutral = product/catalog exact sRGB; Standard = NEVER (clips)
- `exposure=0.3` (tune 0.0-0.5 per HDRI), `gamma=1.0`
- Fallback: if AgX absent from OCIO → Filmic + Medium High Contrast
- (Older Cycles-vs-Eevee note still lists Filmic as default — superseded.)

### Camera
- Focal: 28mm wide hero / 35mm mid hero (default) / 50mm one-cabin / 85mm detail; avoid 24mm (edge distortion)
- `sensor_width=36` (full-frame), `shift_y=0.1` (vertical-correct exterior)
- DoF: `focus_distance=8.0`, `aperture_fstop=8.0` (f/8 sharp archviz). Architectural f/5.6-f/11; product hero f/2.8-5.6; cinematic f/1.4-2.8
- Iteration: render small region (Camera → Render Region / `render.use_border=True`, 200×200 or 512×512 crop) — saves ~95% iteration time

### Lighting (Sun + HDRI sync)
- HDRI: Polyhaven 4K minimum, strength 0.5-1.2 (too high = flat shadows)
- Sun: `energy=3.5` (3-5 clear, 1-2 overcast), `angle=radians(0.5)` sharp / 3° soft. Colors: 5500K neutral (1.0,0.95,0.85); golden-hour 3200K (1.0,0.78,0.55); overcast 7000K (1.0,0.98,0.95)
- Sync: world env_tex Rotation Z sets sun direction; match sun Z-rotation; verify shadows run same direction. Sun Position addon (`addon_enable(module='sun_position')`) — enable sometimes fails, fallback manual.

### Compositor finishing (order matters)
Ultimate order: Render Layers → Lens Distortion (subtle) → Glare → Color Balance → RGB Curves (S-curve) → Hue/Sat → Vignette → Chromatic Aberration → File Output. Cycles-8GB order: Denoise → Color Balance → Glare → Lens Distortion → Vignette → Film Grain → Composite. Rule: color-grade linear first, glare needs HDR, glare BEFORE vignette (else halo'd dark edges).
- Lens Distortion: distort 0.005 (max 0.01), dispersion 0.005-0.01
- Glare: BLOOM (5.x) / Fog Glow, quality HIGH, threshold 1.0, size 7, mix -0.6
- Color Balance teal-orange: lift (0.95,1.0,1.05) cool shadows, gamma neutral, gain (1.05,1.0,0.95) warm highlights
- RGB Curves S: pts (0.25,0.20) & (0.75,0.80)
- Hue/Sat: saturation 1.05
- Vignette: box mask scale 0.85, blur 200px feather, mix 0.4 (Cycles-8GB: blur 50px, multiply 0.85)
- Chromatic aberration 0.5 (minimal)
- Film grain: noise scale 1500, fac 0.04 (Cycles-8GB: ×0.02)

### Output
- Working: PNG RGB 16-bit, compression 15. Master: OPEN_EXR_MULTILAYER, 32-bit float, ZIP codec.
- Passes to enable (Cycles-8GB): Combined, Diffuse Direct/Indirect, Glossy Direct, Mist (atmospheric depth), Cryptomatte Object.

### Light Groups (Cycles-8GB)
`vl.lightgroups.add(name=...)` + `lamp.lightgroup="key_sun"`; groups e.g. key_sun / sky_fill / practicals. HDRI CANNOT join a light group — use Environment pass instead.

### Memory / decimate / instancing (Cycles-8GB)
- Collection instancing: 300 plant copies share 1 mesh; BVH build >5s on 300 instances → use linked duplicates
- Decimate: background trees 0.3, mid-ground 0.6, hero keep
- Hide vs delete: `obj.hide_render=True` keeps mesh in memory; use `obj.hide_set(True)` + exclude from view layer for true VRAM unload
- Adaptive Subdivision (hero ground only): dicing 1.0 render / 8.0 viewport; Displacement→"Displacement and Bump". NEVER on 300 instanced plants (use bump/normal maps).

### Headless CLI render rules (validated 2026-06-10, Ultimate)
`blender.exe -b scene.blend --python render_script.py -o "C:\abs\path\prefix_" -F PNG -f 1`
1. ALWAYS `scene.use_nodes = False` in render script — active compositor nodes → all-black output, no error
2. ALWAYS save before headless render (`bpy.ops.wm.save_as_mainfile`) — MCP edits live only in running instance; headless reads disk
3. ALWAYS absolute `-o` paths — relative writes to `C:\` root
4. NEVER World Volume Scatter on exteriors — density=0.002 → entire exterior pitch-black in Cycles 5.1 (HDRI+sun interaction), no error
Headless CLI is crash-safer than MCP `render_viewport_to_path` for tight-memory heavy scenes.

### Render time budget (RTX 3070, verified)
- 1080p / 256 samples / OIDN = **~60-90 sec/frame** (Magnolia: cabin + 7 oaks + 46 hedge + 50+ plants + 10 stones)
- 4K / 512 / OIDN = ~10-15 min/frame
- `texture_limit_render='1024'` → 35-50% faster
- Bottlenecks: BVH on 300 instances >5s; volume bounces with no fog (set volume=0); transmission too low (glass black); VRAM swap

### Cycles vs Eevee Next verdict
Eevee Next for preview, Cycles for finals. Cycles REQUIRED: hero/product-page cover, golden-hour/dusk, night+emission (volumetric haze/bloom), heavy reflections (hottub water, raamglas), final marketing. Eevee Next fine for: build preview (MCP `get_viewport_screenshot`), style iterations, storyboard for user sign-off, animation previews. Eevee misses off-screen (screen-space) reflections, weak on caustics/volumetric/SSS.

### Cycles Zombie Mesh debug (all-black Cycles, Eevee/Workbench OK)
Root cause: unintended huge-bbox mesh (tens-thousands of meters) fills camera frustum; Cycles BVH treats it as ray-absorbing occluder while Eevee/Workbench z-clip or ignore it.
Diagnosis (ablation): (1) confirm engine divergence — render BLENDER_EEVEE + BLENDER_WORKBENCH + CYCLES; (2) hide all but cabin (whitelist: parentboard, wall-, roof, deur, pole-, foundation); (3) binary-search enabling half the hidden by category; (4) scan visible meshes, flag any single object height >50m; (5) delete by name.
Symptom triage: Cycles black + Eevee OK → huge-bbox >50m; Cycles black + Eevee black → HDRI load/view transform/exposure; Cycles converges sub-30s on 1080p → adaptive hit uniform color (all-black/all-white); Cycles partial-bad → wrong light paths / volume.
Cause sources: gLTF imports with shared naming (`Object_0`...) leaving orphans; failed transform_apply on shared mesh; gLTF Y-up→Z-up inverse-rotation matrix (set `o.parent=None` before `o.location`); half-failed scale (looks small in viewport, actually 1000m).
Example — Roosmarijn 2026-06-05: 34 `Hetz_` topiary zombies dim 700×700×1200m at z=600m from a bad hedge scale; fix `name.startswith("Hetz_") and bbox_h>5` delete → render works. Cost 8+ min misdiagnosis before pattern.
Prevention: after every gLTF import log naming+bbox; flag objects dim >15m (non-ground); rename imports to predictable namespace (avoid `Object_X`).

### Style Overlay Production System (built 2026-05-21, status current)
One command per cabin×style: `CABIN=Magnolia-300x200 STYLE=modern blender.exe -b --python "pilots/styles/style_overlay.py" -f 1` → ~30s headless (1080p, 256 sa, OIDN). Output: `pilots/<Cabin>/style-<style>/<Cabin>_<style>.blend` + `_hero.png`. Base at `pilots/base/<Cabin>.blend`; profiles = `STYLES["<style>"]` dict in `pilots/styles/style_overlay.py`.
5 built-in style profiles (HDRI / walls / garden / sun / camera / look):
- **modern (Japandi)**: kloppenheim_06_puresky; walls luxehouse-grijs-gedompeld; formal hedge 18 trees + 5 oaks + cherry + boxwood + hydrangea + kalmia + stepping stones; sun 5500K energy 3.5; 35mm dist 2.2×; Medium High Contrast
- **cottage (English)**: kloofendal_43d_clear overcast; walls luxehouse-onbehandeld; NO hedge, 3 oaks, roses+hydrangea+spiraea, poppy beds, ferns; sun 4500K energy 2.0; 35mm dist 2.0×; Medium Low Contrast
- **scandi (forest)**: forest_slope; walls luxehouse-grijs-gedompeld; NO hedge, 7 oaks dense, hydrangea, stepping stones, ferns; sun 3200K golden energy 3.5; 28mm dist 2.3×; Medium High Contrast
- **boerderij (farmhouse)**: kloofendal_43d_clear; walls kdi_rabat; spruce_fence backdrop, 4 oaks, elderberry, open grass; sun 4500K energy 2.5; 35mm dist 2.1×
- **natuurhout (natural hybrid)**: kiara_1_dawn; walls luxehouse-onbehandeld; hedge 14 trees + cherry + 4 oaks + boxwood + 3 bush types + ferns + stones + poppies; sun 5000K energy 3.0; 35mm dist 2.2×
Capacity: 33 base × 5 styles = **165 hero renders** in ~83 min (33×5×30s).
Open tune-issues (demo 2026-05-21): trees too close in modern (move backdrop y=-12 vs -7); cherry sometimes tiny at edge; bush positions hardcoded fail on wide zijwand cabins (scale w/ bbox); hedge spacing needs auto-widen for wide cabins; camera distance too short for 7m+ cabins; no interior assets (empty behind windows); path-to-door stepping stones toggle-only.

### Render Manifest Schema + Batch Orchestrator (status critical)
Single YAML/JSON drives 165 renders; Python `orchestrator.py` runs headless via `--background --python`.
- Manifest sections: `project` (name blokhutten-marketing-2026, blender_version 5.1.0, output_root, cabin_master_dir, lib_release v2026-05-22, provenance_root), `defaults`, `recipes` (lighting/compositor/camera by name), `output_bundles`, `shots`
- Defaults example: CYCLES/GPU, res [1920,1080], samples 256, noise 0.005, time_limit 600, OIDN ACCURATE, AgX "AgX - Punchy" exposure 0.0, PNG 16-bit compression 15, persistent_data false, texture_limit 2048
- Recipes referenced by name not duplicated (change HDRI strength globally); `output_bundle` decouples render from delivery (one render → many derivatives); `assets_referenced` = dependency graph for smart re-render + sparse LFS pull; `qc.reference_image` + `ssim_threshold` (0.95) for auto-diff; path templating `{id}/{NN}/{date}`
- JSON Schema at `manifest.schema.json`, validated in CI: `check-jsonschema --schemafile manifest.schema.json manifest.yaml`; VS Code via `yaml.schemas`
- CLI: `blender --background --factory-startup --python orchestrator.py -- --manifest manifest.yaml --state .render_state.json --workers 1`; `--smoke`; `--shot <id>`; `--resume`; `--invalidate-asset <path>`; `--invalidate-since <git-ref>`; `--force`
- Smoke mode overrides: res (128,72), samples 8, denoiser NONE, time_limit 15 → full 165-shot sweep ~5 min, catches missing assets/recipes/cameras before 4h batch
- Smart batching sort key `(cabin, lighting, engine, priority)`: cabin primary (persistent_data ON within cabin group, ~30s BVH saving/shot); lighting keeps HDRI loaded (~3s each); Cycles batch first, EEVEE last; priority override for hero
- Do NOT run multiple Blender on one GPU (VRAM contention crash) — one Blender per GPU is the floor
- Per-shot flow: check state (skip if done + hashes unchanged) → `git lfs pull` refs → `read_factory_settings` → link cabin master collection (`bpy.data.libraries.load(link=True)`) → style overlay → lighting recipe → compositor NodeTree → camera preset → render settings → preflight audit (abort on fail) → render (capture wall-time/samples/denoise) → async derivatives → hash + provenance + SSIM → update state
- Preflight reuses `scripts/validate_scene.py` in same process; shot skipped if `errors != []`
- Failure handling: crash-safe per-shot `state.flush()`; OOM (exit 137/VRAM in stderr) → drop texture_limit to 1024, retry once; missing asset → LFS pull retry once; hard timeout → mark failed, log failures.json, continue. Resume skips status==done unless --force.
- Naming: `{cabin}_{style}_{cam}_{season}_v{NN}_{YYYYMMDD}.{ext}`, auto-increment v{NN} by scanning dir; sidecar JSON same stem
- Post-process derivatives (async `ProcessPoolExecutor`, overlap CPU encode w/ GPU render):

| Derivative | Res | Format | Tool |
|---|---|---|---|
| master | 3840×2160 | PNG 16-bit | Blender |
| hero_2k | 2048×1152 | AVIF q55 | avifenc |
| hero_2k | 2048×1152 | WebP q80 | cwebp |
| web_1k | 1920×1080 | WebP q78 | cwebp |
| thumb | 800×450 | WebP q75 | cwebp |
| social_v | 1080×1920 | WebP q80 | ImageMagick crop center 60% |
| hdr_pq | 3840×2160 | AVIF Rec.2100-PQ | avifenc --cicp 9/16/9 |

- Cost report: `kwh=(secs/3600)*gpu_tdp/1000`, `cost_eur=kwh*0.32` (NL 2026). RTX 3070 @220W 60s = 0.0037 kWh = €0.0012; 165-shot @avg 90s ≈ 4.1 kWh ≈ €1.30
- SSIM QC: `structural_similarity(ref,new,channel_axis=2)`; flag (don't fail) if < threshold for human review
- EU AI Act provenance (Art 50): per-shot `<output>.provenance.json` listing ai_generated_assets (model+prompt_hash), non_ai_assets, renderer, view_transform; aggregated to `renders/_provenance/batch_<date>.jsonl`
- Versioning: semver `manifest_version`, git-tagged (manifest-v1.2.0); orchestrator records manifest_version+git_sha in every sidecar
- Parallel option B (single workstation multi-GPU): PowerShell `ForEach-Object -Parallel` set `$env:CUDA_VISIBLE_DEVICES`, `-ThrottleLimit 2`

### Flamenco Render Farm self-hosted (status critical, recommended >50 shots)
Flamenco 3 = 3-tier (Blender+addon → Manager :8080 → Workers → Shaman/SMB), scale "1-10 artists, 1-100 machines single LAN". Layout: Manager on RTX 3070 dev box (also Worker #1) + 1-2 extra LAN workers + Shaman on Manager's biggest SSD (no NAS).
- Install: single-binary win64/linux64/macOS from flamenco.blender.org/download (contains manager.exe + worker.exe). Manager `flamenco-manager.exe` → Setup Assistant at http://localhost:8080. Workers: Linux systemd `ExecStart=/opt/flamenco/flamenco-worker -manager http://192.168.1.10:8080`; Windows via NSSM. Workers UDP-autodiscover; `-manager` flag only if discovery fails.
- `flamenco-manager.yaml`: manager_name, listen :8080, database sqlite, task_timeout 10m, worker_timeout 1m, shared_storage_path Z:/flamenco; shaman enabled garbageCollect period 24h maxAge 744h (31 days); `blender` one-way variable (per-worker path), `jobs` two-way variable (rewrites Z:\flamenco↔{jobs} on submit/dispatch)
- Asset paths: Option A SMB identical drive letter (Z:\ Windows, /mnt/flamenco Linux); **Option B recommended = Shaman** (SHA256+length dedup, uploads only new files, per-job symlink checkout, survives 31 days) — obvious win for 1000-frame batch sharing HDRIs/grass/Sketchfab
- Security: no built-in auth (LAN-only design). Bind LAN-only `listen: "192.168.1.10:8080"`; Windows Firewall rule RemoteAddress 192.168.1.0/24; remote workers via WireGuard/Tailscale; TLS+basic auth via Caddy/nginx if public
- Queue: web UI :8080, priority -100…100 (default 50), pause/requeue/cancel, auto-retry default 3 (`task_fail_after_softfail_count`), failed tasks blacklist worker; webhooks since 3.3
- REST API `/api/v3/jobs` (no auth header, LAN). `scripts/push_to_flamenco.py`: type "simple-blender-render", chunk_size 1 (max parallelism), settings blendfile/frames("1-250" or "1,5,10-20")/format PNG/render_output_path `{jobs}/render-output/{job}/######`/fps 24. OpenAPI at `/api/v3/openapi.json`. Custom per-frame logic (style-overlay variants): drop JS job-type in `C:\flamenco\scripts\` (orchestrator note names it `scripts/blokhutten.js`).
- Alternatives ruled out: BlendFarm (abandoned 2021), CrowdRender (splits 1 frame, useless for batch), SheepIt (GPL/privacy for commercial), custom CLI loop (no recovery/queue). Cloud (RebusFarm/Garage) €30-80 per 1000 frames — only wins when <2h turnaround matters.
- Power cost NL May 2026: RTX 3070 ~220W + ~80W system = ~300W wall; 8h = 2.4 kWh = €0.70-0.80/night/machine @ €0.28-0.32/kWh; 3 workers 8h ≈ 7 kWh €2.00-2.20/night. 1000 frames @ ~3min/frame = 50h single-GPU → ~17h on 3 workers; total ≈ €4-5 vs cloud €25-40 (self-host wins ~6-8×).
- First-day setup ~30 min: extract → manager Setup Assistant (point blender.exe, storage C:\flamenco\storage, enable Shaman) → run worker.exe → Blender install flamenco-3.x-addon.zip, Manager URL http://localhost:8080, Fetch Job Types → open magnolia_modern.blend → Flamenco panel Simple Blender Render frames "1" chunk 1 → Submit → output C:\flamenco\storage\jobs\<job-id>\render-output\0001.png. Multi-worker = run worker binary on box N.

### Multi-Season Variant Pipeline (status critical)
ONE cabin master → 4 seasons. 33 cabins × 5 styles × 4 seasons = 660 renders. Strategy HYBRID: trees swap by collection (bare vs leafy topologically differ); grass/ground/sedum/sky/sun/compositor driven by single `season` float [0,1] (0=winter, 0.25=spring, 0.50=summer, 0.75=autumn). NEVER two seasons loaded at once.
- Sun noon altitude De Bilt 52.10°N (KNMI/NOAA ±0.3°): summer solstice 61.4°, equinox 37.9°, winter solstice 14.5°. Golden-hour: summer 18:00 ~22°, spring/autumn 17:00 ~15°, winter 14:30 ~8°. Azimuth: noon due south 180° year-round; sunset NW summer ~305° to SW winter ~232°.
- Phenology (Wageningen): birch yellows mid-Oct falls early Nov; oak holds into Dec; lavender flowers late-Jun–mid-Aug; sedum Aug-Sep.
- HDRIs per season: Spring kiara_1_dawn / spruit_sunrise / qwantani_dawn_2; Summer kloofendal_43d_clear / kloppenheim_06 / golden_gate_hills / belfast_sunset; Autumn qwantani_puresky / cobblestone_street_night / kloofendal_overcast_puresky; Winter snowy_forest_path_01 / winter_lake_01 / the_sky_is_on_fire / snowy_cemetery
- Compositor grade (Color Balance offset/power/slope = lift/gamma/gain, season-driven Mix): Spring lift(.02,.01,.03) gain(1.02,1.03,1.05) sat 0.95; Summer neutral lift, gain(1.05,1.05,1.00) sat 1.05 exp +0.10; Autumn lift(.03,.02,0) gamma 0.98 gain(1.05,1.02,.95) sat 0.90; Winter lift(.02,.02,.05) gamma 1.02 gain(.98,1.00,1.05) sat 0.85
- Ground `MAT_Ground_Universal` ColorRamp(season): winter #DCE6EC, spring #8FB36E, summer #4F7A36, autumn #6E5439; roughness mix(0.45 summer, 0.15 snow); snow subsurface 0.3 IOR 1.31 emission 0.02. Driver `scene["ground_season"]`.
- Snow GN `GN_SnowScatter`: Distribute on Faces masked Normal.z>0.7, edge falloff via Proximity to Boundary, bake to mesh for hero; material Base #F4F8FB subsurface 0.3 radius (0.8,0.9,1.0) rough 0.15 emission 0.02; roofs bias toward eaves.
- Fallen leaves GN `GN_LeafFall`: density ∝ 1/distance-to-trunk, 80-120/m² within 2m of trunks vs 15-25/m² elsewhere, 5-7 hue variants, random yaw 0-360 pitch ±20°, scale 0.7-1.3, 2-tri alpha quads, 50K instances <200MB.
- One-click swap `apply_season()` maps: SEASONS_MAP {winter 0.0, spring 0.25, summer 0.50, autumn 0.75}; SUN_ALT {14,38,61,38}; SUN_AZ {winter 232, spring 220, summer 305, autumn 245}. Toggles `SEASON_*` collections hide_render/hide_viewport, sets ground_season, rotates RECIPE_SUN, loads HDRI, applies compositor preset.
- VRAM: cabin master ~200MB + active season overlay (linked) ~400MB = ~600MB, safe on 8GB with texture_limit 2048 + persistent_data False.
- Vegetation lib: `lib/vegetation/trees/<species>/<species>_<season>.blend` each exporting collection `TREE_<SPECIES>_<SEASON>` (linked not appended); pine evergreen gets winter snow overlay. GN_SeasonState float drives grass length/leaf-card alpha/color.
- Schedule: 165/season; Summer first (broad appeal, easiest light), Autumn (reuse minus props, swap trees+comp), Winter (most distinct, holiday), Spring last (premium only). RTX 3070 1080p/256/~60s → 165×60s = 2.75h/season, ~11h total. Realistic quad-set only for 33 heroes (~132 renders); supporting shots stay summer.
- Season-identifier prop (client reads in 0.3s): Spring tulip pot + blossom; Summer parasol + lavender bloom + bicycle; Autumn pumpkins + scarf-on-chair + leaves; Winter snow roof + candle glow + skis/sled.
- A/B via GrowthBook (KPIs: tile CTR, configurator-open, offerte-aanvraag); cron `0 0 1 mar,jun,sep,dec *` swaps CMS hero to current season.
- Future v2 "render-once composite-many": render all AOV + Cryptomatte (Object+Material) once, swap leaf-color/sky/snow via masks in Photoshop/Affinity/Natron — no re-render; requires every tree/grass/prop tagged in Cryptomatte; best for top-10 heroes.

### Anti-Uncanny final checklist (Ultimate)
Wear-on-edges (Bevel/Pointiness); ≥3 mats weathered (drip/patina/dirt); per-instance Hue via Object Info>Random; ≥1 "life" prop (book/mug/shoes); not all parallel/symmetric; directional light (Sun+HDRI synced); FG/MG/BG layers; plants IN ground −2 to −5cm (not floating); no pure black/white; hardware present if visible.

### Per-scene overrides (Ultimate + Style notes)
- **Magnolia** (Modern Japandi, plat dak): AgX High Contrast, sun 3.0, HDRI kloppenheim_06_puresky or kiara_1_dawn
- **Roosmarijn** (Modern warm honey, carport): 2560×1440 (not 1080p), samples **512** (dark carport converges only at 512), AgX look None (catalog) / Medium High (lifestyle), exposure 0.05, HDRI eilenriede_park_2k.hdr @ strength 0.37, Sun_Golden 5.8W (1.0,0.85,0.65), carport fills Fill_Canopy 26W + Fill_Canopy_BackWall 24W + Fill_Carport_Overhead 11W + Rim_Bike 12W, texture_limit 4096, canonical `roosmarijn_modern_FINAL.png`
- **Camelia** (Scandi, donker): AgX Medium High, sun 3.5 golden (1.0,0.78,0.55), HDRI qwantani_dusk_2 or kloofendal
- **Lelie** (English Cottage): AgX Medium Low, sun 1.5 overcast, HDRI kloofendal_overcast_puresky

### Open gaps noted
Sun Position addon Python enable sometimes fails (fallback manual); compositor node Python parametrization tricky (sometimes easier manual); AgX "Punchy" look only Blender 4.3+.


---

<a id="8"></a>
# §8. Compositing & color grading

Three source notes. Newest (2026-05-22, both `status: critical`): **Compositor Automation Python Deep** (code/batch-driven, Blender 5.0 API) and **Compositor Post-Processing Advanced** (recipe reference, 4.2+/5.x). Older (2026-05-08, `status: current`): **Color Grading for Marketing Renders** (manual/UI + per-style looks). Where they differ on view transform, the newer notes use **AgX**; the older note says **Filmic** (see conflict note below).

### View transform / color management
- Newer notes: stay on **Filmic / AgX**; SDR PNG delivery = `view_settings.view_transform = "AgX"` (Compositor Automation §17).
- Older note (Color Grading): **Filmic** (default), NOT Standard. Standard = blown highlights, bad colors. (Color Grading)
- **CONFLICT / current**: older note prescribes Filmic; both newer critical notes prescribe AgX. Treat **AgX** as current default for delivery; Filmic still acceptable per older note. (Compositor Post-Processing says "Filmic / AgX" interchangeably.)
- Look curves (Filmic, UI): None/Medium = neutral for grading; High = marketing pop; Very High = moody; Low = cottage/soft. (Color Grading)
- Exposure slider in Render Properties: ±0.5 as "too dark / too light" client knob. (Color Grading)
- HDR delivery: `"Khronos PBR Neutral"` (4.2+) OR `"AgX"` + `look = "AgX - Punchy"`; `color_depth="16"`, `file_format="PNG"`, tag Rec.2100-PQ. EXR-16 + Rec.2020 primaries = safer master. (Compositor Automation §17)

### CRITICAL Blender 5.0 API break (Compositor Automation §0)
- `scene.node_tree` is **gone** in 5.0. Compositor now: `scene.compositing_node_group` (may be None).
- Bootstrap pattern:
```python
nt = getattr(scene, "compositing_node_group", None) or scene.node_tree
if nt is None:
    nt = bpy.data.node_groups.new("Comp", "CompositorNodeTree")
    scene.compositing_node_group = nt
scene.use_nodes = True
```
- `nt.nodes` / `nt.links` collections unchanged. **Always use string socket keys** (`"Image"`) not int indices — order changed in 5.0 (Glare/Cryptomatte gained inputs). (§1)
- Also set `scene.render.use_compositing = True`, `scene.render.use_sequencer = False`. (§18)

### Pipeline order (canonical — enforce; §6 Automation, §1 Advanced)
```
RLayers → Denoise → Cryptomatte/AOV grade → Exposure → ColorBalance → Saturation/Curves
        → Mist depth shift → Glare → LensDistortion+CA → Defocus → Vignette → Grain → Composite/FileOut
```
- Exposure & color-balance in **linear scene-referred space** — BEFORE non-linear effects (else double-correct).
- **Glare BEFORE lens distortion**: distorting first warps the bright samples glare reads → smeared streaks.
- **Vignette AFTER glare**: vignette must darken bloom bled into corners; else glare re-brightens darkened corners.
- **Grain ALWAYS last** (sensor noise on top of optics); grain before color-balance → gain stretches noise into colored speckle.
- Render to **multilayer EXR (32-bit float)** for non-destructive.
- Older manual note's simpler UI pipeline: White balance → Tone curve → Color wheels → Vignette → Sharpen/glow → LUT → Output. (Color Grading)

### CompositorNode type strings (verified vs bpy.types, §2 Automation)
| Purpose | Type ID |
|---|---|
| Render input | `CompositorNodeRLayers` |
| Final out | `CompositorNodeComposite` |
| Preview | `CompositorNodeViewer` |
| File out | `CompositorNodeOutputFile` |
| Color grade | `CompositorNodeColorBalance` |
| Tonemap | `CompositorNodeTonemap` |
| Exposure | `CompositorNodeExposure` |
| Curves | `CompositorNodeCurveRGB` |
| Mix | `CompositorNodeMixRGB` |
| Glare/bloom | `CompositorNodeGlare` |
| Lens distort | `CompositorNodeLensdist` |
| Cryptomatte | `CompositorNodeCryptomatteV2` |
| Alpha-over | `CompositorNodeAlphaOver` |
| Denoise | `CompositorNodeDenoise` |
| Hue/Sat | `CompositorNodeHueSat` |
| Ellipse mask | `CompositorNodeEllipseMask` |
| Blur | `CompositorNodeBlur` |
| Invert | `CompositorNodeInvert` |
| Image (EXR/sky in) | `CompositorNodeImage` |
| Scale | `CompositorNodeScale` |
| AOV shader out (in material) | `ShaderNodeOutputAOV` |

### Color Balance (lift/gamma/gain = ASC-CDL) — grade recipes
Use Color Balance primary, Curves for contrast, Hue Correct for selective. `cb.correction_method = "LIFT_GAMMA_GAIN"`; sockets `cb.lift`, `cb.gamma_value`, `cb.gain` = 4-tuple (RGB + 1.0). (Automation §4)

**Time-of-day grades (Advanced §2):**
| Grade | Lift | Gamma | Gain | Result |
|---|---|---|---|---|
| Morning warm | (1.00,0.99,0.97) | (1.02,1.00,0.96) | (1.05,1.01,0.95) | peach highlights, cool shadows |
| Overcast neutral | (0.99,1.00,1.02) | 1.0/1.0/1.0 | 0.97/0.98/1.00 (+5% contrast) | flat blue-leaning |
| Golden hour | (1.00,0.97,0.94) | — | (1.08,1.02,0.88) | amber highlights, magenta shadows |

### Per-style recipe tables (numbers are load-bearing)
**5 NL cabin-style recipes (Automation §20)** — save as `recipes/<style>.json`, driver picks by cabin `style` field:
| Style (project) | CB lift | CB gain | Glare | Vignette | Grain |
|---|---|---|---|---|---|
| Premium cool (Lavendel hero) | [0.98,1.00,1.02] | [1.05,1.02,0.98] | FOG_GLOW thr 0.75 mix 0.06 | 0.18 | 0.022 |
| Cottage warm (Magnolia) | [1.02,1.00,0.98] | [1.08,1.04,0.96] | BLOOM thr 0.60 mix 0.10 size 9 | 0.20 | 0.028 |
| Scandi clean (Camelia) | [1.00,1.00,1.00] | [1.03,1.02,1.01] | FOG_GLOW thr 0.85 mix 0.04 size 6 | 0.10 | 0.015 |
| Editorial moody (Lelie) | [0.94,0.97,1.02] | [1.02,1.00,0.98] | FOG_GLOW thr 0.80 mix 0.05 | 0.24 | 0.020 |
| Modern minimal | [0.99,1.00,1.01] | [1.04,1.03,1.02] | FOG_GLOW thr 0.78 mix 0.05 | 0.14 | 0.018 |

**Python grade presets (Automation §5), style keys map in §12:**
- `premium_cool` → `apply_premium_grade`
- `lifestyle` → CB default lift[1,1,1] gain[1.08,1.04,0.96]; glare BLOOM thr 0.6 mix 0.10 size 9
- `editorial` → CB lift[0.96,0.99,1.04] gain[1.03,1.01,1.00]; glare FOG_GLOW thr 0.85 mix 0.04 size 6; grain 0.018

**Manual per-style marketing looks (Color Grading note) — tone/color/sat/vignette:**
- Modern Minimalist: cool teal shadows, clean white highlights, slight desat, vignette 0.92, magazine-clean.
- English Cottage: low contrast soft S, warm shadows (lift R), vignette 0.95, slight sepia via Hue-Sat.
- Scandinavian/Nordic: medium contrast, cooler (lift B mids), warm only highlights, saturation −10%, vignette 0.90.
- Forest/Wilderness: high contrast, heavy teal shadows + golden highlights, greens +15%, vignette 0.85.
- Mediterranean: high contrast warm, warm yellow-orange wash + vivid blues, saturation +20%, subtle vignette.
- Japanese Zen: low contrast neutral, desat −20%, slight cool, vignette NONE, editorial.
- Boerderij: medium contrast, warm (Hollandse warmte), slight green-shift mids, sat +5%, subtle vignette.
- Tropical/Bali: medium-high contrast, heavy green sat, warm highlights, moderate bloom, vignette 0.92.
- Coastal/duinen: low-med contrast, cool blue-grey, slight desat, subtle grain, vignette NONE (open horizon).
- Industrial/Urban Jungle: high contrast, teal shadows + orange highlights, sat −10% overall / +20% plant-greens, slight cyan, vignette 0.90.
- Prairie (Oudolf): low contrast painterly, warm slight-desat, moderate bloom (grass-tip shimmer), slight grain.
- French Provence: medium contrast warm, warm yellow + lavender sat boost, soft glow, subtle vignette.
- Alpine: high contrast crisp, cool air / warm only stone+wood, sat +10%, vignette 0.92.

**Universal "real-estate marketing look" (Color Grading):** Filmic + Look Medium-High Contrast; Color Balance lift +0.05 mids, gain +0.02 highlights; RGB Curves subtle S (lift 0→0.03, mid 0.5→0.52, highlight 1→0.97); warm shadows (lift R +0.02); vignette 0.93; sharpen 0.08. "Sells 90% of archviz product visuals."

### Tone curve / RGB Curves (manual, Color Grading)
- Basic marketing S-curve: lift dark corner 0,0→0.05,0.05; push mids 0.5→0.5,0.55; compress highlights 1,1→0.95,1.0.
- Teal-and-Orange: shadows subtract R/G add B; highlights add R/G subtract B. Subtle version = premium real-estate.

### Glare / Bloom (Advanced §3, Automation §4)
- **Fog Glow** = 90% of cases. Advanced settings: Threshold 1.0, Size 7-9, Mix −0.6 to −0.4 (negative Mix required; default 0 = cheesy).
- Streaks: nightscapes/lamps only — 4-6 streaks, iterations 3, fade 0.9.
- Simple Star: NEVER (cheesy).
- Stack for archviz: (1) low-threshold Fog Glow thr 1.2 Mix −0.7 = ambient bloom; (2) high-threshold Fog Glow thr 3.0 Mix −0.3 = hot-spot bloom.
- Pitfall: threshold <0.8 floods mids = amateur.
- Python node: `glare_type` (FOG_GLOW/BLOOM/STREAKS), `quality="HIGH"` batch / `"MEDIUM"` preview, `.threshold`, `.mix`, `.size`. Studio "paint-over" final glare FOG_GLOW size 9 thr 0.85 mix 0.05 HIGH. (§19)
- NOTE sign convention differs between notes: Advanced uses **negative** Mix (−0.4…−0.7); Automation recipe JSON uses **positive** mix (0.04–0.10). Both are the same node's `mix`; use the value the specific recipe/note gives.

### Lens distortion + Chromatic Aberration (Advanced §4, Automation §4)
- Blender 4.x+ has dedicated **Chromatic Aberration node**: Intensity 0.3-0.6 = invisible-but-felt; >1.0 = Instagram filter.
- Lens Distortion alt: Distortion 0.005 (barely +), Dispersion 0.002-0.005. SKIP on tight rectilinear interiors.
- Automation recipe default lens: distortion 0.02, dispersion 0.4; node flags `use_projector=False, use_jitter=False, use_fit=True`; set via `.inputs["Distortion"/"Dispersion"].default_value`.

### Vignette (Advanced §5, Automation §4)
- 5.0 has native `CompositorNodeVignette` (`.intensity`); fallback = Ellipse Mask → Blur → Invert → Mix MULTIPLY.
- Advanced manual: Ellipse Mask width 1.0, height 0.5625 (16:9), X=0.5 Y=0.5 → Blur Fast Gaussian X=Y=500 → Mix Multiply factor **0.85-0.92** (subtle pro; 0.5 = too heavy). Best: invert + Mix Multiply fac 0.3-0.5.
- Automation fallback code: EllipseMask width/height 0.85, Blur size 350, Mix MULTIPLY, `strength≈0.15`.
- Manual Color-Grading vignette values by style range 0.85 (drama) → 0.95 (very subtle); NONE for Zen/Coastal.

### Film grain (Advanced §6, Automation §4)
- Strength: Photoreal 0.01-0.02 (near-imperceptible); Cinematic 0.03-0.05; Stylized >0.08.
- Advanced setup: Noise Texture (Greyscale, scale ~1000) → Mix Add 0.02 fac; place AFTER all blurs. Monochrome = desaturate noise; digital = RGB-split with RGB Difference 0.4.
- Automation code: `MixRGB blend_type="OVERLAY"` at grain amount (recipe default 0.02).

### Cryptomatte — targeted/selective grades (Advanced §7, Automation §8)
- Passes: enable CryptoObject/CryptoMaterial/CryptoAsset; `pass_crypto_depth = 6`.
- Node `CompositorNodeCryptomatteV2`: `source="RENDER"`, `.scene`, `.layer_name`, `.matte_id` = comma-separated crypto hashes.
- **Matte → Fac socket** of Mix; image → inputs 1 & 2 (linking image into Fac silently uses luminance = bug, §15).
- Typical archviz: plants +15% saturation; cabin wood +2% red gain; sky −10% saturation — three grades, one render. Also: darken windows 0.7 gain, lift foliage shadows +0.05, warm interior +amber.

### AOVs (Advanced §11, Automation §9)
- Material: `ShaderNodeOutputAOV`, name must match `view_layer.aovs` entry (e.g. `Mask_Facade`, `Cabin`), plug 1.0 into Color. Enable View Layer → Shader AOV → appears as render pass. Best for grouping many objects under one logical mask vs picking each Crypto-ID.
- `add_aov_passes(view_layer, names=("Glass","Plants","Sky"))`, type `"COLOR"`.

### Mist pass / atmospheric perspective (Advanced §8, Automation §7/§16)
- View Layer Mist ON; World → Mist Pass Start/Depth/Falloff **Quadratic** (most natural). Mist range on `scene.world.mist_settings.start/depth`, set before render.
- Setup: Mist → ColorRamp (remap blacks to hold foreground) → Mix Color cool blue **#A8C0D0**. Adds haze without volumetric cost.
- Sky-replacement haze: Mist as Fac on Mix SCREEN with desaturated sky tint. mist start = camera-to-cabin distance, depth = tree-line distance.

### Sky replacement (Automation §16)
- Render `scene.render.film_transparent = True`. Comp: `CompositorNodeImage` load HDRI (e.g. `//hdri/qwantani_2k.exr`) → AlphaOver input[1] (bg); RLayers Image → AlphaOver input[2] (fg, premultiplied). Add mist-driven Mix SCREEN for atmospheric perspective. Recipe field example: `polyhaven/qwantani_dusk_2k.exr`.

### Defocus / DOF in post (Advanced §9)
- In-render DOF for hero shots (correct bokeh on volumetrics, slow); post Defocus for anim/iteration (fast, no proper bokeh on volumetrics).
- Post: Render Layers Depth → Defocus, Use Z-Buffer ON, fStop 1.4-4, Maxblur 16-24.

### Render passes to enable (Automation §7)
combined, z, mist, normal, position, diffuse_color/direct/indirect, glossy_color/direct/indirect, ambient_occlusion, shadow, cycles crypto_object/material/asset, `pass_crypto_depth=6`.

### Light Groups (Cycles 3.2+, polished 4.4-5.0; Advanced §10, Automation §10)
- `view_layer.lightgroups.add()`; `ob.lightgroup = name`; env: `scene.world.lightgroup="Env"`. Each group → own Combined/RLayers output. Mix ADD + per-group Multiply → per-light exposure without re-render. Combine with Cryptomatte mask = surgical (e.g. dim only sun on facade, keep HDRI fill).

### Multi-layer EXR / deferred grading (Automation §11, §13, §18)
- `CompositorNodeOutputFile`: `file_format="OPEN_EXR_MULTILAYER"`, `exr_codec="ZIP"`, `color_depth="32"`; slots Beauty, Crypto00-02, Depth, Normal, Mist. = regrade master.
- **Bake-vs-keep heuristic**: if re-grading **>3 times**, render once to multilayer EXR then graph against EXR via `CompositorNodeImage`. Cycles ~60s (RTX 3070) one-time vs comp ~100ms repeatable. **Below 3 grades = leave live.**
- Deferred-grading pipeline = Multi-layer EXR + Cryptomatte + AOV + Light Groups: one expensive render, infinite cheap re-grades.

### Studio "paint-over" composite — MIR / Bertrand Benoit (Automation §19)
1. Render Cycles at 4K (oversample for crisp grain after downscale).
2. Three crypto branches: sky (lift cool, gain warm-top), foreground (slight gain reduce + sat lift), mid-ground architecture (neutral master).
3. MixRGB MIX per branch, crypto as Fac.
4. Separate haze layer: solid colored card → Mix SCREEN, Mist as Fac, over building only (× inverse-sky crypto so sky doesn't double-haze).
5. Final glare FOG_GLOW size 9, thr 0.85, mix 0.05, HIGH.
6. Downscale to 2.5K with `CompositorNodeScale` = `RENDER_SIZE` + bicubic.
Recipe list: `["sky_grade","fg_grade","midground_grade","haze_layer","subtle_glare","downscale"]`.

### Performance (RTX 3070, 8GB — Automation §13, §14)
- 5.0 compositor is **full-GPU** (CPU Full Frame removed). 1080p full graph (CB→FOG_GLOW size 8→lens→vignette→grain) = **~80-140 ms/frame**; FOG_GLOW+Bloom HIGH dominates. Drop to MEDIUM while authoring = **~30 ms**.
- EEVEE Next: 4.1+ viewport compositor overlay; 4.3+ full passes in compositor; 5.0 default authoring = viewport-shading "Compositor: Always" → recipe live on EEVEE Next. Tune in EEVEE Next → batch-apply to Cycles (glare/lens match, post-effects on framebuffer).

### Batch / headless driver (Automation §12, §18)
- `blender --background pilots/lavendel.blend --python composite_apply.py -- recipes/lavendel_modern_hero.json renders/out.png`
- `composite_apply.py` parses argv after `--`, `apply_recipe(scene, recipe_path)`, sets `scene.render.filepath`, `bpy.ops.render.render(write_still=True)`.
- Recipes stored `pilots/_recipes/<style>.json` (§12) / `recipes/<style>.json` (§20); main script `composite_archviz.py`.
- 1000-render flow: glob `.blend` → render to multilayer EXR → 2nd pass runs comp on EXR via `CompositorNodeImage` = split one-time render from cheap grade.

### Recipe JSON schema (Automation §3)
Fields (all optional, `dict.get()` defaults): `name`, `style`, `color_balance{lift,gamma,gain}`, `exposure`, `saturation`, `lens{distortion,dispersion}`, `glare{type,threshold,mix,size}`, `vignette`, `grain`, `cryptomatte_grades[{layer,matte_ids,saturation/gain}]`, `sky_replace{hdri_strip,image,mist_atmospheric}`, `output{exr_multilayer,ldr_png,hdr_rec2100_pq}`. Example values: glare FOG_GLOW thr 0.75 mix 0.06 size 8, saturation 0.95, lens dist 0.02 disp 0.4, vignette 0.18, grain 0.025.

### Common mistakes / batch-refuse (Automation §15)
1. No clamp before color balance → Cycles fireflies (>1.0) push gain → magenta blowouts. Fix: MixRGB DARKEN flat 1.5, or `cycles.sample_clamp_indirect = 10`.
2. Glare after vignette (order enforced §6).
3. Grain before color balance → colored speckle.
4. No alpha-over for sky replacement.
5. Image into Fac socket → silent luminance bug (crypto matte → Fac; image → Mix 1+2).
6. `nt.links.new()` returns the **link** not the node — wrap link calls, assert non-None in dev.

### File output / resolution (Color Grading note)
- PNG lossless catalog/web: 16-bit RGB, sRGB. JPEG social: 8-bit Quality 95%. EXR pipeline: 32-bit float OpenEXR.
- Resolutions: Instagram 1080×1080 (square) / 1080×1350 (4:5 portrait); Website hero 1920×1080 or 2400×1200; Print catalog 3000×2400 (300 DPI A5); render 4K master, downscale per platform. Output two versions: graded marketing + neutral catalog.

### Photoshop / external round-trip (Advanced §12)
Worth it for: detail painting (dust/leaves/dirt), people/car sticker comp, sky replacement, glow painting, Camera Raw color science. Export 16/32-bit EXR or TIFF, all passes as layers, via **EXR-IO plugin**. SKIP Photoshop for grade/glare/vignette — Blender does identically non-destructive.

### Sharpness / LUT (Color Grading manual)
- Sharpen: Filter > Sharpen very subtle 0.05-0.15; Glare > Bloom low threshold/fade for "crisp + glow".
- LUTs (optional): **Final LUT** addon (free) = .cube realtime viewport preview; **Colorist Pro** (paid) DaVinci wheels in viewport. Sources: IWLTBAP free, Lutify.me (paid), DaVinci Resolve free presets → .cube. Avoid stacking multiple LUTs.

### Avoid (Color Grading)
Standard view transform; excessive saturation ("render" not "foto"); heavy vignette; too much glow/bloom ("fantasy" not real-estate); stacked LUTs; **grading before fixing light/material problems — fix original first**.

### Validation (Automation closing)
Render one frame, dump node tree to JSON (nodes/links → dict), diff against previous golden = catches recipe drift across 1000 renders before client does.


---

<a id="9"></a>
# §9. Photorealism / anti-uncanny-valley principles

### Core thesis (all sources agree)
- **Perfect = fake; imperfect = real.** The gap between "render" and "photo" is *imperfection*, not more detail. Our eyes flag perfect surfaces as CGI (Anti-Uncanny-Valley Rules; ArchDaily).
- "True photorealism lies in the mistakes" (ArchDaily). Realism thrives in scratches, grime, uneven lighting.
- The gap between "almost photoreal" and "indistinguishable" lives in **dirt, scale, and rooted-ness** (Anti-Uncanny Deep).
- **Photoreal** = looks like a photo; **Hyperreal** = better/sharper than a photo, more detail than eye registers in 3 sec (Hyperreal Cabin). Hyperreal = macro+meso+micro; photoreal = macro+meso only.
- Photorealism = 90% from 3 things: **detailed model + lifelike materials + accurate lighting**; remaining 10% (the hyperreal edge) = atmospheric details, story-props, imperfections, color grade, post/AI-upscale (IDDQD).

### Multi-scale detail hierarchy (3 layers — beginners use 1, pros stack 3)
| Layer | What | Visible at | Setup (Anti-Uncanny Deep) |
|---|---|---|---|
| **Macro** (mesh/displacement) | Plank warp, soil dent, sagging gutter | 5m | base mesh + texture |
| **Meso** (normal map + roughness variation) | Wood grain, paver chamfer, leaf curl, knots, plank-naden | 1m | displacement map |
| **Micro** (detail normal 4×–8× tiling + bump) | Cell pores, fingerprint smudges, fabric fuzz | 30cm | Normal Map strength **0.15**; roughness break-up ColorRamp **0.3 → 0.6** |

### Procedural imperfections (restrained — "felt not seen"; if visible in thumbnail, dial back 50%)
| Effect | Node setup (Anti-Uncanny Deep / ArchDaily / Rules) |
|---|---|
| **Edge wear** | `Geometry > Pointiness → ColorRamp (0.5–0.55, or sharp 0.4–0.6)` → mix color 5–10% lighter on convex edges. Alt: Bevel Shader (Cycles only) angle factor → drives roughness/color |
| **Vertical dirt/rain streaks** | `Texture Coord > Object Z → Musgrave/Noise stretched 1:8` → roughness +0.15, darken 8% |
| **Rust/lichen patches** | `Voronoi F1` masked by world-Z under 0.3m |
| **Dirt in cavities** | AO shader output → ColorRamp → multiply base-color (darker in cavities) |
| **Per-instance color var** | `Object Info > Random → ColorRamp → HSV Hue shift (small range 0.95–1.05)` |

### 7 imperfection categories (Anti-Uncanny-Valley Rules)
1. **Wear-on-edges** (Bevel Shader / Pointiness / vertex-paint) — wear is on edges not flats.
2. **Dirt/grime** — collects at wall bottoms, cavities, ground-line, window corners.
3. **Plant color variation** — 3–4 tints per plant + per-instance; Object Info Random → Hue.
4. **Soft creases/wrinkles** — cushions/curtains never perfectly taut (Cloth modifier low-iter bake ~frame 50, or crease-brush sculpt).
5. **Imperfect alignment** — no two planks perfectly parallel; random rotation/position offset on repeats.
6. **Weathering/patina** — new+weathered base-color masks blended via Noise+Pointiness; drip/rain/water-damage.
7. **Subtle dust/haze** — World Volume Scatter density **0.001–0.005**; Mist Pass mixed in compositor.

### Weathering follows physics (ArchDaily — direction matters)
- Paint chips on corners/edges first, especially **sun-facing** side.
- Moss grows only on **shade side** of roof.
- Water stains follow gravity = **vertical streaks** under gutter line.
- Sun-bleach heavier on south gevel than north.

### Wood material believability (Anti-Uncanny Deep + Hyperreal Cabin)
- **Anisotropic 0.3–0.5**, rotation driven by grain direction (Tangent from UV).
- **Subsurface** subtle 0.02–0.15 (NOT 1.0); Random Walk method; IOR 1.4.
- **Per-plank color var**: `Object Info Random → ColorRamp (3 wood hues) → mix at 0.3`.
- **Roughness FOLLOWS grain**: pores rougher (0.7) than fibers (0.4).
- **Edge weathering**: Pointiness → lighten + roughen edges.
- **Plank gaps**: real 0.5–2mm (open joint 8–12mm); models omit → looks fake. Fix: Bevel modifier 0.5mm on edge, shift planks 1–2mm apart, AO auto-darkens gap line.

**SSS per wood species** (Hyperreal Cabin) — Weight / Radius(R,G,B) / Color:
| Species | Weight | Radius | Color |
|---|---|---|---|
| Cedar | 0.10 | 1.5,0.8,0.3 | #C4895C |
| Pine | 0.08 | 1.2,0.6,0.2 | #DBAA72 |
| Oak | 0.05 | 0.8,0.4,0.15 | #8C6240 |
| Larch | 0.07 | 1.0,0.5,0.2 | #B6855A |
| Douglas | 0.06 | 1.0,0.5,0.2 | #B07A48 |
| Shou Sugi Ban (charred) | 0.0 | n/a | n/a |
- SSS **yes** on vurenhout/thin planks/sunlit gevel; **no** on solid oak interior, all-dark wood, Shou Sugi Ban. Generic wood SSS color warm orange-brown #A87445.

### Plant / vegetation believability (Anti-Uncanny Deep + Hyperreal Cabin + Env Art)
- **Translucent BSDF** mixed at 0.3 with Principled, color warmer (orange-green); **Backface boost** via `Geometry > Backfacing`.
- **Per-leaf hue**: Object Info Random → Hue/Saturation ±0.05.
- **Grass bottom-up gradient**: `Generated Z → 50% albedo at root, full color at tip`.
- **Root darkness / grounding**: -2cm sink + 2–3cm Voronoi dirt ring/mulch mound at every base, randomized per instance; snap-to-ground ray-cast, bury 0.5–2cm.
- **Asymmetry**: Random rotation Z 0–360°, scale 0.85–1.15, tilt ±5°; hero plants remove 1–2 branches by hand.
- Density: designed perennial border 5–8 plants/m²; shrub 1 per 2–3m²; tree 1 per 15–25m²; wild meadow 12–25 stems/m². **Odd-number clusters (3/5/7), triangular not grid.** (Env Art)

### Lighting killers (Anti-Uncanny Deep §6 — what destroys photoreal)
- ❌ Pure black shadows → Sun angle **2–3°** (not 0.5°) + 0.3-strength fill (5500–6500K).
- ❌ Standard view transform → use **AgX or Filmic**, never Standard (clips highlights). (Env Art recommends Filmic + Medium High Contrast; note current project default is **AgX** per system context.)
- ❌ HDRI strength wrong → **0.3–0.7** + matching Sun lamp direction.
- ❌ No bounce light → hidden weak warm emission plane below ground (0.05 strength) simulates earth bounce.
- ❌ Accidental mixed color temp → sun 5200K + interior 3200K must be **intentional**.
- Sun+HDRI hero: Sun strength 3–5, angle 2° (sharp shadows), HDRI strength 1.0 rotated to match sun; Nishita Sky Texture as no-HDRI fallback (Env Art).
- Overcast/product-clarity: HDRI overcast 10000K (`kloofendal_partly_cloudy_4k`, `rural_landscape_overcast_4k`), strength 1.0–1.5, no extra sun (Env Art).
- **HDRI with clouds essential** — clear-sky reflection in glass reads fake; cloudy reflection sells it (Hyperreal Cabin).

### Anti-uncanny rules — CABIN CONTEXT (Anti-Uncanny Deep §7, CRITICAL)
1. **Cabin TOUCHES ground** — foundation -2mm into grade + dirt skirt.
2. **Grass intersects plinth** 1–3cm (comb-out disabled at edge).
3. **Slight asymmetry** — rotate cabin 0.5° Z, tilt patio stones ±1°.
4. **Wear at use points** — darker paver under door (foot polish), scuffed handle area.
5. **Human-scale cues** — chair (45cm seat), bike (1.05m bars), mug (10cm) anchor scale.
6. **Plants rooted** — -2cm sink + 3cm Voronoi dirt mound, per-instance random.
7. **AO contact pixel under EVERY object** — no floating shadow.

### Dutch construction dimensions matrix (Anti-Uncanny Deep §3 — real value / Blender)
| Element | Real | Blender |
|---|---|---|
| Cedar plank thickness | 18–22mm | 0.020m |
| Cedar exposed width (Rhombus) | 68–95mm | 0.085m |
| Plank gap (open joint) | 8–12mm | 0.010m |
| Klinker waalformaat | 200×50×60–80mm | exact |
| Klinker dikformaat | 210×70×80mm | exact |
| Joint width pavers | 3–5mm | 0.004m |
| Window frame depth (HSB DIN 68121) | 67–114mm | 0.090m |
| Door handle height NL | 1000mm from floor | 1.00m |
| Roof overhang | 200–400mm side / 300–500mm front | 0.30m |
| Lawn edge to paver (grass higher) | -5 to -10mm | -0.008m |
| Plinth above grade | 50–100mm | 0.075m |

**Note — dimension conflict**: Hyperreal Cabin lists plankdikte 28–44mm, plankbreedte 100–200mm, door 800×1900mm, raam 600×800→1200×1500mm, dak-overstek 30–50cm, plinth 100–200mm. Anti-Uncanny Deep (newer, 2026-05-22, marked `status: critical`) gives the more precise per-element matrix above and **supersedes** for cedar plank + handle + overhang specifics; Hyperreal Cabin's door/window sizes still useful where Deep is silent.

### Glass / hardware / roof (Hyperreal Cabin)
- **Glass**: Glass BSDF IOR 1.5, Roughness 0.0, + dirt via Noise (scale 50, distortion 1.0) → ColorRamp (0.4–0.6) → mix 0.05–0.1; vertical rain streaks (Object Z, vertical noise scale 1 / horizontal 5); fingerprint mask add to roughness 0.15; edge dirt via Bevel. Eevee Next needs SSR+Raytracing ON. Show interior glimpse (chair/lamp/plant) + warm area light for twilight glow-pop signature shot.
- **Hardware present or it's fake**: deurkruk (Metallic 1.0, Roughness 0.4, polished grip wear), 2–3 hinges/door (rust on screws, per-screw color var), lock+keyplate (scratch around keyhole), NL window PVC/alu grips, screws 4–6mm on load points with per-screw rotation var + rust spots.
- **Roof materials**: bitumen shingles roughness 0.85–0.9, granulate bump (Noise scale 200, strength 0.05), per-shingle Object-Info-Random, Polyhaven `roof_07`/`roof_shingles_*`; EPDM roughness 0.5; dakpannen roughness 0.65 (`roof_tiles_*`); golfplaten roughness 0.4–0.5 corrugated displacement + rust streaks; wooden shingles with moss on shade side.

### Adaptive subdivision + micro-displacement (Hyperreal Cabin — render-time only)
- Subdivision Surface (Simple, Render 4–6) → Shade Smooth → Adaptive ON, **dicing rate 1.0**, offscreen dicing 4; **Cycles Feature Set: Experimental**.
- Displacement chain: Image Texture → Math subtract 0.5 → Multiply 0.005–0.01 → Displacement node (Scale 1, Midlevel 0.5) → Output.
- **Macro displacement** scale 0.005–0.02; **micro** 0.0005–0.001; beyond 0.05 = blob.
- Budget (M4 MacBook): no adaptive 5min/frame; dicing 1.0 = 12–15min; dicing 0.5 = 25min+. **Only on hero elements** (close-up wall, door); fillers stay lo-res.

### Story / narrative "lived-in" details (all sources — shortest route out of the valley)
- Props that suggest life: coffee mug, open book, half-drunk wine glass, chair not parallel/skewed, flower in vase with one fallen petal, walking shoes by door, plant with a few yellow leaves, awkwardly overhanging climbing roses, bread on outdoor counter (Rules; ArchDaily; IDDQD).
- Motion suggestion in stills: chimney smoke plume (not column), hottub steam, leaf motion-blur (ON, low subframes), string-lights unevenly spaced (Rules).
- **Common to top studios**: render with EXTRA geometry the architect didn't ask for (potted plants, bikes, hose reels, garden tools) = the "lived-in" tell (Anti-Uncanny Deep §8).
- No empty showroom shots; every render has a human-narrative element + subjective (warm/cool) color grade, no neutral render look (IDDQD).

### Top studio techniques (Anti-Uncanny Deep §8)
| Studio | Technique |
|---|---|
| **MIR** | Volumetric fog 0.005–0.015, "god rays" via Volume Scatter, deliberate underexposure +0.3 lift in post |
| **Brick Visual** | Storytelling props, shallow DoF f/2.8–f/4 on hero |
| **Bloomimages** | Chromatic aberration 0.3–0.5 in compositor, film grain 0.02 Luma noise, lens vignette 0.15 |

### Guru rules — Andrew Price (Photorealism Explained)
1. **Reference, reference, reference** (5–10 refs of similar cabins/gardens).
2. **Don't trust your eyes** — eye adapts in 30 sec; render fullscreen ↔ swap with reference photo → spot 3 differences → fix → repeat.
3. **Imperfect is perfect.**
4. **Composition first** — mistake is 90% time on detail / 10% comp; should be 50/50.
5. **Light is the secret** — spend disproportionate time on lighting; perfect material + bad light = nothing.

### Lazy rules — Ian Hubert (works at film-VFX level)
1. **Lo-fi geo + hi-fi photo texture** — box with good texture beats hi-poly flat-material; don't model each plank, use displacement wall.
2. **Real photos > modelling** — kitbash, photo projection, photoscan all more legit than scratch-modelling.
3. **Atmosphere covers sins** — fog/haze/DoF hide weak detail; background trees can be card-billboards if haze between (also Env Art: billboard plane + Track To for far trees, renders <1s).
4. **Specific > generic** — a specific dirty mug beats a perfect coffee cup; one fallen leaf beats perfect leaves.
5. **Speed > perfection** — 100 iterations beat 1 perfectionist take; don't over-model the cabin (use GLB as-is, focus on scene-dressing).

### Hyperreal = montage (IDDQD)
- Not pure 3D: combines 3D render + photomontage (real photo elements) + matte painting (dramatic skies, distant landscapes). Plan to render key elements separately for compositor recombination with real skies / distant tree silhouettes.
- "Anticipation of the physical space + promise of the real world" — put viewer in the garden before they visit.

### AI upscaling (Anti-Uncanny Deep §9; Hyperreal Cabin)
- **PROJECT RULE: NO AI for marketing** (per feedback_ai_images; Deep §9 flags it explicitly). Below is study-only guidance.
- **Topaz Gigapixel ✅** — fidelity/restoration model, preserves original detail; "Art & CG" model for renders; 4× 1080p→4K sweet spot; local; ~$100 lifetime.
- **Magnific ❌** — hallucinates; "Creativity" >2 reinvents building (alters window mullions, plank counts, brick patterns); wrong for accurate product visuals.
- Speed route: 1080p render (5–10min) + Topaz 4× (~30s) → 7680×4320, indistinguishable in marketing vs 4K-direct (30–60min).

### 20% idealization rule for marketing (Rules)
- 80–90% photoreal + 10–20% idealization sells better than 100% photoreal: sky slightly bluer, flowers lusher, light more golden, **no people** (viewer self-projects). This is editorial styling, not "fake."

### Render budget by tier (M4 MacBook — Hyperreal Cabin)
| Tier | Time/frame | Use |
|---|---|---|
| Eevee preview | 30s | iteration |
| Cycles photoreal (256 samples, denoise) | 5–10min | catalog, social |
| Cycles hyperreal (512 samples, adaptive subdiv, micro-displacement) | 25–45min | marketing hero |
| + Topaz upscale | +30s | finishing |

*(Project-specific hardware note from MEMORY: RTX 3070 does 1080p/256 samples in ~60s; texture_limit_render=2048 + use_persistent_data=False keeps under 8GB VRAM — this supersedes the M4 timings for Beike's actual pipeline.)*

### Red flags — "that looks fake" (Rules)
- Key-light without fill (high-contrast); glass 100% transparent, no interior reflection/dust; grass on perfectly equal spacing; identical repeated plants/trees; perfectly taut cushions; wood perfectly clean (no knots/color var); cloudless perfect-blue sky; no shadow / ungrounded vegetation; 100% mirror reflection (most surfaces 80–95% diffuse).

### Final 15-point checklist (Anti-Uncanny Deep §10 — before declaring render done)
1. Cabin TOUCHES ground (dirt skirt); 2. every plant rooted (-2cm + dirt ring); 3. grass intersects plinth/pavers/edges; 4. AO contact under every prop; 5. no pure black/white pixel (color-pick 4 corners); 6. color temp consistent OR intentional; 7. Filmic/AgX active, exposure ±0.3 check; 8. per-instance variation on >5 hues/leaves/planks; 9. edge wear on >3 surfaces; 10. detail normal layered (4×–8× tiling, strength <0.2); 11. anisotropy on wood+metal; 12. translucency on leaves+grass tips; 13. volumetric haze 0.005–0.01; 14. human-scale prop; 15. background tree-line occludes sky.

### Reference-comparison workflow (Hyperreal Cabin + Andrew Price)
- Collect 5–10 reference photos → render fullscreen → spot 3 differences → fix → re-render until indistinguishable. Per-render checks: sun-direction matches HDRI shadow; no clipping shadows/highlights; plants IN ground not ON; glass has interior+exterior reflection; hardware present; grain direction consistent per plank; plank-gap shadow lines visible; per-shingle roof variation; plinth visible.

### Environment-art hard rules (Env Art — learned from 2 failed Magnolia pilots, 30 Apr 2026)
- Plants only in bed-zones, never on gravel/lawn; snap-to-ground ray-cast (code in note), bury 0.5–2cm; scatter via GN Distribute Points (density 0.5–4 Poisson) + Shrinkwrap-before-GN so scatter follows ground displacement.
- Hardscape not coplanar: deck 8–15cm above gravel; edging board 5cm×10cm; Cortenstaal strip 4mm×12cm (roughness 0.6, #6B3A1F, metallic 0.4). Stepping stones Z-offset = -0.4×stone_size, flush/just-below gravel.
- DIY Adirondack real spec: seat depth 50cm, height 35cm front/28cm back (8° slant), backrest 95cm at 15°, armrest 14cm, slats 7cm × 1cm gap (Array+Mirror). Never one solid plank.
- Hedges: never solid plane (reads plastic) — GN scatter of leaf-clusters on displaced plane (density 80, scale 0.7–1.3, top vertex-group denser); or 3 stacked alpha planes for background >8m only. Avoid volume hedges.
- Per-scene checklist gate: cabin 50–65% frame width, 25–35% sky/background; camera 1.5–1.6m height, 35–50mm focal, 3/4 angle; max 3 staffage categories; **≤8 checkmarks → don't render, fix first.**

### Production pipeline essentials (Archviz Production — status: critical)
- File roots: local/ (per-workstation, unversioned), shared/ (previews/renders, unversioned), svn/ (versioned .blend). For 33-cabin×5-style: `lib/cabins/{template}/` + `pilots/{template}-{style}/`.
- Naming: `{show}-{type}-{name}.{variant}-{task}-v{version}_{info}.{ext}`, all lowercase, underscores for spacing, dashes for separators, no spaces/`+=#^*&()?`. Render ex: `lavendel_modern_hero_v02_20260522.png`; material `mat_wood_cedar_v03`.
- Version control winner (Blender Studio 2024 benchmark): **Git LFS with .blend compression** (beats SVN+vanilla Git). `git lfs track "*.blend" "*.exr" "*.tif" "*.psd" "*.fbx" "*.abc"`. Anchorpoint adds file-locking (binary merges impossible).
- Backup 3-tier: auto-save 2–5min; .blend1/2/3 (Save Versions 3–5); manual incremental at milestones. Daily rsync/Time Machine, weekly offsite (Backblaze/B2), monthly cold.
- Linking: **Library Override ⭐** (link + override only needed props, upstream propagates). Central `_master_assets.blend` with COL_trees/COL_furniture_modern/COL_furniture_scandi/COL_materials_wood.
- Batch: `blender -b file.blend -o //render/####.png -f 1 --log-file render.log`; Python orchestrator with resumable JSON state for 100+ scenes.
- Render farm: Flamenco ⭐ (free, official) / BlendFarm local; GarageFarm/RebusFarm/SheepIt cloud (1080p Cycles frame $0.05–0.25 managed).
- QC pre-render script flags: scale ≠1.0, hidden-from-render, missing textures (`img.has_data==False`), bbox outliers (100× scene mean = unit error), unassigned materials, unlinked datablocks. Always real-world units. Validate exposure with 18% grey primitive + Filmic False Color.
- Deliverables: master 32-bit linear EXR ACEScg (working) / ACES2065-1 (archive); client sRGB PNG. 4K (3840×2160) hero / 2K preview / 1080p web. ACES = de-facto archviz standard. For 33×5=165 renders: Kitsu self-hosted OR Notion+scripts, <$30/month.
- Top production failures: scope creep, unrealistic deadlines, late scale errors, asset-library divergence, no file locking, no resumable queue, color-space mismatch at delivery, fragmented feedback.

### Portal lights (Env Art — Cycles only)
- Rectangle area lights at window openings with "Portal" checkbox ON → more indirect interior light + better convergence.


---

<a id="10"></a>
# §10. MCP, Python automation & plugin stack

### A. MCP control plane — ahujasid/blender-mcp (CURRENT STACK)
- Default server = **ahujasid/blender-mcp** on **localhost:9876** (TCP socket). Industry default; sponsored by Warp; current version **1.5.5**; requires **Blender 3.0+, Python 3.10+, `uv`** (ahujasid blender-mcp; Blender MCP + AI Asset Pipeline Deep; AI Blender Integration Landscape 2026).
- **Two-component architecture**: (1) Blender addon `addon.py` = TCP socket server inside Blender, configurable via `BLENDER_HOST`/`BLENDER_PORT` env vars; (2) MCP server `src/blender_mcp/server.py` bridges Claude/Cursor/VS Code to addon via JSON-over-TCP. Protocol: `{type, parameters}` request → `{status, result}` response (ahujasid blender-mcp).
- **Install + auth**: `uvx blender-mcp` runs the MCP shim; on Blender side install `addon.py`, enable + toggle "Start MCP Server" (binds localhost:9876). No API key for core. Polyhaven/Sketchfab/Hyper3D each have per-service toggles + key fields in addon N-panel (Blender MCP + AI Asset Pipeline Deep).
- **Telemetry**: collects anonymized prompts/code/screenshots — disable via addon checkbox or `DISABLE_TELEMETRY=true` (ahujasid blender-mcp).
- **`execute_blender_code`** = arbitrary `bpy` Python; primary scene mutator; "powerful but potentially dangerous" (ahujasid blender-mcp; Blender MCP + AI Asset Pipeline Deep).

**Core MCP calls** (Blender MCP + AI Asset Pipeline Deep):
- Inspect: `get_scene_info()`, `get_object_info(name)`, `get_viewport_screenshot()`
- Polyhaven: `search_polyhaven_assets`, `download_polyhaven_asset`, `set_texture`
- Sketchfab: `search_sketchfab_models`, `get_sketchfab_model_preview`, `download_sketchfab_model`
- Hyper3D Rodin: `generate_hyper3d_model_via_text`/`via_images`, `poll_rodin_job_status`, `import_generated_asset`
- Hunyuan3D: `generate_hunyuan3d_model`, `poll_hunyuan_job_status`, `import_generated_asset_hunyuan`

**Timing**: small `execute_blender_code` <1s; Polyhaven 3-20s/asset (1K-4K); Sketchfab 5-90s; Rodin 30-90s (Blender MCP + AI Asset Pipeline Deep).

**Failure modes** (verified via repo issues):
- **Issue #219**: truncated JSON on large payloads (`Incomplete 51-byte JSON`) — socket framing chokes when result > buffer (e.g. `get_scene_info` on 200-object scene)
- **Issue #50**: `MCP error -32001 Request Timed out` on long ops; default timeout ~60s
- **Hung renders**: `bpy.ops.render.render(write_still=True)` from addon socket thread blocks event loop; agent times out while Blender keeps rendering
- **Issue #73**: "No effect after success" — scene mutated but viewport not redrawn (call ran off-thread)
- First command per session sometimes fails (re-run); Hyper3D free-tier daily quota; multiple instances collide on port 9876 (ahujasid blender-mcp; Blender MCP + AI Asset Pipeline Deep)

**MCP best practices** (Blender MCP + AI Asset Pipeline Deep):
- Each `execute_blender_code` <50 lines / <2s wall-clock; chain calls
- **Never render via MCP.** Save .blend then headless: `blender --background scene.blend --python render.py` — RTX 3070 hits **1080p / 256spp ~60s** with `texture_limit_render=2048` and `use_persistent_data=False`
- After mutation batches, use focused `get_scene_info()` not full tree
- Socket dies → restart Blender server toggle only; `uvx` side reconnects

### B. Custom asset import (blokhutwinkel .blend/.fbx/.obj/.skp/.glb/.dae)
- blender-mcp has **no dedicated import tool** — use `execute_blender_code` with the right `bpy.ops.import_scene.*` (Custom Asset Import via execute_blender_code).
- FBX: `bpy.ops.import_scene.fbx(filepath=..., global_scale=1.0, use_anim=False, axis_forward='-Z', axis_up='Y')`
- OBJ: `bpy.ops.import_scene.obj(..., global_clamp_size=0, axis_forward='-Z', axis_up='Y')`
- .blend append: `with bpy.data.libraries.load(path, link=False) as (data_from, data_to): data_to.objects = data_from.objects` then link each to a collection
- glTF/GLB: `bpy.ops.import_scene.gltf(filepath=...)`; DAE: `bpy.ops.wm.collada_import(...)`
- **SKP**: no native `bpy.ops` — ask user to export to FBX in SketchUp
- Post-import: validate bbox dims (print `obj.dimensions.x/y/z`); if 1000× off use `obj.scale=(0.001,)*3` + `transform_apply(scale=True)`. Blender = Z-up; rotate `rotation_euler[2]=radians(180 or 90)` for +Y-forward (front faces camera from south). Reset origin `bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')` then `obj.location=(0,0,0)`. Missing textures → Polyhaven wood applied manually, Rodin as last resort.
- Suggested input drop path: `~/Documents/event-branding/blokhutten/_input/`. Workflow: import → `get_scene_info()` → scale/orient/origin fix → scene composition (Custom Asset Import via execute_blender_code).

### C. Asset pipeline — Polyhaven / Sketchfab / Rodin / Hunyuan3D
**Polyhaven** (HTTP API `https://api.polyhaven.com`, no auth, CC0):
- `search_polyhaven_assets(asset_type="hdri"|"model"|"texture", categories="...")`; `download_polyhaven_asset(asset_id="kloppenheim_06_puresky", asset_type="hdri", resolution="1k")`
- **Resolution policy**: HDRI **1K** previews/lookdev, **2K** hero (4K only >8K final — VRAM not worth at 2560×1440 hero); models = 2K textures default
- No free-form tag search via MCP (categories only). Workaround: pull `.../assets?type=2&categories=plant`, filter client-side on `tags`. Confirmed hits: `flowering_bush_01`, `wild_grass_01-03`, `garden_chair`, `terracotta_pot_01`, `wooden_planter_03`. **NOT in Polyhaven (May 2026)**: lavender, boxwood, hetz_midget, wild_rooibos_bush → fall back to Sketchfab
- **Texture path bug** (→ pink material): addon writes `_2k.jpg` to image datablock but disk file is `_2k.png` (Polyhaven serves PNG for normal/roughness). Fix loop: for each `bpy.data.images` with missing filepath, try `.png/.jpg/.exr` alt, set `img.filepath`, `img.reload()` (Blender MCP + AI Asset Pipeline Deep; 5.x re-test note in Blender 5.x Archviz Features §8)

**Sketchfab** (API key already in addon config):
- `search_sketchfab_models(query=..., categories="nature-plants", downloadable=True)`, `get_sketchfab_model_preview(uid=...)`, `download_sketchfab_model(uid=...)` (auto-imports GLB). `downloadable=True` filters to CC-BY/CC0/Sketchfab-Free
- **Scale (mandatory)**: GLB arrives in cm → `obj.scale=(0.01,0.01,0.01)` + `transform_apply(scale=True)`; then remove `Sketchfab`-named CAMERA/LIGHT objects
- **GLTF hierarchy quirk**: GLBs nest 90° X-rotation on root empty (Y-up→Z-up). Apply rotation+scale on **every node before re-parenting** (else rotated child): `transform_apply(location=False, rotation=True, scale=True)` on all imported
- **License compliance**: CC-BY = author + URL in `RENDER_INDEX.md`; CC0 free; Sketchfab-Free-Download (proprietary) = OK in rendered output, **not** redistributable as source GLB (Blender MCP + AI Asset Pipeline Deep)

**Hyper3D Rodin** (text/image → 3D; Gen-2 10B params / Gen-2.5 Ultra):
- `generate_hyper3d_model_via_text(prompt="...single object", tier="Regular"|"Sketch"|"Detail")` → `poll_rodin_job_status(job_id)` → `import_generated_asset(job_id, name)`. `via_images`: 1-4 reference photos to match real-world brand
- **Cost (May 2026)**: pay-per-download ~$0.50-$1.50/model; generation preview free, credit burns on download. Plans: Free, Education $15, Creator $20→$30/mo (30 credits ≈$1/credit), Business $60→$120
- **Quality**: clean quad topology + PBR-correct for sculpted/manufactured props (vases, fixtures, statues, lanterns). Topology beats Hunyuan for animation. **Poor for vegetation** (leaves = solid blobs, no alpha)
- **Use for**: unique branded item, sculpture/statue centerpiece, vintage/handmade not on Polyhaven/Sketchfab. **Don't use for**: trees/hedges/grass, generic chairs, anything with text/labels, anything <1.5m camera distance in 4K hero (Blender MCP + AI Asset Pipeline Deep; AI Blender Integration Landscape 2026)

**Hunyuan3D 2.5** (Tencent, open-weights fallback):
- `generate_hunyuan3d_model(prompt=..., quality="high")` → `poll_hunyuan_job_status` → `import_generated_asset_hunyuan`
- Runs locally: **6GB VRAM shape** / **16GB shape+texture**. RTX 3070 (8GB) = shape only; texture pass needs cloud (ThinkDiffusion/fal.ai ~$0.05-0.15/gen — cheapest AI option). Cleaner geometry than Rodin for organic smooth shapes (fruit, animals); Rodin wins hard-surface + PBR. Use when Rodin credits exhausted / organic-sculptural / offline-safe (Blender MCP + AI Asset Pipeline Deep)

**Verdict for archviz**: Rodin for hero props, Hunyuan3D for batch + offline (AI Blender Integration Landscape 2026).

### D. Asset decision matrix (Blender MCP + AI Asset Pipeline Deep §10)
| Need | First choice | Fallback | Never |
|---|---|---|---|
| Generic vegetation (trees/grass/ferns) | Polyhaven model | Sketchfab CC0 | AI |
| Specific Dutch shrub (boxwood/hetz_midget/lavender) | Sketchfab tag search | Sketchfab Free DL | AI / Polyhaven |
| HDRI sky | Polyhaven 1K/2K | — | BlockadeLabs for hero |
| Custom prop (sculpture/branded chair) | Rodin (text/image) | Hunyuan3D | Polyhaven |
| Texture common surface (wood/plaster) | Polyhaven 2K | Vault recipe | AI |
| Texture unique close-up | Manual procedural / vault recipe | StableGen+ControlNet | Dream Textures for hero |
| Cabin structural geometry | **Parametric GN5 always** | — | AI of any kind |
| Real garden terrain | Polycam scan as reference | Hand-modeled topo | AI |

**Anti-patterns**: AI for hero geometry (reads "off" <2m); AI textures >2m wide (tiling/warp); AI for anything with text (garbled letters — use UV-mapped real images); AI for cabin structure (product must be parametric + dimensionally exact). **EU AI Act Article 50** (in force **2 Dec 2026**): machine-readable marking + visible disclosure; penalty up to **€15M or 3% global turnover** → **log every AI-generated asset** to `assets/_provenance.json` with `ai_generated: True`, prompt, job_id; include as appendix in cabin deliverable PDF (Blender MCP + AI Asset Pipeline Deep §11-12).

### E. AI texture / HDRI / vegetation tooling
- **StableGen** (sakalond) ⭐ = best PBR texture pipeline. Clone `github.com/sakalond/StableGen`, enable as addon; backend **ComfyUI** (remote supported 2026); **SDXL or FLUX.1-dev** weights. ControlNet-guided (Depth+Canny) UV-correct projection; IPAdapter style transfer; UV Inpaint Mode for seams. **~30-90s / 1024² projection on RTX 3070**; batch overnight. Use only for one-off unique close-up surfaces (e.g. custom Shou Sugi Ban charring) — manual procedural is default for cabin walls (deterministic, scale-correct, license-clean)
- **Dream Textures** (carson-katri): local SD without ComfyUI, default 512² → upscale to 2K (Topaz/realesrgan-ncnn); concept tiles/mood boards only, don't ship in hero
- **DT2DB bridge** = Dream Textures + DeepBump (diffuse → full PBR normal/height)
- **BlockadeLabs Skybox AI**: 8K (16K Business) equirectangular EXR; free tier 5 gen/mo; paid $20/100cr, $48/300cr, $112/500cr ($48/mo worth it if >5 unique HDRIs/mo). Stylized "concept" look, visible AI sky smearing at horizon — **never final hero**; Polyhaven superior for archviz overcast/diffuse
- **Vegetation**: no mature AI-from-text tool (May 2026). Use GN scatter + Quixel Megascans plants + Botaniq; Hunyuan3D for ornamental specimens (boxwood, cherry)
- **Polycam** photogrammetry: client scans garden on iPhone → GLB → `bpy.ops.import_scene.gltf()`, decimate <50K tris, use as terrain reference only (bake height field, regenerate vegetation); never ship raw scan
- **Biggest gap in current stack**: no AI texture variation tool — StableGen+FLUX directly addresses 33-cabin variation need (AI Blender Integration Landscape 2026; Blender MCP + AI Asset Pipeline Deep)

### F. Alternative MCP servers & GitHub automation tools
- **PatrykIti/blender-ai-mcp** ⭐ — production-shaped, goal-first routing, deterministic verification, vision-assisted; **best upgrade** to replace ahujasid for production (safety policies + workflow matcher reduce broken-scene cycles)
- **minihellboy/claude-blender** — Claude-Code-targeted; 20+ tools; three-layer (CLI → Python MCP → addon JSON-RPC TCP :9876); **timer-polled TCP (not threaded)** because Blender Python API is not thread-safe (all ops on main thread); local AI: Shap-E (text→3D), TripoSR (image→3D), ComfyUI bridge at `127.0.0.1:8188`, procedural rock/terrain/building generators; needs Blender 4.0+ (tested 4.3), Python 3.10+, optional torch/diffusers/transformers/trimesh/rembg; `blender_get_scene` detail levels minimal/basic/detailed/full (minihellboy claude-blender)
- Other servers: Official Blender Lab MCP (blender.org/lab, doc-focused); 3D-Agent (scene-level planning); sandraschi/blender-mcp (FastMCP 3.1 + webapp + VSE 20 ops); huggingface/meshgen (local Llama/Qwen/DeepSeek); jlpschell/blender-mcp-server (51 tools, PolyMCP); dhakalnirajan/blender-open-mcp (Ollama offline); GongRzhe Image-Generation-MCP (Flux via Replicate) (Claude Skills GitHub Tools; AI Blender Integration Landscape 2026)
- **Top-3 highest-leverage installs** (Claude Skills GitHub Tools §4): (1) **BlenderProc** (DLR-RM) — turns 33 cabins into parameterized JSON-driven scene library, deterministic batch renders; (2) **PatrykIti/blender-ai-mcp**; (3) **headless-blender-container** (BlenderKit) + GitHub Actions for nightly renders
- Other GitHub tools: oqton/blenderless (headless render API), agmmnn/polydown (batch FBX/GLTF/USD downloader), vvoovv/bcga (shape-grammar building generator — directly relevant to cabin variants), lucianjames/AssetLibraryTools (batch asset-marking), LogicReinc/BlendFarm (network renderer), boschresearch/image-render-actions-std-blender (GitHub Actions CI), Topl1nk Polyhaven-HDRI-Downloader, agmmnn/awesome-blender (curated index) (Claude Skills GitHub Tools §3)

### G. Claude Code skills / connectors for Blender
- **Blender Toolkit** (Dev-GOM marketplace / mcpmarket): primitives, PBR assignment, modifiers, Mixamo retargeting — worth installing. Install: `/plugin marketplace add Dev-GOM/claude-code-marketplace`
- **Anthropic official Blender connector** (April 2026) — native Claude integration (also SketchUp, Adobe)
- **Current setup IS SOTA for archviz**: `Vault/Claude/` + ahujasid MCP (AI Blender Integration Landscape 2026)
- **Skill structure** (Anthropic spec): `SKILL.md` (1500-2000 words, numbered procedure = process) + `references/` (materials.md, lighting.md, validation.md = knowledge) + `scripts/` (validate_scene.py, headless_render.py, style_overlay.py). Frontmatter: `name`, `description` (trigger phrases), `allowed-tools` (Claude Skills GitHub Tools §7)

### H. CI / batch render pipeline for 33 cabins (Claude Skills GitHub Tools §9)
- `.github/workflows/nightly-renders.yml`: cron `'0 2 * * *'` (2am daily), matrix over 33 cabin names, container `blenderkit/headless-blender:5.1`, step `blender -b pilots/base/${cabin}.blend --python scripts/render_nightly.py`, upload-artifact
- CI = preview quality (**128 samples**); full 2K runs via VPS cron with GPU passthrough

### I. Blender Python automation deep reference (all from Blender Python Automation Deep Reference unless noted)
**Geometry Nodes via Python (4.x interface system)**:
- `ng = bpy.data.node_groups.new(name, "GeometryNodeTree"); ng.is_modifier = True`; sockets via `ng.interface.new_socket(...)`
- `GeometryNodeDistributePointsOnFaces` `distribute_method='POISSON'` (blue-noise, no clumping) or `'RANDOM'`
- `FunctionNodeRandomValue`: `outputs[1]`=float, `outputs[0]`=vector; scale random default 0.8–1.2
- Chain: DistributePoints → InstanceOnPoints ← CollectionInfo (Separate Children=True, Reset Children=True) → RealizeInstances → GroupOutput
- Attach: `m = obj.modifiers.new("Scatter","NODES"); m.node_group=ng; m["Socket_2"]=density` (interface sockets use identifier keys)
- Density from vertex paint: `GeometryNodeInputNamedAttribute` type `'FLOAT'` name `"density"` → dist Density input

**Materials via Python** (Principled BSDF values):
- Glass: Transmission Weight 1.0, **IOR 1.52**, Roughness 0.02; dirt via Noise Scale 50 → ColorRamp element pos 0.55 → MixShader with Diffuse (0.15,0.13,0.10)
- Weathered wood: Noise (low scale, high distortion) → Mapping stretch Y 20× → ColorRamp → BaseColor; 2nd Noise → Bump strength 0.05
- Leaf: TRANSLUCENT BSDF mixed 50/50 with Principled, mix driven by Geometry>Backfacing, alpha texture blend mode `'CLIP'`
- Concrete: Noise + Voronoi → rough grey base; Wicker fabric: 2 Wave Textures at 90°, multiply

**bpy.ops vs low-level API**:
- Direct data (`bpy.data.objects.new`, `mesh.from_pydata`) = **10-100× faster**, deterministic, headless-safe; bpy.ops mutates context, records undo, slow at scale, context-dependent
- Context override: `with bpy.context.temp_override(...):` (since 3.2). Use `id_block.asset_mark()` not `bpy.ops.asset.mark`. `select_all` needs `mode='OBJECT'`. Never call ops in tight loops

**Light groups + passes (Cycles only)**: `vl.lightgroups.add(name="Key")`; `lamp.lightgroup="Key"`; each group → `Combined_<name>` pass for compositor re-balance without re-render. Enable passes: combined, diffuse_direct/indirect, glossy_direct, ambient_occlusion, z, mist; `sc.cycles.use_pass_volume_direct=True`

**Compositor automation**: `CompositorNodeGlare` glare_type='BLOOM' threshold 1.0; `CompositorNodeColorBalance` correction_method='LIFT_GAMMA_GAIN'; `CompositorNodeLensdist` Distortion 0.02

**Drivers (wind anim)**: `obj.driver_add('rotation_euler',0)`, type SCRIPTED, SINGLE_PROP var → scene custom prop `["wind_strength"]`, expr `"sin(frame/12 + id(self).location[0]) * wind * 0.08"`; use driver variables (depsgraph tracks), phase via `id(self).location`; armatures use COPY_ROTATION + `constraint.driver_add("influence")`

**bmesh**: always `ensure_lookup_table()` after topology change; `bmesh.ops.bevel(..., offset=0.01, segments=3, profile=0.7, affect='EDGES')`; `bm.free()`; never hold bmesh refs across operators

**Recurring gotchas**: (1) depsgraph staleness → `bpy.context.view_layer.update()` after modifier swaps; (2) .blend save invalidates held Python pointers; (3) `bpy.data.objects.new()` does NOT link to collection — must explicitly link; (4) undo doesn't revert direct data writes, only ops; (5) headless skips viewport-only features (workbench AO); (6) asset preview generation needs UI — generate once interactively, save .blend

**Collections**: one per logical group (`_props/trees`, `_props/rocks`, `_lights`, `_geo/cabin`), prefix internal with `_`; for 1000s of instances use `obj.instance_collection=coll` empty instancer over deep nesting; `coll.hide_render`/`hide_viewport` for toggling

### J. Shared-data transform_apply pitfall (CRITICAL — Blender Shared-Data Transform Apply Pitfall)
- When objects share mesh data (`clone.data = source.data`), `transform_apply()` **silent-fails or corrupts ALL instances** (applies vertex shift to shared data). Symptoms: "objects don't move" / "transforms do nothing" / bbox huge (>50m) / `o.location` ≠ `matrix_world.translation` / multiple objects jump to one spot.
- Before applying: check `print(o.data.users)` — if >1, data is shared.
- **Fixes**: (1) `bpy.ops.transform.translate(value=(dx,dy,dz))` respects matrix on shared data; (2) make unique `clone.data = source.data.copy()` before apply; (3) set `o.matrix_world` directly (nukes rotation) or `o.matrix_world.translation=(x,y,z)`; (4) parent to empty + transform empty (cleanest for groups — preserve child `matrix_world` after re-parent).
- For animations: **NEVER apply**, always use object transform.
- **Real cases (Roosmarijn 2026-06-05)**: (a) Birch hero `Birch_2_Birch_Atlas_0` wouldn't move (0.92,-7.66)→(4.5,-8) due to gltf import 90° X-rotation in `matrix_local` that didn't decompose → transform_apply silent-failed 4+ min; fix = delete original, keep positioned .001/.002 clones. (b) Hetz topiary sf=0.0596 (0.7m/12m) applied to shared data multiple times → world bbox 700m×1200m zombie meshes broke entire Cycles render.

### K. Efficiency / hotkeys / custom operators (Blender Efficiency Hotkeys + Workspaces)
- **Custom pie menus** auto-load from `scripts/startup/blw_pies.py`; F8 lighting pie (`BLW_MT_lighting_pie` → recipes overcast/golden/midday/blue_hour/studio/night via `cabin.apply_recipe`), F9 compositor pie, F10 scene audit (validate_scene.py), Shift+F12 render-with-recipe
- Startup script layout `~/.config/blender/5.1/scripts/startup/`: blw_pies.py, blw_ops.py (cabin.next_camera, cabin.validate, cabin.render_with_recipe), blw_keymap.py, blw_workspace.py — all `.py` in `scripts/startup/` auto-load
- Register keymap in `wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')`
- **Lock interface for render**: `bpy.context.scene.render.use_lock_interface = True` (prevents UI hangs)
- Asset Browser catalogs live in `blender_assets.cats.txt` (version-control it); blokhutwinkel catalogs: `cabin_parts/`, `vegetation/{trees,hedges,groundcover}`, `hardscape/stones`, `furniture/garden`, `lighting/recipes`, `style_overlays/{cottage,scandi,modern,boho}`
- Face Project snap = drop plants onto terrain (enable "Project Individual Elements" for scatters); Increment+Absolute Grid Snap on 50mm grid for klinkers
- **Performance**: distant trees Display As Bounds (skip GN eval in viewport, renders full); Simplify viewport subdiv 0; `texture_limit_render=2048` + `use_persistent_data=False` keeps RTX 3070 8GB stable; top-bar/status-bar shows VRAM during render
- Save: `Save As Copy` keeps current path (milestones e.g. `cabin_M24_v3_milestone.blend`); `Save Incremental` auto-bumps `_001→_002` (5.x); `External Data > Make Paths Relative` must-do before commit
- Est. **~5min/render saved → 5×165 = 825min ≈ 13.75h per full pipeline cycle**

### L. Blender 5.x API / feature changes (Blender 5.x Archviz Features)
- **GN 5.x**: Closures (node groups as values — refactor `style_overlay` per style), Bundles (typed multi-output), For Each Geometry Element (per-plank variation), Volume SDF nodes, UV Tangent + per-corner normals, Mesh Boolean v3 (manifold-preserving)
- **Shaders**: Principled BSDF v3 — Thin Film input (300-1000nm + IOR; window glass 400nm IOR 1.5), OpenPBR alignment (Specular Tint → F0/F82), Coat as proper layer, Subsurface scaled to radius; Raycast node (fake AO/curvature)
- **View transform**: **AgX is default** (Filmic legacy). Upgrade code: `scene.view_settings.view_transform='AgX'`, `scene.view_settings.look='AgX - Punchy'`. AgX+Punchy+exposure **+0.3** ≈ Filmic Medium High Contrast 4.x. Rec.2100-PQ/HLG for HDR; ACES 2.0 shipped
- **Cycles**: OIDN temporal stability improved (albedo+normal passes still required for ALBEDO_NORMAL prefilter); CPU +15% on Windows (Embree); Light Tree default (`scene.cycles.use_light_tree=True` for nightshots); Shadow Caustics (Manifold NEE)
- **EEVEE Next** (draft only, 10× faster, NOT final hero): `engine='BLENDER_EEVEE_NEXT'`, `use_raytracing=True`, `ray_tracing_method='SCREEN'|'PROBES'`, `taa_render_samples=64`
- **API breaking**: Python 3.13; addons declare `bl_info["blender"]>=(5,0,0)`; `bgl` removed → use `gpu` module; mathutils now float32 (may need explicit numpy.float64 cast); Action slots replace tracks; access `scene.cycles.samples` not `scene["cycles"]` subscript
- **5.x watch-outs/regressions**: BAT-Pack needs ≥2.0; PolyHaven addon `_2k.jpg` vs `_2k.png` re-test; old 4.x GN sockets convert lossily (re-save + check warnings); OIDN preferred over OptiX (OptiX kept for noisy caustic interiors); **persistent data leaks memory faster on RTX 3070 8GB → keep `use_persistent_data=False`**

### M. Architecture / cabin plugin stack (Architecture Plugins Stack — cabins are 8m × 3.4m / 8000mm × 3400mm)
- **Archipack PRO €49** ⭐ — parametric walls/roofs/windows/doors, auto-boolean openings; `bpy.ops.archipack.wall2/window/roof`, params via `obj.data.archipack_wall2[0]`; fastest for orthogonal shells (free lite ships with Blender)
- **Sverchok FREE** ⭐ — 600+ nodes, Grasshopper-like; build ONE master node tree (width/depth/roof-pitch sliders) to generate all 33 template variants (v2 replacement for manual builds)
- **CAD Sketcher FREE** — constraint 2D sketch (lock 8m×3.4m floorplan then extrude); pre-1.0, back up files
- **Trowel** (was Brick Stack) — 17 country brick presets incl **Dutch waaltjes/waalformaat (210×100×50mm)**, Flemish bond = authentic Dutch klinker; free alt = BrickTricks / built-in Brick Texture node (0.5 offset)
- **Gardener addon ~€45** (Superhive) — 96 hedge biomes incl beech (beuken haag) on Geo-Scatter
- Others: ProWood shader pack (Shou Sugi Ban + cedar two-tone), MeasureIt-ARCH FREE (dimension callouts → SVG/DXF/PNG), Truss Generator ~$15, Stairs Maker ~$25, HardOps+BoxCutter $38 lifetime (boolean window/door cuts), Building Tools (ranjian0 free), HiFi Architecture Builder v4.5.8, Archimesh (free)
- **SKIP Bonsai BIM** (IFC) unless client wants IFC deliverables — overkill for marketing renders

### N. 3D-print verdict on Blender MCP (both servers)
- Both ahujasid and minihellboy MCP: **wrong tool for deterministic FDM print parts** — Blender mesh kernel does not enforce manifoldness (the "constant battle" in CAD comparisons); no native print-prep (no manifold check, orientation optimizer, or support generator). Good for art + scene composition + AI asset gen (Shap-E organic shapes); for parametric printable parts prefer CadQuery / flowful-ai cad-skill; downstream still need manifold validation + repair before slicing (ahujasid blender-mcp; minihellboy claude-blender)

### Currency / conflict notes
- All concept notes dated 2026-05-22 except Custom Asset Import (2026-04-30) and Shared-Data Pitfall (2026-06-05, newest). No direct contradictions.
- **ahujasid = CURRENTLY USING**; PatrykIti/blender-ai-mcp flagged as recommended future replacement for production (not yet adopted).
- Filmic → **AgX supersedes** as 5.x default.
- CLAUDE.md/MEMORY note (not in these files): live sessions run **two MCP servers** — `mcp__Blender__*` (capital) for scene work, `mcp__blender__*` (lowercase community addon) for Sketchfab/PolyHaven downloads; heavy scenes crash via MCP → always headless CLI render.


---

<a id="11"></a>
# §11. Assets, inventory & garden styles

### Local project asset root & decision rule
- Root: `C:\Users\beike\Documents\Blender-blokhutten\assets\` (Blokhutten Project Asset Inventory).
- Priority order (ALWAYS): **real texture > 3D model > procedural**. Only build procedural if no suitable inventory asset. Read inventory page BEFORE building any shader/material/scene element (Project Asset Inventory).
- Blokhutwinkel GLB imports come in **cm** → apply **0.01× scale** after import + delete embedded camera (Garden Style Inspiration Catalog; MEMORY blokhutwinkel_glb_scale).

### Blokhutwinkel real-product textures (PRIMARY for cabin materials)
Path: `assets/blokhutwinkel-textures/8192/` — 8K real-product textures; use these first, not Polyhaven/procedural (Project Asset Inventory).

| File | Type | Cabin use |
|---|---|---|
| `luxehouse-grijs-gedompeld.jpg` | dark grey stained wood | **Wall** (Camelia/Magnolia dark Scandi) |
| `luxehouse-grijs.jpg` | light grey wood | Wall lighter alt |
| `luxehouse-onbehandeld.jpg` | natural untreated | Wall natural cedar/larch |
| `hardhout-deuren-ramen.jpg` | hardwood doors/windows | **Door + frame + windows** (warm contrast) |
| `hardhout.jpg` | hardwood general | Trim variants |
| `douglas.jpg` | Douglas fir warm | **roofBeam, roofboard, poles** |
| `douglas-rabat.jpg` | Douglas rabat profile | Wall accent |
| `kdi_rabat.jpg` | KDI rabat | Wall budget |
| `kdi_potdeksel_zwart.jpg` / `kdi_rabat_fbz_zwart.jpg` | KDI black | Dark accent |
| `beton.jpg` | concrete | **foundationBeam** |
| `shingles-zwart.jpg` | black bitumen shingles | **roofPlate** (sloped) |
| `staalpannen-antraciet.jpg` | anthracite steel tiles | Metal roof |
| `epdm.jpg` | EPDM rubber | **flatroof-40-board** (Magnolia flat roof) |
| `muur-diff.jpg` + `muur-disp.jpg` | brick | Foundation alt |

- `8192-complete/` has full PBR for `luxehouse-onbehandeld` (_COLOR/_NRM/_DISP/_OCC/_SPEC.png).

**Camelia proven per-material mapping (replicate for Magnolia):** wall=`luxehouse-grijs-gedompeld`, door=`hardhout-deuren-ramen`, roofBeam/roofboard/poles=`douglas`, roofPlate=`shingles-zwart`, foundationBeam=`beton`, canopyWall=`luxehouse-grijs-gedompeld`, flat roof=`epdm`.
- **Camelia node graph:** TexCoord(Object)→Mapping(scale 4)→ImageTexture A; second Mapping(scale 5.5, rot 75°)→ImageTexture B (same image); Noise(scale 1.5, detail 2)→ColorRamp(0.35–0.65 sharp)→Mix.Fac; Mix(MIX, A→Color1, B→Color2)→BSDF Base Color. **BSDF Roughness: 0.85 wood, 0.55 hardwood door, 0.9 shingles.** Result = two-tone Scandi (dark grey wall + warm hardwood accents).

### Polyhaven textures (local `assets/polyhaven/textures/`)
| Folder | Maps (2K JPG) | Use |
|---|---|---|
| `dark_planks` | diff+nor_gl+rough | Dark wall (Japandi); dim HSV |
| `brown_planks_09` | diff+nor+rough | **Warm cedar/larch wall** — verified 2026-05-21 |
| `forrest_ground_01` | diff+nor+rough+disp | Path edges, dirt patches |
| `paving_stones_64` | diff+nor+rough | Stone path/terrace |

- **PBR setup:** nor_gl & rough set `colorspace = 'Non-Color'`; TexCoord(Object)→Mapping→3×ImageTexture→BSDF; anti-tile = 2 mappings (different scale+rotation) blended via Noise.
- **Verified warm-cedar recipe (2026-05-21) on `brown_planks_09`:** map1 scale (5,5,5) rot 0°; map2 scale (3.5,3.5,3.5) rot 75° (1.5 rad); blend Noise scale 2.0. Cedar **HSV: hue 0.52, saturation 1.15, value 1.0**. Per-plank variation via Object Info Random → ColorRamp 0→0.92 grey, 1→1.08 warm (±10% brightness), Multiply onto HSV factor 0.7. **BSDF: roughness from texture, Specular IOR 0.4, normal strength 1.0** (Project Asset Inventory).

### Polyhaven HDRIs (local `assets/polyhaven/hdri/`, 2K)
| File | Mood | Style match |
|---|---|---|
| `kloppenheim_06_puresky` | clear bright | Modern Minimalist, Mediterranean |
| `kloofendal_43d_clear` | clear day | Standard daylight |
| `kiara_1_dawn` | soft dawn | Japandi, Scandi |
| `qwantani_dusk_2` | golden hour | Hero, Scandi sauna |
| `forest_slope` | dappled forest | Forest cabin |
| `spaichingen_hill` | overcast hill | Cottage |
| `syferfontein_18d_clear` | midday clear | Bright product shots |
| `venice_sunset` | warm sunset | Mediterranean dramatic |
| `the_sky_is_on_fire` | extreme sunset | Marketing dramatic |
| `moonless_golf` | night | Twilight |

- Other named HDRIs referenced across notes: `symmetrical_garden` (modern formal), `studio_garden` (cottage/English, clear midday harsh shadows), `kloppenheim_03`, `gem_2` (Mediterranean warm midday), `qwantani_noon`, `sunflowers_puresky` (boerderij), `snowy_park_01` (winter), `kloofendal_43d_clear_puresky`.
- **Dutch overcast signature look (all CC0):** `kloppenheim_02_puresky`, `qwantani_puresky`, `overcast_soil_puresky`, `belfast_sunset` (Free Asset Libraries).
- Resolutions available 1k/2k/4k/8k/16k; **use 4k or 8k for sales visuals**, 16k only for extreme reflection close-ups (Polyhaven source).
- Sun strength cues: Modern midday strength 1.0; Mediterranean midday strength 2.0–2.5; golden-hour mood strength 2–3, camera EV −0.5 (Garden Style Palette/Catalog).

### Polyhaven 3D models (local `assets/polyhaven/models/`, *_2k.blend/.gltf)
- **Plants:** anthurium_botany_01, calathea_orbifolia_01, pachira_aquatica_01 (indoor decor), periwinkle_plant, fern_02, moss_01 (Japandi/zen), wild_rooibos_bush (Med), shrub_01/02/03/04, shrub_sorrel_01 (Med), weed_plant_02, dandelion_01.
- **Flowers:** flower_gazania, flower_heliophila.
- **Trees:** pine_tree_01, jacaranda_tree.
- **Stones:** boulder_01 (.gltf), stone_01.
- **Furniture:** outdoor_table_chair_set_01, coffee_table_round_01, painted_wooden_bench, Sofa_01, modern_arm_chair_01, potted_plant_01/02/04.

### Sketchfab assets (local `assets/sketchfab/<category>/`)
**Flowering bushes:** `kalmia_latifolia_galaxy` (white+pink, ~1.5m — working rhododendron substitute), `bigleaf_hydrangea_...ue_raw` (blue/white 0.7–1.2m, 8 variants A–H), `goldmound_spiraea_red` (~1.5m), `azalea_..._lidar_scan` (pink ~1.3m, real geometry), `elderberry_...ue_raw` (white ~1.5m, 7 variants), `field_poppy_...ue_raw` (red ~0.6m, 8 variants), `multi_color_butterfly_bush` (~2m), `roses`. **DO NOT USE `rhododendron_azalea_free_download`** — contains stray insect/dragon mesh.
**Trees:** `tree_english_oak_forest_01_usd` (8–14m, variants A–D; use B/C/D for backdrop), `tree_yoshino_cherry_01_usd` (6–7m, pink blossom A–D), `maple_tree_scan_trunk_4_lod` (~5m photogrammetry), `five_birch_trees_pack_lowpoly`, `billboard_tree_pack` (far BG). Avoid `pine_tree_trio_free_download` (only ~0.94m, too small).
**Topiary/hedge:** `hetz_midget_arborvitae_round_tree_topiary` — **only hedge asset**, 2.5m, EMPTY parent + MESH children, duplicate for hedge row, **scale 0.4× for boxwood balls**, origin 1m above base (bbox z_min=1.0 → sink −1m).
**Path stones:** `mossy_stones_pack` (4 stones 0.13–0.34m, scale up+flatten Z), `cobblestones_scan`, `flagstone_floor_8k_ue_raw`, `construction_gravel_8k_ue_raw`, `grey_natural_slate_stone_wall`, `japanese_mossy_stone_wall_...` (Japandi). Avoid `rocky_stone_path_scan` (14×19m landscape).
**Ground/grass:** `1024_mat_025_grass` (1K PBR — Object coords + Mapping scale 0.3–0.5, do NOT stretch), `game_ready_grass` (billboard cards), `wild_grass_...ue_raw` (8 real 3D clumps 0.3–1.6m, originals at scale 0.01 → MULTIPLY scale), `ribbon_grass_...`, `lady_fern_...ue_raw` (9 variants shade), `clovers_plants_foliage`.
**Furniture:** `adirondack_chair_photogrammetry`, benches (`bench`, `wooden_bench_low_poly`), `bistrot_table_and_chair`, `deck_chair`, `dining_set`, `outdoor_chair_scan_medpoly`, `outdoor_relax_chair`, `pergola`, `picnic_table_low_poly`.
**Lighting:** `garden_lamp.blend`, `lamp_2/3.blend`, `low_poly_garden_lamp_stylized`, `old_lantern`, `solar_panel`.
**Decor:** `birdbaths`, `cc0_rose_arch`, `terracotta_pot`, `optimized_potted_plants`, `old_wicker_basket`, `small_wooden_bird_feeder`.
**Deck/wall:** `wooden_deck_a`, `spruce_fence`. **Tools:** `axe_fab`, `garden_shovel`/`shovel_low_poly`, `tachka.blend` (wheelbarrow).

### Asset gotchas (lessons 2026-05-21, Project Asset Inventory)
- **SM_/UE-raw assets import at scale ~(0.01,0.01,0.01)** — always MULTIPLY, never overwrite: `copy.scale = (copy.scale.x*factor, ...)`.
- **GLTF parent transforms:** setting child `location` is local space. Unparent keeping world matrix: save `matrix_world`, `parent=None`, restore.
- **Floating meshes:** origin not always at base — compute world z_min over bound_box corners, `obj.location.z -= min(zs)`. Per anti-uncanny rule sink plant **−0.02 to −0.05 into ground** (not just touch).
- **USD trees (oak/cherry)** import with loose Branch prototypes as siblings — hide all objects whose name contains `ASY_Branches`/`Sub_Branches`/`Yoshino_Cherry_Branch` (hide_viewport+hide_render).
- **Open inventory gaps:** no real charred/Shou Sugi Ban texture (combine `dark_planks` + procedural Voronoi crack); no dedicated boxwood (use hetz_midget @0.4×); no cypress; no roof-tile texture (Polyhaven `roof_07`/`roof_shingles_*` to download); no hardware (deurkruk/scharnieren/slot).
- **Avoid:** pure black for Shou Sugi Ban (reads plastic).

### User-curated / import workflows (User Curated Assets)
- Log every asset with UID + name + size + use case + source platform per session.
- Asset UID `35d5a983f95d4776b128c0a132ede63d` (2026-05-21, Lavendel zijwand carport) — source unidentified; Sketchfab API returned 404 (maybe Hyper3D Rodin/Hunyuan or Blender's own plugin).
- Three import paths: (A) user downloads via Blender Sketchfab plugin → Claude reads via `get_scene_info`; (B) user gives UID → `download_sketchfab_model(uid, target_size)`; (C) AI-gen via `generate_hyper3d_model_via_text`/`generate_hunyuan3d_model` → poll → `import_generated_asset`.

### Cabin inventory: 8 lines × 33 pilots (Blokhutten Cabin Inventory)
Lines (flower names = product lines): **Camelia** (Scandi forest, 250×300), **Dahlia** (Modern/boerderij, 250×250), **Jasmijn** (Cottage hybrid, 300×250), **Lavendel** (Provence Lavender, 400×300), **Lelie** (English cottage, 400×250), **Magnolia** (Modern Japandi, 300×200 — ONLY flat-roof model), **Roosmarijn** (Mediterranean herb, 200×300), **Zonnebloem** (Boerderij sun, 300×300).
- Naming: `<Line> <BaseSize> [+ <Extension> [+ zijwand]]`; folder coding uses hyphens (e.g. `Camelia-250x300-300-zijwand`). Extensions typically +250/+300/+400 cm.
- **33 pilots** total: Camelia 5, Dahlia 4, Jasmijn 5, Lavendel 5, Lelie 5, Magnolia 1, Roosmarijn 3, Zonnebloem 5.
- **3 HERO pilots (full custom blend + many renders):** `Camelia-250x300-300-zijwand` (Scandi forest, dark grey-blue stained walls, 8+ renders), `Lelie-400x250-300-zijwand` (English cottage, light wood, 6+ renders), `Magnolia-300x200` (Modern Japandi, dark grey-blue walls + EPDM flat roof + hardhout door, 13+ renders M20–M26).
- **Materials:** vurenhout/sparrenhout (base), Douglas/lariks (premium, darker, weatherproof).
- **File locations:** master GLB sources `source-glbs/<Cabin>.glb` (33 files, ~6.5–6.8MB each, embedded textures); hero pilots `pilots/<Cabin>/`; batch pilots in worktree `.claude/worktrees/gifted-euclid-92e115/pilots/<Cabin>/` (3 preview renders per style: AI_FINAL, REAL3D_FINAL, V2_FINAL).
- Up to **14 style subfolders** per pilot: style-klassiek-familie, -modern, -modern-pavilion, -modern-urban-cottage, -scandi, -cottage, -english-cottage, -cedar-lounge, -premium-cedar-lounge-wide, -natuurhout-veranda, -boerderij, -forest-wilderness, -japanese-zen, -hot-tub-premium. Combinatorics: 33 × ~14 = ~460+ renderable scenes.
- Render status: 3 hero + 30 batch = 33 folders; **132 renders in gallery** (auto-detected). `pilots/gallery.py` auto-detects worktree pilots since 2026-05-21; shows 36 sections on http://localhost:8090 (note: viewer server also runs on localhost:8765 per MEMORY; gallery on 8090).
- Batch→hero promotion (per pilot): import GLB → apply blokhutwinkel textures via Camelia node graph → unhide door+glass+chrome+pot plants (13 elements) → Ultimate Render Recipe → garden context per style → 1080p Cycles GPU. Estimate ~1u setup + 1min render each.

### Blokhutwinkel.nl (client context)
- Dutch supplier of blokhutten, tuinhuizen, veranda's, garages, carports, tuinkantoren, chalets, camping pods, pipowagens, kapschuren, overkappingen. Showroom Zutphen ("Europe's largest", 100+ models on-site, 10.000+ total incl. maatwerk). Free NL+BE delivery >€250. Offers free technical (CAD-style) 3D drawing — our value-add = sfeer/context/multiple styles.
- **Roof styles (product):** plat, zadel, lessenaar, piramide, wolfeind, boog, schuur, gedraaid, paviljoen.
- Product↔style hints: sauna-chalet→Scandi+hottub; tuinkantoor→Modern+corten+siergrassen; kapschuur→boerderij+moestuin+kippen; pipowagen→bos+dennen+firepit; paviljoen→zen or cottage; veranda→terras+lounge+warm avondlicht.

### Tekentool v2 — pole distribution rules (reverse-engineered 2026-04-29)
- Extra middle poles per wall span (mm): ≤5500=0; >5500=+1; >6500=+2; >9700=+3; >13000=+4; >16250=+5. Side-wall span = `depth_cm × 10`; depths 300/360/420/510 → 0 extra, 600 → +1.
- **System types (max overhang):** PRIMA_4_CORNERS 100mm; PRIMA_5_CORNERS 500mm; PRIMA_8_CORNERS 500mm; PRO_SYSTEM 859mm (inner poles allowed); LOG_CABIN 1500mm; LOG_CABIN_PORCH 400mm. POLES_CENTERED default true for PRO_SYSTEM/LOG_CABIN/LOG_CABIN_PORCH.
- Wall types: OUTER, INNER, CHALET (LogCabin default), SKELETON, ATTACHMENT, RAILING, NONE, GLASSPANE, GLASSFRONT.
- Roof types: FLAT, SADDLE, PYRAMID (4-corner + 0 rooms only), ASYMMETRIC, PENT. **Saddle pitch by roof width t:** 5° (t>4000 & 4 corners); 17° (t<4000); 21° (t>4000, SADDLE default); 26° (t>6500); 30° (t>5500).

### Free asset libraries (external — CC0/royalty-free, Free Asset Libraries + Asset Library Map)
- **HDRI:** Poly Haven ⭐ (CC0, no login, 1k–16k), HDRMAPS freebies (HMTools addon), HDRI Skies, HDRI Hub free samples, Blender Institute archive. Paid: HDRMaps (€10–30), Poliigon.
- **PBR textures:** ambientCG ⭐ (2000+ CC0, addon), Poly Haven (8K+), 3dtextures.me (CC0 @1K free), FreePBR (600+ 2K), TextureCan, CGBookcase (CC0+seamless tool), Sketchup Texture Club (klinker), Lightbeans (brick), **RawCatalog European klinker photogrammetry** (asset/2312), ShareTextures, TextureBox. textures.com (best for "3D Scanned Charred Wood Shou Sugi Ban"). Paid: Poliigon $25–30/mo.
- **Vegetation:** Poly Haven Models ⭐, **The Plant Library (BD3D)** 170+ (1.5GB, Geo-Scatter biomes, gumroad), BlenderKit free (`is_free:true`), Botaniq free tier + Engon scatter (polygoniq), Geo-Scatter 31 free biomes + Biome-Reader, Quaternius Ultimate Nature Pack (CC0 low-poly), Sketchfab CC0, Tree-It, The Grove 3D (paid ~€136, free-trial trees), MTree (github), Sapling (built-in `Add>Curve>Sapling`), Modular Tree, Quaternius Garden Kit, Poly Pizza (CC-BY). Paid: Botaniq Lite ~$59/Full ~$129, Geo-Scatter ~$67, Graswald ~$99.
- **Scatter engines:** BagaPie free core ⭐ (50+ tools: scatter/ivy-gen/array/boolean, GPL), Geo-Scatter Biome-Reader free, GScatter fully free, Engon (Polygoniq).
- **Furniture:** BlenderKit outdoor-furniture free + fence generator + stone-path set, Chocofur free, 3dsky free (Scandi/European lamps+planters), TurboSquid/CGTrader/Free3D free, Poly Pizza.
- **Dutch specifics:** Lavendel = BlenderKit `lavender bush` / BD3D Drylands biome; Hortensia = BlenderKit Alexander Novgorodtsev hydrangea; Buxus = Botaniq/Quaternius; Beukenheg = Botaniq `beech_hedge`; Klinker = RawCatalog asset/2312 + ambientCG `PavingStones`; Cedar/larch = Poly Haven `weathered_planks`/`wood_table_001`.
- **Quixel Megascans: free tier ENDED** — downloads before 31 Dec 2024 are legit for reuse; new 2025+ assets paid via Fab. For blokhutwinkel: skip Megascans; Poly Haven + Sketchfab + GScatter suffices.
- **License matrix (marketing rule): CC0 or CC BY only; NO CC BY-NC / CC BY-ND.** CC BY-SA = viral, avoid. Avoid crack sites (AeBlender/VFXmed/GFXplugin).
- **Sketchfab curated:** Thomas Flynn (@nebulousflynn) CC0 collections (general / top-100 / architecture). Sketchfab quality varies (game-asset level), scale often wrong (not meters — check `dimensions`), some broken texture paths.
- **Library org convention:** `C:\BlenderAssets\{vegetation,furniture,materials,hdri,scatter}\...`; register via Prefs>File Paths>Asset Libraries; Mark as Asset + Catalog/Tags; use linked libraries for heavy vegetation; version-control `blender_assets.cats.txt`; naming `vendor_assetname_LOD_v##.blend`; pre-render check: 1u=1m scale, origin at base, normals correct, Principled BSDF.
- Item→source template: Adirondack (Sketchfab CC0/BlenderKit), hottub (Sketchfab+own texture), lantaarns (BlenderKit/Polyhaven), firepit (BlenderKit/Sketchfab), tuinslang (procedural curve+cylinder), water (Principled Glass + Wave shader, no library).
- MCP tools: `download_polyhaven_asset`, `download_sketchfab_model`; build local library "download once, use often" at `~/Documents/blender-assets/{hdris,textures,models}/`.

### Photogrammetry for cabin assets (killer hyperrealism trick)
- Tools: Polycam (free web + $60/yr LiDAR), Meshroom (free, needs CUDA GPU), RealityCapture (~$15/mo), Reality Scan (Epic, free non-commercial), Apple Object Capture (macOS free, USDZ→GLB).
- Photo counts: small object (stone/plant) 30–50; medium (bench/wheelbarrow) 80–150; large (wall/gevel fragment) 150–300. **Overlap 60–70%**, 3 heights, 360° every 5–10°.
- Scan candidates: houtblok/boomstam, bemoste rots, plank with grain, bark samples, stones (5 sizes), tegels/kasseien, plant with root, ornament. Do NOT scan: whole cabin, people/animals, cars, cloth. Requires diffuse light, no gloss/transparency, no wind, scale reference (coin/ruler).
- Cleanup: Decimate to 10K–50K (not 1M+), trim edge noise, bake hi→lo normal map, color-correct texture. Storage `~/Documents/blender-assets/scans/{wood,stone,plant,prop}/` as .blend with embedded textures + `library.json`.
- License: own scans on private property = own IP; blokhutwinkel showroom scans need owner permission (commercial use).
- AI single-image-to-3D alt: Stable Fast 3D, TripoSR, Hunyuan3D — placeholder quality, not hyperreal.

---

### GARDEN STYLES

#### Style Bible — 5 CORE styles (current authoritative deep reference; 33×5=165 variants, Garden Style Bible)
Supersedes the older 9-style palette for depth; the 13-style catalog remains the broader inspiration feed.

**Cross-style material slot map:**
| Slot | Modern | Scandi | Japandi | Boerderij | Mediterraan |
|---|---|---|---|---|---|
| 0 Wall | Black potdeksel | Pale cedar/Falu red | Shou-sugi-ban | Wit-gekalkt/log | White stuc |
| 1 Accent | Cor-ten steel | Sage trim | Engawa bamboo | Brick plinth | Terracotta panel |
| 2 Roof | EPDM/zinc flat | Birch shingle/sedum | Charcoal shake | Rode dakpan | Terracotta pantile |
| 3 Deck | Composite ipé | Pale ash whitewash | Bamboo/ash | Rustic eik/klinker | Travertine |
| 4 Trim | Matte black | White 9010 | Warm-black | Bosgroen | Aged teal |
| 5 Door | Matte black+steel | Matching wall | Shou-sugi-ban | Half-Dutch bosgroen | Faded olive |
| 6 Glass | Low-iron | Clear | Shoji reed | Clear+kruisroede | Clear+wrought-iron |

**1. MODERN STRAK:** Wall black potdeksel kdi (RAL 9005 / RAL 7016 anthracite, 22mm rabat); Polyhaven `painted_planks_02` recolour RAL 9005 rough 0.55 or `wood_planks_dirty`. Cor-ten accent (`rust_coarse_01`/`corten_steel`). Roof flat/5° monopitch, EPDM + verholen goot or weathered zinc; fascia max 18cm. Deck composite ipé 145mm wide 4mm gap, perpendicular to face. Plants STRUCTURAL: geknipte Fagus sylvatica hedge 180×60cm, Hetz Midget/Buxus balls row of 5–7 (h.o.h. 50cm), Calamagrostis 'Karl Foerster' drift 15–20, olijf in cor-ten, NO flowers. Hardscape anthracite klinker waalformaat 200×50×85mm elleboogverband or precast 800×400 8mm joint, cor-ten mowing-strip 100mm, split 8–16mm. Lighting matte-black bollard 600mm 2700K IP65 (Astro Borgo), NO solar/festoon. Palette `#0E0E0E`/`#1A1A1A`/`#A78A6E`/`#6B6B6B` + ONE accent (cor-ten `#B85C3E` OR olive `#7A8B5E`). Furniture HAY Palissade, Vipp/Tribù, Serax concrete. Refs Piet Boon, Norm Architects, Koto. Music 70–85 BPM ambient. Persona De Architect/Stedelijke Ondernemer 35–55.

**2. SCANDI/NORDIC:** Wall = (a) pale unfinished cedar weathered silver-grey (`weathered_planks`/`wood_planks_grey`), (b) Falu red oxide `#8B2E1F` + white trim, (c) fjord-grey light shou-sugi-ban (NOT deep black); boards 14–18mm. Trim white RAL 9010 or sage `#B8C5B0`, reveal 6–8mm. Roof birch shingle / 10° monopitch sedum green roof / black standing-seam+snow-rails. Deck pale ash/thermo-pine 120mm soap/whitewash, raised 200–300mm. Plants Betula pendula cluster 3–5 multi-stem (NEVER single), Vaccinium myrtillus, ferns, Lavandula 'Hidcote', Juniperus dwarf, Sedum carpet, Calluna. Hardscape pale gravel 8–12mm, cobble in mosvoegen, cedar boardwalk. Lighting warm 2700K copper lantaarn hung 200–220cm, NO anthracite/solar. Palette `#E6E0D6`/`#D8C3A5`/`#B8C5B0`/`#A78A6E` + mustard `#C49A3A`. Furniture Carl Hansen CH25, Skagerak, sheepskin. Music 60–75 BPM folk. Persona Sauna-Liefhebber/Hygge-Gezin 30–50.

**3. JAPANDI/WABI-SABI:** Wall true yakisugi deep scorched cedar alligator-skin (Polyhaven `charred_wood` or procedural, roughness 0.85, `#2A2A2A` warm-black NOT pure black); boards vertical 90–110mm. Trim warm-black 5mm reveal. Roof deep overhang 50–80cm, engawa walkway 2 sides, cedar shake/charcoal tile, exposed rafter tails. Deck bamboo/thermo-ash 200×30mm, engawa step-down 200mm. Plants Phyllostachys nigra/Fargesia rufa, Acer palmatum 'Bloodgood'/'Sango-kaku', moss (Polytrichum+Leucobryum), niwaki Pinus sylvestris, Ophiopogon 'Nigrescens', Hakonechloa. Hardscape granite stepping stones 400–600mm, karesansui raked white gravel, cedar bridge. Furniture low hinoki bench 40cm, raku planter, tsukubai+shishi-odoshi, yukimi-doro lantaarn. Lighting Akari andon 2200–2400K dimmable. Palette `#2A2A2A`/`#8B6F47`/`#5F7A6A`/`#E8E2D5`. Refs Kengo Kuma, Studio MK27, Van Duysen. Music 50–65 BPM koto/shakuhachi. Persona Rust-Zoeker/Wellness 45–65.

**4. BOERDERIJ/NL LANDELIJK:** Wall = (a) wit-gekalkte potdeksel `#F5EFE3`, (b) honingbruin Douglas log, (c) baksteen plint 90cm + cedar; boards 22mm rabat horizontal. Trim bosgroen `#3A5A3A` OR grijs-blauw `#2F4858` luiken + white 9010, half-open Dutch deur. Roof rode ceramic dakpan (Tuile Romane/oude-Hollandse golfpan, mos `#5F7A6A`), 45° steep saddle, opt dakkapel/riet; NO leien/metaal. Plants Lavandula angustifolia, Rosa 'Graham Thomas'/'Constance Spry' op rozenboog, Pelargonium in melkbus, stokrozen, Hortensia 'Annabelle', kruiden raised bed, klimop; density HIGH. Hardscape oude baksteen/kasseien visgraat-verband, klinker waalformaat path 90cm STRAIGHT to door (formal cottage rule), kastanje-schutting. Furniture 3m boer-tafel, houten bank, smeedijzer, terracotta clusters 3/5/7, melkbus planter, vogelhuisje. Lighting smeedijzer sconce 150–170cm 2400K E27 Edison, NO solar/LED-strips. Palette `#F5EFE3`/`#3A5A3A`/`#7A3526`/`#7B6D5C`. Music 80–100 BPM Dutch-folk. Persona Plattelandsgezin/Hobby-Boer 35–65.

**5. MEDITERRAAN:** Wall = (a) white stuc `#F4ECDE` hand-troweled 3–5mm relief (`painted_plaster_wall`/`concrete_wall_005` recolour), (b) terracotta cladding `#D4A574`. Trim aged terracotta `#B85C3E` or grey `#8C7B66`, luiken faded teal `#5A7878`/olive. Roof terracotta pantile 25–35° mixed batch, cedar rafter tails 30–40cm overhang, opt pergola. Deck travertine 600×400mm tumbled (`travertine_tiles_03`) or aged teak grey, light mortar joints. Plants Olea europaea twisted 2–3m, Lavandula stoechas, Rosmarinus hedges, Citrus limon in pot, Cypress columns, Salvia/Thymus mass, Verbena bonariensis; NO pampas/hortensia/tropical. Hardscape travertine, pebble mosaics, terracotta clusters 5–7, light-beige gravel (NOT grey). Furniture Sika-Design/Vincent Sheppard wicker, wrought-iron, kelim, Talavera. Lighting rattan lantern 2200K, festoon between olijfbomen. Palette `#F4ECDE`/`#7A8B5E`/`#B85C3E` + cobalt `#3A6B8A`. Music 90–110 BPM Spanish guitar. Persona Vakantieganger/Premium Recreatie 40–60.

**Anti-pattern reminder (all 5 styles forbid):** vliegend gras op gravel, UV-sphere boxwoods, calathea/anthurium outdoors, solid-green hedge walls, scatter without bed-boundaries, stepping stones boven grind, DIY-block furniture proportions.

#### 13-Style Inspiration Catalog (broader feed, Garden Style Inspiration Catalog Extended)
Per style: Latijnse plantnamen + props + HDRI + hex palette + inspiration URLs. Styles: 1 Modern Minimalist, 2 English Cottage, 3 Scandinavian/Nordic, 4 Forest/Wilderness, 5 Mediterranean, 6 Japanese Zen (Karesansui — rocks in 3/5/7 odd groups, never symmetric), 7 Boerderij/Dutch Farmhouse (boerengroen RAL 6009), 8 Tropical/Bali (winterharde NL alts: Trachycarpus i.p.v. Cocos, Musa basjoo), 9 Coastal/Duinen (Ammophila arenaria, Hippophae, Eryngium maritimum), 10 Industrial/Urban Jungle (corten + Parthenocissus vertical), 11 Prairie/Piet Oudolf (**70% structuur / 30% filler, plant in drifts, "learn to love brown", Calamagrostis 'Karl Foerster'/Molinia 'Transparent'/Panicum 'Heavy Metal'/Echinacea/Veronicastrum**), 12 French Provence (Lavandula ×intermedia 'Grosso', Wisteria, Cupressus 'Stricta'), 13 Alpine/Berghut (edelweiss, gentiaan, Larix decidua; wildflower peak July–Aug).
- Mediterranean mulch trick: 5cm gravel under plants (anti-fungus, authentic look).
- **Style × product matchmaker:** Tuinkantoor→Modern/Industrial/Prairie; Sauna-chalet/barrel→Scandi/Forest/Alpine; klassieke blokhut zadeldak→English Cottage/Boerderij/Provence; veranda/overkapping→Mediterranean/Provence/Tropical; paviljoen/priëel→Cottage/Zen/Provence; kapschuur→Boerderij/Industrial; pipowagen/pod→Forest/Coastal/Boerderij; plat-dak modern→Modern/Industrial/Zen; strand/duin→Coastal/Scandi; berg-chalet→Alpine/Scandi/Forest; tuinhuis Douglas/lariks→Scandi/Forest/Boerderij.
- MCP production tips: one render-pass per style (same camera, only dressing changes); scatter groundcover first then place solitairs; rotate HDRI before tweaking materials; set plants to real max height (hollyhock 2.5m vs lavendel 0.6m); brand accent color subtly echoed on cushion/pot.

#### 9-Style Palette (older, superseded by Bible for the 5 core; still holds lighting-moods)
- Adds two overlays NOT in the Bible: **#8 Golden Hour/Avond** (lighting-mood over any style: warm HDRI qwantani_dusk_2/the_sky_is_on_fire, sun strength 2–3, EV −0.5, practicals ON 2700K window/string/lantaarn — use for product-page hero) and **#9 Winter/Sneeuw** (GN snow-particle scatter on grass, rookpluim volumetric, hulst-bes red accent, HDRI `snowy_park_01`).
- Also has **#5 Terras+Hot Tub/Lounge** (hardhout ipé/teak vlonder, pampas flanking, bamboo privacy, olijfboom, string-lights, HDRI gem_2/sunset/blue hour — instagrammable premium).
- **Combination rule:** render 3–4 styles per cabin (not all 9); one style must always be a golden-hour version for the product-page hero.

### Cross-references / related notes (not read here)
Wood Material Recipes for Cabin Visuals, Procedural Shou Sugi Ban Shader Recipe, Ultimate 1080p Cycles Render Recipe, Lighting Recipes for Cabin Archviz, Hyperrealistic Cabin Rendering Beyond Photoreal, Vegetation Scattering Recipes, Geo-Scatter Plugin, ahujasid blender-mcp, Blokhutwinkel Real Product Textures, Photoreal Archviz Anti-Uncanny-Valley Rules.


---

<a id="12"></a>
# §12. Project builds, lessons & garden-style research

Dense distillation across 11 vault notes. All 11 read in full; none missing/empty.

### A. Render-fix lessons — the big June/July 2026 review round (Blokhut Render-Fix Lessons)
16 blokhut marketing renders reviewed with Beike as critical reviewer. Per-topic: fout → waarom → fix.

**Paden (paths)**
- NIET: amoebe-stapstenen op zwarte bedding (`MAT_PadBed`); platte witte fallback-mats (`*Flag`/`*PaverFB`, base 0.8 = "wit plastic"); pad dat niet op de deur aansluit ("pad naar nergens"); kaarsrecht auto-paver-pad.
- WEL: sluit pad niet logisch aan → gewoon weghalen ("niet elke scene heeft een pad nodig"). Schoon gazon > lelijk pad. Echte terrassen (`Klinker`/`Terras`/hout/deck) SPAREN — alleen pad-stenen + bedding weg.
- Kernles: een materiaal-fix lost geen VORM-probleem op (warmere kleur haalde amoebe-vormen niet weg).

**Groene/witte blobs**
- NIET: platte "Mos"-schijven (`MosPlek`/`MosEiland`, `MAT_MosProc`/`MAT_MosHeuvel`), witte amoebe-zand (`Karesansui`).
- WEL: detecteer op NAAM ("Mos"/"Karesansui") + platte-schijf-vorm, NIET op base-kleur (groen kan via shader-node komen; base toonde 0.8 grijs → base-color-check mist `MosEiland`).

**Licht (grootste les)**
- Recept: HDRI (sfeer-passend) + STERKE directionele zon/maan + LICHTE volumetrische mist (height-falloff) + AgX + warme praktische lampen.
- NIET: plat licht; verzadigd-blauwe maan/mist = "blauwe horror-gloed"; te dichte mist = "vaag/wazig"; pure backlight = donkere gevel.
- Fixes: plat → sterkere zon (bv 300%) + echte HDRI + beetje mist. Blauwe gloed → fog-kleur NEUTRALISEREN (~`0.86, 0.85, 0.83`) ÉN zon/maan ontzadigen (zacht koel-wit); avondsfeer = laag lichtniveau + warme lampen, niet blauwe tint. Vaag → mist dunner (~`0.012` aan de grond) + AgX Medium-High Contrast + key sterker. Lavendel/koude grijze gevel onder roze dauw-HDRI (`kiara_1_dawn`) → zon FRONTAAL op hero-gevel (azimuth naar camerazijde), HDRI-strength ~`0.6`, zon warm-goud E~`9` elev ~`15°` (anders kleurt HDRI de gevel paars).
- Mist neemt lichtkleur over → houd neutraal/warm, nooit verzadigd. Overhaul = vooral mist toevoegen + zon/contrast tunen, HDRI meestal niet vervangen.

**Camera**
- NIET: hoog (z≈3.6) + wijd (35 mm) + gecentreerd + heel plateau in beeld = poppenhuis/maquette.
- WEL: lager (ooghoogte), strakkere lens (~50 mm), 3/4-hoek. Uitzondering: groendak-USP → hoog genoeg voor dak. Poppenhuis = camera-probleem, geen licht-probleem.

**Blokhut-textuur richting (nerf)**
- NIET: GLB-import zet board-mats (`basetexture-firstLayer-*` → wand/dak/fascia) op BOX-projectie op Object-coords → op potdeksel/rabat loopt nerf 90° verkeerd (verticaal tegelgrid).
- WEL: zet op mesh-`UVMap` + FLAT-projectie → nerf loopt horizontaal met de plank mee. Helper `cl.uv_board_textures()` in `scripts/cabin_lib.py` (relinkt TexCoord.UV→Mapping, projection BOX→FLAT, Mapping-scale blijft; fixt wand+dak+fascia in één call). Uitrol via `rollout_texture.py`. Geldt over ALLE scenes.

**Gras over hardscape / dek-gras-naad**
- Mechaniek: gazon = GN-scatter (`GN_GrassMasked` → `GrassTuft_X`), strooit alleen waar per-vertex float `grass > 0.5` op `GrassEmitter`.
- NIET: nieuw dek erbovenop leggen zonder masker → gras groeit over patio.
- WEL: zet `grass = 0.0` op emitter-verts binnen dek-footprint (+marge) via `ge.data.attributes["grass"]` loop over wereld-coords. Beike-voorkeur: verhoogd dek (~14 cm) steekt boven grastufts (~10 cm) → restgras verborgen ÓNDER de slab, gazon loopt tot fascia, GÉÉN grind-strip nodig.
- Kernles: gras op patio = MASKER-kwestie, geen materiaal.

**Asset-transform valkuil**
- Sommige props (bv `painted_wooden_bench`) hebben object-`location = (1000,1000,0)` + compenserende mesh-offset → geometrie belandt tóch op (0,0) in de cabin. `move_root_to`/`ground_to` grijpen niet.
- Check: `obj.location` vs `obj.matrix_world.translation` sterk verschillend? Dan offset. Fix: verwijderen of `obj.matrix_world` direct zetten. (Zie Blender Shared-Data Transform Apply Pitfall.)

**Werkwijze**: iteratief + kritisch, valideer op 1 scene → toon → dan batchen. Proben vóór fixen (Blender 5.1 `-b --python` dump-script: objecten + wereld-bbox + lichten + materiaal-nodes) — nooit namen/coords gokken. Headless CLI, één GPU-render tegelijk (HIP-warning onschuldig op NVIDIA/CUDA). Droogloop vóór destructieve batch. Review via lokale galerij (`python -m http.server 8765` + `generate_gallery.py`). Textuur/masker-fixes zijn snel + batchbaar (geen render nodig).
- Voorbeeld-templates: Lelie Ochtendnevel = warme-dauw (zon 300% + kiara_dawn HDRI + mist 0.022). Lelie Avondkubus = blue-hour (`qwantani_dusk` + koele maan + mist 0.012 + de-blue + crisp). Magnolia Wintertuin = houten dek op deur + `grass`-masker (dek→gazon) + UV-textuur-fix + warme dauw (kiara_dawn 0.6, zon E9 elev15 frontaal, haze 0.010, AgX Base); kapotte `painted_wooden_bench` verwijderd.
- Repo-docs: `docs/PLAN_lighting_overhaul.md`, `docs/ROUND2_feedback.md`. Tools: `remove_paths_blobs.py`, `add_atmosphere.py`, `build_path_rebuild.py`, `fix_*_light.py`, `fix_wintertuin_v5.py`.

### B. Lavendel build disasters — 19 iterations, v1–v19, 2026-05-21/22 (Lavendel Build Lessons Learned)
Every mistake documented so they never recur:
1. `bpy.data.libraries.load()` brings ALL variants (a–h) → land at origin (0,0,0) INSIDE cabin (169 dup plants v15–v18). Fix: `wm.append` on the COLLECTION, OR filter to one variant in load, OR hide `_b`.._h` after load. **NEVER use `libraries.load` for polyhaven plants.**
2. Linked-duplicate of empty: confusion over "the root" (Sketchfab GLTF root = `Sketchfab_model`; Polyhaven GLB = top Empty, no parent, loc 0,0,0). Select ALL descendants recursively, dup, move only new_root; children follow parent matrix_world.
3. Filename-based delete matched core `Object_X` (deleted schutting). Fix: whitelist known-keeper ancestors before deleting.
4. Camera framing not checked before placement (bushes at x=±7 outside 35 mm frame). Compute visible X-cone at each Y depth first.
5. Self-check too optimistic (v15 "good" while bushes in cabin, 24×19 m jacaranda at origin). HARD AUDIT CHECKLIST: no bbox-center in cabin x[0,4]×y[−1.7,1.7]; no dims >10 m (non-ground); schutting in frame; path endpoint within 1 m of door (x1.7,y1.5); <100 non-cabin objects; no `.001`+ dup >5 same pos; all trees outside; no magenta.
6. `jacaranda_tree_2k.blend` = 24×19×19 m even at scale 1, multi-LOD → DON'T use. Use `Tree_English_Oak_Forest`/`Tree_Yoshino_Cherry` USD (later superseded — see #11).
7. HSV Value 0.5 made anthracite path invisible → use HSV Value 0.75.
8. Hedge balls (Hetz_Midget, 1.8 m h, ~1.5 m crown) at 1.3 m spacing → gaps. Use array modifier or 0.6–0.8 m spacing, or long rectangular hedge mesh.
9. Polyhaven blends reference `_2k.jpg/.exr` but on-disk files are `_2k.png` → MAGENTA (82 images has_data=False). Fix: `find_match` script remaps `img.filepath` to `_2k.png` variant + `img.reload()`.
10. `wild_rooibos_bush_2k.blend` MISSING textures entirely → manual Principled BSDF + Noise (scale 25) + ColorRamp (lavender `0.4,0.25,0.55` @0.35 / leaf green `0.15,0.3,0.12` @0.65) → BSDF roughness 0.85.
11. USD trees (Yoshino, English_Oak) import LEAFLESS (importer misses GN/point-instancers). Use GLTF trees: `five_birch_trees_pack_lowpoly_lods_gltf`, `pine_tree_trio_free_download_gltf`, `maple_tree_scan_trunk_4_lod_gltf`. **This SUPERSEDES lesson #6's USD recommendation.**
12. Birch pack imports 5 trees + LODs (30 meshes; IDs 0,2,3,4,5 — no "1"; 6 meshes each). Filter by name, hide LODs/extras after import.

**Dahlia Oogsttuin (2026-06-12)**: `painted_grass/diff_2k.jpg` corrupt (94 bytes) → magenta; use `aerial_grass_rock` + HueSat (hue 0.53, sat 1.08, val 1.06). `_duplicate_collection_at` multi-variant bug (copies ALL variant offsets → 1 tree = 20 m loose pieces) → cluster source-meshes, pick highest cluster as donor. Birch scene.gltf = ~1600 empties over km's, unusable via copy. `field poppy nonUE-gltf` lives in `standard/` submap. Camera from (+X,+Y): world +X = LEFT in frame. HueSat: hue >0.5 → green, <0.5 → warm honey (gevel-warmte ~0.488). `periwinkle_plant` + `shrub_sorrel_01` have NO on-disk textures → procedural leaf-green. GLTF picnic table imports upside-down.

**Zonnebloem Zomeravond (2026-06-12)**: `flower_gazania_2k.blend` contains giant ground-scan meshes (mats `scan_2/4/5`) → donor-picker MUST skip `scan_*`. GLTF dining-set: max-Z = chair back not tabletop → find tabletop as thin (<12 cm) + wide (>0.6 m) mesh. Compute FOV — a path straight before the door can fall fully out of frame (camera 6 m beside). Klinker slabs on equal z → z-fighting black patch → edge-to-edge or 1 cm higher. Hedge GN-density 380 too thin (backlit see-through); 700 + sprig +25% + hedge +12% higher = dense. No tree as festoon anchor at dusk (dark crown pollutes rooflines) → wooden pole. `view_layer.update()` before every bbox measure (else stale matrices).

**16-scene session (2026-06-13) — cabin_lib.py born** (8 primary + 8 alt-style hero scenes, all 1080p preview):
- `tree_rings_clustered(full_only=True)`: sort donors by vert-count, use only full half → fixes leafless-pine at source (Camelia/Magnolia).
- `load_asset_clusters` MUST use `coll.all_objects` not `.objects` (weed_plant_02 nests in sub-collections → "0 placed").
- `fix_broken_image_materials()`: non-existent image → procedural green (plant keywords) or grey; catches sorrel/periwinkle/weed/rooibos + generic "Material" names.
- `weed_plant_02` = coarse broadleaf weed, NOT fine ornamental grass → looks like random houseplants; use 3daistudio-lavendel-OBJ drift or omit.
- `painted_wooden_bench` = WHITE-painted (blows out in dark/misty scene → force charcoal).
- `auto_upright` = heuristic (min-height=upright) — correct for pots/picnic, tipped the bistro-set over → apply only after visual confirm.
- Karesansui rake: deterministic per-vertex z-wave + 'rake' float-attr → Attribute node → ColorRamp (grooves dark). Displace-with-WOOD/RINGS was unreliable.
- Volumetric fog (Lelie): Principled Volume in a BOUNDED box (not whole ground — VRAM), density ~0.03 with height-falloff (MapRange on Generated-Z), anisotropy 0.45 (forward-scatter god-rays), low sun elev 6–9° behind. Density 0.011 invisible; 0.03 = MIR-painterly dew.
- Glass roughness 0.05 → 0.18 on all doors (kills blown-out white air/HDRI reflection triangle).
- `remove_in_cabin(prefix,x,y)`: scatter spills child-meshes into cabin volume → remove on world-bbox overlap, not center.

**QA-ronde 16 scenes (2026-06-13) — structural placement bugs**: paths to nowhere → always front-of-frame→door (`cl.place_along(names,p0,p1,z)`). Slab z-fighting → gap between + 1–3 cm above crossed plane. Planting ON path → check plant-XY vs path-bbox. 8K product-textures → black disc / OOM (`T_vl1iaf0lw_8K_B.png` flagstone, 8K epdm/douglas/hardhout → 'Malloc returns null', mesh renders PURE BLACK); use solid Base-Color for small stones; never >2–3 heavy renders at once (QA OOM'd at ~18–22 parallel processes). Cluster-donor magenta: `place_cluster` leaves original donor meshes in `Asset_*` collections (sorrel/periwinkle render magenta despite recolored copies) → `cl.force_base_color` per-object or purge donor collection. Props in wall/shadow → keep in front of back wall; weak warm fill-area for dark verandas. Floaters via dup_hierarchy → `cl.ground_to(name)` after each dup. Stale inspect-crops → verify with a FRESH render before touching an approved scene.
- New cabin_lib helpers: `ground_to`, `move_root_to`, `force_base_color`, `place_along`, `full_tree_donors`, `tree_rings_clustered(full_only)`, `volumetric_fog`, `fix_broken_image_materials`, `remove_in_cabin`, `auto_upright`, `keep_one_xy_cluster`, `audit`, `inspect_cams`. Diagnose: `scripts/audit_scene_deep.py`, `scripts/render_topdown.py` (workbench).

### C. Lavendel Zijwand reference inspiration (Lavendel Zijwand Reference Inspiration)
User-supplied 12 refs (2026-05-21). Signature Lavendel architectuur:
- **Two-tone walls**: BLACK (`kdi_potdeksel_zwart.jpg` or `kdi_rabat_fbz_zwart.jpg` in `blokhutwinkel-textures/8192/`) + CEDAR (`luxehouse-onbehandeld.jpg` on zijwand-interior + beams). Flat dak met natural douglas roof beam. Open zijwand-carport met cedar interior reveal (dark outside, light inside). Cedar structural pilars.
- Carport floor MUST be klinker/herringbone paving (grey/anthracite/cream), NIET grass. Furniture: wicker sofa set + coffee table (most premium) / 2 chairs + wood table / white design chairs. Lighting: pendant(s) warm bulb + ≥2 wandlampen; evening or day both work. Plant pots flanking entrance (white/black/grey ceramic) + lush plants. Backdrop: wooden fence (horizontal slats, most common) / hedge / mature trees for depth.
- Asset translations: black window frames → `pot_anthracite`; klinker → `paving_stones_64` polyhaven or `flagstone_floor` sketchfab; white gravel → `construction_gravel_vl0mfbllw_8k`; fence → `spruce_fence_gltf`; garden chairs → `outdoor_relax_chair_gltf`/`adirondack_chair_photogrammetry`; picnic bench → `picnic_table_low_poly_gltf`; pendants → `old_lantern_gltf`/`low_poly_garden_lamp`. MISSING at time: wicker sofa/rattan, wandlamp, lavender plant, cypress, yucca/dragon tree.
- Ref 11 = HERO target (highest level): animal lifestyle prop (dog, no face), decorative sculptures, gabion stone-basket planter, multiple warm lights, herringbone→lawn transition.

### D. Jasmijn Hygge Golden-Hour scene plan v2 (2026-06-10, Opus, build-ready) (Jasmijn Hygge Golden-Hour Scene Plan 2)
- **Cabin** `Jasmijn-300x250-300-zijwand`: dense module 300×250 (+X) + open overkapping 300 (−X), flat roof. Concept: Scandi late golden-hour hygge. Overkapping-opening faces +Y = camera.
- **Envelope (headless measured, cm)**: total bbox −321.3→+321.3 (642.6 w) × −145.4→+145.4 (290.8 d) × 0→234. Dense module x −3→+301, y −129→+125, floor +5, wall→207. Overkapping x −301→−3. Front wall plane y +125.5. Dak-overstek voorrand y +143 (drip-edge), bottom ~205 top ~230. Deur midden x+148 (73→224, w151), y 121.5→128.7, opening 5→195, glas 98→180. Floor-top z+5.
- **Materials (11)**: `basetexture-firstLayer-{wall,canopyWall,door,foundationBeam,poles,roofBeam,roofboard,roofPlate}`, `chrome`, `glass`, **`flatroof-71-board-mat`** (nr 71 — use THIS in loops, not 67/19/103). 151 meshes, 1 camera, 0 lights.
- **Deck (douglas)**: `Deck_Carport` x−301→−3 y−127→+123 top z+5; `Deck_Apron` x−309→+309 y+123→+470 top z+5 (closes on gevel y+125 — NO gap). `MAT_Deck`: `douglas.jpg` (8192) BOX proj, Mapping Object, Scale (0.4,7.14,1) → 14 cm planks along X; Voronoi DISTANCE_TO_EDGE (scale 7.14, randomness 0) seams (ColorRamp 0.0→0.06); plank-noise (scale 3.5, detail 10, ColorRamp 0.70→1.08 MULTIPLY); macro-noise (scale 1.2, fac 0.06); bump 1.0 dist 0.008; HSV val 1.03, roughness 0.55.
- **Tiles** `MAT_Ground_Tiles`: Color1 (0.40,0.40,0.42) Color2 (0.33,0.33,0.35), Mortar (0.06,0.06,0.065) Size 0.03, Brick W0.5/Row0.5, Mapping Object Scale (1.67,1.67,1) → 60 cm. Base `Ground_Base` plane 200×200 m at z−2, `MAT_Meadow` warm-tan.
- **Hedge (GN, real leaves)** — supersedes old AI-leaf-card method: rounded box per side (bevel, shade-smooth), Distribute Points on Faces (Poisson ~500/m²) → Instance sprig (from `shrub_03` ~1.2k verts) → Align Euler to Normal (outward waaier, no donor-sphere) → random Z + scale 0.8–1.3. `MAT_HedgeLeaf`: shrub textures + Subsurface 0.12 + HSV sat 0.68/val 0.76. Height 185 < wall 207 < dak 230. Hedge boxes: Back x−640→+640 y−205→−175 z0→185; West x−665→−635; East x+635→+665.
- **Beplanting**: Oudolf drifts (grass `grass_medium_02` alpha; sketchfab grasses ×0.01). Planter bak `Planter_Back` z0→28 with soil-fill (grasses root IN bak). Buxus bollen flank door at (x+90,y+170)+(x+206,y+170) Ø50–60 on deck z+5. Statement trees = **pines** `pine_tree_01_2k.blend` (full PBR): BackRight_1 (x+390,y−240,h600), BackRight_2 (x+470,y−300,h520), BackLeft (x−430,y−260,h540), all behind hedge y<−175. (Berk→den: no clean birch asset, den fits Scandi + on-disk.)
- **Lighting**: `Sun_Golden` SUN energy 4.5, color (1.0,0.78,0.55)≈3300 K, angle 2.5°, dir `normalize(−0.45,−0.78,−0.22)` (front-right +X+Y, elev ~14°) via `d.to_track_quat('-Z','Y')`. HDRI `qwantani_dusk_2_2k.hdr` strength 0.55 (alts venice_sunset / kiara_1_dawn). Fills (use_shadow=False): `Fill_Carport` AREA 300×200 energy 50 (1.0,0.86,0.72); `Fill_BackWall` AREA 180×130 energy 25. Glows: `Interior_Glow` POINT energy 22 (1.0,0.66,0.36) behind door; `Fire_Glow` POINT energy 18 (1.0,0.42,0.14); Lantern ×2 POINT energy 4; StringLights emission (1.0,0.72,0.40) strength ~30, bollen Ø3 spacing 25.
- **Camera** `Camera_Hero` lens 35 mm, sensor 36, pos (x−150,y+820,z158), target (x+30,y+30,z118), DOF on, focus ~7.5 m, f/4.0, shift_y +0.04, no tilt. Framing NDC: cabin x 0.18→0.80, dakrand y~0.72, deck-voorrand y~0.12. Lock via 960×540 diag-render before props.
- **Cabin materials (Scandi grijs-geolied)**: wall = `luxehouse-grijs-gedompeld.jpg` BOX scale(4,4,4) bump 0.4; canopyWall same +HSV val 1.08; roofboard/beam/foundation/poles = `douglas.jpg` BOX bump 0.4; door = `hardhout-deuren-ramen.jpg` UV; roofPlate = `staalpannen-antraciet.jpg`; flatroof-71 = `epdm.jpg`; glass transmission 1.0 IOR 1.45; chrome metallic 1.0 roughness 0.25. Daktrim/fascia NIET wijzigen (standing rule). After swap: `img.reload()` + force `img.pixels[0]`.
- **Render (Cycles GPU, RTX 3070)**: test 2560×1440 @50% (1280×720) 128 samp adaptive 0.01; hero 2560×1440 @100% **256 samples** (→512 if lounge noisy) adaptive 0.005 min 64; OpenImageDenoise RGB_ALBEDO_NORMAL prefilter ACCURATE; light paths max 8 diffuse 3 glossy 4 transmission 8, clamp_indirect 5.0, blur_glossy 1.0; `texture_limit_render='2048'` (8K→2K, VRAM-safe on 8 GB; OOM→'1024'), `use_persistent_data=False`; AgX look `AgX - Base Contrast` exposure 0.25 gamma 1.0; 16-bit PNG. RTX 3070 ≈ 45–90 sec.
- **Critical headless rules (Roosmarijn-verified)**: `scene.use_nodes=False` (compositor on → all-black, no error); `wm.save_as_mainfile` before headless (MCP changes live in RAM); absolute `-o` path; NEVER World Volume Scatter (→ exterior pitch-black in Cycles 5.1). CLI = `blender.exe -b <blend> --python render_final_clean.py -o <abs> -F PNG -f 1`.
- All assets on disk → ZERO token-generation needed (Replicate out of texture workflow).

### E. Cabin walkthrough animation video (Cabin Walkthrough Animation Video Production)
- Shots: drone orbit 6–12 s (Bezier Circle radius 12 @ z3.0, Follow Path + Track-To, curve height 2.5–4 m, 15–20° down look, NEVER 45–60° top-down "Zillow", lens 28–35 mm). Easing = Bezier Auto-Clamped on Evaluation Time (linear = amateur tell). Push-in 15→3 m/8 s. Dolly-zoom Hitchcock: dolly 15→3 m + zoom 50→10 mm, once/video MAX. Interior first-person Z=1.65 m lens 24–28 mm, Noise mod on Z-Location scale 15 strength 0.02 (2 cm), rotation X 0.5°. Wide truck 0.8 m/s.
- Camera shake: premium hero NEVER; lifestyle OK ≤0.5° (scale 8–12); Camera Shakify addon at 30–50%.
- FPS: 24 cinematic / 30 social. Cycles 128–256 samp + adaptive (0.005, min 64). EEVEE Next = 80% of social loops. Persistent Data ON (saves 10–30 s/frame).
- RTX 3070 render-time (720 f = 30 s @24fps, 1080p): Cycles OptiX 128+OIDN ~5–6 h; 256 ~9–10 h; EEVEE Next 64 ~25–35 min. Hybrid: EEVEE master + Cycles 3–5 s hero splice = 80% quality/10% time.
- Animated sun: Sun Position addon, keyframe Time; sun temp 4500K→2700K over 30 s via Blackbody. Motion blur: shutter 0.5 (180°), samples 8 (16 for fast rotation), +30% time, only when camera moves.
- Audio: Pixabay royalty-free instrumental, 60–90 BPM, acoustic guitar + soft synth, avoid upbeat ukulele; YT Audio Library 2nd; DaVinci duck −8 dB.
- Export: TikTok/Reels 1080×1920 H.264 High@4.2 10–15 Mbps 30fps; YouTube 1920×1080 8–12 Mbps 24/30; master 3840×2160 ProRes 422 LT/DNxHR SQ ~120 Mbps; audio AAC 192 kbps 48 kHz. Keep <250 MB. Render master 4K 16:9, crop 9:16 from center (frame cabin in center 60%).
- Grading: lift +0.02, highlights −0.05, midtone temp −200K, highlights +200K, saturation 0.92, 35 mm grain 25%.
- Animation pitfalls: per-frame OIDN = grass shimmer → OIDN Temporal (render Vector+Position, `oidnDenoise --quality high --temporal`, kills ~90% flicker). Fireflies → clamp Indirect 5.0 (Direct 0). Shimmering volumetrics → uncheck Use Animated Seed. Glossy flicker → glossy 4, samples 256+. GN scatter pop-in → bake GN to mesh. Edit rhythm 30 s = 4–5 shots × 6–7 s (not 12 × 2.5 s).

### F. WebGL + AR configurator (WebGL + AR Cabin Configurator)
- Pipeline: Blender → glTF 2.0 .glb (Draco) → `gltf-transform` → Cloudflare R2. Draco 60–90% reduction (20 MB→3–5 MB), decoder ~200 KB self-host. KTX2/Basis: UASTC for normals, ETC1S for albedo/roughness/AO/emission. Polycount <300K tris/cabin, hero 500K. File targets: <8 MB glb WebGL, <15 MB usdz AR (Apple sweet-spot 4–8 MB, ceiling ~25 MB, ≤100K polys, textures ≤2048²). Lightmaps only on default static hero (1024² AO+GI second UV; skip for style switcher).
- Stack: three ^0.168, @react-three/fiber ^8.17, drei ^9.114, rapier, zustand ^4.5, leva ^0.9. `<Environment>` 1K equirect HDR (~200–400 KB). Tone: Blender AgX + Three ACESFilmic + toneMappingExposure 0.85 (close). `<ContactShadows>` for catalog, 1 directionalLight PCFSoft for hero only. OrbitControls minPolar π/6 maxPolar π/2.1, enablePan false, auto-rotate 0.5 rad/s idle 8s. State = Zustand (NOT Context — re-renders 3D subtree). Style switch = reassign `mesh.material` from library (~30 ms). Options = named nodes `opt_porch` toggle `mesh.visible`. Mobile dpr [1,1.5].
- AR = `<model-viewer>` src glb + ios-src usdz, `ar-modes="webxr scene-viewer quick-look"`, `ar-scale="fixed"` (users can't rescale — critical for true 4×3 m). Pre-convert glb→usdz via Apple Reality Converter / usd_from_gltf (don't trust auto). Export meters scale 1.0, test with tape measure day 1.
- Perf (mobile): FCP <1.8 s (SSR static hero), LCP <2.5 s 4G, TTI <3 s, cold start ~150 KB gz, glb load <2 s, 60 desktop/30+ mobile FPS, <100 draw calls.
- SSR: Django REST + React/Vite, hero PNG (1920×1080 WebP) as LCP, `<button>Open 3D configurator</button>` mounts React island lazy R3F. Pricing: POST `/api/quote/` debounce 250 ms, show `prijs vanaf €X incl. 21% BTW`, lead POST `/api/leads/` with `toDataURL('image/webp',0.7)`. CDN R2 hashed names Cache-Control immutable; Brotli the JS bundle not glb. WebGL2 ~97% support; WebXR = Chrome Android 79+ only, iOS = AR Quick Look; 3% fallback = 360° turntable (36 frames × 30°).
- Study: **Lugarde 3D Configurator + AR** (Dutch, first in NL/EU for cabin AR, `lugarde-configurator.nl`), Tuindeco, Tuinhuizenspecialist, IKEA Place (98% auto-scale, returns −30%), Wayfair, WaWa Sensei R3F tutorials.
- Cost ~€1–5/month recurring (R2 ~5 GB, existing VPS). MVP 1 cabin × 2 styles = 5–6 h; then batch 32 × 5 in week 2.

### G. Marketing strategy B2B (Marketing Strategies B2B Dutch Cabin Sellers)
- **Competitors (2026 audit)**: Lugarde = only serious threat (authentic lifestyle staging, owns "premium maker"). Pineca/Tuindeco = studio cutout/white wall (Ikea-flat). Blokhutwinkel base = catalog elevations on grass + 360° rotators. Gap: 7/8 use elevation on flat grass, 2/8 any interior, 0/8 persona-staging, 1/8 (Lugarde) consistent atmosphere, 0/8 AVIF, 0/8 seasonal, 0/8 real-time configurator. Moat = ship all → visual reference 2–3 years.
- **Personas**: A Hybrid worker 35–50, €70–120k, 300×200/300×300 + insulation ("Werk aan huis, niet op huis"). B Empty-nester wellness 50–65, 400×300/500×300 + sauna/zithoek ("De kinderen uit, jouw plek terug"). C Mantelzorgwoning 40–65, 500×400/600×400 + bathroom/kitchen/bed ("Dichtbij maar privé"). D Extra slaapkamer 25–40, 200×200/250×250 ("Logé met privacy").
- **Shot ratio per cabin/style** (33×5 = 165 scenes): 1 hero (3/4 eye-level golden hour) + 1–2 detail + 1–2 interior + 1 wide + 1+ seasonal ≈ 5–7 → ~1000 final renders at rollout.
- **EU AI Act (2 Aug 2026)**: AI-gen images need visible disclosure (penalty up to 3% EU turnover). Cycles renders NOT AI-generated (deterministic light transport) → badge "100% renders. Geen AI." NO Magnific/Topaz upscale, NO SD inpaint, NO ChatGPT texture-clean on marketing renders; Photoshop color/exposure/sharpen OK. Safer phrasing "Geen synthetische afbeeldingen. 3D-renders gemaakt in Blender." (confirm with legal — Article 50; NL ACM / UK CMA interpret separately).
- **Web specs**: hero 2000×1125 AVIF q55 <200 KB / WebP q80 <400 KB; thumbs 800×450; detail 1600×900 or 1200×1200 AVIF q60; lightbox 3000×1688 q70; print 300 dpi CMYK 3 mm bleed, A4 2480×3508, TIFF/PDF-X-1a (render 4K → downsample). Tooling `sharp`/`pillow-avif-plugin`.
- **Premium cues**: atmospheric haze, golden hour/moody overcast (not noon flat), persona prop, background depth, material micro-detail, 3/4 angle, plants ≥3 sizes/3 species, real Dutch context (klinker waalformaat, schutting). AVOID: flat noon, white cyclorama, bare lawn, identical plant pattern, drone overhead, symmetric elevation, no human-scale anchor.
- **Distribution**: product hero 16:9; Pinterest 2:3 no-logo plant-heavy; IG feed 1:1 detail; reel/TikTok 9:16 EEVEE turntable; YouTube 16:9 1080p 10-s flythrough; newsletter 3:1; brochure A4+4; fair banner 2×1 m (8K source).
- **Budget/ROI**: ~$10–15/render (mostly labor, 50 min build+render+post; compute ~$0.05 RTX 3070). 1000 renders ~$10k vs €200k–500k outsource = 95% savings. Payback <50 sales.

### H. SEO + accessibility product pages (SEO + Accessibility Archviz Product Pages)
- Schema.org Product JSON-LD per page (name, description, image[], brand, sku/mpn, gtin13, offers with price BTW-incl, priceValidUntil, shippingDetails, hasMerchantReturnPolicy 14 days FreeReturn, aggregateRating, additionalProperty). OG type=product + Twitter summary_large_image; render dedicated 1200×630 WebP social variant (AVIF spotty in OG scrapers).
- Alt text 100–150 chars from manifest, never "Foto van…", decorative → `alt=""`; auto-generate 165, manually review 33 heroes. Title <60, meta <155; each of 5 styles = unique canonical URL. URL `/tuinhuis/{cabin}-{w}x{d}cm/{style}/`, self-canonical, 301 via Django contrib.redirects (never 302/JS), no `?style=` query. Hreflang nl-NL/nl-BE/de-DE + x-default, reciprocal required.
- **Core Web Vitals** (p75 mobile 4G): LCP <2.5 s (hero AVIF <200 KB, fetchpriority high, preload); CLS <0.1 (aspect-ratio CSS every img); INP <200 ms (debounce configurator); FCP <1.8 s (critical CSS <14 KB); TTFB <800 ms (Django+Redis+Cloudflare edge). `<picture>` AVIF/WebP/JPEG srcset; below-fold loading lazy. CDN Cloudflare Images/imgproxy on-the-fly from single PNG.
- **WCAG 2.2 AA**: contrast 4.5:1 body / 3:1 large & UI; 44×44 (2.2 min 24×24) targets use 48; new 2.2 SC — 2.4.11 focus not obscured, 3.3.7 redundant entry, 3.3.8 accessible auth. Configurator: style switcher role=radiogroup, swatches `<button>` label "Zwart cedar — RAL 9005" never color-only, 3D viewer + "Bekijk als foto's" fallback, aria-live polite. Cookie banner two equal buttons no dark patterns (AP NL). Forms autocomplete tokens, errors role=alert. PDF via WeasyPrint/Prince PDF/UA, validate PAC 2024.
- Testing: Google Rich Results + Schema Validator in Lighthouse CI (assert LCP<2.5, CLS<0.1, perf>85 per PR). Monitoring: Cloudflare RUM, WebPageTest NL/BE weekly, Sentry INP, CrUX. A/B GrowthBook, min 1000 sessions/variant. NL-SEO: Merchant Center BTW-incl feed, Beslist/Kieskeurig/Tweakers, `€ incl. 21% BTW` prominent (Prijzenwet), vergunningsvrij landing pages top-20 gemeenten, .nl ccTLD primary.

### I. Garden-style research + Blender production reference (Research - Blender+Blokhutten aankleding; Research - Diepe Blender Garden Cabin Reference; Research - Tuinstijlen 13 stijlen)
- **MCP workflow**: blender-mcp v1.5.5 (ahujasid) — stable for scene-composition, not parametric CAD. No native import → `execute_blender_code` + `bpy.ops.import_scene.fbx/obj/gltf` or `libraries.load` for .blend. Iterate: `get_viewport_screenshot` → user approval. `DISABLE_TELEMETRY=true` env var (else prompts/code/screenshots go to Ahuja). First-command-fail known → just re-run.
- **GLB import (blokhutwinkel files)**: come in cm → always 0.01× scale + camera weg (feedback_blokhutwinkel_glb_scale).
- **Render defaults**: Cycles required for finals (photoreal HDRI), EEVEE Next for previews; 2560×1440, 256 samples + OIDN. M4 MacBook ~5–10 min/frame @256; batch 8 ~60–90 min. (RTX 3070 numbers elsewhere much faster.)
- **Scattering**: GScatter (free, GN-based, density/scale/rotation/wind, viewport-proxies, camera-culling) = first stop; Geo-Scatter full (paid, 170+ biomes) only if insufficient. GN pattern = distribute-points-on-faces + weight-paint density-mask + rotation/scale jitter + slope-mask (Blender 3.0+). Free 170+ HQ Plant Library (BD3D Gumroad).
- **Trees/wind**: Sapling Tree Gen (built-in, free, parametric); The Grove 3D (paid, best photoreal + wind); Modular Tree (free, node/L-system). Wind without sim = GN noise-texture on object position.
- **Lighting**: Sun Position addon (built-in) syncs sun with HDRI rotation. Polyhaven cabin/garden HDRIs: `solitude` (overcast field), `tiergarten` (autumn park overcast), `qwantani_dusk_2`, `kloofendal_43d_clear_puresky`, `studio_garden`, `symmetrical_garden`, `gem_2` (4–22K CC0). Mix-shader trick (HDRMaps): two env-textures mixed via Light-Path Is-Camera-Ray (nice background + different lighting HDRI). **Color temps**: golden hour 3200–3500K, midday 5600K, overcast 7000K, blue hour 9000K.
- **Materials**: procedural wood = 10-node Voronoi+Noise+ColorRamp (Samuel Sullins). Shou Sugi Ban = 3D-scanned charred wood (textures.com), cedar/larch traditional, pine cheaper. Polyhaven wood: `weathered_planks`, `rough_wood`, `pine_bark`, `bark_brown_02`. Free PBR Scorched Wood Charcoal 2K (freepbr.com).
- **Camera**: 24–35 mm wide, 35–55 mm hero, avoid <30 mm (distortion). Two-point perspective via Shift-Y (verticals stay vertical). Eye-level doesn't sell — low viewpoint + slight upward shift (heroic) or knee-height (human).
- **Anti-uncanny-valley**: "true photorealism lies in the mistakes" (perfect = fake). Wear-on-edges (paint chips corners first), soft creases (cushions/curtains imperfect), imperfect plants (broken leaves, uneven growth, non-uniform scatter density).
- **Asset libraries**: Free = Polyhaven CC0, GScatter, BlenderKit free, Sketchfab CC0 (Thomas Flynn `sketchfab.com/nebulousflynn/collections`), Free PBR, Ambientcg. Paid = Botaniq Lite (28)/Full (66); Quixel Megascans now via Fab.com (not free outside Unreal since 2025). Sketchfab commercial → filter CC0/CC-BY only (CC BY-NC = no-go). Hyper3D Rodin / Hunyuan3D = AI last-resort for missing props.
- **Atmosphere**: Volume Forge addon (local volumetric without filling scene). Mist Pass built-in. Three fog domains: ground-mist + horizon-haze + distance-atmosphere.
- **Post**: Final LUT addon (imports .cube in compositor); Colorist Pro (paid). Marketing look = warm shadows + slight desat midtones + highlight bump.
- **13 garden styles** (Garden Style Inspiration Catalog Extended is the master catalog): Modern Minimalist, English Cottage, Scandinavian, Forest/Wilderness, Terras+HotTub, Japanese Zen, Boerderij, Golden-Hour overlay, Winter/Sneeuw + Mediterranean, Tropical/Bali, Coastal/Duinen, Industrial/Urban Jungle, Prairie (Oudolf), French Provence, Alpine.
  - **Oudolf 70/30**: 70% structure (grasses + late-bloomers) + 30% filler, plant in drifts not dots, leave dead stems in winter.
  - Mediterranean: gravel-mulch 5 cm under plants (anti-fungus + look); olijf/lavendel/rozemarijn/cypres.
  - Karesansui: odd rock counts (3-5-7), never symmetric; moss=land, raked gravel=water.
  - Cottage plant heights (3D scale): hollyhock 2.5 m, delphinium 2 m, lavendel 0.6 m.
  - NL-tropical: Trachycarpus fortunei + Musa basjoo (winterhard, Bali look without climate-illogic). Coastal NL: helmgras (Ammophila arenaria) + duindoorn (Hippophae rhamnoides, orange berries). Alpine bloom July–Aug only.
  - **Style-product matchmaker**: sauna-chalet → Scandi/Forest/Alpine; tuinkantoor → Modern/Industrial/Prairie; klassieke blokhut → Cottage/Boerderij/Provence; kapschuur → Boerderij; pipowagen → Bos; paviljoen → Cottage/Zen; veranda → Terras+Lounge.
- **Open questions (unresolved in research)**: full Polyhaven-HDRI-per-style mapping, complete seasonal-variant sets, camera fly-through (wind covered), "blokhutwinkel marketing LUT" (needs brand-design pass), AI-upscale post-Blender (Topaz/Magnific — undocumented), incoming file format/scale/brand-rules for real cabin files.


---

<a id="13"></a>
# §13. 3D-print blokhutten (Blender to FDM)

Two competing routes exist for turning Blokhutwinkel cabins into FDM prints. **Current/preferred (as of 25 jun 2026): the PARAMETRIC route** (Blokhut Parametric Print Generator) — it supersedes the voxel route for crisp rabat and large/open models. The **voxel route** (Blokhut Print Pipeline / HANDOFF) remains valid only for small/dense models where you want the real GLB texture 1:1.

### Route decision (voxel vs parametric)
| | Voxel (`build_blokhut.py`) | Parametric (`batch_blokhutten.py`) |
|---|---|---|
| Rabat planklijnen | rounded/"mush" | knife-sharp (zaagtand-profiel) |
| Hek/spijlen | "worstjes" | scherpe latten |
| Memory | thrashes on large/open | light (~2-4 GB) |
| Source needed | tekentool-GLB required | maten only (autonomous) |
| Faces | ~40-115k | ~0.5-3k (small) |
| Watertight | yes (1 body) | usually multiple overlapping bodies (slicer fuses) |
- **Don't voxel** for crisp rabat or large/open models. **Do voxel** only for exact GLB texture on small/dense models. (Parametric Print Generator)
- The 17 jun (Mac) Print Pipeline note originally REJECTED full parametric rebuild as "fragile"; the PC (25 jun) proved it works and is superior — parametric now current. (both notes)

### Hardware & setup (PC)
- Ryzen 7 5800 / RTX 3070 / 32 GB. Blender **5.1.1** at `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`. (Parametric Print Generator; HANDOFF)
- System-Python is machine-wide (`C:\Python312`) → use `pip install --user` (else Access-denied). Libs: trimesh, numpy, scikit-image, matplotlib, **rtree** (needed for printcheck ray-cast). (Parametric Print Generator; HANDOFF lists trimesh/numpy/scikit-image/matplotlib)
- **PATH GOTCHA:** live iCloud is `C:\Users\beike\Desktop\Icloud\iCloudDrive\` (has current `Vault\Claude\`+`Documents\`). Home-root `C:\Users\beike\iCloudDrive\` is a stale/partial mount. Output STLs → `…\Vault\Claude\blokhut-print\output\` (syncs to Mac). (Parametric Print Generator; contradicts MEMORY's Obsidian-vault path — use Desktop\Icloud mount)
- Work dir: `C:\Users\beike\blokhut-print\`. (both)

### Machine split (PC ↔ Mac)
- **PC** = heavy compute: Blender voxel-remesh / parametric build → `*_printready.stl` (no Bambu, no printer needed). **Mac** = slice+print in Bambu Studio (installed, printer connected). (HANDOFF)
- Data-flow: tekentool-GLB → (PC) pipeline → `*_printready.stl` (~2-4 MB) → `Documents\Vault\Claude\blokhut-print\output\` → iCloud → Mac → Bambu Studio. (HANDOFF)
- NOTE (Parametric Print Generator, 25 jun): PC now slices+prints itself too (Bambu Studio + P2S, per MEMORY) — supersedes Mac-only-print in older HANDOFF.

### Scripts (`C:\Users\beike\blokhut-print\`)
- **Parametric:** `parametric_cabin.py`, `parametric_dallas.py`, `batch_blokhutten.py`, `printcheck.py`, `batch_check.py`, `master_index.py`, `recv_glb.py`, `extract_shell.py`, `dump_groups.py`. (Parametric Print Generator)
- **Voxel:** `inspect_glb.py` (JSON-chunk only, structure/bbox), `analyze_parts.py` (locates door/floor/roof world-bbox), `glb_extract.py` (POSITION+indices only, ignores 8K textures → shell-STL), `build_blokhut.py` (orient→solidify→voxel-union→decimate→clean door→roof flat→flip→export; PER-MODEL config on top), `render_clay.py` (grazing/scheerlicht for rabat relief). (Print Pipeline; HANDOFF)

### GLB export from tekentool (browser, no export button)
- Tekentool `tekentool-v2.blokhutwinkel.nl`, Y-up, cm units. 3D view is a **same-origin iframe** `/3d?ui=hidden` on **Babylon.js 4.2.2** with `BABYLON.GLTF2Export`. (Print Pipeline; HANDOFF)
- Console (normal Chrome, Mac): find iframe with `.contentWindow.BABYLON`, `scene = B.Engine.LastCreatedScene`, `await B.GLTF2Export.GLBAsync(scene,'blokhut',{shouldExportNode:n=>!EXCLUDE.test(n.name||'')})` → blob → `<a download>` → ~85 MB in Downloads (textures included, pipeline ignores them). Top-level await fails in console → use async-IIFE; Babylon is on iframe not window. (Print Pipeline; HANDOFF)
- EXCLUDE regex (HANDOFF): `/backgroundsphere|groundplane|manmesh|balustrade|buitenbar|cube|l-shape|shutter|fitting|doorhandle|scharnier|^a$|^w$|^wv|^[0-9]/i` → keeps ~252 cabin meshes (Print Pipeline says ~252). Inspect `scene.meshes.map(m=>m.name)` if unsure.
- **Under browser-automation (Claude-in-Chrome / CDP) downloads do NOT work** — the `<a download>` blob never lands on disk. Fixes (Parametric Print Generator):
  - Only enter 3D-mode after picking system+template (that's when the iframe loads).
  - Use REAL mouse input (computer tool / CDP Input); synthetic DOM clicks don't reach Angular.
  - Scene handle: `B.EngineStore.Instances[0].scenes[0]` (`Engine.LastCreatedScene` can be null under automation).
  - POST the GLB blob to a local mini-server `recv_glb.py` on `127.0.0.1:8799` (handles CORS + Private-Network preflight); `fetch(...,{method:'POST',body:blob})` from the page (https→127.0.0.1 allowed by Chrome).
  - CDP eval ~45s timeout; 85 MB serialize can exceed it → kick export non-blocking + poll status.

### Voxel route: hybrid core + gotchas (Print Pipeline; HANDOFF)
- **HYBRID = chosen:** voxel-remesh walls+roof (melts plank-soup into 1 hollow solid, keeps rabat planklijnen) + a clean parametric door from blocks added AFTER voxel-union (sharp) + roof cut flat. Full CadQuery rebuild rejected (fragile) in this note.
- **OOM:** `trimesh.load()` on these GLBs decodes 47× 8K textures (~12 GB) → crash → use own geometry-only extractor.
- **Voxel 0.2 OOMs** on 16 GB with Bambu open → use **0.30** on Mac; PC can go **0.2** (finer=sharper, slower). SHARP-remesh is faster but turned rabat into "stipjes" → do NOT use.
- Voxel time scales `(model ÷ voxel)³`, single-threaded: 150 mm @ 0.3 = 500³ = heavy; 180 mm @ 0.25 = 720³ = **20 min** on Mac. Mac rule: TARGET ≤ 150 mm + voxel 0.3.
- **Y-up → Z-up:** rotate +90° X.
- **Solidify:** `use_even_offset=False` (else 78 m spikes); first weld verts + dissolve degenerate faces.
- **Omit floor** → hollow shell, open bottom (else voxel fills solid massief).
- **Door:** GLB door → blubber in voxel → drop it (materials `glass/door/window/translucent/frosted/chrome/mat1`, nodes `inset/double/dd/doorhandle/scharnier/handle/hinge`) and rebuild parametric AFTER voxel. Match window sizes to real product photo: **DD04 door = double, window top ~30%, glaslat-rand, closed lower panel ~53-55%** (Print Pipeline says ~53%, HANDOFF ~55%). Not "2 random holes".
- **Posts/palen:** add NONE new; `glb_extract` writes real post positions (`pole-N`/`wallcorner`, excludes scaffold/foundation) to `<shell>.poles.json`; build only thickens those (+3 cm / thicken=3.0).
- **Boolean solver (Blender 5.1)** = FLOAT / EXACT / MANIFOLD. Use **MANIFOLD** (clean+light; FLOAT leaves splinters, EXACT heavy). Cutters must overlap the wall (not coplanar).
- **Roof flat:** GLB fascia sticks ~0.5 mm above roof deck → ruins first layer when printed upside-down → boolean-cut everything above `ROOF_DECK_CM`. (Non-flat roof: don't flip, no cut, maybe support.)
- **Junk:** tekentool drops loose "FF-DS" panels at origin (~14 mm off building) → keep LARGEST body: `big=max(m.split(only_watertight=False),key=lambda b:len(b.faces))`. If the BUILDING splits into 2 bodies (not just junk) → thicker wall (raise `thick`) or coarser voxel to bridge seams.
- **Decimate:** planar DISSOLVE 4° after cuts → 174 MB→7 MB, no visible loss.
- Build args after `--`: `IN_shell.stl OUT_base TARGET_MM VOXEL_MM PRESET`; e.g. `... 130 0.30 naam`. Pipeline: orient→solidify→voxel-union→decimate→clean door→thicken existing posts→roof flat→flip→writes `.stl`+`.blend`+`_printready.stl`.
- PRESETS include `magnolia` (flat-roof DD04, printed+approved) and `newyork` (cabin + side-overkapping). Preset dict fields: `ROOF_DECK_CM`, `WALL_FRONT_CM`, `thick=1.6`, `DOOR=dict(x=(x0,x1), top, stile=12, toprail=20, win_h=55, midrail=10, mullion=6, bead=4)` (mullion=0 = single door), `POSTS=dict(enable=True, thicken=3.0)`.
- Render: factory-empty `.blend` has no world → create one; use grazing light for relief.

### Parametric techniques (Parametric Print Generator)
- **Rabat = continuous zaagtand-profiel per wall:** bottom proud P=1 mm → top flush T=2 mm, exposure E=6 mm (E=5 fine, E=8 coarse). One solid per wall, NOT loose plank-boxes (else "largest body" fragments).
- **Door: boolean DIFFERENCE FAILS** on merged mesh → use PLANK-SKIP: build front wall in segments around the opening + separate door boxes (frame, stiles, rails, mullion, recessed lower panels + inset), UNION only, solver `EXACT`. Double door → leave 2 windows open on top.
- **Hoeklatten** (vertical 6 mm proud) + **boeideel** (fascia hanging ~7 mm down) + **gevel-driehoeken** (`gable_fill`) close the cabin under a sloped roof.
- **Roof skeleton** (spanten dakvoet→nok + nokgording + muurplaten) CONNECTS roof to frame (else roof is a separate body) and shows construction in open carport.
- Sloped roof doesn't balance on its ridge → **print upright + support**. Flat roof → roof-on-bed, no support.
- **Multiple overlapping bodies is OK** — Bambu fuses overlapping solids at slice; don't chase 1 watertight body when parts overlap.
- **Camera:** door is on -y wall; angled corner-cam hides it → render straight-on. Open carport bottom is dark → add fill light to see the skeleton.
- **Detail research first:** `dump_groups.py` for mesh groups + per-instance bbox + clay-render BEFORE recreating. Found `wallcorner` (hoeklatten), `fasciaboard` (boeideel 19 cm), `double-door-inset` (door panels). NB `pole-N-scaffold` = small connector plates, NOT the big knieschoren.

### Memory / RAM lessons (Parametric Print Generator)
- Voxel TARGET too high → Blender swaps to pagefile → hours of "thrashing" with no progress; a thrashing build NEVER sends a completion message. Monitor blender commit-mem actively; intervene before RAM limit.
- Beike's archviz render-batch (`render_final.py`, separate project) often runs parallel, ~20 GB — wait for it before a heavy build (RAM contention = both thrash). Parametric builds are light enough to run alongside.
- Before killing `blender`: check process command-lines (`Get-CimInstance Win32_Process`) — killed another pipeline's render jobs by accident once. A monitor summing ALL blender processes gives misleading numbers with multiple pipelines.

### Print settings & validation
- **Bambu P2S · PLA Basic · 0.20 mm · 0% infill · brim 4 mm · wall loops 4-5.** (Parametric Print Generator; Print Pipeline; HANDOFF all agree)
- Flat roof → roof-on-bed (flip 180° X), NO support. Zadel/lessenaar → upright + support. (Parametric Print Generator)
- ~98 mm model ≈ ~75 g / ~3.5-4 h (Print Pipeline).
- **Bed-fit:** P2S bed ≈ 256 mm; keep ≤ ~248 mm. Carport/overkapping overstek OH=14 → footprint width ≤ ~220 cm else > bed. (Parametric Print Generator) — Bambu P2S build volume 256×256×256 mm (FDM Design Rules).
- **Validation:** `printcheck.py` (watertight; floaters via bbox-overlap of loose bodies; wall-thickness via rtree ray-cast; overhang%). Batch `batch_check.py` (+bed-fit) → `INDEX.md`; `master_index.py` → `MASTER_INDEX.md` across batches. (Parametric Print Generator)

### Batch generator (Parametric Print Generator)
- `batch_blokhutten.py` = one `build(cfg)` + config-dicts. Axes in print-mm: **X=breedte, Y=diepte, Z=hoogte**. Vary `kind` (cabin/carport/overkapping) × `roof` (flat/saddle/mono) × `door` (none/single/double) × `window` × `plank` (5/6/8 mm) × size. Per-config `try/except` so one failure doesn't kill batch; writes `_batch_meta.json`; `_batch_meta.json`. **48 models generated (31 cabins, 7 carports, 10 overkappingen)** in `batch/`..`batch4/`. Extend = add config + run.

---
## FDM design rules (general — Bambu P2S, 0.4 mm nozzle, PLA)

### Wall thickness (FDM Design Rules)
| Element | Min | Recommended |
|---|---|---|
| Vertical wall | 1.2 mm (3× 0.4 perim) | 2.0 mm |
| Horizontal slab | 0.8 mm (4 layers @0.2) | 1.2 mm |
| Reinforcing rib | 1.6 mm | 2.4 mm |
Below min: slicer drops to single perimeter or skips.

### Overhangs / bridges / edges (FDM Design Rules)
- Overhang ≤45° = no support; 45-60° = rough; >60° = needs support.
- Bridges ≤20 mm print fine; >20 mm sag.
- **Bottom edges: CHAMFER not fillet** (fillets need support). 0.4 mm × 45° chamfer = fillet look, no penalty.

### Orientation / tolerances / adhesion (FDM Design Rules)
- Largest flat face on bed; tall narrow parts on side; threads vertical.
- XY ±0.1 mm typical; Z better than XY but layer-line texture. Holes print 0.2 mm undersized, ream after.
- First layer 0.2 mm min (0.24 safer); brim/skirt for parts <30 mm² contact; tall narrow → `extend_stl_base` (bambu-printer-mcp).
- Bambu P2S: 256³ mm, 0.4 mm nozzle stock (0.2/0.6 available), layer heights 0.08/0.12/0.16/0.20/0.24/0.28, AMS 5 spool slots (elsewhere "4-slot"), auto bed leveling.

### Veranda template specifics (FDM Design Rules)
- Solid parts NOT loose boxjes; brace angle (schorenhoek) must match real construction; wandpanelen = horizontal grooves = plankenpatroon; Frameportalen = palen+balk+Y-schoren+gordingen+voetplaten as one solid.

---
## Joints & connectors (veranda modular research)

### PLA vs PETG (PLA vs PETG for Connectors)
- PLA very brittle, snaps within ~10 flex cycles; PETG flexes thousands. PLA good for magnet-embed, dovetail, static pin, heat-set. PLA ❌ for snap-fit / living hinge / print-in-place hinge. PETG softens 80°C vs PLA 60°C.
- Hybrid: all structural/static modules PLA; **hinged door = PETG** (needs to swing thousands of times); +~€5/spool; small PETG spool = hundreds of doors. AMS 4-slot → PLA+PETG simultaneously.

### Joint clearances — PLA, 0.4 mm nozzle, well-calibrated (FDM Joint Type Catalog; veranda research)
| Fit | Gap |
|---|---|
| Press fit (hammered) | -0.05 to -0.15 mm |
| Snug friction (hand) | 0.20 mm |
| Sliding (smooth) | 0.40 mm (1× extrusion) |
| Free-running (loose) | 0.80 mm (2× extrusion) |
| Magnet slot (6×2 mm magnet) | 6.3 × 2.3 mm |
- Rule of thumb: start 0.25 mm, adjust ±0.05 from test. Print 5-step ladder 0.15/0.20/0.25/0.30/0.35 mm.
- **Calibrated value (MEMORY, 23 apr):** sliding-fit dovetail gap = **0.15 mm** on P2S + PLA Basic + 0.16 mm layer — this is the measured real value, tighter than the generic 0.25 mm start.

### Why the Apr-21 pinnetjes-en-riggeltjes failed (FDM Joint Type Catalog; veranda research)
- Pins = thin cylinders (1-2 perimeters) snap under side load (PLA brittle); riggeltjes (thin tabs) printed vertically = layer-line fracture; both needed <0.1 mm clearance but real printer drift is 0.15-0.20 mm → miss-fit/jam; no slop-tolerant fallback.

### Print orientation for joint strength (Print Orientation)
- Rule: print joints HORIZONTALLY so filament runs ALONG the joint length (layer bond only 50-70% of inline strength). Force perpendicular to layers = separation.
- Per part: Frameportaal flat (palen horizontal); cassette/zijwand flat, dovetail along long edge; boeideel flat, long side ↔ X; dakpaneel deck-up (bevels down); pin/dovetail-male features horizontal along part.
- Slicer for load-bearing features: walls ≥3, top/bottom ≥4, infill ≥40% gyroid (100% for pins), layer height 0.16 mm for joint detail.

### Connector strategy — decision
- **CURRENT / user choice = PRINT-ONLY assembly** (no magnets/screws/heat-set inserts). Reason: simpler BOM, no polarity, no pause-at-layer, one filament spool = infinite verandas; assumes 5-10 (dis)assemblies not thousands → friction+gravity enough. (veranda research; MEMORY "no magnets") — **supersedes** the magnet recommendation in Magnet-Embedded note.
- Four print-only mechanisms: (1) **Dovetail rail sliding** — 1-2° taper, 0.25 mm gap, slide from top, taper+gravity lock; (2) **Tongue-and-groove** — flat tongue 4-6 mm, 0.3 mm gap; (3) **Drop-pin** — loose 4-5 mm Ø × 15-20 mm cylinder through aligned holes (lock only); (4) **Registration pins integral** — 3-5 mm Ø, 0.3 mm clearance, positioning only.
- Per-joint (print-only): Frameportaal↔Achtercassette/Zijwand = vertical dovetail 8 mm wide × 4 mm deep, 1° taper, 0.25 mm gap; Frameportaal↔Boeideel = horizontal tongue 5×3 mm, 0.3 mm gap; Portalen↔Dakpaneel = 4× registration pins 5 mm Ø × 8 mm, 0.3 mm clearance; optional dak-lock = drop-pin 4 mm Ø × 15 mm; Wand↔raam/deur-insert = dovetail rail rondom 4 mm wide × 2 mm deep, 1° taper; hinged door = print-in-place PETG hinge pin Ø2 mm in slot Ø2.4 mm.
- **Rib-in-groef (MEMORY, validated 30 apr):** vertical rib 3×3 mm × 60% post height instead of cylindrical pins.

### Magnets (ALTERNATIVE only — kept for future projects) (Magnet-Embedded)
- Neodymium N42 (N52 only if needed). Sizing: <50 g → 2× 6×2 mm (~1 kg); 50-200 g → 4× 8×3 mm (~3-4 kg); 200-500 g → 4× 10×3 mm (~6-8 kg).
- Slot for 6×2 mm: dia 6.3 mm, depth 2.3 mm, wall around ≥1.2 mm, cap 0.4-0.6 mm (2-3 layers). Pause-at-layer: e.g. layer 18 = Z 3.6 mm @0.2 layer; insert at pause, resume caps it.
- Veranda BOM ~32 magnets (€3-6 AliExpress / €15-25 hobby store), +4-5 min pause-time.

### Modular openings / inserts (Modular Architectural Print System; veranda research)
- Standardize 2-3 opening sizes: klein 60×80 mm (raam), medium 80×120 mm (raam-groot), groot 90×180 mm (deur). Inserts reusable across all templates of that size.
- Insert library: `window_60x80_clear`/`_pause`, `window_80x120_4pane`, `door_90x180_fixed`, `door_90x180_hinged` (PETG), `blank_60x80`, `display_60x80` (Event-Branding logo). "Glas": clear PETG/TPU sandwich, or pause-at-layer transparent film. Hinge-pin horizontal for strength; hero-display only (print time).

---
## Meta-workflow & tooling (research notes)

### Manifold validation (Manifold Mesh Validation)
- Printable solid must be closed manifold: each edge shared by exactly 2 faces, no self-intersections, consistent normals. Failure modes: open edge (infill leaks), non-manifold edge 3+ faces (wrong wall count), self-intersection (missing layers), flipped normals (inside-out), zero-thickness shell (skipped).
- Libs: `manifold3d` (guaranteed by construction), `trimesh` (`is_watertight`/`is_winding_consistent`/`is_volume`), `Open3D`, Blender 3D-Print toolbox. If `is_watertight` fails, fix the source script, don't repair.
- **Always 3MF, never STL for slicer hand-off** — STL drops topology; re-imported STL may not be manifold. 3MF preserves topology; glTF `EXT_mesh_manifold` most modern. (contrast: the current cabin pipeline actually ships `_printready.stl` because parametric bodies overlap and Bambu fuses them.)

### CAD-as-code & self-correcting loop (Parametric CAD-as-Code; Self-Correcting 3D Design Loop; Research: Claude+Blender)
- Python script = source of truth, mesh = throwaway artifact: deterministic (lock `requirements.txt`/Docker), versioned (git diff v7→v8), composable (`VerandaSpec(width=...)`).
- Blender fails this (binary .blend, imperative ops, no manifold guarantee); CadQuery (OpenCASCADE, real fillets/chamfers/shells) + manifold3d (boolean can't fail) pass. Research verdict: **Blender is the wrong tool for FDM printables** (good for scenes/art/asset gen); recommended stack = CadQuery + manifold3d + Bambu Studio CLI, Claude as orchestrator. (NB: superseded in practice for cabins by the working Blender voxel + parametric route on the PC.)
- Loop: write/edit versioned script → run → emit STL/3MF + JSON status → render ≥4-6 orthographic PNGs → manifold check (assert watertight) → Claude vision-reviews vs `design-review.md` checklist → fail→edit / pass→export+slice. Avoid single-render, no-JSON, file-overwriting, no-checklist. Reference: `flowful-ai/cad-skill` (PolyForm Noncommercial — pattern only), `iancanderson/openscad-agent` (versioned `model_001.scad`).
- Bambu Studio CLI: `--slice --load-settings --load-filaments --export-3mf --pipe`; output `.gcode.3mf`; generates hundreds of MB temp files → run in isolated temp dir, delete after. Don't use `/tmp` (macOS cleans >3 days); use `<repo>/var/slice-jobs/<uuid>/` and `generated_assets/<commit>/`. End-to-end MCP: `DMontgomery40/bambu-printer-mcp` (STL manip + slice + FTPS + MQTT, P2S supported; license unconfirmed).
- design-review.md checklist (FDM Design Rules): walls ≥1.2 mm, slabs ≥0.8 mm, overhangs ≤45° or support-OK, bridges ≤20 mm, chamfer not fillet, largest face on Z=0, holes compensated (+0.3 slip / -0.1 press).

### Cabin lines / status
- 8 cabin-lijnen / 33 varianten buildable via pipeline (Print Pipeline; Blokhutten Cabin Inventory). Voxel route works end-to-end for flat-roof cabins (Magnolia-type, DD04 door). Named presets: `magnolia` (printed+approved), `newyork`.
- MEMORY (25 jun): PC does voxel-remesh→printready.stl AND slices/prints itself (Bambu Studio + P2S). MEMORY (3D-print GLB-doors): real DD-18-0050 door in `parametric_blokhut.py` — import→remove glass→rotation_mode XYZ→voxel-remesh→wall grips kozijn (OVR); Camelia done, 7 to go.


---

<a id="14"></a>
# §14. Current project state (hot list & recent sessions)

### Hot cache header status (hot.md — evergreen, "Last Updated 2026-05-22")
- NOTE: hot.md's own `updated:` field and "Last Updated" both read **2026-05-22** — the hot cache is STALE relative to newer session work (Roosmarijn 6-10, Zonnebloem 6-05, print pipeline 6-24/25, and the CLAUDE.md MEMORY.md project notes which supersede it). Treat hot.md as the *self-automation research index*, not the current cabin state. The current cabin state lives in MEMORY.md project notes (see below) and the per-scene session logs.
- Tooling state (hot.md): Blender **5.1** + ahujasid blender-mcp (**port 9876**); Polyhaven enabled; Sketchfab needs API key for new downloads. Vault path listed as `C:/Users/beike/iCloudDrive/Vault/Claude/` (older path — MEMORY says live vault is now under `C:\Users\beike\Desktop\Icloud\iCloudDrive`). Pilots: `C:/Users/beike/Documents/Blender-blokhutten/pilots/`.

### CURRENT branch / git working state (from env, 2026-07-01)
- Branch: **weekend-renders** (main = main).
- In-progress edits on `.blend` files: Camelia scandi, Lelie cottage, Magnolia modern; preview PNGs modified for Dahlia (tuinkantoor + leeshoek), Lavendel (pluktuin + lavendelveld). `scripts/cabin_lib.py` modified.
- Recent commits all **Lavendel Pluktuin** iterations (boog opgeschoond, zwevende klimrozen weg, potten weg/tafel naar patio-midden, front-links hero-hoek, zwevers gegrond).
- Many untracked `swap_*` pyc's, `_diag/`, `_round2_review/` + review HTMLs, `add_atmosphere.py`, `apply_grass_16.py`, `apply_grass_scene.py`, and freshly downloaded Polyhaven models under `assets/polyhaven/models/` (Sofa_01, anthurium, calathea, coffee_table_round_01, dandelion, fern_02, gazania/heliophila flowers, jacaranda_tree, modern_arm_chair_01, moss_01, outdoor_table_chair_set_01, pachira_aquatica_01, painted_wooden_bench, etc.).

### Project state per MEMORY.md (current authority — supersedes hot.md)
- **16/16 scenes** built at REALISM_PREVIEW level (8 primary + 8 alt-style), completed 20 jun; index `docs/INDEX_scenes.md` (project_8_scene_plans; project_realism_overhaul_pause). Finale **2560×1440** renders still to be chosen.
- Realism overhaul: swap real Polyhaven/Sketchfab props for hand-built boxes — `swap_lib.py` + per-scene `swap_*.py` (project_realism_overhaul_pause; feedback_no_procedural_props).
- Render-fix round 2 (24 jun): reviewed 16 renders (v3 blends, gallery on localhost:8765); paths/blobs removed; light overhaul plan = `docs/PLAN_lighting_overhaul.md`; PDF 12-16 feedback = `docs/ROUND2_feedback.md` (project_render_fixes_round2).
- Goal (pending, do AFTER per-scene review fixes): the Lelie Ochtendnevel "light-comes-through" look (volumetric haze + low warm sun + AgX) applied to ALL scenes (project_ochtendnevel_light_goal).
- Zentuin #13 (Roosmarijn Zentuin): Beike does himself elsewhere — **do not touch** in the render-fix round (project_zentuin_other_session).

### Recent-session logs (auto-generated stubs — LOW content)
- **2026-07-01** (session log): 8 machine "Session ended" entries, all **0 turns**, "Pending learnings flagged: 8, saves 0" — no substantive work recorded.
- **2026-06-30**: 2 entries, 0 turns — empty.
- **2026-06-25**: door/window GLB conversion — "zoek de GLBs van de deuren en ramen van blokhutwinkel en zet ze in de vault zodat de PC erbij kan"; result: **all 75 converted, 0 errors — 242 MB ASCII-OBJ → 8.3 MB binary GLB**, verifying GLBs contain real geometry. (Ties to project_3dprint_glb_doors: real DD-18-0050 door in `parametric_blokhut.py`.)

### 2026-06-24 session — 3D-print voxel-remesh handoff Mac→PC (print pipeline)
- Working on Magnolia + NYL print models. Magnolia extract found **10 real posts** (4 corner posts + wall corners); NYL found only 1 (canopy posts named differently).
- **SHARP-remesh** test on Magnolia (background, ~3-4 min): keeps angular/sharp edges instead of rounding, and is lighter on memory. Magnolia at **1.5×**, real corner posts thickened (no added posts).
- Voxel-timing tuning on wide NYL model: voxel **0.3 @ 150mm** ≈ 5 min (vs 20 min); voxel **0.4** = fastest batch ≈ 3 min. Slowness is purely the voxel calc on the wide NYL model.
- User complaints driving iteration: still posts on the front; not sharp/realistic; walls/planks lack the discussed overlay; slightly-protruding planks look wrong (as dots/stippels).
- Decision: move print work to the **PC** (do it while also doing Blender). Full copy-paste handoff written. Mac had no Bambu installed / not connected yet. Output folder to be created on PC where PC drops STLs → syncs back to Mac.
- Mac disk cleanup context: Chrome was 4.5 GB over 20 processes; freed to 64% after closing Spotify/Chrome. (Aligns with MEMORY project_blokhut_print_pipeline: PC now does voxel-remesh→printready.stl AND slices/prints itself in Bambu Studio + P2S since 25 jun; workdir `C:\Users\beike\blokhut-print\`.)

### 2026-06-10 session — Roosmarijn v9→v12 render polish (CANONICAL FINAL)
- Scene file: `pilots/Roosmarijn-200x300-400-zijwand/style-modern/roosmarijn_warm.blend`. Camera: `Camera_A_Product_Hero` — **45mm, horizontal, shift_y = -0.143**.
- Canonical output: `pilots/.../roosmarijn_modern_FINAL.png` — **2560×1440, 16-bit PNG, Cycles GPU**, render time **~1:46 on RTX 3070**.
- Iterations: v9 baseline → v9-clean (512 samples, OIDN guided, 4096 tex, 2560×1440) → v10 (carport fill + bike rim-light + wand macro-noise + vlonder weathering + tegel grout — Volume Scatter disaster) → v11 (readable carport, bike top-light) → v12 CANONICAL.
- **Production render recipe (`render_final_clean.py`)**: 2560×1440 @ 100%, **512 samples, adaptive 0.005**, OIDN **RGB_ALBEDO_NORMAL ACCURATE**, **4096 tex**, AgX **look=None**, **exposure=0.05**, **use_nodes=False**, 16-bit PNG.
- **Test render (`render_test_clean.py`)**: 50% (→1280×720), 128 samples, adaptive 0.01, OIDN, 2048 tex, 8-bit PNG.
- Critical render flags (always): `scene.use_nodes = False` (KRITIEK — prevents all-black render); always `bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)` via MCP before headless (headless reads disk, not MCP memory).
- Bugs+fixes: (1) **World Volume Scatter density=0.002 → entire exterior pitch-black** (Cycles 5.1 world-volume + HDRI); fix = never use World Volume Scatter here, HDRI strength back to 0.40. (2) Relative `-o` path → wrote to `C:\`; fix = always absolute `-o`. (3) `Rim_Bike` was behind bike acting as fill; repositioned (-4.5,-2,2) → **(-2.4,-0.6,2.5)** top-light. (4) Wrong material targeted — `Patio_Vlonder` uses `MAT_WoodDeck_Clean`, not `MAT_Vlonder`; target via `obj.data.materials[0].name`.
- Carport light rig (readability; carport must stay darker than outside, cap ~24W BackWall): Fill_Canopy **26W** (3.5m rect over canopy); Fill_Canopy_BackWall **24W** (2m rect back wall); Fill_Carport_Overhead **11W** (new, over opening); Rim_Bike **12W** at (-2.4,-0.6,2.5).
- Wood material (v10-v12): macro zone-variation = Noise (scale 1.2, detail 3) → ColorRamp 0.87-1.0 → Mix MULTIPLY on base, factor 0.06-0.08. Voronoi plank-seam bump (Feature=Edge, randomness 0.0) → Bump distance **16mm** (was 6mm). Per-plank Object-Info Random → ColorRamp **0.72-1.08** (was 0.80-1.00) → MULTIPLY. HueSat Value **1.0** (was 0.97).
- Tile grout: `Invert(Brick.Factor) × mortar_dark` → Mix MULTIPLY; jitter noise on Brick Offset × 0.05 → Mix ADD.
- Background soften: HDRI strength 0.40→**0.37**; HueSat saturation 0.96→**0.91**; Sun_Golden **5.8W** stays key.
- OPEN ITEM for v13: current AgX `look='None'` is flat/catalog; wiki standard = `look='AgX - Medium High Contrast'` for premium lifestyle look — recommend switch + **exposure 0.15-0.20** + check highlights.
- Cleanup: all 50+ iteration PNGs deleted, kept only `roosmarijn_modern_FINAL.png` (16.7 MB).

### 2026-06-05 session — Zonnebloem hero + Roosmarijn warm build (AI-tooling heavy)
- **Zonnebloem 300×300 +300 zijwand (modern dark)**: base `pilots/base/Zonnebloem-300x300-300-zijwand.blend` → `pilots/Zonnebloem-300x300-300-zijwand/style-modern/zonnebloem_modern.blend`. 2-tone: kdi_potdeksel_zwart exterior + luxehouse-onbehandeld → later kdi_rabat_fbz_zwart canopy (fix "pale wood band"). **Forest_slope HDRI** (user wanted forest backdrop, not sky). v1 (256 samples, 1440p) → v2 (1080p AgX wiki recipe) → v3 (tree-fill back-right + carport + plants -X side). Final `zonnebloem_modern_HERO_FINAL_v2_0001.png`.
- **Roosmarijn 200×300 +400 zijwand (warm honey cottage)**: base → `roosmarijn_warm.blend`. Honey hardwood via HSV-shift (sat 1.05, val 1.05). Gravel ground (Voronoi pebbles) + clay paver patio (Brick). Camera NW **(-5, 7, 1.55), 35mm, target (0,0,1.2)**. **Kiara_1_dawn HDRI**, warm sun (1.0, 0.82, 0.62). Hedge still WIP (leaf-card scatter via particles, sphere-normal trick).
- Toolchain: **Replicate flux-schnell** (patina textures, hedge color textures boxwood/beech/yew, leaf-sprig white-bg alpha ✓); **3D AI Studio tencent-rapid** (bicycle NL city, hydrangea bush, lavender plant ✓ OBJ+PBR color/metallic/roughness/normal); Polyhaven append (Sofa_01, outdoor_table_chair_set, modern_arm_chair, potted_plant 01/02/04, shrub_01-04, fern_02, weed_plant, dandelion, periwinkle, shrub_sorrel, flower_heliophila); Sketchfab (spruce_fence, hetz_midget, birch pack 5 trees+LODs, pine_trio, ribbon_grass, wild_grass, axe, garden_shovel, wheelbarrow/tachka, wicker_basket).
- Render times: Zonnebloem v1 **10:46** (2560×1440, 256 samp, OPTIX, 4.4GB VRAM); v2 wiki recipe **0:31** (1920×1080, 256 samp, AgX, 16-bit); Roosmarijn v2 post-cleanup **0:31** (1920×1080, 256 samp, 3.5GB VRAM); v3 same.
- Critical bugs/fixes: (1) **Cycles all-black** = 34 hetz topiary "zombies" (700m×1200m each, floating z=600m) absorbing all rays; Eevee/Workbench rendered fine; fix = ablation-by-group to find huge bbox → delete (→ Cycles Zombie Mesh Debug Pattern). (2) Magenta plants = Polyhaven Group-shaders pointing `.jpg` while disk has `_2k.png`; fix = path-fixer trying variants (`base.png/.jpg/_2k.png/_2k.jpg`) + Mix-RGB green-fallback node (fac=1 loaded, fac=0 green). (3) Hero birch in carport sightline at (0.92,-7.66) → delete original Birch_2, keep .001/.002. (4) Lavender at y=1.78 inside patio (y=1.55-4.80); fix = patio start y=2.05 + planting-bed strip. (5) Floating birches z=1.9-2m (shared-mesh matrix-decomp) → `bpy.ops.transform.translate(value=(0,0,-z_min))` (world-space). (6) Shared mesh data breaks `transform_apply` (→ Blender Shared-Data Transform Apply Pitfall).
- User-feedback patterns codified: "ren je niet uit jezelf" (render only on explicit go); "saai/leeg" (diversify, don't reuse same models); "planten in vloer" (always check bbox-z); "heg = groen blok" (texture-on-box not 3D → leaf-card scatter); "assets ergens anders dan polyhaven" (broaden sources).
- Open (as of 6-05): hedge particle-scatter visual verify; rose-bush gen blocked (35/55 credits); scene "organize" pass; Roosmarijn hero render with new hedge awaiting user OK.

### 2026-05-22 session — Showroom render pipeline (Lavendel v4→v16) — EARLY/procedural era (largely superseded by real-asset overhaul)
- Pipeline: `PLAN.json → build_scene.py → BASE.blend → extend_scene.py + EXT.json → FULL.blend + RENDER.png`; idempotent. ~50s per showroom render, 1920×1080 PNG.
- Verified on 3 cabins: **Lavendel-400x300** (door +Y, 4.5×3.4m), **Magnolia-300x200** (door +Y, 3.5×2.4m), **Camelia-250x300-300-zijwand** (door +X, 6×3.4m +side). Camera auto-derivation works for +X/-X/+Y/-Y doors.
- Composition sweet spot: camera **(4.0-4.5, 8.0-8.5, 1.5), lens 30-35mm, target Y=0**; rule-of-thirds target Y -0.2 to -0.3. Too close (3.5,6.5) v12; too far (7.5,9.0) v5.
- Values: birch crown_start_z = h*0.55 (not 0.40), schutting **2.1m**; stones **z=0.025** (NOT z=-0.03 — grass blades 4.5cm hide below 5cm); plant border hortensia **65cm** radius, lavender **35cm**, sedum **22cm**; pavers ≥50cm, **2cm gap** grout; dark pot 40cm radius × 60cm height.
- Lighting dial: sun_angle 1.0 diffuse / 0.6 showroom / 0.3 catalog; sun_energy **5.0** for visible cast shadows; HDRI rotation **220°**; AgX **Punchy** view transform.
- **23 mei DEEP QUALITY PUSH** (after user "moet beter"): switched procedural sphere-clusters → REAL Polyhaven `.blend` assets. `extend_scene_real.py` (~430 LOC). Assets: pine_tree_01_2k, potted_plant_01_2k, wild_rooibos_bush_2k (purple flowers), shrub_01_2k boxwoods; PBR brown_planks_09 schutting, dark_planks deck, aerial_grass_rock ground. Techniques: `libraries.load` + `obj.copy()` linked dupes (Collection Instance failed — hide cascades); **HIDE_OFFSET=(1000,1000,0)** + `hide_render=True` on sources; `scale_heavy_textures(1024)` after import (VRAM); `remap_broken_image_paths()` (.exr→.png); **MAX 4 trees + 6 bushes + 2 pots + 2 boxwoods** safe on RTX 3070 8GB; avoid heavy furniture (bench/armchair 5+ PBR = OOM).
- 7 verified lighting moods table: midday (kloofendal_48d_partly_cloudy), **hero** (kloofendal_43d_clear + sun_alt 35, warm afternoon ★), dawn (kiara_1_dawn + sun_alt 25), overcast (kloofendal_overcast, no shadows), **forest** (forest_slope_2k ★★), cherry (partly_cloudy + cherry foliage), winter (overcast + bare birches), skybluedeep (kloppenheim_06_puresky).
- Batch tool `scripts/batch_renders.py`; also build_scene.py, extend_scene.py (~900 LOC/10 fns), build_comparison.py, audit_cabin.py, compare_render.py, validate_scene.py; `training/cabin_orientations.json` (all **34 cabins** audited); `training/LESSONS.md` (35+ entries).
- Critical rules (this era): never place garden elements before get_cabin_info() (door dir first); never GLTF-import headless (Sketchfab plants crash — use procedural, NOTE this rule later reversed by real-asset overhaul); never stones z<0; never 8+ boxwood "groene bollen" (AI-dump look); always use real cabin files from `pilots/base/`.
- DISK rule: packed-Polyhaven .blends are 100-500MB each → `rm training/builds/*.blend` after each render, keep only PNGs (3MB), stay 5+GB free (disk hit 100% caused file truncation).

### hot.md self-automation research index (38 vault pages written 2026-05-22, waves 1-11)
- Not cabin-state; a knowledge base. Notable pages: Blender Python Automation Deep Reference; Cycles Optimization for 8GB Archviz (RTX 3070 samples/bounces/denoise/persistent-data/light-groups); Lighting Recipes Catalog 25 (`apply_recipe()`, NL max sun 14° December); Garden Style Bible 5 Core Styles (Modern Strak/Scandi/Japandi/Boerderij/Mediterraan); Camera Composition Preset Library 32 (`apply_camera()`, cabin math MAX_DIM×1.5+3); Render Manifest Schema + Batch Orchestrator (single YAML → 165 renders, self-host €4-5/1000-frame); Multi-Season Variant Pipeline (660 renders 33×5×4, NL sun 61° summer/14° winter @52°N); Flamenco Render Farm; Procedural Cabin Generator GN5+Bonsai; ACES OCIO + Atmospherics; NL Building Code (Bbl 2026: 5m/3m/30m², brandafstand 5m WBDBO); Marketing B2B Dutch Cabin Sellers (EU AI Act **Aug 2 2026** disclosure — Cycles exempt); Site-Specific Cabin Placement (PDOK + AHN4/5/6 + Blender Hoogtedata Addon by Thomas Kole).
- `~/.claude/skills/blender-archviz/SKILL.md` created (6 critical rules, 15-step build order, audit script, safe-geometry whitelist, render settings for RTX 3070).
- Legacy parked files (this era): `lavendel_REBUILD_FINAL.blend` + `magnolia_REBUILD_FINAL.blend` awaiting "ja render now"; reusable `pilots/styles/build_dutch_garden_hero.py` (10-step). Lessons #9-14 in Lavendel Build Lessons Learned (Polyhaven .jpg-vs-.png path bug, missing wild_rooibos textures→manual mat, USD trees import leafless→use GLTF birch, birch pack 5 trees×3 LODs filter by name, always texture-fix pass after import, verify via viewport screenshot not bbox).

### Conflicts / supersession summary
- **hot.md (2026-05-22) is superseded** for cabin-state by: real-asset overhaul (23 mei onward), the 6-05/6-10 per-scene builds, and MEMORY.md project notes (16/16 scenes done, round-2 fixes, print pipeline on PC). Use hot.md only as the research/automation page index.
- Blender version conflict: hot.md/6-10 headless CLI both reference **Blender 5.1**; MEMORY reference_blender_mcp confirms two MCP servers (capital `mcp__Blender__*` for scene work, lowercase `mcp__blender__*` for asset downloads).
- "Never GLTF import headless / use procedural" (5-22) is **reversed** by the real-asset/no-procedural direction (23 mei + feedback_no_procedural_props): hand-built boxes now rejected in favor of real assets from `assets/sketchfab/` + `assets/polyhaven/` + cabin_lib toolkit.
- AgX look conflict (open): finished Roosmarijn uses `look='None'`; wiki standard + v13 recommendation = `AgX - Medium High Contrast` + exposure 0.15-0.20.

> **Niet gevonden/leeg:** 2026-07-01.md (present but 0-turn auto-stub, no substantive content); 2026-06-30.md (present but 0-turn auto-stub, no substantive content); 2026-06-25.md (present, only 1 substantive turn: door/window GLB conversion)
