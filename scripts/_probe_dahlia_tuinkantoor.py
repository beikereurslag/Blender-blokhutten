import bpy
from mathutils import Vector
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Dahlia-250x250-300-zijwand\style-modern-urban-cottage\dahlia_tuinkantoor.blend"
bpy.ops.wm.open_mainfile(filepath=F)
sc=bpy.context.scene
def bb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
print("DT_START")
# the named fakes from the shopping list
NAMED=('cortenbak','slab','bollard','bureau','desk','laptop','werkplek','pad','path','vloer','floor','terras')
print("--- named fakes / surfaces:")
for o in bpy.data.objects:
    nl=o.name.lower()
    if any(k in nl for k in NAMED):
        if o.type=='MESH' and len(o.data.vertices):
            b=bb(o); mats=[s.material.name if s.material else None for s in o.material_slots]
            print(f"  {o.name:26s} v{len(o.data.vertices):4d} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}] mats={mats}")
        else:
            print(f"  {o.name:26s} type={o.type} loc={tuple(round(v,2) for v in o.location)}")
# materials on path/floor surfaces -> AI textures?
print("--- surface material images:")
seen=set()
for o in bpy.data.objects:
    nl=o.name.lower()
    if any(k in nl for k in ('slab','pad','vloer','floor','terras','bureau')):
        for s in o.material_slots:
            m=s.material
            if m and m.name not in seen and m.use_nodes:
                seen.add(m.name)
                imgs=[n.image.name for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]
                print(f"  {m.name}: imgs={imgs}")
# cameras
print("--- cameras:")
for o in bpy.data.objects:
    if o.type=='CAMERA':
        t=" (ACTIVE)" if sc.camera==o else ""
        print(f"  {o.name}{t} loc({o.location.x:.2f},{o.location.y:.2f},{o.location.z:.2f}) lens={o.data.lens:.0f}")
# does the cabin have a roofed area w/o floor? list wall/roof/floor extents
print("--- structure extents (wall/roof/floor/overkap):")
cats={'WALL':('wand','wall','muur','board','beschot'),'ROOF':('dak','roof','overkap','overstek','fascia','flatroof'),'FLOOR':('vloer','floor','deck','vlonder'),'POST':('paal','pole','post','staander')}
for cat,kws in cats.items():
    xs=[];ys=[];zs=[];n=0
    for o in bpy.data.objects:
        if o.type!='MESH' or not len(o.data.vertices): continue
        if any(k in o.name.lower() for k in kws):
            b=bb(o); xs+=[b[0],b[1]];ys+=[b[2],b[3]];zs+=[b[4],b[5]];n+=1
    if n: print(f"  {cat}: {n} objs x[{min(xs):.2f},{max(xs):.2f}] y[{min(ys):.2f},{max(ys):.2f}] z[{min(zs):.2f},{max(zs):.2f}]")
    else: print(f"  {cat}: none")
print("DT_END")
