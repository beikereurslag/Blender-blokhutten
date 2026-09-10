"""Scene-13 zone-probe: alle mesh-objecten in de zentuin-zone (voor de hut) met
base-color, om het witte karesansui-vlak, de groene blob en het onbekende object te
vinden. Plus maple-subtree info."""
import bpy
from mathutils import Vector

def wbb(ms):
    cs=[]
    for m in ms: cs += [m.matrix_world @ Vector(c) for c in m.bound_box]
    if not cs: return None
    return (min(c.x for c in cs),max(c.x for c in cs),min(c.y for c in cs),max(c.y for c in cs),min(c.z for c in cs),max(c.z for c in cs))

def basecol(o):
    if o.material_slots and o.material_slots[0].material and o.material_slots[0].material.use_nodes:
        b=next((n for n in o.material_slots[0].material.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if b: return [round(v,2) for v in b.inputs['Base Color'].default_value[:3]]
    return None

print("\n==== ZENZONE meshes (center in x[-4,2] y[1.5,7]) ====")
rows=[]
for o in bpy.data.objects:
    if o.type!='MESH' or not len(o.data.vertices): continue
    b=wbb([o])
    if not b: continue
    cx=(b[0]+b[1])/2; cy=(b[2]+b[3])/2
    if not (-4<cx<2 and 1.5<cy<7): continue
    nl=o.name.lower()
    if any(k in nl for k in ('zndeck','wall-','roof','fascia','trim','board','hedge')): continue
    mat=o.material_slots[0].material.name if o.material_slots and o.material_slots[0].material else '-'
    rows.append((round(cx,1),round(cy,1),o.name,round(b[4],2),round(b[5],2),len(o.data.vertices),mat,basecol(o)))
for cx,cy,nm,z0,z1,nv,mat,col in sorted(rows, key=lambda r:(r[1],r[0])):
    print(f"  ({cx:5.1f},{cy:4.1f}) {nm:<26} z[{z0:.2f},{z1:.2f}] v={nv:<6} mat={mat:<18} col={col}")
print(f"==== {len(rows)} meshes")

# maple subtree
mp = bpy.data.objects.get("ZenMaple_root")
if mp:
    ms=[c for c in mp.children_recursive if c.type=='MESH' and len(c.data.vertices)]
    b=wbb(ms); nv=sum(len(m.data.vertices) for m in ms)
    print(f"\nMAPLE ZenMaple_root: meshes={len(ms)} verts={nv} bbox x[{b[0]:.1f},{b[1]:.1f}] y[{b[2]:.1f},{b[3]:.1f}] z[{b[4]:.2f},{b[5]:.2f}]")
    for m in ms: print(f"   {m.name:<30} v={len(m.data.vertices)} mat={m.material_slots[0].material.name if m.material_slots and m.material_slots[0].material else '-'}")
print("==== end\n")
