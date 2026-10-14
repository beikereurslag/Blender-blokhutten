"""Raycast vanuit camera door beeld-pixels om object+materiaal te identificeren.
Gebruik: blender -b --python scripts/_probe_ray.py -- <scene.blend> <resx> <resy> <px,py> [<px,py> ...]
px,py in pixels (0,0 = top-left).
"""
import bpy, sys
from mathutils import Vector
argv = sys.argv; a = argv[argv.index("--")+1:]
F = a[0]; RX = int(a[1]); RY = int(a[2]); pts = a[3:]
bpy.ops.wm.open_mainfile(filepath=F)
scn = bpy.context.scene
dg = bpy.context.evaluated_depsgraph_get()
cam = scn.camera
corners = cam.data.view_frame(scene=scn)   # [TR, BR, BL, TL] in cam-local at depth -1
mw = cam.matrix_world
TR, BR, BL, TL = [mw @ c for c in corners]
org = mw.translation

def ray_through(px, py):
    u = px / RX                # 0..1 left->right
    v = 1.0 - (py / RY)        # 0..1 bottom->top
    top = TL.lerp(TR, u)
    bot = BL.lerp(BR, u)
    target = bot.lerp(top, v)
    d = (target - org).normalized()
    hit, loc, nrm, idx, obj, mat = scn.ray_cast(dg, org, d)
    if not hit:
        return f"  px({px},{py}) u={u:.3f} v={v:.3f} -> NO HIT"
    o = bpy.data.objects.get(obj.name)
    mname = "?"
    if o and o.material_slots and 0 <= idx < len(o.data.polygons):
        midx = o.data.polygons[idx].material_index if idx < len(o.data.polygons) else 0
        if midx < len(o.material_slots) and o.material_slots[midx].material:
            mname = o.material_slots[midx].material.name
    allmats = [s.material.name if s.material else '<none>' for s in (o.material_slots if o else [])]
    return (f"  px({px},{py}) -> HIT {obj.name}  faceMat={mname}  loc=({loc.x:.2f},{loc.y:.2f},{loc.z:.2f})  "
            f"dist={(loc-org).length:.1f}  slots={allmats}")

print("PROBE_START", F, "res", RX, RY)
for p in pts:
    px, py = [int(x) for x in p.split(",")]
    print(ray_through(px, py))
print("PROBE_END")
