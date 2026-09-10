import bpy, collections
from bpy_extras.object_utils import world_to_camera_view
F=r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Lavendel-400x300-400-zijwand\style-mediterraan\lavendel_lavendelveld.blend"
bpy.ops.wm.open_mainfile(filepath=F)
scn=bpy.context.scene; cam=bpy.data.objects.get("HeroCam"); scn.camera=cam
bpy.context.view_layer.update()
us=[]
for o in bpy.data.objects:
    if o.type=='EMPTY' and (o.name.startswith("Lav_") or o.name.startswith("Lavendel")):
        c=world_to_camera_view(scn,cam,o.matrix_world.translation)
        if c.z>0: us.append(c.x)
us.sort()
print("U_START n_in_frame=",len(us))
b=collections.Counter()
for u in us: b[round(u//0.1*0.1,1)]+=1
for k in sorted(b): print(f"  u {k:.1f}-{k+0.1:.1f}: {b[k]}")
import statistics
print("  min=%.2f p25=%.2f med=%.2f p75=%.2f max=%.2f"%(us[0],us[len(us)//4],statistics.median(us),us[3*len(us)//4],us[-1]))
print("U_END")
