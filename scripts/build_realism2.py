import bpy, math

# camera diagnostiek
cam = bpy.data.objects.get("Camera_hero")
if cam:
    print(f"CAM loc={[round(v,2) for v in cam.location]} lens={cam.data.lens} "
          f"rot={[round(math.degrees(a),1) for a in cam.rotation_euler]} sensor_fit={cam.data.sensor_fit}")

leaf = bpy.data.materials.get("leaf_02_Mat")

# oude heg weg (zowel rechthoeken als arc)
for o in list(bpy.data.objects):
    if o.name.startswith("HEDGE_"):
        bpy.data.objects.remove(o, do_unlink=True)

dtex = bpy.data.textures.get("hedge_disp") or bpy.data.textures.new("hedge_disp", type='CLOUDS')
dtex.noise_scale = 0.35

cx, cy = 1.0, 2.0   # camera kijkt richting cabin/dit punt
R, H = 13.0, 2.7
bpy.ops.object.select_all(action='DESELECT')
count = 0
for i, deg in enumerate(range(110, 341, 8)):   # 200deg arc, weg van camera
    th = math.radians(deg)
    x = cx + R * math.cos(th); y = cy + R * math.sin(th)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, H / 2))
    o = bpy.context.active_object
    o.name = f"HEDGE_arc_{i}"
    o.rotation_euler = (0, 0, th + math.pi / 2)
    o.scale = (2.6, 0.9, H)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    sub = o.modifiers.new("s", 'SUBSURF'); sub.subdivision_type = 'SIMPLE'; sub.levels = 3; sub.render_levels = 3
    dis = o.modifiers.new("d", 'DISPLACE'); dis.texture = dtex; dis.strength = 0.14
    if leaf:
        o.data.materials.clear(); o.data.materials.append(leaf)
    count += 1
print(f"HEDGE arc: {count} segmenten, R={R}m, H={H}m")

out_blend = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Lavendel-400x300-400-zijwand\style-modern\lavendel_realism_wip.blend"
bpy.ops.wm.save_as_mainfile(filepath=out_blend)
print("SAVED", out_blend)
print("BUILD_DONE")
