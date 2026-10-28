"""Snelle VRAM-veilige preview render vanuit de actieve (of opgegeven) camera.
Run: blender.exe -b <file.blend> --python preview_render.py -- <out.png> [cam] [samples] [resx] [resy]
"""
import bpy, sys

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
out = argv[0] if len(argv) > 0 else "//preview.png"
cam = argv[1] if len(argv) > 1 else None
samples = int(argv[2]) if len(argv) > 2 else 64
resx = int(argv[3]) if len(argv) > 3 else 1280
resy = int(argv[4]) if len(argv) > 4 else 720

sc = bpy.context.scene
sc.render.engine = 'CYCLES'

prefs = bpy.context.preferences.addons['cycles'].preferences
chosen = None
for t in ('OPTIX', 'CUDA'):
    try:
        prefs.compute_device_type = t
        prefs.get_devices()
        if any(d.type == t for d in prefs.devices):
            chosen = t
            break
    except Exception as ex:
        print("device type", t, "failed:", ex)
if chosen:
    for d in prefs.devices:
        d.use = (d.type == chosen)
    sc.cycles.device = 'GPU'
    print("GPU:", chosen, "->", [d.name for d in prefs.devices if d.use])
else:
    sc.cycles.device = 'CPU'
    print("Geen GPU, CPU fallback")

sc.cycles.samples = samples
sc.cycles.use_denoising = True
sc.cycles.texture_limit_render = '2048'
sc.render.use_persistent_data = False
sc.render.resolution_x = resx
sc.render.resolution_y = resy
sc.render.resolution_percentage = 100

if cam and cam in bpy.data.objects:
    sc.camera = bpy.data.objects[cam]
print("Camera:", sc.camera.name if sc.camera else None)

sc.render.filepath = out
sc.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(write_still=True)
print("RENDER_DONE", out)
