import bpy
from mathutils import Vector
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Dahlia-250x250-300-zijwand\style-modern-urban-cottage\dahlia_tuinkantoor.blend"
bpy.ops.wm.open_mainfile(filepath=F)
def bb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
print("BOXES_START")
# all top-level mesh objects, sorted, that are box-like and low (planter-ish)
for o in sorted(bpy.data.objects, key=lambda o:o.name):
    if o.type!='MESH': continue
    n=o.name.lower()
    if any(k in n for k in ('planter','bak','crate','box','soil','plant','werkplek','bench','seat','kist','pot')):
        b=bb(o)
        print(f"  {o.name:28s} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}]")
print("--- ALL non-RZ, non-cabin top-level meshes (parentless):")
for o in sorted(bpy.data.objects, key=lambda o:o.name):
    if o.type!='MESH' or o.parent: continue
    if o.name.startswith(('RZ_','DtFloor','DtPaver')): continue
    b=bb(o)
    dz=b[5]-b[4]
    if dz < 1.2 and b[4] < 0.6:   # low-ish standalone objects
        print(f"  {o.name:28s} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}]")
print("BOXES_END")
