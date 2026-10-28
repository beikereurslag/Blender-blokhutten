"""Top-down placement-diagnose LITE: verberg zware bomen/heg, render alleen
cabin + props + hardscape footprint. Workbench SOLID, lage res -> geen OOM.
Run: blender -b --python render_topdown_lite2.py -- <blend> <out_png> <scale>
"""
import bpy, sys
argv = sys.argv[sys.argv.index("--")+1:]
OUT = argv[0]
SCALE = float(argv[1]) if len(argv)>1 else 12.0
# scene already loaded via -b <blend>
scene=bpy.context.scene

HIDE=('treering','pine_tree','berk','hedge','sketchfab','painted_wooden_bench','hedgesprig')
to_del=[o for o in bpy.data.objects if any(k in o.name.lower() for k in HIDE)]
for o in to_del:
    try: bpy.data.objects.remove(o, do_unlink=True)
    except Exception as e: print('del-fail',o.name,e)
# free heavy mesh/image data blocks directly (no operator/context needed)
for m in list(bpy.data.meshes):
    if m.users==0:
        try: bpy.data.meshes.remove(m)
        except Exception: pass
for im in list(bpy.data.images):
    try: im.buffers_free()
    except Exception: pass

cam=bpy.data.cameras.new("TopCam"); cam.type='ORTHO'; cam.ortho_scale=SCALE
co=bpy.data.objects.new("TopCam",cam); scene.collection.objects.link(co)
co.location=(0.0,1.0,30.0); co.rotation_euler=(0,0,0)
scene.camera=co
scene.render.engine='BLENDER_WORKBENCH'
try:
    scene.display.shading.light='STUDIO'
    scene.display.shading.color_type='OBJECT'
    scene.display.shading.show_shadows=False
    scene.display.shading.show_cavity=False
except Exception as e: print(e)
scene.render.resolution_x=1000; scene.render.resolution_y=1000
scene.render.filepath=OUT
bpy.ops.render.render(write_still=True)
print("[topdown-lite] "+OUT)
