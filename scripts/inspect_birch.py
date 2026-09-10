import bpy
from mathutils import Vector

for pre in ("Birch_4", "Birch_5"):
    print("=== group", pre)
    for o in bpy.data.objects:
        if o.name.startswith(pre):
            if o.type == 'MESH':
                zs = [(o.matrix_world @ Vector(c)).z for c in o.bound_box]
                wz = f"[{min(zs):.2f},{max(zs):.2f}]"
            else:
                wz = f"loc.z={o.matrix_world.translation.z:.2f}"
            print(f"  {o.name!r} type={o.type} parent={o.parent.name if o.parent else None} "
                  f"hide_render={o.hide_render} vis={o.visible_get()} wz={wz}")

# ook de empties die als parent dienen
print("=== parents/empties")
for o in bpy.data.objects:
    if o.name.startswith("background_birch") or o.name in ("Birch 4", "Birch 5"):
        print(f"  {o.name!r} type={o.type} loc={[round(v,2) for v in o.location]} "
              f"parent={o.parent.name if o.parent else None}")
print("INSPECT_DONE")
