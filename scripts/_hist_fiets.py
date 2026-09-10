import bpy
from mathutils import Vector
F=r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Dahlia-250x250-300-zijwand\style-modern-urban-cottage\dahlia_tuinkantoor.blend"
bpy.ops.wm.open_mainfile(filepath=F)
f=bpy.data.objects.get("Fiets_root")
m=[c for c in f.children_recursive if c.type=='MESH'][0]
mw=m.matrix_world
zs=sorted((mw@v.co).z for v in m.data.vertices)
n=len(zs)
print("HIST_START n=",n,"minz=%.3f maxz=%.3f"%(zs[0],zs[-1]))
# verts per 5cm-band tot 0.6m
import collections
band=collections.Counter()
for z in zs:
    band[round(z//0.05*0.05,2)]+=1
for b in sorted(band):
    if b<=0.65: print(f"  z {b:.2f}-{b+0.05:.2f}: {band[b]:5d} verts")
# percentiel
print("  p01=%.3f p02=%.3f p05=%.3f p10=%.3f"%(zs[int(n*.01)],zs[int(n*.02)],zs[int(n*.05)],zs[int(n*.10)]))
print("HIST_END")
