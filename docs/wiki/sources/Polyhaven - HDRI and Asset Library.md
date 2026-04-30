---
type: source
source_type: asset_library
title: "Poly Haven — Free HDRI + Texture + Model Library"
author: "Poly Haven (community-funded, ZA)"
date_published: 2026
url: https://polyhaven.com/
confidence: high
tags:
  - source
  - polyhaven
  - hdri
  - blender
  - assets
related:
  - "[[Polyhaven]]"
  - "[[ahujasid blender-mcp]]"
  - "[[Blender Scene Composition Workflow via MCP]]"
key_claims:
  - "Honderden gratis HDRI's, ready to use, geen login vereist"
  - "Alle assets CC0 (public domain) — commerciële use OK"
  - "16K unclipped HDRI's beschikbaar voor outdoor scenes"
  - "Direct downloadbaar via blender-mcp (Polyhaven integratie)"
---

# Poly Haven — Free HDRI + Asset Library

Community-funded ZA-bedrijf. Alle content CC0 (public domain — geen attributie verplicht, commercial OK). Volledige integratie met blender-mcp via dedicated Polyhaven tools (zie [[ahujasid blender-mcp]]).

## Categorieën relevant voor blokhut-scenes

### HDRI's (lighting + sky)
- **Outdoor > Nature**: bos, weide, berg-omgevingen
- **Outdoor > Garden**: speciaal voor tuin-context (Studio Garden, Symmetrical Garden)
- **Sky-only / dawn / dusk / night**: voor blue hour / golden hour / night shots

### Textures
- Hout (vloer, planken, schors)
- Grond (gras, mos, grind, aarde, sneeuw)
- Steen (natuursteen, leisteen, baksteen)
- Beton, metaal (corten staal!), tegel

### 3D Models
- Bomen (alle seizoenen)
- Planten (varens, struiken, bloemen)
- Tuinmeubilair (banken, tafels)
- Decoratie (lampen, fire pit, etc)

## Bekende garden HDRI's

| Naam | Beschrijving | Use case |
|---|---|---|
| `studio_garden` | Clear midday garden courtyard, sterk zonlicht, harde schaduwen | Cottage tuin, Engelse stijl |
| `symmetrical_garden` | Symmetrische tuin midday, partly cloudy | Modern formele tuin |
| `qwantani_dusk_2` | Sunset met goudgele tinten | Avond / golden hour shots |
| `kloofendal_43d_clear` | Open veld late afternoon | Bos / wildernis context |
| `dancing_hall` of `lebombo` | Indoor/buiten transition | Veranda + terras shots |

## Workflow via blender-mcp

```
search_polyhaven_assets(asset_type="hdris", categories="outdoor,nature")
  → list met asset_id's
download_polyhaven_asset(asset_id="qwantani_dusk_2", asset_type="hdris", resolution="4k")
set_texture(...)
```

Resolutions beschikbaar: 1k / 2k / 4k / 8k / 16k. Voor verkoopvisuals: **4k of 8k** in HDRI volstaat (16k alleen bij extreme close-ups van reflecties).

## Verdict

Eerste stop voor elke buitenscene. CC0 betekent: geen licentie-zorgen voor blokhutwinkel.nl marketing. Combineren met Sketchfab voor specifieke props (tuinmeubels, planten-soorten die Polyhaven niet heeft).
