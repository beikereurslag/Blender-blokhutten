"""Losse render van kruidenterras v5 -> R2b-preview (geen re-save/pack; snel)."""
import bpy
BLEND = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Roosmarijn-200x300-400-zijwand\style-mediterraan\roosmarijn_kruidenterras_v5.blend"
PNG   = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Roosmarijn-200x300-400-zijwand\style-mediterraan\roosmarijn_kruidenterras_R2b_PREVIEW.png"
bpy.ops.wm.open_mainfile(filepath=BLEND)
s = bpy.context.scene
s.render.engine = 'CYCLES'
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'CUDA'; prefs.get_devices()
    for dv in prefs.devices: dv.use = True
    s.cycles.device = 'GPU'
except Exception as e:
    print("dev", e)
s.cycles.samples = 96
s.cycles.use_denoising = True
s.cycles.denoiser = 'OPENIMAGEDENOISE'
s.cycles.texture_limit_render = '1024'   # 8GB headroom: zware Mist-volume + bomen
s.render.use_persistent_data = False
s.render.resolution_x = 1600; s.render.resolution_y = 900; s.render.resolution_percentage = 100
s.render.filepath = PNG
print(f"[render] start view={s.view_settings.view_transform}/{s.view_settings.look} exp={s.view_settings.exposure}")
bpy.ops.render.render(write_still=True)
print("[render] DONE -> " + PNG)
