---
type: entity
entity_type: organization
title: "Sketchfab"
created: 2026-04-30
updated: 2026-04-30
tags:
  - entity
  - asset-library
  - 3d-models
status: current
related:
  - "[[Sketchfab - CC Library]]"
  - "[[ahujasid blender-mcp]]"
---

# Sketchfab

Het grootste publieke 3D-model platform op het web. Eigendom van Epic Games sinds 2021. 600.000+ Creative Commons-licensed modellen vrij beschikbaar; nog veel meer onder commerciële licenties.

## License-realiteit (kritiek!)

Niet alles op Sketchfab is gratis voor commerciële use:

| License | Commercial OK? | Voor blokhut-marketing |
|---|---|---|
| CC0 | ✅ Ja | ✅ Beste keuze |
| CC BY | ✅ Ja, attribution | ✅ OK |
| CC BY-SA | ⚠️ Viral | ⚠️ Vermijd |
| CC BY-NC | ❌ Nee | ❌ NIET gebruiken |
| CC BY-ND | ❌ Geen modificaties | ❌ NIET gebruiken |
| Royalty-free (paid) | ✅ Per license | Backup-optie |

## Integraties

- **Blender Add-on**: official Sketchfab plugin, browse + download in viewport
- **blender-mcp**: `search_sketchfab_models`, `download_sketchfab_model`, `get_sketchfab_model_preview`, `get_sketchfab_status` (zie [[ahujasid blender-mcp]])

## Curator-tip

[Thomas Flynn (nebulousflynn) CC0 collection](https://sketchfab.com/nebulousflynn/collections/cc0-9e9b8c5442ab4b59ba16b6fa5e43b8da) — Sketchfab community manager onderhoudt een gecureerde CC0 lijst, eerste plek om te zoeken naar safe assets.

## Use case voor cabin-scenes

Specifiek-stilistische modellen die Polyhaven niet heeft:
- Specifieke planten (japanse esdoorn, klimrozen, hortensia, pampas)
- Tuinmeubels in stijl (Adirondack chair, scandi lounge, japans bamboe)
- Decoratie (lantaarns, fire pits, hottubs, kippen, vogelhuisjes)
- Voertuigen (oldtimer, fiets, kano)

## Beperkingen

- Quality varieert wild (CC0 vaak game-asset niveau)
- Schaal vaak fout (niet meters) — altijd `dimensions` checken na import
- Sommige modellen hebben broken texture-paths
