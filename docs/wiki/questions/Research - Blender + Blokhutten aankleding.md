---
type: synthesis
title: "Research: Blender + Blokhutten Aankleding voor Verkoopvisuals"
created: 2026-04-30
updated: 2026-04-30
tags:
  - research
  - blender
  - blokhutten
  - blokhutwinkel
  - visuals
  - mcp
status: developing
related:
  - "[[Blender Scene Composition Workflow via MCP]]"
  - "[[Garden Style Palette for Cabin Visuals]]"
  - "[[Custom Asset Import via execute_blender_code]]"
  - "[[Geometry Nodes Scattering for Outdoor Scenes]]"
  - "[[Cycles vs Eevee Next for ArchViz]]"
  - "[[Blokhutwinkel.nl]]"
  - "[[Polyhaven]]"
  - "[[Sketchfab]]"
sources:
  - "[[Blokhutwinkel.nl - Product Categories]]"
  - "[[Polyhaven - HDRI and Asset Library]]"
  - "[[Sketchfab - CC Library]]"
  - "[[HDRMaps - Realistic HDRI Lighting Exterior ArchViz Blender]]"
  - "[[ahujasid blender-mcp]]"
---

# Research: Blender + Blokhutten Aankleding voor Verkoopvisuals

## Overview

User maakt verkoopvisuals voor blokhutwinkel.nl: één blokhut tonen in **3-4 verschillende tuinscènes** om de veelzijdigheid te demonstreren. Oorspronkelijke aanpak (Twinmotion) wordt vervangen door **Blender + Claude via blender-mcp**, omdat de MCP-integratie samen-werken in real-time mogelijk maakt. User werkt visueel mee in Blender (niet headless), Claude stuurt via MCP-tools en `execute_blender_code`.

## Key Findings

### Track 1 — Blender MCP Workflow (zie [[Blender Scene Composition Workflow via MCP]])

- **blender-mcp v1.5.5** (ahujasid) is volwassen en stabiel voor scene-composition; minder geschikt voor parametrische CAD (Source: [[ahujasid blender-mcp]])
- **Geen native import-tool** voor user-files — gebruik `execute_blender_code` met `bpy.ops.import_scene.fbx/obj/gltf` of `bpy.data.libraries.load` voor .blend (Source: [[Custom Asset Import via execute_blender_code]])
- **Iteratie-loop**: `get_viewport_screenshot` na elke wijziging → user goedkeuring → volgende stap. User is visueel meekijkend (zie [[feedback_3dprint_blender_workflow]])
- **Telemetry uit** via `DISABLE_TELEMETRY=true` env var (anders gaan prompts/code/screenshots naar Ahuja)
- **Eerste-command-fail** is bekend issue, simpel opnieuw uitvoeren

### Track 2 — Tuin/Landschap Stijlen (zie [[Garden Style Palette for Cabin Visuals]])

9 stijlen gedocumenteerd, met **specifieke planten/materialen/props/HDRI per stijl**:

