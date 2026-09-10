"""Snelle top-down WORKBENCH-render (placement-diagnose: overlaps, aansluitingen).
Run: blender -b --python render_topdown.py -- <blend> <out_png> <scale>
Workbench = licht, concurrent-veilig, geen GPU/VRAM-druk.
"""
import bpy, sys
from mathutils import Vector
argv = sys.argv[sys.argv.index("--")+1:]
BLEND, OUT = argv[0], argv[1]
SCALE = float(argv[2]) if len(argv)>2 else 22.0
bpy.ops.wm.open_mainfile(filepath=BLEND)
scene=bpy.context.scene
cam=bpy.data.cameras.new("TopCam"); cam.type='ORTHO'; cam.ortho_scale=SCALE
co=bpy.data.objects.new("TopCam",cam); scene.collection.objects.link(co)
co.location=(0.0,0.5,30.0); co.rotation_euler=(0,0,0)  # recht naar beneden
scene.camera=co
scene.render.engine='BLENDER_WORKBENCH'
try:
    scene.display.shading.light='STUDIO'
    scene.display.shading.color_type='TEXTURE'
    scene.display.shading.show_shadows=True
    scene.display.shading.show_cavity=True
except Exception as e: print(e)
scene.render.resolution_x=1000; scene.render.resolution_y=1000
scene.render.filepath=OUT
bpy.ops.render.render(write_still=True)
print("[topdown] "+OUT)
