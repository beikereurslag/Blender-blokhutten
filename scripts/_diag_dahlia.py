import bpy, math
from mathutils import Vector

F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Dahlia-250x250-300-zijwand\style-scandi\dahlia_leeshoek.blend"
DIAG = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Dahlia-250x250-300-zijwand\style-scandi\_diag_top.png"
bpy.ops.wm.open_mainfile(filepath=F)
sc = bpy.context.scene

def wb(name_sub):
    cs = []
    for o in bpy.data.objects:
        if name_sub.lower() in o.name.lower() and o.type == 'MESH' and len(o.data.vertices):
            cs += [o.matrix_world @ Vector(c) for c in o.bound_box]
    if not cs: return None
    xs=[c.x for c in cs]; ys=[c.y for c in cs]; zs=[c.z for c in cs]
    return (min(xs),max(xs),min(ys),max(ys),min(zs),max(zs))

print("DIAG_START")
for key in ("deur", "door", "Vlonder", "Deur_Stoep", "Pad", "Fauteuil", "Tafel", "RZ_", "Hout", "lavendel", "rooibos"):
    b = wb(key)
    if b: print(f"{key}: x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}]")

# top-down ortho camera
cam = bpy.data.cameras.new("TopCam"); cam.type = 'ORTHO'; cam.ortho_scale = 16
camo = bpy.data.objects.new("TopCam", cam); sc.collection.objects.link(camo)
camo.location = (0.0, 2.0, 30.0); camo.rotation_euler = (0, 0, 0)
sc.camera = camo
sc.render.resolution_x = 1100; sc.render.resolution_y = 1100
sc.cycles.samples = 24
sc.render.filepath = DIAG
bpy.ops.render.render(write_still=True)
print("DIAG_DONE", DIAG)
