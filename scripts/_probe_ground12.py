"""Scene 12 - zoek het grijze vlak vóór/onder de hut. Lijst ALLE platte vlakken op
grondniveau (footprint>1.2m, dun, z laag) met materiaal+kleur, en dump het
Ground_Grass-materiaal (is het grijs rock of groen gras?)."""
import bpy
from mathutils import Vector

def wbb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]
    return (min(c.x for c in cs),max(c.x for c in cs),min(c.y for c in cs),max(c.y for c in cs),min(c.z for c in cs),max(c.z for c in cs))

def basecol(m):
    if m and m.use_nodes:
        b=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if b:
            linked = b.inputs['Base Color'].is_linked
            src = ""
            if linked:
                fn = b.inputs['Base Color'].links[0].from_node
                src = fn.type + ("/"+fn.image.name if getattr(fn,'image',None) else "")
            return ([round(v,2) for v in b.inputs['Base Color'].default_value[:3]], "LINKED:"+src if linked else "flat")
    return (None,None)

print("\n==== PLATTE GROND-VLAKKEN (footprint>1.2, h<0.6, z<0.4) ====")
for o in bpy.data.objects:
    if o.type!='MESH' or not len(o.data.vertices) or o.hide_render: continue
    b=wbb(o); w=b[1]-b[0]; d=b[3]-b[2]; h=b[5]-b[4]
    if w>1.2 and d>1.2 and h<0.6 and b[4]<0.4:
        m=o.material_slots[0].material if o.material_slots and o.material_slots[0].material else None
        col,mode=basecol(m)
        print(f"  {o.name:<26} x[{b[0]:.1f},{b[1]:.1f}] y[{b[2]:.1f},{b[3]:.1f}] z[{b[4]:.2f},{b[5]:.2f}] "
              f"mat={m.name if m else '-':<20} col={col} {mode}")

print("\n==== Ground_Grass materiaal-nodes ====")
g = bpy.data.objects.get("Ground_Grass")
if g and g.material_slots and g.material_slots[0].material:
    m=g.material_slots[0].material
    print("  mat:", m.name, "use_nodes", m.use_nodes)
    for n in m.node_tree.nodes:
        info=""
        if n.type=='TEX_IMAGE': info="img="+(n.image.name if n.image else "NONE")+(" MISSING" if n.image and not n.image.packed_file and n.image.filepath and not __import__('os').path.exists(bpy.path.abspath(n.image.filepath)) else "")
        if n.type=='RGB': info="rgb="+str([round(v,2) for v in n.outputs[0].default_value[:3]])
        if n.type=='BSDF_PRINCIPLED':
            bc=n.inputs['Base Color']; info="basecol_linked="+str(bc.is_linked)+" val="+str([round(v,2) for v in bc.default_value[:3]])
        print(f"   {n.type:<22} {n.name:<22} {info}")
print("==== end\n")
