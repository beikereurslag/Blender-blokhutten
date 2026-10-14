"""Lichte materiaal/terras-check. Schrijft naar file. Geen geometry-eval.
Run: blender -b --python dump_mats.py -- <blend> <outtxt>
"""
import bpy, sys
argv = sys.argv[sys.argv.index("--")+1:]
BLEND, OUT = argv[0], argv[1]
bpy.ops.wm.open_mainfile(filepath=BLEND)
L=[]
def P(*a): L.append(" ".join(str(x) for x in a))

P("=== MATERIALS (check magenta/missing/broken) ===")
for m in sorted(bpy.data.materials,key=lambda x:x.name):
    base=""
    if m.use_nodes:
        bsdf=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if bsdf:
            c=bsdf.inputs['Base Color'].default_value
            base="rgb(%.2f,%.2f,%.2f)"%(c[0],c[1],c[2])
            # magenta check
            if c[0]>0.7 and c[1]<0.2 and c[2]>0.7: base+=" <-- MAGENTA?"
    P("%-30s users=%d %s"%(m.name[:30],m.users,base))

P("=== TEXTURE IMAGES (missing files) ===")
for img in bpy.data.images:
    if img.source=='FILE':
        import os
        p=bpy.path.abspath(img.filepath)
        ok=os.path.exists(p)
        if not ok:
            P("MISSING %-30s -> %s"%(img.name[:30],img.filepath))

P("=== SHED MESH INFO ===")
shed=bpy.data.objects.get('shed')
if shed and shed.type=='MESH':
    me=shed.data
    P("shed verts=%d polys=%d mats=%s"%(len(me.vertices),len(me.polygons),[m.name if m else None for m in me.materials]))
    P("shed modifiers=%s"%[ (mod.name,mod.type) for mod in shed.modifiers])

P("=== END ===")
open(OUT,"w",encoding="utf-8").write("\n".join(L))
print("WROTE",len(L))
