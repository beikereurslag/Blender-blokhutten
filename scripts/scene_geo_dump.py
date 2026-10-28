"""Dump per-root-object world-bbox + footprint zonder depsgraph-render.
Run: blender -b --python scene_geo_dump.py -- <blend>
Geen render -> blijft binnen RAM. Helpt placement-diagnose zonder top-down.
"""
import bpy, sys
from mathutils import Vector
argv = sys.argv[sys.argv.index("--")+1:]
BLEND = argv[0]
bpy.ops.wm.open_mainfile(filepath=BLEND)

def root_meshes(o):
    out=[]; st=[o]
    while st:
        x=st.pop()
        if x.type=='MESH': out.append(x)
        st.extend(x.children)
    return out

def wbb(meshes):
    pts=[(m.matrix_world @ Vector(c)) for m in meshes for c in m.bound_box]
    if not pts: return None
    return (min(p.x for p in pts),max(p.x for p in pts),
            min(p.y for p in pts),max(p.y for p in pts),
            min(p.z for p in pts),max(p.z for p in pts))

rows=[]
for o in bpy.data.objects:
    if o.parent is not None: continue
    if o.type in ('LIGHT','CAMERA'): continue
    ms=root_meshes(o)
    if not ms: continue
    bb=wbb(ms)
    if not bb: continue
    cx=(bb[0]+bb[1])/2; cy=(bb[2]+bb[3])/2
    rows.append((o.name,o.type,bb,cx,cy,o.hide_render))

rows.sort(key=lambda r:(r[3],r[4]))
print("=== GEO DUMP (root objects, sorted by x then y) ===")
for name,typ,bb,cx,cy,hr in rows:
    print("OBJ %-26s c=(%.2f,%.2f) x[%.2f..%.2f] y[%.2f..%.2f] z[%.2f..%.2f] %s%s" % (
        name, cx, cy, bb[0],bb[1], bb[2],bb[3], bb[4],bb[5],
        "HIDDEN " if hr else "", typ))
print("COUNT %d" % len(rows))
