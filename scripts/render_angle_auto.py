# scripts/render_angle_auto.py — lifestyle alt-hoek, AUTO afgeleid van HeroCam (schaalt mee per scene).
# Dichterbij (0.62x afstand) + lager (1.42m) + blik richting open bay (+X). Nieuwe cam, niet-destructief.
# Gebruik: blender -b --python scripts/render_angle_auto.py -- <scene.blend> <out.png> [samples] [rx] [ry] [tgtx]
import bpy, sys
from mathutils import Vector
a = sys.argv[sys.argv.index("--")+1:]
SCENE, PNG = a[0], a[1]
samples = int(a[2]) if len(a) > 2 else 200
rx = int(a[3]) if len(a) > 3 else 2560
ry = int(a[4]) if len(a) > 4 else 1440
tgtx = float(a[5]) if len(a) > 5 else 0.8
bpy.ops.wm.open_mainfile(filepath=SCENE)
scn = bpy.context.scene
hero = bpy.data.objects.get("HeroCam") or scn.camera
hx, hy, hz = (hero.location.x, hero.location.y, hero.location.z) if hero else (8.0, 10.0, 1.6)
loc = (hx * 0.72, hy * 0.72, 1.45)
tgt = (tgtx, 2.8, 1.05)   # richt naar BUITEN in de deck/meubel-zone, niet op de deurlijn
cam = bpy.data.cameras.new("WeekendAltCam"); cam.lens = 50; cam.clip_start = 0.02; cam.clip_end = 2000.0
co = bpy.data.objects.new("WeekendAltCam", cam); scn.collection.objects.link(co)
co.location = loc
d = Vector(tgt) - Vector(loc); co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
scn.camera = co
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    _gpu = 'CUDA'
    for _t in ('OPTIX', 'CUDA'):
        prefs.compute_device_type = _t; prefs.get_devices()
        if any(d.type == _t for d in prefs.devices): _gpu = _t; break
    for dv in prefs.devices: dv.use = (dv.type == _gpu)
    print("[gpu]", _gpu)
    scn.cycles.device = 'GPU'
except Exception as e:
    print("dev", e)
scn.cycles.samples = samples
scn.cycles.adaptive_threshold = 0.008
scn.cycles.use_denoising = True
scn.cycles.denoiser = 'OPENIMAGEDENOISE'
scn.cycles.texture_limit_render = '2048'
scn.render.use_persistent_data = False
scn.render.resolution_x = rx; scn.render.resolution_y = ry
scn.render.image_settings.file_format = 'PNG'; scn.render.image_settings.color_depth = '16'
scn.render.filepath = PNG
print(f"[angle-auto] hero=({hx:.1f},{hy:.1f}) -> altloc=({loc[0]:.1f},{loc[1]:.1f},{loc[2]:.1f}) tgt={tgt}")
bpy.ops.render.render(write_still=True)
print("[angle-auto] " + PNG)
