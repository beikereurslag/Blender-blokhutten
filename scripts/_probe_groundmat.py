"""Print het grond-materiaal (base-color keten) van een blend: image-textuur (origineel)
of procedureel (herkleurd door fix_broken_image_materials?). Run:
  blender -b <blend> --python _probe_groundmat.py
"""
import bpy, os
from mathutils import Vector
# grootste platte grondvlak
ground=None; best=0
for o in bpy.data.objects:
    if o.type!='MESH' or not len(o.data.vertices): continue
    nl=o.name.lower()
    if not any(k in nl for k in ('ground','grass','gras','terrain','grond')): continue
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]
    area=(max(c.x for c in cs)-min(c.x for c in cs))*(max(c.y for c in cs)-min(c.y for c in cs))
    if area>best: best=area; ground=o
print("FILE", os.path.basename(bpy.data.filepath))
if not ground:
    print("  GEEN grond-object gevonden");
else:
    print("  ground obj:", ground.name)
    m=ground.material_slots[0].material if ground.material_slots else None
    if not m: print("  GEEN materiaal")
    else:
        print("  mat:", m.name)
        nt=m.node_tree
        b=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if b:
            bc=b.inputs['Base Color']
            if bc.is_linked:
                src=bc.links[0].from_node
                print("  base_color <- ", src.type, src.name)
                # volg keten terug, zoek image of noise
                kinds=[n.type for n in nt.nodes]
                imgs=[n.image.name for n in nt.nodes if n.type=='TEX_IMAGE' and n.image]
                miss=[]
                for n in nt.nodes:
                    if n.type=='TEX_IMAGE' and n.image:
                        ap=bpy.path.abspath(n.image.filepath) if n.image.filepath else ""
                        st="packed" if n.image.packed_file else ("ok" if ap and os.path.exists(ap) else "MISSING")
                        miss.append(n.image.name+":"+st)
                print("  node-types:", sorted(set(kinds)))
                print("  images:", miss if miss else "GEEN (procedureel!)")
                print("  noise/ramp aanwezig:", any(t in kinds for t in ('TEX_NOISE','VALTORGB')))
            else:
                print("  base_color FLAT =", [round(v,2) for v in bc.default_value[:3]])
