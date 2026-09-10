import bpy
from mathutils import Vector
F=r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Lavendel-400x300-400-zijwand\style-boerderij\lavendel_pluktuin.blend"
bpy.ops.wm.open_mainfile(filepath=F)
def bb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box];xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
def wz(o):  # world min/max z incl children
    ms=[c for c in [o]+list(o.children_recursive) if c.type=='MESH' and len(c.data.vertices)]
    cs=[c.matrix_world@Vector(v) for c in ms for v in c.bound_box]
    if not cs: return None
    return min(p.z for p in cs),max(p.z for p in cs),(min(p.x for p in cs)+max(p.x for p in cs))/2,(min(p.y for p in cs)+max(p.y for p in cs))/2
print("PK_START")
print("CAM",bpy.context.scene.camera.name,tuple(round(v,2) for v in bpy.context.scene.camera.location))
print("== TAFEL/BANK + POT + TERRAS/PAD + VLOER ==")
for o in sorted(bpy.data.objects,key=lambda x:x.name):
    n=o.name.lower()
    if any(k in n for k in ('tafel','table','bank','bench','picknick','picnic','dining','eet','pot','terras','pad','klinker','vloer','floor','deck','stoep','plank','rozenboog','pergola','arch')):
        if o.type=='MESH' and len(o.data.vertices):
            b=bb(o);print(f"  {o.name:26s} MESH x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.3f},{b[5]:.3f}]")
        else:
            w=wz(o)
            print(f"  {o.name:26s} {o.type} loc{tuple(round(v,2) for v in o.location)}"+(f" childZ[{w[0]:.3f},{w[1]:.3f}]" if w else ""))
print("== BLOEMEN/STRUIKEN (min-z = zweef-check) ==")
fl=[o for o in bpy.data.objects if o.type in ('EMPTY','MESH') and any(k in o.name.lower() for k in ('hortensia','hydrangea','roos','rose','bloem','flower','struik','bush','azalea','spiraea','elder','butterfly','kalmia','poppy'))]
roots=[o for o in fl if o.type=='EMPTY' or not o.parent]
print(f"  bloem-objs={len(fl)} roots={len(roots)}")
for o in roots[:40]:
    w=wz(o)
    fly="  <-- ZWEEFT" if (w and w[0]>0.06) else ""
    print(f"    {o.name:28s} {o.type} {'minz=%.3f'%w[0] if w else 'loc'+str(tuple(round(v,2) for v in o.location))}{fly}")
print("== cabin wall/pole footprint ==")
ws=[bb(o) for o in bpy.data.objects if o.type=='MESH' and any(k in o.name.lower() for k in ('wall','pole','parentboard','fascia'))]
if ws:
    print(f"  cabin x[{min(b[0] for b in ws):.2f},{max(b[1] for b in ws):.2f}] y[{min(b[2] for b in ws):.2f},{max(b[3] for b in ws):.2f}]")
print("PK_END")
