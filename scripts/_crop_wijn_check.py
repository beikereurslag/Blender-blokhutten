import bpy
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Camelia-250x300-300-zijwand\style-mediterraan\camelia_wijnterras.blend"
bpy.ops.wm.open_mainfile(filepath=F)
sc=bpy.context.scene
sc.render.resolution_x=900;sc.render.resolution_y=700;sc.cycles.samples=48
try:
    sc.cycles.device='GPU'
    prefs=bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type='CUDA';prefs.get_devices()
    for d in prefs.devices: d.use=True
except Exception as e: print(e)

def shot(name, loc, tgt, lens=55):
    from mathutils import Vector
    cam=bpy.data.cameras.new(name);cam.lens=lens
    co=bpy.data.objects.new(name,cam);sc.collection.objects.link(co)
    co.location=loc
    d=(Vector(tgt)-Vector(loc)).normalized()
    co.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
    sc.camera=co
    sc.render.filepath=r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Camelia-250x300-300-zijwand\style-mediterraan\\"+name+".png"
    bpy.ops.render.render(write_still=True)
    print("SHOT",name)

# olive pot cluster at world x3.3 y2.4
shot("_chk_olive",(5.5,4.0,1.2),(3.3,2.2,0.6),lens=70)
# bistro table + chairs at x-1.6 y3.5
shot("_chk_table",(1.8,6.2,1.4),(-1.6,3.5,0.6),lens=55)
print("DONE")
