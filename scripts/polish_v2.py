# scripts/polish_v2.py — AgX + subtiele DoF + lichte exposure-compensatie. Niet-destructief.
# Gebruik: blender -b --python scripts/polish_v2.py -- <scene.blend> <v2.blend> <preview.png> <look> [exp]
#   look = "high"  -> 'AgX - Medium High Contrast' (zonnig/golden/sunset/helder/middag)
#   look = "base"  -> 'AgX - Base Contrast'        (overcast/blue hour/mist/zen/zacht)
import bpy, sys
from mathutils import Vector
a = sys.argv[sys.argv.index("--")+1:]
SCENE, V2, PNG, look = a[0], a[1], a[2], a[3]
exp = float(a[4]) if len(a) > 4 else 0.4   # AgX maakt donkerder; compenseer licht
bpy.ops.wm.open_mainfile(filepath=SCENE)
scn = bpy.context.scene
vs = scn.view_settings
vs.view_transform = 'AgX'
vs.look = 'AgX - Medium High Contrast' if look == 'high' else 'AgX - Base Contrast'
vs.exposure = exp
cam = scn.camera or bpy.data.objects.get("HeroCam")
if cam:
    scn.camera = cam
    cam.data.clip_start = 0.02
    # subtiele DoF: focus op cabin-midden (world origin-omgeving), zachte voorgrond/achterring
    cam.data.dof.use_dof = True
    cam.data.dof.aperture_fstop = 6.0
    cam.data.dof.focus_distance = (cam.location - Vector((0, 0, 1.2))).length
# render-veilig + preview
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'CUDA'; prefs.get_devices()
    for dv in prefs.devices: dv.use = True
    scn.cycles.device = 'GPU'
except Exception as e:
    print("dev", e)
scn.cycles.samples = 130
scn.cycles.use_denoising = True
scn.cycles.texture_limit_render = '2048'
scn.render.use_persistent_data = False
scn.render.resolution_x = 1600
scn.render.resolution_y = 900
scn.render.image_settings.file_format = 'PNG'
scn.render.image_settings.color_depth = '8'
scn.render.filepath = PNG
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=V2)
bpy.ops.render.render(write_still=True)
print("[v2] " + PNG)
