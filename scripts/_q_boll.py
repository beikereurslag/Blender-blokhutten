import bpy, sys, re
from mathutils import Vector
F=sys.argv[sys.argv.index("--")+1]
bpy.ops.wm.open_mainfile(filepath=F)
def wc(o):
    cs=[o.matrix_world @ Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs]; ys=[c.y for c in cs]; zs=[c.z for c in cs]
    return ((min(xs)+max(xs))/2,(min(ys)+max(ys))/2,min(zs),max(zs))
print("QB_START")
print("-- bollard parts --")
for o in sorted(bpy.data.objects,key=lambda x:x.name):
    if re.match(r"LaBoll\d", o.name):
        if o.type=='MESH':
            c=wc(o); print(f"  {o.name:14s} c=({c[0]:.2f},{c[1]:.2f}) z[{c[2]:.2f},{c[3]:.2f}] parent={o.parent.name if o.parent else None}")
        elif o.type=='LIGHT':
            print(f"  {o.name:14s} LIGHT loc=({o.location.x:.2f},{o.location.y:.2f},{o.location.z:.2f}) parent={o.parent.name if o.parent else None}")
print("-- pavers --")
for o in sorted(bpy.data.objects,key=lambda x:x.name):
    if re.match(r"LaPaver_\d", o.name) and o.type=='MESH':
        c=wc(o); print(f"  {o.name:12s} c=({c[0]:.2f},{c[1]:.2f}) z[{c[2]:.2f},{c[3]:.2f}]")
print("QB_END")
