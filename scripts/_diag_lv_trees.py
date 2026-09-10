import bpy
from mathutils import Vector
F=r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Lavendel-400x300-400-zijwand\style-mediterraan\lavendel_lavendelveld.blend"
bpy.ops.wm.open_mainfile(filepath=F)
def bb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box];zs=[c.z for c in cs];xs=[c.x for c in cs];ys=[c.y for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
print("TR_START")
import collections
vis=collections.Counter(); hid=collections.Counter()
rows=[]
for o in bpy.data.objects:
    if o.type!='MESH': continue
    n=o.name.lower()
    if 'pine' not in n and 'tree' not in n and 'jacar' not in n: continue
    k='needle' if 'needle' in n else('twig' if 'twig' in n else('deadbr' if 'dead_branch' in n else('branch' if 'branch' in n else('trunk' if 'trunk' in n else('leaf' if 'leaf' in n or 'leaves' in n else('lod' if 'lod' in n else 'other'))))))
    hr=o.hide_render
    (hid if hr else vis)[k]+=1
    b=bb(o)
    rows.append((o.name,k,hr,o.hide_viewport,round(b[5]-b[4],1),round(b[5],1)))
print("VISIBLE (render) per kind:", dict(vis))
print("HIDDEN (render) per kind:", dict(hid))
print("-- objecten die in render zichtbaar zijn, gesorteerd op hoogte (top=tall bomen) --")
for nm,k,hr,hv,h,top in sorted([r for r in rows if not r[2]], key=lambda r:-r[4])[:30]:
    print(f"  {nm:34s} kind={k:7s} h={h:4} top={top:4} hide_vp={hv}")
print("TR_END")
