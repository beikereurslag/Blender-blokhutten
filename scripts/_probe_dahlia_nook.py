import bpy, math
from mathutils import Vector

F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Dahlia-250x250-300-zijwand\style-scandi\dahlia_leeshoek.blend"
bpy.ops.wm.open_mainfile(filepath=F)

def info(sub):
    for o in bpy.data.objects:
        if sub.lower() in o.name.lower():
            d = o.dimensions
            r = [round(math.degrees(a),1) for a in o.rotation_euler]
            # local +Y and +X in world (to infer facing)
            fy = (o.matrix_world.to_3x3() @ Vector((0,1,0))).normalized()
            fx = (o.matrix_world.to_3x3() @ Vector((1,0,0))).normalized()
            print(f"{o.name}: loc({o.location.x:.2f},{o.location.y:.2f},{o.location.z:.2f}) "
                  f"dim({d.x:.2f},{d.y:.2f},{d.z:.2f}) rotZ={r[2]} "
                  f"+Yworld({fy.x:.2f},{fy.y:.2f}) +Xworld({fx.x:.2f},{fx.y:.2f}) type={o.type}")

print("PROBE_START")
for k in ("Fauteuil", "Tafel", "lantaarn", "lantern", "Lamp", "Vlonder", "deur", "DeurPot", "Pad", "lavendel", "rooibos"):
    info(k)
print("PROBE_END")