1. **Modern Minimalist** — corten staal, siergrassen, beton, Acer als sculpturale solitair (Source: Calibre/Doika)
2. **English Cottage** — hollyhocks, delphiniums, lupins, klimrozen 'Graham Thomas', smeedijzer (Source: BBC Gardeners' World, Monrovia)
3. **Scandinavian** — berken, mos, Shou Sugi Ban gevel, hottub, fire pit (Source: Honka, Dwell)
4. **Forest / Wilderness** — dichte begroeiing, varens, paddenstoelen, hangmat, kano
5. **Terras + Hot Tub** — ipe-vlonder, pampasgras, string-lights, ronde hottub (Source: HGTV, Bullfrog Spas)
6. **Japanese Zen** — geraakt grind, japanse esdoorn, mos, bamboe, granieten lantaarn (Source: Wikipedia Japanese dry garden, Nero Tapware)
7. **Boerderij / Landelijk** — moestuin, kippen, fruitbomen, kruiwagen, smeedijzer hek
8. **Golden Hour mood** (overlay over andere stijlen) — warm HDRI, sun strength 2-3, EV -0.5
9. **Winter / Sneeuw** — sneeuwscatter, bevroren takken, rookpluim, kerst-krans

**Stijl-product matchmaker** (zie [[Blokhutwinkel.nl - Product Categories]]):
- Sauna-chalet → Scandi + Hottub
- Tuinkantoor → Modern Minimalist
- Kapschuur/garage → Boerderij
- Pipowagen → Bos
- Paviljoen/priëel → Cottage of Japans-Zen
- Veranda → Terras + Lounge

### Track 3 — Asset-bronnen + Lighting (zie [[Polyhaven]], [[Sketchfab]])

- **Polyhaven**: CC0 (public domain), HDRI's + textures + models — eerste stop. Specifieke garden HDRI's: `studio_garden_4k`, `symmetrical_garden_4k`. Resolutions tot 16k beschikbaar (Source: [[Polyhaven - HDRI and Asset Library]])
- **Sketchfab**: 600.000+ CC-licensed models. **Filter op CC0 of CC BY** voor commercial gebruik — CC BY-NC is no-go voor blokhutwinkel-marketing. Curated CC0 lijst van Thomas Flynn (Source: [[Sketchfab - CC Library]])
- **Hyper3D Rodin / Hunyuan3D**: AI-gegenereerde models als laatste redmiddel voor missende custom props
- **Geometry Nodes scatter** (Blender 3.0+) verslaat oude particle system voor gras/foliage; vertex-group als density-mask om paden vrij te houden (Source: [[Geometry Nodes Scattering for Outdoor Scenes]])
- **Cycles vereist** voor finals (photoreal, accurate HDRI-lighting). Eevee Next prima voor previews tijdens scene-build (Source: [[Cycles vs Eevee Next for ArchViz]], [[HDRMaps - Realistic HDRI Lighting Exterior ArchViz Blender]])
- **Render-tijd op M4 MacBook**: ~5-10 min/frame met Cycles bij 256 samples + denoise. Batch van 8 finals per blokhut: ~60-90 min totaal

### Track 4 — Blokhutwinkel.nl Productcontext (zie [[Blokhutwinkel.nl]])

- 9 productcategorieën, 100+ modellen showroom, 10.000+ totaal aanbod
- Materialen: vurenhout (basis) en Douglas/lariks (premium, donkerder)
- 9 dakstijlen: plat (modern), zadel (cottage), wolfeind (chalet), paviljoen (Aziatisch)
- **Eigen 3D-tekening service is technisch (CAD-style)** — onze meerwaarde = sfeer + omgeving + meerdere stijlen per product

## Aanbevolen aanpak (als bestanden binnenkomen)

```
1. User dropt blokhut-bestand in ~/Documents/event-branding/blokhutten/_input/
2. Ik importeer via execute_blender_code (FBX/OBJ/glTF/.blend)
3. Schaal + oriëntatie + origin valideren
4. Kies 3-4 stijlen uit de Style Palette die bij dit specifieke product passen
5. Per stijl:
   a. Polyhaven HDRI download
   b. Ground plane + texture
   c. Major elements (bomen, struiken — handmatig)
   d. Geometry Nodes scatter (gras, kleine planten)
   e. Hardscape + props (Sketchfab CC0/CC BY)
   f. Lighting finalisatie (HDRI + sun + practicals)
   g. Camera setup (1.6m hoogte, 35-50mm lens, 1/3 compositie)
   h. Eevee preview screenshot → user-akkoord
   i. Cycles final render (2560x1440, 256 samples + OIDN)
6. Output: ~/Documents/event-branding/blokhutten/<product>/style-X/
7. 6-8 finale renders per blokhut (3-4 stijlen × 2 angles)
```

## Key Entities

- [[Blokhutwinkel.nl]] — klant / opdrachtgever, leverancier brondata
- [[Polyhaven]] — primaire CC0 asset-bron (HDRI/textures/models)
- [[Sketchfab]] — secundaire asset-bron voor specifieke modellen (filter CC0/CC BY)
- [[ahujasid blender-mcp]] — de bridge tool tussen Claude en Blender

## Key Concepts

- [[Blender Scene Composition Workflow via MCP]] — de iteratie-loop tussen Claude en user
- [[Garden Style Palette for Cabin Visuals]] — de 9 stijlen-matrix
- [[Custom Asset Import via execute_blender_code]] — workaround voor missende import-tool
- [[Geometry Nodes Scattering for Outdoor Scenes]] — moderne scatter-aanpak voor foliage
- [[Cycles vs Eevee Next for ArchViz]] — render-engine keuze per use case

## Contradictions

Geen harde contradicties tussen sources. Wel een licht spanningsveld:

- **Sketchfab quality vs commerciële licenties**: hoogste quality models op Sketchfab zijn vaak NIET CC0/CC BY (paid royalty-free). Voor blokhutwinkel-marketing moeten we accepteren dat we soms iets lagere quality krijgen of moeten betalen voor specifieke premium props. Polyhaven dekt dit deels op met hun CC0 model-collectie maar mist breedte.

## Open Questions

- **Welk format komen de blokhuts binnen?** SketchUp (.skp), FBX, .blend, .obj? Bepaalt importpipeline.
- **Schaal-conventie van blokhutwinkel-bestanden?** Meters, mm, of inches? Validatie nodig na eerste import.
- **Hebben we de blokhut-models met materialen + textures, of alleen mesh?** Ontbrekende textures = werk voor Polyhaven hout-substituten.
- **Hoeveel blokhuts in batch?** 1-2 als pilot of 10+ direct? Bepaalt of we templated approach moeten doen.
- **Render-target resolutie**: web-only (1920x1080), print + web (2560x1440), of 4K (3840x2160)?
- **Brand-rules voor blokhutwinkel** (kleur, logo-placement, watermerk)? Onbekend — vragen aan user.

## Sources

- [[Blokhutwinkel.nl - Product Categories]] — 2026 | productcatalogus + 3D-service info
- [[Polyhaven - HDRI and Asset Library]] — 2026 | CC0 asset-bron, MCP-integratie
- [[Sketchfab - CC Library]] — 2026 | 600K+ CC-licensed models, license-matrix
- [[HDRMaps - Realistic HDRI Lighting Exterior ArchViz Blender]] — 2024 | Cycles HDRI workflow, Mix Shader trick
- [[ahujasid blender-mcp]] — 2025 | reference MCP server, tool-set, security caveats
