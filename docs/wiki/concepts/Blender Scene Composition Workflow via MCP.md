---
type: concept
title: "Blender Scene Composition Workflow via MCP"
created: 2026-04-30
updated: 2026-04-30
tags:
  - concept
  - blender
  - mcp
  - workflow
  - claude
status: current
related:
  - "[[ahujasid blender-mcp]]"
  - "[[Polyhaven - HDRI and Asset Library]]"
  - "[[Sketchfab - CC Library]]"
  - "[[Custom Asset Import via execute_blender_code]]"
  - "[[Cycles vs Eevee Next for ArchViz]]"
  - "[[Garden Style Palette for Cabin Visuals]]"
---

# Blender Scene Composition Workflow via MCP

De iteratie-loop voor Claude (mij) + user samen scenes opbouwen rond een geleverde blokhut. User werkt visueel mee in Blender (zie [[feedback_3dprint_blender_workflow]] — niet headless), ik stuur via MCP-tools en `execute_blender_code`.

## Voorbereidende setup (eenmalig)

1. Blender open, addon `blender-mcp` geïnstalleerd, "Connect to Claude" aan (poort 9876)
2. `DISABLE_TELEMETRY=true` env var (voorkomt dat user-prompts/code naar Ahuja's server gaan)
3. Polyhaven-integratie aan in addon-panel
4. Hyper3D Rodin / Hunyuan3D: optioneel, alleen bij missende custom props
5. Empty scene → Cycles render engine, Color Management Filmic

## Blokhut import (eerste actie per scene)

User levert .blend / .fbx / .skp van blokhutwinkel. Blender-MCP heeft géén dedicated import-tool — gebruik `execute_blender_code` (zie [[Custom Asset Import via execute_blender_code]]).

```python
import bpy
bpy.ops.import_scene.fbx(filepath="/Users/.../blokhut_X.fbx", global_scale=1.0)
# of voor .blend:
bpy.ops.wm.append(directory="/Users/.../blokhut_X.blend/Object/", filename="Blokhut")
```

Direct na import:
- `get_scene_info()` — controleer dat de blokhut binnen is
- `get_object_info(name="...")` — check schaal (meters!) en oriëntatie
- Verplaats naar wereld-origin, oriëntatie: voorgevel naar +Y

## Scene-build loop (iteratief)

Per stijl uit [[Garden Style Palette for Cabin Visuals]]:

### Stap 1 — Ground + Sky
```
download_polyhaven_asset(asset_id="<HDRI keuze>", asset_type="hdris", resolution="4k")
```
Plane onder blokhut (40x40m), apply ground-texture (Polyhaven gras/grind/grond).

### Stap 2 — Major landscape elements
```
download_polyhaven_asset(asset_id="oak_tree_01", asset_type="models")
search_sketchfab_models(query="japanese maple")
```
Plaats 3-7 grote elementen (bomen, struiken) handmatig op smart positions (driehoek-compositie, niet symmetrisch).

### Stap 3 — Foliage scattering
Geometry Nodes scatter voor gras + kleine planten op grond-plane. Density-mask voor paden (0 density) en bedden (hoge density). Zie [[Geometry Nodes Scattering for Outdoor Scenes]].

### Stap 4 — Hardscape + props
Pad, hekwerk, terras, meubilair, hottub. Veelal Sketchfab CC0-models. Schaal **altijd checken** (meters).

### Stap 5 — Lighting finalisatie
- HDRI strength tunen (1.0-2.0)
- Eventueel sun light parallel met HDRI sun (voor scherpere schaduwen)
- Avond: emission shader op ramen (warm 2700K, strength 5-10)
- String lights / lantaarns: emission spheres

### Stap 6 — Camera + render
- Camera op 1.6m hoogte (oog-niveau), licht naar boven 5° (hero feel)
- 35mm of 50mm focal length (geen wide-angle distortion)
- Composition: blokhut 1/3 vanaf links of rechts, niet centered
- `get_viewport_screenshot()` — preview met Eevee
- Bij goedkeuring: full Cycles render (1920x1080 of 2560x1440, 256 samples + denoise)

## Iteratie-checks (verplicht na elke stap)

1. `get_viewport_screenshot()` — visuele check
2. User geeft go / no-go in chat
3. Bij no-go: aanpassen via `execute_blender_code` of native MCP tool
4. **Niet doorploegen zonder goedkeuring** — user is visueel meekijkend

## Render-batch per blokhut

Voor 1 blokhut → 3-4 stijlen → 2 angles per stijl = 6-8 finale renders.

## Output organisatie

- `~/Documents/event-branding/blokhutten/<product_naam>/`
  - `style-modern/` (PNG renders)
  - `style-cottage/`
  - `style-scandi/`
  - `_source.blend` (per stijl, voor herbruikbaarheid bij andere blokhuts)

## Fallbacks

- Hyper3D Rodin / Hunyuan3D pas inzetten als Polyhaven + Sketchfab niets bruikbaars hebben (custom prop)
- Bij MCP timeout: `execute_blender_code` direct met de bewerking
- Bij eerste-command-fail: opnieuw uitvoeren (bekend issue, zie [[ahujasid blender-mcp]])
