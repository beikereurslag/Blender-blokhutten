---
type: source
source_type: asset_library
title: "Sketchfab — Creative Commons 3D Model Library"
author: "Sketchfab (Epic Games)"
date_published: 2026
url: https://sketchfab.com/features/free-3d-models
confidence: high
tags:
  - source
  - sketchfab
  - 3d-models
  - blender
  - assets
related:
  - "[[Sketchfab]]"
  - "[[ahujasid blender-mcp]]"
  - "[[Polyhaven - HDRI and Asset Library]]"
key_claims:
  - "600.000+ gratis CC-licensed 3D modellen"
  - "Licenties variëren: CC BY, CC BY-NC (geen commercieel), CC0 (public domain)"
  - "Filter op licentie nodig voor commerciële use"
  - "MCP-integratie via blender-mcp: search_sketchfab_models + download_sketchfab_model"
---

# Sketchfab — Creative Commons Library

Het grootste publieke 3D-model platform. Eigendom van Epic Games sinds 2021. Volledige integratie via blender-mcp (zie [[ahujasid blender-mcp]]).

## Licentie-realiteit (kritiek voor commercial use)

| Licentie | Commercial OK? | Attribution? | Kan onbeperkt gebruikt? |
|---|---|---|---|
| **CC0** | ✅ Ja | ❌ Niet vereist | ✅ Vrij |
| **CC BY** | ✅ Ja | ✅ Verplicht | ✅ |
| **CC BY-SA** | ⚠️ Ja, maar afgeleide werk moet ook CC BY-SA | ✅ | ⚠️ Viral |
| **CC BY-NC** | ❌ Nee | ✅ | ❌ Voor blokhut-marketing onbruikbaar |
| **CC BY-ND** | ⚠️ Geen modificaties toegestaan | ✅ | ⚠️ Ongeschikt voor scene-aanpassing |

**Voor blokhutwinkel.nl visuals**: filter op **CC0** of **CC BY** alléén. CC BY-NC is een no-go.

## Curatie-tip: Thomas Flynn's CC0 collectie

User `nebulousflynn` (Sketchfab community manager) onderhoudt een [CC0-collectie](https://sketchfab.com/nebulousflynn/collections/cc0-9e9b8c5442ab4b59ba16b6fa5e43b8da) met goed gecureerde public-domain modellen — eerste plek om te zoeken.

## Use case voor cabin-scenes

Polyhaven dekt textures + HDRI + algemene props. Sketchfab pakken we voor specifieke modellen die Polyhaven mist:

- Specifieke plant-soorten (klimrozen, hortensia, japanse esdoorn)
- Tuinmeubels in specifieke stijlen (Adirondack chair, Scandinavisch teakhouten lounge, Japans bamboe)
- Decoratie (lantaarns, fire pit, vogelhuisjes, kippen voor boerderij-stijl)
- Voertuigen (auto bij carport, fiets, boot in cottage-vijver)
- Personen (alleen 1-2 silhouetten op afstand, geen close-up gezichten — match brand rule "minimal people")

## Workflow via blender-mcp

```
search_sketchfab_models(query="english climbing rose", downloadable=true)
  → check licenses in result
download_sketchfab_model(uid="...")
  → import in scene
```

## Caveats

- Quality varieert wild (CC0 modellen zijn vaak game-asset niveau, niet always photoreal)
- Model schaal vaak fout (niet in meters) — altijd controleren in Blender en `global_scale` aanpassen
- Sommige downloads zijn .fbx, anderen .glb of .obj — blender-mcp handelt het meestal af
