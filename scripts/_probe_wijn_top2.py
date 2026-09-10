import bpy
from mathutils import Vector
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Camelia-250x300-300-zijwand\style-mediterraan\camelia_wijnterras.blend"
DIAG = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Camelia-250x300-300-zijwand\style-mediterraan\_diag_wijn_top2.png"
bpy.ops.wm.open_mainfile(filepath=F)
sc=bpy.context.scene
def bb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
print("T2_START")
for nm in ("CwFloor","CwTerrasMain","CwTerrasDoor","Pad"):
    o=bpy.data.objects.get(nm)
    if o: print(f"  {nm:14s} {tuple(round(x,2) for x in bb(o))}")
    else: print(f"  {nm}: MISSING")
# olive pot cluster: list each child mesh bbox + the olive foliage
print("--- OlijfPot children:")
op=bpy.data.objects.get("OlijfPot")
if op:
    print("  root", tuple(round(x,2) for x in bb(op)) if op.type=='MESH' else "(empty)", "loc",tuple(round(x,2) for x in op.location))
for o in bpy.data.objects:
    if o.name.lower().startswith("olijfpot") and o.type=='MESH':
        b=bb(o); print(f"    {o.name:16s} dz{b[5]-b[4]:.2f} z[{b[4]:.2f},{b[5]:.2f}] x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}]")
print("T2_END")
cam=bpy.data.cameras.new("Top");cam.type='ORTHO';cam.ortho_scale=13
co=bpy.data.objects.new("Top",cam);sc.collection.objects.link(co)
co.location=(0,1,30);co.rotation_euler=(0,0,0);sc.camera=co
sc.render.resolution_x=1100;sc.render.resolution_y=1100;sc.cycles.samples=24
sc.render.filepath=DIAG
bpy.ops.render.render(write_still=True)
print("DIAG_DONE")
