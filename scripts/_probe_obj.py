"""Gericht object-probe. Dump objecten waarvan de naam een van de via argv
meegegeven trefwoorden bevat, met world-bbox, parent, collection, verts, mat.
Run:  blender --background scene.blend --python scripts/_probe_obj.py -- kw1 kw2 ...
"""
import bpy, sys
from mathutils import Vector

argv = sys.argv
kws = [k.lower() for k in (argv[argv.index("--")+1:] if "--" in argv else [])]

def wbb(o):
    if o.type == 'MESH' and len(o.data.vertices):
        cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
        xs=[c.x for c in cs]; ys=[c.y for c in cs]; zs=[c.z for c in cs]
        return (min(xs),max(xs),min(ys),max(ys),min(zs),max(zs))
    return None

print("\n==== PROBE kws:", kws, "file:", bpy.data.filepath)
hits = []
for o in bpy.data.objects:
    nl = o.name.lower()
    if kws and not any(k in nl for k in kws):
        continue
    hits.append(o)

# group: show empties (roots) and meshes; skip _m# clutter unless few hits
roots = [o for o in hits if o.type != 'MESH' or '_m' not in o.name.lower()]
show = roots if len(roots) >= 1 and len(hits) > 60 else hits
for o in sorted(show, key=lambda x: x.name)[:80]:
    par = o.parent.name if o.parent else "-"
    b = wbb(o)
    bb = f"wz[{b[4]:.2f},{b[5]:.2f}] wx[{b[0]:.2f},{b[1]:.2f}] wy[{b[2]:.2f},{b[3]:.2f}]" if b else "(no-mesh)"
    nv = len(o.data.vertices) if o.type == 'MESH' else 0
    mat = o.material_slots[0].material.name if (o.type=='MESH' and o.material_slots and o.material_slots[0].material) else "-"
    print(f"  {o.name:<34} {o.type:<5} loc=({o.location.x:6.2f},{o.location.y:6.2f},{o.location.z:6.2f}) "
          f"par={par:<18} {bb} v={nv} mat={mat}")
print(f"==== {len(hits)} hits ({len(show)} shown)\n")
