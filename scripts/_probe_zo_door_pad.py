"""Read-only: deur-stoep, bistrotafel(top-z), lavendel, Pad-route, cabin-front.
Geen save."""
import bpy
from mathutils import Vector
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Zonnebloem-300x300-300-zijwand\style-scandi\zonnebloem_ochtendhoek.blend"
bpy.ops.wm.open_mainfile(filepath=F)

def bb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)

print("PROBE2_START")
# bistrot table parts (zoek alles 'bistro')
print("--- table parts (bistro/table) ---")
for o in bpy.data.objects:
    if o.type=='MESH' and ('bistro' in o.name.lower() or 'table' in o.name.lower() or 'tafel' in o.name.lower()):
        b=bb(o); print(f"  {o.name:30s} z[{b[4]:.3f},{b[5]:.3f}] x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}]")

# deur / stoep / cabin-front
print("--- deur/stoep/wall/pole/board (cabin front) ---")
fronts=[]
for o in bpy.data.objects:
    n=o.name.lower()
    if o.type=='MESH' and any(k in n for k in ('deur','stoep','door','wall','pole','board','floor','cwfloor')):
        b=bb(o)
        print(f"  {o.name:28s} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}]")

# lavendel / bloemen
print("--- lavendel/flower/bloem objects ---")
for o in bpy.data.objects:
    n=o.name.lower()
    if any(k in n for k in ('lavend','flower','bloem','salvia','allium')):
        b=bb(o) if o.type=='MESH' else None
        print(f"  {o.name:30s} {o.type} {('x[%.2f,%.2f] y[%.2f,%.2f] z[%.2f,%.2f]'%(b[0],b[1],b[2],b[3],b[4],b[5])) if b else 'loc'+str(tuple(round(v,2) for v in o.location))}")

# Pad route (ribbon verts -> centerline)
print("--- Pad route (ribbon centerline) ---")
pad=bpy.data.objects.get("Pad")
if pad:
    vs=[pad.matrix_world@v.co for v in pad.data.vertices]
    # verts komen in paren (l,r); centerline = gemiddelde per paar
    cl=[]
    for i in range(0,len(vs)-1,2):
        c=(vs[i]+vs[i+1])/2; cl.append(c)
    print(f"  Pad verts={len(vs)} centerline pts={len(cl)}")
    for c in cl:
        print(f"    ({c.x:.2f},{c.y:.2f},{c.z:.2f})")
print("PROBE2_END")
