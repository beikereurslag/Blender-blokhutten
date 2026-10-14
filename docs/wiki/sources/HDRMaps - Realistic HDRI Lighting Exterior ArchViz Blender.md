---
type: source
source_type: tutorial_blog
title: "HDRMaps — Realistic HDRI Lighting for Exterior ArchViz in Blender"
author: "HDRMaps"
date_published: 2024
url: https://hdrmaps.com/blog/realistic-hdri-lighting-for-exterior-archviz-in-blender/
confidence: medium
tags:
  - source
  - blender
  - hdri
  - lighting
  - archviz
related:
  - "[[Polyhaven - HDRI and Asset Library]]"
  - "[[Cycles vs Eevee Next for ArchViz]]"
  - "[[Blender Scene Composition Workflow via MCP]]"
key_claims:
  - "Cycles vereist voor correcte HDRI-lighting in arch-viz"
  - "Mix Shader + Light Path Node trick: scherp HDRI in reflecties, soft in achtergrond"
  - "IES profiles voor accent-licht naast HDRI verhoogt realisme"
---

# HDRMaps — Realistic HDRI Lighting for Exterior ArchViz

Tutorial-blog gericht op architectural visualization workflow. Niet peer-reviewed maar praktisch correct — bruikbaar voor onze cabin-scene aanpak.

## Kerntechniek: HDRI als hoofdlichtbron

1. World tab → Surface → enable Use Nodes → Background
2. Color → Environment Texture → load `.exr` of `.hdr` file (van Polyhaven)
3. Strength: 1.0 default, soms 0.5-2.0 om matching met scene-exposure

## Mix Shader trick (Light Path Node)

Probleem: HDRI mooi voor lighting, maar achtergrond ziet er goedkoop uit (lage resolutie, of compositie matched niet met scene).

Oplossing:
- 2 Environment Textures: één scherp (voor reflecties + lighting), één blurred of solid color (voor achtergrond)
- Mix Shader gestuurd door Light Path → Is Camera Ray
- Camera ziet de soft achtergrond, maar reflecties + indirect light gebruiken de scherpe HDRI

## Aanvullende lichtbronnen

Voor hero-shots niet alleen HDRI — aanvulling:
- **Sun light** met hoek matching de HDRI sun position (anders dubbele schaduwen)
- **Area lights** voor accent op gevel of voordeur
- **IES profiles** voor lampjes / spot-verlichting in avond-scenes

## Render-tijd tips

- Adaptive sampling aan (saved 30-50% render-tijd)
- Denoising: OpenImageDenoise of OptiX (bij NVIDIA GPU)
- Light Tree (Blender 4.0+) voor scenes met veel lichtbronnen — auto-importance-sampling

## Concrete settings voor blokhut-scenes

| Tijd-of-day | HDRI keuze | Sun strength | Camera exposure |
|---|---|---|---|
| Golden hour | `qwantani_dusk_2` of `the_sky_is_on_fire` | 2.0-3.0 | -0.5 EV |
| Overcast / soft | `rural_landscape_4k` | 0 (HDRI bevat sun) | 0 EV |
| Blue hour | `kloppenheim_03` | 1.0 (warm tint) | -0.3 EV |
| Night + practicals | dark HDRI + window emission | 0.1 | +0.7 EV |

## Verdict

Cycles is verplicht voor photoreal externe arch-viz. Eevee Next kan voor preview maar mist accurate global illumination van HDRI's bij complex foliage.
