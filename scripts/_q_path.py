import bpy, sys, re
from mathutils import Vector
F=sys.argv[sys.argv.index("--")+1]
bpy.ops.wm.open_mainfile(filepath=F)
def wbb(o):
    cs=[o.matrix_world @ Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return (min(xs),max(xs),min(ys),max(ys),min(zs),max(zs))
PAT=re.compile(r'(flag|paver|slab|pad|cobble|stone|steen|tegel|stap|tobi|eiland|island|zand|sand|kares|mos|loper|bed|grind|gravel|karesansui)',re.I)
print("QP_START")
groups={}
for o in sorted(bpy.data.objects,key=lambda x:x.name):
    if o.type!='MESH' or not len(o.data.vertices): continue
    if not PAT.search(o.name): continue
    b=wbb(o)
    mat=o.material_slots[0].material.name if o.material_slots and o.material_slots[0].material else '<none>'
    key=re.sub(r'[_\.]?\d+$','',o.name)  # group by base name
    groups.setdefault(key,[]).append((o.name,b,mat,len(o.data.vertices)))
for key,items in groups.items():
    xs=[];ys=[];zs=[];mats=set();vt=0
    for n,b,m,v in items:
        xs+=[b[0],b[1]];ys+=[b[2],b[3]];zs+=[b[4],b[5]];mats.add(m);vt+=v
    print(f"  [{key}* x{len(items)}] x[{min(xs):.2f},{max(xs):.2f}] y[{min(ys):.2f},{max(ys):.2f}] z[{min(zs):.2f},{max(zs):.2f}] verts={vt} mats={sorted(mats)}")
print("QP_END")
