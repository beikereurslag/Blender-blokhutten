import bpy, sys, re
from mathutils import Vector
F=sys.argv[sys.argv.index("--")+1]
bpy.ops.wm.open_mainfile(filepath=F)
def wbb(o):
    cs=[o.matrix_world @ Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return (min(xs),max(xs),min(ys),max(ys),min(zs),max(zs))
def matinfo(m):
    if not m: return ("<none>",None,[])
    bc=None;imgs=[]
    if m.use_nodes:
        for n in m.node_tree.nodes:
            if n.type=='BSDF_PRINCIPLED': c=n.inputs['Base Color'].default_value;bc=(round(c[0],2),round(c[1],2),round(c[2],2))
            if n.type=='TEX_IMAGE' and n.image: imgs.append(n.image.name)
    return (m.name,bc,imgs)
SKIP=re.compile(r'(ground|wall-|roof|fascia|beam|pole|deck|vloer|terras|path_bed|DEUR|scharn|board|parentBoard|bed$)',re.I)
GREENNAME=re.compile(r'(leaf|blad|moss|mos|sedum|green|groen|plant|lily|pad|clover|klaver|fern|varen|grass)',re.I)
print("QBLOB_START")
for o in sorted(bpy.data.objects,key=lambda x:x.name):
    if o.type!='MESH' or not len(o.data.vertices): continue
    if SKIP.search(o.name): continue
    b=wbb(o); ze=b[5]-b[4]; w=max(b[1]-b[0],b[3]-b[2])
    if ze>0.3 or w>2.5: continue   # alleen platte, kleine objecten
    mats=[matinfo(s.material) for s in o.material_slots]
    # groen? base groenig OF image/mat-naam groen-achtig
    green=False
    for mn,bc,imgs in mats:
        if bc and bc[1]>bc[0]+0.02 and bc[1]>bc[2]+0.02: green=True
        if GREENNAME.search(mn) or any(GREENNAME.search(i) for i in imgs): green=True
    if green or GREENNAME.search(o.name):
        print(f"  {o.name:26s} zext={ze:.2f} w={w:.2f} z[{b[4]:.2f},{b[5]:.2f}] verts={len(o.data.vertices)} mats={mats}")
print("QBLOB_END")
