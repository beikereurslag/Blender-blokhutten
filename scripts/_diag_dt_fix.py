"""Read-only: Dahlia Tuinkantoor — fiets + alle bestrating/deck/vloer + bollard. Geen save."""
import bpy
from mathutils import Vector
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Dahlia-250x250-300-zijwand\style-modern-urban-cottage\dahlia_tuinkantoor.blend"
bpy.ops.wm.open_mainfile(filepath=F)

def bb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)

print("DTFIX_START")
keys=('fiets','bike','bicycle','cycle','wiel','frame','deck','vlonder','terras','slab','paver',
      'tegel','klink','pad','vloer','floor','bollard','stoep','beton','square','concrete')
print("--- matching objects (bbox, z laag->hoog telt voor zweven/aansluiten) ---")
for o in sorted(bpy.data.objects,key=lambda x:x.name):
    n=o.name.lower()
    if any(k in n for k in keys):
        if o.type=='MESH' and len(o.data.vertices):
            b=bb(o); print(f"  {o.name:34s} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.3f},{b[5]:.3f}] v={len(o.data.vertices)}")
        else:
            print(f"  {o.name:34s} {o.type:7s} loc{tuple(round(v,2) for v in o.location)}")
print("--- ALL top-level mesh objects ---")
print("  ", sorted(o.name for o in bpy.data.objects if o.type=='MESH' and not o.parent))
print("--- collections ---")
print("  ", [(c.name,len(c.objects)) for c in bpy.data.collections])
print("DTFIX_END")
