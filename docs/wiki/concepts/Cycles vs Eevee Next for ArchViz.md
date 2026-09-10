---
type: concept
title: "Cycles vs Eevee Next for ArchViz"
created: 2026-04-30
updated: 2026-04-30
tags:
  - concept
  - blender
  - render
  - cycles
  - eevee
  - archviz
status: current
related:
  - "[[Blender Scene Composition Workflow via MCP]]"
  - "[[HDRMaps - Realistic HDRI Lighting Exterior ArchViz Blender]]"
---

# Cycles vs Eevee Next for ArchViz

Welke render-engine voor blokhut-visuals? Korte versie: **Eevee Next voor preview, Cycles voor finals**.

## Verschillen

| Eigenschap | Cycles | Eevee Next (4.2+) |
|---|---|---|
| **Type** | Path-tracing (physically accurate) | Real-time rasterization + screen-space tricks |
| **Render-tijd** | Minuten per frame | Seconden per frame |
| **HDRI-lighting** | Native, accurate | Goed met Eevee Next, niet perfect |
| **Soft shadows** | Photoreal | Goed maar niet exact |
| **Glossy reflecties** | Accurate | Screen-space (mist off-screen reflecties) |
| **Caustics** | Met add-on | Beperkt |
| **Volumetric (mist, rook)** | Volledig | Beperkt |
| **Foliage / scatter** | Excellent met denoising | OK maar minder fotorealistisch |
| **Subsurface scattering** | Physically based | Approximatie |

## Verdict per use case voor blokhut-scenes

### Cycles verplicht voor
- Hero-shots (product-page cover) — moet photoreal
- Golden hour / dusk renders — accurate global illumination cruciaal
- Avond-scenes met emission lights — volumetric haze + bloom
- Renders met veel reflecties (hottub-water, raamglas)
- Final marketing-output

### Eevee Next prima voor
- Workflow-preview tijdens scene-build (zie via MCP `get_viewport_screenshot`)
- Snelle stijl-iteraties (pak ik design-richting?)
- Storyboard-frames voor user-akkoord vóór final
- Animation previews

## Render-settings voor cabin-finals (Cycles)

```
Resolution: 2560x1440 (high-res print + web)
of 1920x1080 (web-only)
Samples: 256 (genoeg met denoise) tot 1024 (foliage-heavy scenes)
Denoiser: OpenImageDenoise (CPU) of OptiX (NVIDIA GPU)
Adaptive Sampling: ON (threshold 0.01)
Light Tree: ON (Blender 4.0+)
Tile Size: 2048 (GPU) of 32-64 (CPU)
Persistent Data: ON (sneller bij animations)
```

## GPU vs CPU op user laptop

User werkt op MacBook Air M4 (zie [[Research - OpenClaw op MacBook Air M4]]). M4 heeft Metal-acceleratie voor Cycles maar niet OptiX. Bij heavy scenes: 5-10 min/frame realistisch. Voor batch van 8 finale renders per blokhut: ~60-90 min totale render-tijd.

**Alternatief**: cloud render farm (FoxRenderfarm, GarageFarm) bij tijdsdruk. Niet eerste keuze, eerst kijken of M4 het haalt.

## Praktische tip: Render Region

Bij iteratie: render alleen kleine regio (Cycles → Camera → Render Region). Test materiaal/light op 200x200 px voordat full-frame render start. Bespaart 95% iteratie-tijd.

## Color management

- View Transform: **Filmic** (default voor 4.0+) — beste voor photoreal
- Look: **Medium High Contrast** voor product-shots
- Exposure: **0** als HDRI correct geschaald, anders -0.5 tot +0.5 EV
- Niet "Standard" view transform voor archviz — geeft blown-out highlights
