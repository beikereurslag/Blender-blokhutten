import bpy, sys, re
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
F=sys.argv[sys.argv.index("--")+1]
bpy.ops.wm.open_mainfile(filepath=F)
scn=bpy.context.scene; cam=scn.camera
def wbb(o):
    cs=[o.matrix_world @ Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return (min(xs),max(xs),min(ys),max(ys),min(zs),max(zs))
def ndc(co):
    c=world_to_camera_view(scn,cam,Vector(co));return (round(c.x,2),round(c.y,2))
PAT=re.compile(r'(hortensia|hydrangea|bloem|flower|klaproos|lavendel|lavender|pot|struik|bush|border|roos|rose|plant_|Spiraea|perk|bed_)',re.I)
SKIP=re.compile(r'(_LOD[1-9]|needle|branch|twig|leaf|blad)',re.I)
print("QF_START")
seen=set()
for o in sorted(bpy.data.objects,key=lambda x:x.name):
    if o.type not in ('MESH','EMPTY'): continue
    if not PAT.search(o.name) or SKIP.search(o.name): continue
    # groepeer op basis-naam
    key=re.sub(r'[_\.]?\d+$','',o.name)
    if key in seen: continue
    seen.add(key)
    members=[x for x in bpy.data.objects if re.sub(r'[_\.]?\d+$','',x.name)==key]
    locs=[]
    for m in members:
        if m.type=='EMPTY': locs.append((m.location.x,m.location.y))
        elif m.type=='MESH' and len(m.data.vertices):
            b=wbb(m); locs.append(((b[0]+b[1])/2,(b[2]+b[3])/2))
    if locs:
        print(f"  [{key}* x{len(members)}] posities: " + ", ".join(f"({x:.1f},{y:.1f})" for x,y in locs[:12]))
print("QF_END")
