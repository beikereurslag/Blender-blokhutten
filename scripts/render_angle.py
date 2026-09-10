# scripts/render_angle.py — extra marketing-camerahoek (nieuwe cam, niet-destructief).
# Gebruik: blender -b --python scripts/render_angle.py -- <scene.blend> <out.png> <lens> <lx> <ly> <lz> <tx> <ty> <tz> [samples] [rx] [ry]
import bpy, sys
from mathutils import Vector
a = sys.argv[sys.argv.index("--")+1:]
SCENE, PNG = a[0], a[1]
lens = float(a[2]); loc = (float(a[3]), float(a[4]), float(a[5])); tgt = (float(a[6]), float(a[7]), float(a[8]))
samples = int(a[9]) if len(a) > 9 else 200
rx = int(a[10]) if len(a) > 10 else 2560
ry = int(a[11]) if len(a) > 11 else 1440
bpy.ops.wm.open_mainfile(filepath=SCENE)
scn = bpy.context.scene
cam = bpy.data.cameras.new("WeekendAltCam"); cam.lens = lens; cam.clip_start = 0.02; cam.clip_end = 2000.0
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
bpy.ops.render.render(write_still=True)
print("[angle] " + PNG)
