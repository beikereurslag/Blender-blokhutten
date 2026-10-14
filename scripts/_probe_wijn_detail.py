import bpy, math
from mathutils import Vector
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Camelia-250x300-300-zijwand\style-mediterraan\camelia_wijnterras.blend"
bpy.ops.wm.open_mainfile(filepath=F)

def bb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)

print("DET_START")
# Terras material + build
t=bpy.data.objects.get("Terras")
print("Terras:", "verts",len(t.data.vertices),"polys",len(t.data.polygons),
      "mats",[s.material.name if s.material else None for s in t.material_slots],"bb",tuple(round(x,2) for x in bb(t)))
ds=bpy.data.objects.get("Deur_Stoep")
print("Deur_Stoep:", "verts",len(ds.data.vertices),"mats",[s.material.name if s.material else None for s in ds.material_slots])
pad=bpy.data.objects.get("Pad")
print("Pad:", "verts",len(pad.data.vertices),"mats",[s.material.name if s.material else None for s in pad.material_slots])
# Terras material coord type
for mn in set([s.material.name for s in t.material_slots if s.material]):
    m=bpy.data.materials.get(mn)
    if m and m.use_nodes:
        mp=next((n for n in m.node_tree.nodes if n.type=='MAPPING'),None)
        tc=next((n for n in m.node_tree.nodes if n.type=='TEX_COORD'),None)
        src="?"
        if mp:
            src=[(l.from_socket.name) for l in mp.inputs['Vector'].links]
        print(f"  mat {mn}: mapping_src={src}")

# wine bottle + glasses + table + chair
print("--- props of interest:")
for o in bpy.data.objects:
    nl=o.name.lower()
    if any(k in nl for k in ('wijn','fles','bottle','glas','bistro','bistrot','table','tafel','assise','osier','bezier','stoel','chair')):
        b=bb(o)
        par=o.parent.name if o.parent else None
        print(f"  {o.name:34s} type={o.type:5s} parent={par} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}]")

# olive pots orientation: check rotation of OlijfPot top-levels
print("--- OlijfPot top-levels (parent=None) rot:")
for o in bpy.data.objects:
    if o.name.lower().startswith('olijfpot') and o.parent is None:
        r=[round(math.degrees(a),0) for a in o.rotation_euler]
        b=bb(o)
        print(f"  {o.name:18s} rot={r} z[{b[4]:.2f},{b[5]:.2f}]")
print("DET_END")
