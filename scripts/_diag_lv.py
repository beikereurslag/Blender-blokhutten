import bpy, math
from mathutils import Vector
F=r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Lavendel-400x300-400-zijwand\style-mediterraan\lavendel_lavendelveld.blend"
bpy.ops.wm.open_mainfile(filepath=F)
def bb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]; xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
print("LV_START")
print("CAM", bpy.context.scene.camera.name, tuple(round(v,2) for v in bpy.context.scene.camera.location))
print("== POTTEN / TERRAS / STOEP / PAD / EDGE ==")
for o in sorted(bpy.data.objects,key=lambda x:x.name):
    n=o.name.lower()
    if any(k in n for k in ('pot','terras','stoep','deur','door','lvpath','lvedge','flag','vloer','floor')):
        if o.type=='MESH' and len(o.data.vertices):
            b=bb(o); mats=[m.name for m in o.data.materials]
            print(f"  {o.name:26s} MESH x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.3f},{b[5]:.3f}] {mats}")
        else:
            print(f"  {o.name:26s} {o.type} loc{tuple(round(v,2) for v in o.location)}")
print("== CABIN-FOOTPRINT (wall/pole/parentBoard front-y) ==")
ys=[]
for o in bpy.data.objects:
    n=o.name.lower()
    if o.type=='MESH' and any(k in n for k in ('wall','pole','parentboard','fascia')):
        b=bb(o); ys.append((o.name,b))
for nm,b in ys[:6]: print(f"  {nm:30s} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}]")
xs=[b[0] for _,b in ys]+[b[1] for _,b in ys]; yy=[b[2] for _,b in ys]+[b[3] for _,b in ys]
if xs: print(f"  -> cabin x[{min(xs):.2f},{max(xs):.2f}] y[{min(yy):.2f},{max(yy):.2f}]")
print("== LAVENDEL clusters ==")
lav=[o for o in bpy.data.objects if 'lavendel' in o.name.lower() or o.name.lower().startswith('lav')]
roots=[o for o in lav if o.type=='EMPTY']
print(f"  lav-objs={len(lav)} roots(empty)={len(roots)}")
for o in roots[:8]: print(f"    {o.name} loc{tuple(round(v,2) for v in o.location)} scale{tuple(round(v,2) for v in o.scale)}")
# lavendel materiaal
lm=set()
for o in lav:
    for s in getattr(o,'material_slots',[]):
        if s.material: lm.add(s.material.name)
print("  lav-materials:", lm)
print("== BOMEN: pine top-level objecten ==")
pine=[o for o in bpy.data.objects if o.type=='MESH' and 'pine' in o.name.lower() and not o.parent]
print(f"  pine top-level mesh count={len(pine)}")
import collections
kinds=collections.Counter()
for o in pine:
    nm=o.name.lower()
    k='needle' if 'needle' in nm else ('twig' if 'twig' in nm else ('deadbranch' if 'dead_branch' in nm else ('branch' if 'branch' in nm else ('trunk' if 'trunk' in nm else ('lod' if 'lod' in nm else 'other')))))
    kinds[k]+=1
print("  pine-part kinds:", dict(kinds))
print("  collections:", [(c.name,len(c.objects)) for c in bpy.data.collections])
print("LV_END")
