import bpy
from mathutils import Vector
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Camelia-250x300-300-zijwand\style-mediterraan\camelia_wijnterras.blend"
bpy.ops.wm.open_mainfile(filepath=F)
def bb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
print("FAC_START")
KW=('deur','door','kozijn','raam','window','wand','wall','gevel','board','beschot','paal','post','pole','sill','threshold','drempel')
front=[]
for o in bpy.data.objects:
    if o.type!='MESH' or not len(o.data.vertices): continue
    nl=o.name.lower()
    if any(k in nl for k in KW):
        b=bb(o)
        if b[2] < 2.2 and b[4] < 2.6:
            front.append((o.name,b))
for nm,b in sorted(front):
    print(f"  {nm:32s} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}]")
print("--- terrace slabs:")
for nm in ("CwFloor","CwTerrasMain","CwTerrasDoor"):
    o=bpy.data.objects.get(nm)
    if o: print(f"  {nm:14s} {tuple(round(x,2) for x in bb(o))}")
if front:
    fy=[b[2] for _,b in front]; fx0=min(b[0] for _,b in front); fx1=max(b[1] for _,b in front)
    print(f"--- FRONT facade min-y~{min(fy):.2f}  x_span[{fx0:.2f},{fx1:.2f}]")
print("FAC_END")
