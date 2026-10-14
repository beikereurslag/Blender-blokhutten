"""Lichte top-down WORKBENCH-render zonder texturen (geen VRAM-blowup).
Run: blender -b --python render_topdown_flat.py -- <blend> <out_png> <scale>
"""
import bpy, sys
argv = sys.argv[sys.argv.index("--")+1:]
BLEND, OUT = argv[0], argv[1]
SCALE = float(argv[2]) if len(argv)>2 else 22.0
bpy.ops.wm.open_mainfile(filepath=BLEND)
scene=bpy.context.scene
cam=bpy.data.cameras.new("TopCam"); cam.type='ORTHO'; cam.ortho_scale=SCALE
co=bpy.data.objects.new("TopCam",cam); scene.collection.objects.link(co)
co.location=(0.0,0.5,30.0); co.rotation_euler=(0,0,0)
scene.camera=co
scene.render.engine='BLENDER_WORKBENCH'
try:
    scene.display.shading.light='STUDIO'
    scene.display.shading.color_type='SINGLE'  # geen texturen -> geen VRAM-blowup
    scene.display.shading.single_color=(0.6,0.6,0.62)
    scene.display.shading.show_shadows=True
    scene.display.shading.show_cavity=True
except Exception as e: print(e)
# limiteer texturegrootte hard
try:
    scene.render.use_persistent_data=False
except Exception: pass
scene.render.resolution_x=900; scene.render.resolution_y=900
scene.render.filepath=OUT
bpy.ops.render.render(write_still=True)
print("[topdown] "+OUT)
