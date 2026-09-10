---
type: concept
title: "Custom Asset Import via execute_blender_code"
created: 2026-04-30
updated: 2026-04-30
tags:
  - concept
  - blender
  - mcp
  - python
  - import
status: current
related:
  - "[[ahujasid blender-mcp]]"
  - "[[Blender Scene Composition Workflow via MCP]]"
---

# Custom Asset Import via execute_blender_code

Blender-mcp heeft **geen dedicated tool** voor het importeren van een door user geleverd .blend / .fbx / .obj / .skp bestand. Workaround: arbitrary Python via `execute_blender_code`. Dit is essentieel omdat de blokhuts van blokhutwinkel.nl als custom file binnenkomen.

## Bestandstypes en bijbehorende ops

```python
import bpy

# FBX (meest waarschijnlijk vanuit CAD/SketchUp export)
bpy.ops.import_scene.fbx(
    filepath="/path/blokhut.fbx",
    global_scale=1.0,
    use_anim=False,
    axis_forward='-Z',
    axis_up='Y'
)

# OBJ
bpy.ops.import_scene.obj(
    filepath="/path/blokhut.obj",
    global_clamp_size=0,
    axis_forward='-Z',
    axis_up='Y'
)

# .blend (append objects)
with bpy.data.libraries.load("/path/blokhut.blend", link=False) as (data_from, data_to):
    data_to.objects = data_from.objects
for obj in data_to.objects:
    if obj is not None:
        bpy.context.collection.objects.link(obj)

# SKP (SketchUp) — vereist add-on of pre-converted FBX/OBJ
# Geen native bpy.ops voor .skp — vraag user om export naar FBX in SketchUp

# glTF / GLB (modern web standard, ook van Sketchfab)
bpy.ops.import_scene.gltf(filepath="/path/blokhut.glb")

# DAE (Collada, oudere format)
bpy.ops.wm.collada_import(filepath="/path/blokhut.dae")
```

## Schaal-validatie na import

```python
import bpy
imported = [o for o in bpy.context.selected_objects if o.type == 'MESH']
for obj in imported:
    # Bounding box dimensies
    dims = obj.dimensions
    print(f"{obj.name}: {dims.x:.2f} x {dims.y:.2f} x {dims.z:.2f} m")
```

Als blokhut 1000x kleiner of groter dan verwacht: `global_scale` aanpassen of `obj.scale = (0.001, 0.001, 0.001)` daarna `bpy.ops.object.transform_apply(scale=True)`.

## Oriëntatie-fix

Blokhutwinkel-tools exporteren vaak met Z-up of Y-up afhankelijk van bron-software. Standaard in Blender = Z-up.

```python
# Roteren naar +Y forward (voorgevel kijkt naar camera vanuit zuid)
import math
obj.rotation_euler[2] = math.radians(180)  # of 90, afhankelijk
bpy.ops.object.transform_apply(rotation=True)
```

## Materialen-fallback

Geïmporteerde modellen hebben vaak basic materials of geen textures (broken texture paths). Controle:

```python
for slot in obj.material_slots:
    print(slot.material.name if slot.material else "EMPTY")
```

Bij missing textures: 
- Hout-textures van Polyhaven aanvragen en handmatig toepassen
- Hyper3D Rodin als laatste redmiddel voor missende custom props

## Origin reset

Geïmporteerde objects hebben origin vaak op (0,0,0) van bron-file, niet aan basis van blokhut. Reset:

```python
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
# Verplaats naar wereld-origin
obj.location = (0, 0, 0)
```

## Workflow samengevat

1. User dropt bestand op een vaste path (bijv. `~/Documents/event-branding/blokhutten/_input/`)
2. Ik run `execute_blender_code` met juiste `bpy.ops.import_scene.<format>()`
3. Validate met `get_scene_info()`
4. Schaal + oriëntatie + origin via één extra `execute_blender_code` block
5. Verder met scene-composition (zie [[Blender Scene Composition Workflow via MCP]])
