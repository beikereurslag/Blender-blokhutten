# De Regentuinkamer — lean working brief for Astra (token-budget version)

Beike approved the concept in `docs/PLAN_astra_garden.md`. That document is the spec. This brief replaces the long onboarding prompt: everything you need to know is below. Do NOT re-read the compendium, the wiki, or the script library up front.

Address me as "Beike", answer in English, one scene, one gate at a time.

## Context budget rules (these matter more than anything else)

1. **Read nothing whole that is bigger than 10 KB.** Grep for a section, read 40–80 lines around the hit, stop. The compendium (`docs/VAULT_blender_blokhutten_compendium.md`, 328 KB) is a lookup table, never a read. Section anchors: §6 vegetation, §7 render/batch, §10 MCP, §13 3D-print.
2. **Every Blender interaction returns at most 20 lines.** Write bpy code that prints a summary (counts, bbox, names of failures), never object dumps. Never call `get_scene_info` on the full scene; query named objects.
3. **Write scripts to disk, run them, read the summary.** Prefer `blender.exe --background file.blend --python script.py` for anything that touches more than a few objects; MCP live calls only for small edits and viewport checks I ask for.
4. **No screenshots for aesthetics.** I have Blender open, I am the eyes. Code validates correctness.
5. **Reports per gate: one screen, tables only.** No justification prose, no restating the plan. Format: did / checked / failed / need from Beike.
6. **One gate per session.** When a gate is approved, stop; I start a fresh session for the next gate with this brief plus the plan.
7. Preview renders: 960×720 / 24 samples, AgX, texture limit 2048, persistent data off. Finals only after my explicit OK.

## Hard rules (distilled, complete for this job)

- Cabin GLB imports in cm: scale 0.01 once, delete its camera, rotate as the plan states. Run `scripts/fix_cabin_boards.py` on the cabin (plank alignment), board texture along the plank via `cl.uv_board_textures()` in `scripts/cabin_lib.py`.
- Real assets only, exactly the shopping list in the plan. Inspect before use. No procedural props. Hedge = one verified shrub sprig, Poisson geometry-nodes scatter, outward rotation. Tree clusters under 50k verts get hidden (`scripts/hide_bare_trees.py`).
- Nothing inside the closed room, nothing in the door clearance, grass keeps a 0.15 m band off the route. Dense backdrop, no sky leak, no visible world edge.
- Save with `wm.save_as_mainfile` before any headless render. `scene.use_nodes = False` unless compositing is intended.
- No commits, no deletions of existing files, no /tmp, no auto-cleanup. If a tool is blocked, hand me the copy-paste command. PowerShell 5.1: no `&&`.
- Print: P2S, PLA Basic, 0.16 mm, gap 0.15 mm sliding fit, 18° sawtooth relief, ribs 3×3 mm, no magnets/screws. `qa/island_check.py` per part. Ceilings 180 mm (support) / 194 mm (none). Tree support only via GUI.

## Blender MCP

Server is registered in Codex (`mcp_servers.blender`). Blender 5.1 must be open with the BlenderMCP add-on toggled on (port 9876). If `get_scene_info` fails, ask me to toggle it; retry once; nothing else.

## Files you may open whole (small)

- `docs/PLAN_astra_garden.md` (the spec, 20 KB)
- `WERKWIJZE_REVIEWLOOP.md` (3.6 KB)
- `scripts/validate_scene.py` (10 KB, run it, do not rewrite it)

Everything else: grep, then read the hit only.

## Current gate

State which gate is active at the start of your first reply, then do only that gate.
