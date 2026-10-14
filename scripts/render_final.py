# scripts/render_final.py — generieke finale render.
# Gebruik: blender -b --python scripts/render_final.py -- <scene.blend> <out.png> [samples] [resx] [resy]
import bpy, sys
a = sys.argv[sys.argv.index("--")+1:]
SCENE, PNG = a[0], a[1]
samples = int(a[2]) if len(a) > 2 else 240
rx = int(a[3]) if len(a) > 3 else 2560
ry = int(a[4]) if len(a) > 4 else 1440
bpy.ops.wm.open_mainfile(filepath=SCENE)
scn = bpy.context.scene
cam = scn.camera or bpy.data.objects.get("HeroCam")
if cam:
    scn.camera = cam
    cam.data.clip_start = 0.02
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
scn.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
scn.cycles.denoising_prefilter = 'ACCURATE'
scn.cycles.max_bounces = 6
scn.cycles.transmission_bounces = 12
scn.cycles.texture_limit_render = '2048'
scn.render.use_persistent_data = False
scn.render.resolution_x = rx
scn.render.resolution_y = ry
scn.render.image_settings.file_format = 'PNG'
scn.render.image_settings.color_depth = '16'
scn.render.filepath = PNG
bpy.ops.render.render(write_still=True)
print("[final] " + PNG)
