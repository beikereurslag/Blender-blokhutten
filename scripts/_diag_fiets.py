import bpy
from mathutils import Vector
F=r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Dahlia-250x250-300-zijwand\style-modern-urban-cottage\dahlia_tuinkantoor.blend"
bpy.ops.wm.open_mainfile(filepath=F)
f=bpy.data.objects.get("Fiets_root")
print("FIETS_START")
print("root loc", tuple(round(v,3) for v in f.location))
for c in f.children_recursive:
    if c.type=='MESH' and len(c.data.vertices):
        cs=[c.matrix_world@Vector(v) for v in c.bound_box]
        zs=[p.z for p in cs]; xs=[p.x for p in cs]; ys=[p.y for p in cs]
        print(f"  {c.name:30s} z[{min(zs):.3f},{max(zs):.3f}] x[{min(xs):.2f},{max(xs):.2f}] y[{min(ys):.2f},{max(ys):.2f}] v={len(c.data.vertices)}")
print("FIETS_END")
