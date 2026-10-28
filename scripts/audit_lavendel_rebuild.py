"""Headless audit van een .blend: schaal, strays, missing textures, camera.
Run: blender.exe -b <file.blend> --python audit_lavendel_rebuild.py
"""
import bpy, os, json
from mathutils import Vector

sc = bpy.context.scene
rep = {
    "file": bpy.data.filepath,
    "objects": len(bpy.data.objects),
    "engine": sc.render.engine,
    "res": [sc.render.resolution_x, sc.render.resolution_y],
    "samples": getattr(sc.cycles, "samples", None) if sc.render.engine == 'CYCLES' else None,
    "active_camera": sc.camera.name if sc.camera else None,
    "cameras": [o.name for o in bpy.data.objects if o.type == 'CAMERA'],
    "materials": len(bpy.data.materials),
}

vis = [o for o in bpy.data.objects if o.type == 'MESH' and o.visible_get()]
mn = Vector((1e9,) * 3); mx = Vector((-1e9,) * 3)
for o in vis:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        for i in range(3):
            mn[i] = min(mn[i], w[i]); mx[i] = max(mx[i], w[i])
rep["visible_meshes"] = len(vis)
rep["world_size"] = [round(mx[i] - mn[i], 2) for i in range(3)]
rep["z_range"] = [round(mn.z, 2), round(mx.z, 2)]

# strays: ver onder grond of ver buiten 40m
strays = []
for o in vis:
    loc = o.matrix_world.translation
    if loc.z < -2 or abs(loc.x) > 40 or abs(loc.y) > 40:
        strays.append([o.name, round(loc.x, 1), round(loc.y, 1), round(loc.z, 1)])
rep["stray_count"] = len(strays)
rep["strays"] = strays[:25]

# missing textures
missing = []
packed = 0
for img in bpy.data.images:
    if img.packed_file:
        packed += 1
        continue
    if img.source == 'FILE' and img.filepath:
        if not os.path.exists(bpy.path.abspath(img.filepath)):
            missing.append(img.name)
rep["packed_images"] = packed
rep["total_images"] = len(bpy.data.images)
rep["missing_image_count"] = len(missing)
rep["missing_images"] = missing[:25]

print("AUDIT_JSON_START")
print(json.dumps(rep, indent=2))
print("AUDIT_JSON_END")
