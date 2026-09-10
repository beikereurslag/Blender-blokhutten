import bpy, re, collections
from mathutils import Vector
F=r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Lavendel-400x300-400-zijwand\style-mediterraan\lavendel_lavendelveld.blend"
bpy.ops.wm.open_mainfile(filepath=F)
clusters=collections.defaultdict(list)
for o in bpy.data.objects:
    if o.type!='MESH' or o.hide_render: continue
    m=re.match(r'(TreeRing_\d+|TreeFillL_\d+|TreeFillR_\d+|RingPine_\d+)', o.name)
    if m: clusters[m.group(1)].append(o)
print("CL_START  clusters:",len(clusters))
def foliage_mat(o):
    for s in o.material_slots:
        if s.material:
            nm=s.material.name.lower()
            if any(k in nm for k in ('needle','leaf','twig','foliage','blad','naald')): return True
    return False
bare=[]
for name in sorted(clusters):
    objs=clusters[name]
    verts=sum(len(o.data.vertices) for o in objs)
    fol=any(foliage_mat(o) for o in objs)
    mats=set()
    for o in objs:
        for s in o.material_slots:
            if s.material: mats.add(s.material.name)
    tag="BARE" if (not fol and verts<3000) else "ok"
    if tag=="BARE": bare.append(name)
    print(f"  {name:16s} members={len(objs)} verts={verts:6d} foliage_mat={fol} -> {tag}  mats={sorted(mats)[:4]}")
print("BARE clusters:",bare)
print("CL_END")
