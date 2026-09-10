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
PAT=re.compile(r'(DEURBASIC$|drempel|plateau|vlonder|deck|terras|plank|plat|step|JfPath_bed|JfSand|Zandbak|tafel|table|bank|bench|fontein|fountain|PaverPath)',re.I)
print("QL_START cam=",tuple(round(v,1) for v in cam.location))
seen=set()
for o in sorted(bpy.data.objects,key=lambda x:x.name):
    if o.type!='MESH' or not len(o.data.vertices): continue
    mname=o.material_slots[0].material.name if o.material_slots and o.material_slots[0].material else ''
    if not (PAT.search(o.name) or 'PaverPath' in mname or 'PadBed' in mname): continue
    b=wbb(o); cx=(b[0]+b[1])/2; cy=(b[2]+b[3])/2
    print(f"  {o.name:24s} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}] mat={mname} ndc{ndc((cx,cy,(b[4]+b[5])/2))}")
print("QL_END")
