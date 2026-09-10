import bpy
from mathutils import Vector

def world_minz_visible(mesh_prefix):
    mn = 1e9
    for o in bpy.data.objects:
        if o.type == 'MESH' and not o.hide_render and o.name.startswith(mesh_prefix):
            for c in o.bound_box:
                mn = min(mn, (o.matrix_world @ Vector(c)).z)
    return mn

def ground(empty_name, mesh_prefix, target_z=0.0):
    mn = world_minz_visible(mesh_prefix)
    if mn > 1e8:
        print(f"FIX: {mesh_prefix} geen zichtbare meshes"); return
    e = bpy.data.objects[empty_name]
    mw = e.matrix_world.copy()
    mw.translation.z -= (mn - target_z)
    e.matrix_world = mw
    bpy.context.view_layer.update()
    new = world_minz_visible(mesh_prefix)
    print(f"FIX: {mesh_prefix} wereld-min-z {mn:.2f} -> {new:.2f} (empty '{empty_name}' verlaagd)")

ground("background_birch_Birch_4", "Birch_4_Birch")
ground("background_birch_Birch_5", "Birch_5_Birch")

if "camera" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["camera"], do_unlink=True)
    print("FIX: stray 'camera' verwijderd")

out_blend = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Lavendel-400x300-400-zijwand\style-modern\lavendel_REBUILD_FINAL_fixed.blend"
bpy.ops.wm.save_as_mainfile(filepath=out_blend)
print("FIX: opgeslagen ->", out_blend)
print("FIX_DONE")
