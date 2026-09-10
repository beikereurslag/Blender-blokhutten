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
scene.render.engine='CYCLES'
try:
    scene.cycles.device='GPU'
except Exception as e: print("dev",e)
scene.cycles.samples=48
scene.cycles.adaptive_threshold=0.05
scene.cycles.use_persistent_data=False
scene.render.use_persistent_data=False
try:
    scene.cycles.texture_limit_render='2048'
    scene.cycles.use_texture_limit=True
except Exception as e: print("texlim",e)
scene.render.resolution_x=1000; scene.render.resolution_y=1000
scene.render.filepath=OUT
bpy.ops.render.render(write_still=True)
print("[topdown-cycles] "+OUT)
