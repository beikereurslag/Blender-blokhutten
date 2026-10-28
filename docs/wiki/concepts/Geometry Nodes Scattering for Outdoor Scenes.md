---
type: concept
title: "Geometry Nodes Scattering for Outdoor Scenes"
created: 2026-04-30
updated: 2026-04-30
tags:
  - concept
  - blender
  - geometry-nodes
  - scattering
  - foliage
status: current
related:
  - "[[Blender Scene Composition Workflow via MCP]]"
  - "[[Garden Style Palette for Cabin Visuals]]"
  - "[[Cycles vs Eevee Next for ArchViz]]"
---

# Geometry Nodes Scattering for Outdoor Scenes

Voor cabin-tuin-scenes: handmatig elke graspol of bloem plaatsen is onbegonnen werk. Geometry Nodes (Blender 3.0+) is de moderne aanpak — flexibeler en performanter dan oude particle system.

## Core node-pattern

```
[Geometry Input] 
  → Distribute Points on Faces (density, seed)
  → Instance on Points (instance: collection van plant-meshes)
  → [Geometry Output]
```

## Density-control

Cruciaal voor realisme: niet uniform scatteren. Drie maskering-technieken:

### 1. Vertex group als density-mask
- Paint een vertex group op grond-plane (1.0 waar gras moet, 0.0 op pad)
- Multiply met `Distribute Points on Faces` density input

### 2. Texture-driven density
- Noise Texture node → Density input
- Maakt "patchy" verdeling (sommige plekken vol, andere kaal)

### 3. Geometry-based mask
- Distance from path-curve > X meter → density 1.0, anders 0.0
- Resultaat: gras stopt automatisch bij paden

## Variatie per stijl

| Stijl | Scatter techniek |
|---|---|
| **Modern minimalist** | Lage density gras + losse blokken siergrassen handmatig op vaste posities |
| **Cottage** | Hoge density bloemenchaos, mix van 5-7 plant-types in instance collection |
| **Scandinavisch** | Gemiddeld gras + losse mos-patches + scatter van varens onder bomen |
| **Bos / wildernis** | Gelaagd: grote bomen handmatig (5-10), middelgrote struiken scatter (medium density), klein gras + varens (hoge density) |
| **Japans-zen** | GEEN gras-scatter op grind — alleen mos-patches handmatig + raked-pattern in grind-texture |
| **Boerderij** | Moestuin-bedden: rij-patroon (gridden niet random scatter) voor groenten |

## Performance-tip

Scatter-instances worden in Cycles render-tijd gerealiseerd. 100.000+ grasprietjes = mogelijk. **Maar**: bewaar high-poly meshes voor close-ups. Voor distance: low-poly versies + LOD-trick met `Switch by Distance`.

## Ready-made addons als alternatief

Als handmatig scatten te veel werk:
- **Botaniq** (gratis tier) — door Polygoniq, kant-en-klare scatter-presets
- **Graswald** — premium maar fotorealistisch
- **Real Grass** addon

Voor blokhut-visuals: Geometry Nodes vanaf scratch is genoeg (we hebben tijd in Blender, niet productiedruk zoals games).

## Volgorde bij scene-build

1. Eerst grond-plane subdividen (200x200 vertices voor 40x40m plane)
2. Vertex-group painten (waar wel/geen scatter)
3. Geometry Nodes modifier toevoegen op plane
4. Plant-collection vullen (5-10 types, juiste schaal in meters)
5. Density tunen via viewport (preview met Eevee)
6. Final render met Cycles
