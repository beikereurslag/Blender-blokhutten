"""Vind zwevende voorgrond-clusters. Lijst alle parent=None objecten waarvan het
mesh-subtree-zwaartepunt in de voorgrond ligt, met world min_z, hoogte, verts en
dominante materialen. Sorteer op min_z (hoogste zwevers bovenaan).
Run: blender --background scene.blend --python scripts/_probe_floaters.py
"""
import bpy
from mathutils import Vector

def subtree_meshes(o):
    return [o] if o.type == 'MESH' and len(o.data.vertices) else [] \
        + [c for c in o.children_recursive if c.type == 'MESH' and len(c.data.vertices)]

def wbb(ms):
    cs = []
    for m in ms:
        cs += [m.matrix_world @ Vector(c) for c in m.bound_box]
    if not cs: return None
    xs=[c.x for c in cs]; ys=[c.y for c in cs]; zs=[c.z for c in cs]
    return (min(xs),max(xs),min(ys),max(ys),min(zs),max(zs))

SKIP = ("hedge", "pine", "tree", "boom", "wall-", "roof", "flatroof", "fascia", "trim-",
        "parentboard", "scharnier", "ground", "terras", "klinker", "deur", "door", "mist",
        "foundation", "pole-", "slinger", "bulb", "draad", "sun", "cam", "lamp", "light")
rows = []
for o in bpy.data.objects:
    if o.parent is not None:
        continue
    nl = o.name.lower()
    if any(k in nl for k in SKIP):
        continue
    ms = subtree_meshes(o)
    bb = wbb(ms)
    if not bb:
        continue
    cx = (bb[0]+bb[1])/2; cy = (bb[2]+bb[3])/2
    if not (-7 < cx < 7 and 0.5 < cy < 9.0):
        continue
    h = bb[5]-bb[4]; w = max(bb[1]-bb[0], bb[3]-bb[2])
    if w > 8:  # skip giant planes
        continue
    nv = sum(len(m.data.vertices) for m in ms)
    mats = set()
    for m in ms:
        for s in m.material_slots:
            if s.material: mats.add(s.material.name)
    rows.append((bb[4], o.name, round(cx,2), round(cy,2), round(h,2), nv, ",".join(list(mats)[:3])))

print("\n==== FOREGROUND CLUSTERS (sorted by min_z desc) ====")
for minz, nm, cx, cy, h, nv, mats in sorted(rows, reverse=True):
    flag = "  <-- ZWEEFT" if minz > 0.05 else ""
    print(f"  min_z={minz:6.2f} {nm:<28} c=({cx:5.1f},{cy:4.1f}) h={h:4.1f} v={nv:<7} [{mats}]{flag}")
print(f"==== {len(rows)} clusters\n")
