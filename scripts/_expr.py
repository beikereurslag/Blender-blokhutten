import bpy, math
from mathutils import Vector
o=[]
t=bpy.data.objects.get("Terras")
me=t.data
o.append("Terras verts=%d polys=%d edges=%d mats=%s"%(len(me.vertices),len(me.polygons),len(me.edges),[m.name if m else None for m in me.materials]))
from collections import Counter
ec=Counter()
for p in me.polygons:
    for ek in p.edge_keys: ec[ek]+=1
o.append("Terras boundary_edges(1face)=%d"%sum(1 for k,v in ec.items() if v==1))
b=bpy.data.objects.get("Bank")
mw=b.matrix_world
fwd=(mw.to_3x3()@Vector((0,1,0))).normalized()
o.append("Bank loc=%s rot=%s scale=%s fwdY=%s"%(tuple(round(x,2) for x in b.location),tuple(round(math.degrees(x),1) for x in b.rotation_euler),tuple(round(x,2) for x in b.scale),tuple(round(x,2) for x in fwd)))
print("PROBE>>> "+" || ".join(o))
