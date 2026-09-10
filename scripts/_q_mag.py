import bpy, sys, re
from mathutils import Vector
F=sys.argv[sys.argv.index("--")+1]
bpy.ops.wm.open_mainfile(filepath=F)
def wbb(o):
    cs=[o.matrix_world @ Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs]; ys=[c.y for c in cs]; zs=[c.z for c in cs]
    return (min(xs),max(xs),min(ys),max(ys),min(zs),max(zs))
print("QM_START")
# roof + barrel + panel + sedum + door
pat=re.compile(r'(roof|flatroof|fascia|Sedum|regenton|barrel|Regenpijp|Paneel|DEURBASIC$|wall-)', re.I)
allmesh=[o for o in bpy.data.objects if o.type=='MESH' and len(o.data.vertices)]
for o in sorted(bpy.data.objects, key=lambda x:x.name):
    if o.type=='MESH' and pat.search(o.name) and len(o.data.vertices):
        b=wbb(o); print(f"  {o.name:30s} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}]")
    elif o.type=='EMPTY' and pat.search(o.name):
        print(f"  {o.name:30s} EMPTY loc{tuple(round(v,2) for v in o.location)}")
# cabin overall footprint from wall-/parentBoard objects
walls=[o for o in allmesh if re.search(r'(wall-|parentBoard|fascia|roofbeam|pole|foundation)', o.name)]
if walls:
    xs=[];ys=[];zs=[]
    for o in walls:
        b=wbb(o); xs+=[b[0],b[1]]; ys+=[b[2],b[3]]; zs+=[b[4],b[5]]
    print(f"  CABIN-SHELL x[{min(xs):.2f},{max(xs):.2f}] y[{min(ys):.2f},{max(ys):.2f}] z[{min(zs):.2f},{max(zs):.2f}]")
# regenton mesh (search children of RZ_mg_regenton)
rt=bpy.data.objects.get("RZ_mg_regenton")
if rt:
    for c in rt.children_recursive:
        if c.type=='MESH' and len(c.data.vertices):
            b=wbb(c); print(f"  [tonkind] {c.name:24s} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}]")
print("QM_END")
