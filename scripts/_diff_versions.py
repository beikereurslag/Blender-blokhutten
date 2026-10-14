"""Compacte fingerprint van een blend om versies te vergelijken (v4 vs v5/v6).
Run: blender -b <blend> --python _diff_versions.py"""
import bpy, os
from mathutils import Vector
scn = bpy.context.scene
objs = list(bpy.data.objects)
meshes = [o for o in objs if o.type == 'MESH']
nverts = sum(len(o.data.vertices) for o in meshes if o.data)
cam = scn.camera
sun = next((o for o in objs if o.type == 'LIGHT' and o.data.type == 'SUN'), None)
lights = [o for o in objs if o.type == 'LIGHT']
# key prefixes
def cnt(pre): return sum(1 for o in objs if o.name.startswith(pre))
world_str = None
if scn.world and scn.world.use_nodes:
    bg = next((n for n in scn.world.node_tree.nodes if n.type == 'BACKGROUND'), None)
    if bg: world_str = round(bg.inputs['Strength'].default_value, 2)
print("FP", os.path.basename(bpy.data.filepath))
print("  objs=%d meshes=%d verts=%d lights=%d colls=%d" % (len(objs), len(meshes), nverts, len(lights), len(bpy.data.collections)))
print("  colls:", sorted(c.name for c in bpy.data.collections)[:14])
if cam:
    e = cam.rotation_euler
    print("  cam loc=(%.2f,%.2f,%.2f) rot=(%.2f,%.2f,%.2f) lens=%.0f shift_y=%.3f" % (
        cam.location.x, cam.location.y, cam.location.z, e.x, e.y, e.z, cam.data.lens, cam.data.shift_y))
if sun:
    print("  sun energy=%.2f rot=(%.2f,%.2f,%.2f) color=%s" % (
        sun.data.energy, sun.rotation_euler.x, sun.rotation_euler.y, sun.rotation_euler.z,
        [round(c, 2) for c in sun.data.color]))
print("  view=%s look=%s exposure=%.2f world_str=%s" % (
    scn.view_settings.view_transform, scn.view_settings.look, scn.view_settings.exposure, world_str))
print("  use_nodes(compositor)=%s" % scn.use_nodes)
print("  prefixes: Grass=%d Lng=%d MwSet=%d Mist=%d GrassEmitter=%d" % (
    cnt("Grass"), cnt("Lng_"), cnt("MwSet"), cnt("Mist"), cnt("GrassEmitter")))
# top-level niet-scatter objecten (grof beeld van dressing)
tops = [o.name for o in objs if o.parent is None and o.type in ('MESH', 'EMPTY')
        and not any(o.name.lower().startswith(p) for p in ('treering', 'birch', 'pine', 'hedge', 'grass', 'wall-', 'roof', 'parentboard', 'flatroof'))]
print("  top-level (max 40):", sorted(tops)[:40])
