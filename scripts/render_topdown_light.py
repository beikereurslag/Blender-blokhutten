"""Lichte top-down WORKBENCH-render zonder textures (placement-diagnose).
Vermijdt OOM-crash op 8192px textures: color_type=OBJECT (geen texture load).
Run: blender -b --python render_topdown_light.py -- <blend> <out_png> <scale>
"""
import bpy, sys
argv = sys.argv[sys.argv.index("--")+1:]
BLEND, OUT = argv[0], argv[1]
SCALE = float(argv[2]) if len(argv)>2 else 22.0
bpy.ops.wm.open_mainfile(filepath=BLEND)
scene=bpy.context.scene
# clamp image sizes om OOM te vermijden
for img in bpy.data.images:
    try:
        img.use_half_precision=True
    except Exception:
        pass
cam=bpy.data.cameras.new("TopCam"); cam.type='ORTHO'; cam.ortho_scale=SCALE
co=bpy.data.objects.new("TopCam",cam); scene.collection.objects.link(co)
co.location=(0.0,0.5,30.0); co.rotation_euler=(0,0,0)
scene.camera=co
scene.render.engine='BLENDER_WORKBENCH'
try:
    scene.display.shading.light='STUDIO'
    scene.display.shading.color_type='MATERIAL'  # viewport material color, geen texture
    scene.display.shading.show_shadows=True
    scene.display.shading.show_cavity=True
except Exception as e: print(e)
scene.render.resolution_x=1000; scene.render.resolution_y=1000
scene.render.filepath=OUT
bpy.ops.render.render(write_still=True)
print("[topdown] "+OUT)
