# Project: full garden in Blender → walkthrough video → 3D-printed garden

You are working for Beike (Blokhutwinkel). Address me as "Beike" in every reply, answer in English. You have access to my Obsidian vault and to this PC. Read before you build; do not ask me things that are already documented.

## 1. Read first (in this order)

Vault root: `C:\Users\beike\Desktop\Icloud\iCloudDrive\Vault\Claude\` (NOT `~\iCloudDrive`, that is an empty stub)
- `wiki/hot.md` and `wiki/index.md` → orientation
- `wiki/concepts/Cabin Hero Build Playbook.md` → the standard build method for a cabin scene. Leading.
- `wiki/projects/Overkapping Scene Differentiation Playbook.md` → my 10 atmospheres; how to make scenes feel different
- `wiki/concepts/Kapschuur Build Lessons.md` → placement/path/anchoring lessons
- `blokhut-print/HANDOFF.md` → print pipeline handoff

Project repo: `D:\Blender-blokhutten\` (branch `weekend-renders`, do not commit)
- `WERKWIJZE_REVIEWLOOP.md` → how we work together: one scene at a time, live review loop
- `docs/VAULT_blender_blokhutten_compendium.md` → deep knowledge, grep it for anything Blender-specific
- `docs/PLAN_lighting_overhaul.md`, `docs/INDEX_scenes.md`
- `scripts/cabin_lib.py`, `scripts/grass_lib.py`, `scripts/swap_lib.py`, `scripts/validate_scene.py`, `scripts/hide_bare_trees.py`, `scripts/fix_cabin_boards.py`
- `scripts/clips_v2/` → the camera/clip engine from the last film round (frame_score test included)
- `pilots/_bk_fetch.py` → headless BlenderKit fetch (OAuth refresh required)
- `pilots/` → existing scenes. These are reference for tooling only, NOT a source of inspiration. Beike scrapped them on 13 July; every new scene starts bare.

Print pipeline: `C:\Users\beike\blokhut-print\` (work dir, QA toolkit in `qa/`, `island_check` is the real spaghetti test)

## 2. Connect to Blender (MCP)

Two Blender MCP servers exist on this PC. Use the community one; it is a plain stdio server any client can launch.

**Server: ahujasid/blender-mcp (community)**
- Launch command: `C:\Users\beike\.local\bin\uvx.exe blender-mcp` (already installed, same entry as in `D:\Blender-blokhutten\.mcp.json`)
- Register it in your MCP config in your own format; the server spec is:
  ```json
  {"blender": {"command": "C:\Users\beike\.local\bin\uvx.exe", "args": ["blender-mcp"], "env": {"DISABLE_TELEMETRY": "true"}}}
  ```
- Blender side: Blender 5.1 at `C:\Program Files\Blender Foundation\Blender 5.1\`. The addon `addon.py` is already installed in `%APPDATA%\Blender Foundation\Blender\5.1\scripts\addons\`. In Blender: N-panel → "BlenderMCP" tab → **Start MCP Server**. It binds `localhost:9876`. Ask me to toggle it; do not assume it is running.
- Handshake test: call `get_scene_info()`. If the first call fails, retry once (known first-call flake). If it keeps failing: only one Blender instance may own port 9876; the fix is to restart the toggle in Blender, the `uvx` side reconnects on its own.
- Tools you get: `execute_blender_code` (bpy, the primary mutator), `get_scene_info`, `get_object_info`, `get_viewport_screenshot`, Polyhaven search/download, Sketchfab search/download, BlenderKit is NOT in this server (use `pilots/_bk_fetch.py`).

**Server: Blender Lab "Blender" (official, capital B)**
- Installed only as a Claude Desktop extension (`ant.dir.gh.blender.blender-mcp` 1.0.1), so not reusable from your side as-is. If you want it, follow https://www.blender.org/lab/mcp-server/ and tell me what to install; it adds API-doc search and screenshot-of-area tools, nothing you strictly need.

**How to use the MCP session (hard rules)**
- The running Blender instance is a shared, live session. I have Blender open and I am the eyes: do NOT take screenshots for aesthetics (token cost); validate correctness by code (bbox, dimensions, object counts, `validate_scene.py`) and ask me what it looks like.
- Keep each `execute_blender_code` call small: under ~50 lines and ~2 s. Chain calls. Large `get_scene_info` on a 200+ object scene truncates the JSON; query focused objects instead.
- Never render through MCP. Save first with `bpy.ops.wm.save_as_mainfile(filepath=...)` (MCP edits live only in RAM, headless reads disk), then render headless:
  ```
  "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" --background <scene>.blend --python <render_script>.py
  ```
  Absolute `-o` output path, `scene.use_nodes = False` unless the compositor is intended (an active compositor silently renders black).
- Blender 5.1 colorspace/reload trap and the rest of the debug recipes are in the compendium §7, §10 and §12. Read §10 before your first call.
- Do not destructively modify or delete objects I did not ask about. Respect existing collection names and structure.

## 3. Goal

Design and build ONE complete, coherent garden around one Blokhutwinkel cabin in Blender, then:
1. render a full walkthrough video (camera path through the garden, not an orbit; orbit clips were rejected),
2. turn the whole garden into a printable model set for the Bambu P2S.

Pick one cabin from the real tekentool GLB exports (see compendium section on GLB export; GLB comes in cm, scale 0.01 after import, delete the camera it brings). Propose the garden concept yourself before building. Originality is required: invent a concept, do not reuse a recipe from an older scene.

## 4. Non-negotiable rules (from my documented feedback)

Working method
- Phases with a hard gate between each: concept → anchoring (ground, paths, borders, back hedge, cabin orientation) → my approval → dressing → my approval → camera → render. Never skip ahead.
- Previews at 960×720 / 24 samples. Full quality only for finals, and only after I say so.
- Heavy renders go headless via the Blender CLI with `--python`, never through an MCP session (it crashes). RTX 3070, 8 GB VRAM: texture_limit_render 2048, use_persistent_data off.
- Validate with code (`validate_scene.py`, object summaries, bounding boxes), not by staring at screenshots. Before you call anything "done", run your own critique: floating objects, low-poly junk, magenta/broken materials, bare trees (tree clusters under 50k verts get hidden), objects inside the cabin, plank misalignment on the cabin (`fix_cabin_boards.py`).
- No commits, no finals, no deletions without my OK.
- Never write to /tmp. Never auto-clean anything.
- If a tool is blocked, give me the copy-paste-ready command. PowerShell 5.1: no `&&` / `||`, split into separate blocks.

Visual
- View transform AgX. Wood board texture runs along the plank, use `cl.uv_board_textures()`.
- Real assets only: BlenderKit first (headless fetch script), then `assets/glbcreator/`, `assets/polyhaven/`, `assets/sketchfab/`. No hand-built procedural props (boxes as towels, planters, paths look fake). Props should be real Blokhutwinkel/Tuindeco products where possible.
- Dense forest/hedge backdrop, no sky leaking through, no "floating island" look. Hedge = geometry-nodes scatter of real shrub leaves, not leaf cards.
- The cabin is always the hero; the garden supports it. Every empty plane gets dressed with real props. Vary camera height and angle along the walkthrough.
- Lighting target: the "light comes through" look (volumetric haze, low warm sun, AgX) from the Lelie Ochtendnevel scene, see compendium.

Print (Bambu P2S, PLA Basic, 0.16 mm layers)
- Print-only assembly: dovetails, ribs-in-groove (3×3 mm rib, 60% of post height), tongue-and-groove. No magnets, screws or inserts.
- Sliding-fit gap 0.15 mm (measured). Visible relief on vertical faces = 18° sawtooth, never a square groove.
- Solid parts via solidify + voxel remesh, watertight, no floating fragments, no thin-wall ratio problems. Run the 10-point rookie checklist in the compendium on every iteration.
- Run `island_check` on every part. Two known measurement traps: bed counts as overhang, bbox span reads slopes as bridges.
- Slicer ceilings: support 180 mm, no-support 194 mm; tree support only via GUI (CLI crashes, exit -50). Prefer one part with minimal loose support (grid 5, plate-only, z-gap 0.24).
- Garden pieces (hedges, trees, furniture, paths) need their own strategy: decide scale (suggest 1:50 or 1:75 so the plate fits), which elements print as one base tile with relief and which are separate drop-in parts, and how tiles connect. Propose this before modelling anything for print.

## 5. Deliverables, in order

1. Concept doc (`docs/PLAN_astra_garden.md`): cabin choice, atmosphere, layout sketch as text/ASCII, prop shopping list with source per item, camera path description, print strategy with tile plan. Wait for my OK.
2. Anchored scene `.blend` + one 960×720 preview. Wait for my OK.
3. Dressed scene + 3 previews from the planned camera path. Wait for my OK.
4. Walkthrough: camera path in `.blend`, review sheet of ~12 keyframes first (use the `clips_v2` frame_score test), then a night-run render script I start myself. Output 1920×1080, ~30–45 s, 24 fps.
5. Print set: per-part STL in `C:\Users\beike\blokhut-print\output\garden\`, QA report per part, one 3MF plate layout, list of anything that cannot pass QA and why.

At every gate: tell me what you did, what you checked, what failed, and what you need from me. No silent turns.
