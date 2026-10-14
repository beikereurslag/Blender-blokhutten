"""Lichte top-down WORKBENCH-render zonder textures (memory-safe).
Run: blender -b --python render_topdown_lite.py -- <blend> <out_png> <scale>
Verlaagt subdiv/particle, schakelt textures uit -> blijft binnen RAM.
"""
import bpy, sys
argv = sys.argv[sys.argv.index("--")+1:]
BLEND, OUT = argv[0], argv[1]
SCALE = float(argv[2]) if len(argv)>2 else 24.0
bpy.ops.wm.open_mainfile(filepath=BLEND)
scene=bpy.context.scene

# kill heavy modifiers/particles to save memory
for o in bpy.data.objects:
    try:
        for m in list(o.modifiers):
            if m.type in ('SUBSURF','PARTICLE_SYSTEM','NODES','MULTIRES'):
                o.modifiers.remove(m)
    except Exception:
        pass
for ps in list(getattr(bpy.data,'particles',[])):
    try: ps.count=0
    except Exception: pass

cam=bpy.data.cameras.new("TopCam"); cam.type='ORTHO'; cam.ortho_scale=SCALE
co=bpy.data.objects.new("TopCam",cam); scene.collection.objects.link(co)
co.location=(0.0,0.5,30.0); co.rotation_euler=(0,0,0)
scene.camera=co
scene.render.engine='BLENDER_WORKBENCH'
try:
    scene.display.shading.light='FLAT'
    scene.display.shading.color_type='SINGLE'
    scene.display.shading.single_color=(0.6,0.6,0.6)
    scene.display.shading.show_object_outline=True
except Exception as e: print(e)
scene.render.resolution_x=900; scene.render.resolution_y=900
scene.render.filepath=OUT
bpy.ops.render.render(write_still=True)
print("[topdown-lite] "+OUT)
