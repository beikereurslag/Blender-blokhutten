import bpy
from mathutils import Vector

scene = bpy.context.scene
leaf = bpy.data.materials.get("leaf_02_Mat")

# verwijder evt. eerdere run
for n in ("HEDGE_back", "HEDGE_right", "HEDGE_left"):
    if n in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[n], do_unlink=True)

dtex = bpy.data.textures.get("hedge_disp") or bpy.data.textures.new("hedge_disp", type='CLOUDS')
dtex.noise_scale = 0.35

def hedge(name, loc, dims):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = (dims[0], dims[1], dims[2])
    bpy.ops.object.transform_apply(scale=True)
    sub = o.modifiers.new("subsurf", 'SUBSURF')
    sub.subdivision_type = 'SIMPLE'; sub.levels = 4; sub.render_levels = 4
    dis = o.modifiers.new("disp", 'DISPLACE')
    dis.texture = dtex; dis.strength = 0.14; dis.mid_level = 0.5
    if leaf:
        o.data.materials.clear(); o.data.materials.append(leaf)
    return o

H = 2.4
# basis z = H/2 zodat onderkant op grond
hedge("HEDGE_back",  (1.0, -4.6, H/2),  (26.0, 0.8, H))   # achterwand x -12..14
hedge("HEDGE_right", (12.5, -1.5, H/2), (0.8, 7.0, H))    # rechter return
hedge("HEDGE_left",  (-10.5, -1.5, H/2), (0.8, 7.0, H))   # linker return
print("HEDGE: 3 segmenten geplaatst, H=2.4m, leaf_02_Mat")

# grass tiling
g = bpy.data.objects.get("ground_grass")
if g and g.active_material and g.active_material.use_nodes:
    nt = g.active_material.node_tree
    mp = next((n for n in nt.nodes if n.type == 'MAPPING'), None)
    tc = next((n for n in nt.nodes if n.type == 'TEX_COORD'), None)
    src = None
    if mp and mp.inputs['Vector'].is_linked:
        src = mp.inputs['Vector'].links[0].from_socket.name
    if mp:
        old = [round(v, 2) for v in mp.inputs['Scale'].default_value]
        mp.inputs['Scale'].default_value = (20.0, 20.0, 20.0)
        print(f"GRASS mapping src={src} scale {old} -> 20")
    else:
        print("GRASS: geen mapping node")

out_blend = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Lavendel-400x300-400-zijwand\style-modern\lavendel_realism_wip.blend"
bpy.ops.wm.save_as_mainfile(filepath=out_blend)
print("SAVED", out_blend)
print("BUILD_DONE")
