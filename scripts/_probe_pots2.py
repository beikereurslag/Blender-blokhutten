import bpy, math
from mathutils import Vector
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Camelia-250x300-300-zijwand\style-mediterraan\camelia_wijnterras.blend"
bpy.ops.wm.open_mainfile(filepath=F)
def bb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
print("P2_START")
for rn in ("Pot_0_root","Pot_1","Pot_2","SM_plant_pot.001","SM_plant_pot.002","SM_plant_pot.003"):
    r=bpy.data.objects.get(rn)
    if not r: print(rn,"MISSING"); continue
    rot=[round(math.degrees(a)) for a in r.rotation_euler]
    print(f"{rn} type={r.type} loc={tuple(round(v,2) for v in r.location)} rot={rot}")
    for c in r.children_recursive:
        if c.type=='MESH' and len(c.data.vertices):
            b=bb(c)
            print(f"    child {c.name:30s} dz{b[5]-b[4]:.2f} z[{b[4]:.2f},{b[5]:.2f}] x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}]")
        else:
            print(f"    child {c.name:30s} type={c.type}")
print("P2_END")
