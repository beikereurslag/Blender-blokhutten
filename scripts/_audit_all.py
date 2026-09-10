"""Batch-audit alle site-scenes op terugkerende fouten: vreselijke paden + groene blobjes.
Loopt over alle _v2.blend, dumpt per scene de verdachte objecten/materialen.
Gebruik: blender -b --python scripts/_audit_all.py
"""
import bpy, re
from mathutils import Vector
ROOT = r"C:\Users\beike\Documents\Blender-blokhutten\\"
SCENES = [
 ("camelia_buitenbad","pilots/Camelia-250x300-300-zijwand/style-hot-tub-premium/camelia_buitenbad_v2.blend"),
 ("camelia_wijnterras","pilots/Camelia-250x300-300-zijwand/style-mediterraan/camelia_wijnterras_v2.blend"),
 ("dahlia_tuinkantoor","pilots/Dahlia-250x250-300-zijwand/style-modern-urban-cottage/dahlia_tuinkantoor_v2.blend"),
 ("dahlia_leeshoek","pilots/Dahlia-250x250-300-zijwand/style-scandi/dahlia_leeshoek_v2.blend"),
 ("jasmijn_theehuis","pilots/Jasmijn-300x250-300-zijwand/style-japandi/jasmijn_theehuis_v2.blend"),
 ("jasmijn_familietuin","pilots/Jasmijn-300x250-300-zijwand/style-klassiek-familie/jasmijn_familietuin_v2.blend"),
 ("lavendel_pluktuin","pilots/Lavendel-400x300-400-zijwand/style-boerderij/lavendel_pluktuin_v2.blend"),
 ("lavendel_lavendelveld","pilots/Lavendel-400x300-400-zijwand/style-mediterraan/lavendel_lavendelveld_v2.blend"),
 ("lelie_ochtendnevel","pilots/Lelie-400x250-300-zijwand/style-forest-wilderness/lelie_ochtendnevel_v2.blend"),
 ("lelie_avondkubus","pilots/Lelie-400x250-300-zijwand/style-modern/lelie_avondkubus_v2.blend"),
 ("magnolia_groene_long","pilots/Magnolia-300x200/style-eco-groendak/magnolia_groene_long_v2.blend"),
 ("magnolia_wintertuin","pilots/Magnolia-300x200/style-scandi/magnolia_wintertuin_v2.blend"),
 ("roosmarijn_zentuin","pilots/Roosmarijn-200x300-400-zijwand/style-japanese-zen/roosmarijn_zentuin_v2.blend"),
 ("roosmarijn_kruidenterras","pilots/Roosmarijn-200x300-400-zijwand/style-mediterraan/roosmarijn_kruidenterras_v2.blend"),
 ("zonnebloem_zomeravond","pilots/Zonnebloem-300x300-300-zijwand/style-boerderij/zonnebloem_zomeravond_v2.blend"),
 ("zonnebloem_ochtendhoek","pilots/Zonnebloem-300x300-300-zijwand/style-scandi/zonnebloem_ochtendhoek_v2.blend"),
]
PATH_RE = re.compile(r'(pad|path|flag|slab|tegel|stap|pav|klink|tobi|stepp|MgPath|Slab|flagstone|loop)', re.I)
MOSS_RE = re.compile(r'(mos|moss|blob|sedum|groen|green)', re.I)

def is_flat(m):
    if not m or not m.use_nodes: return True
    return not any(n.type=='TEX_IMAGE' and n.image for n in m.node_tree.nodes)
def basecol(m):
    if not m or not m.use_nodes: return None
    for n in m.node_tree.nodes:
        if n.type=='BSDF_PRINCIPLED':
            c=n.inputs['Base Color'].default_value; return (round(c[0],2),round(c[1],2),round(c[2],2))
    return None
def zext(o):
    cs=[o.matrix_world @ Vector(c) for c in o.bound_box]
    zs=[c.z for c in cs]; return max(zs)-min(zs)

for name, rel in SCENES:
    print(f"\n===== {name} =====")
    try:
        bpy.ops.wm.open_mainfile(filepath=ROOT+rel.replace('/','\\'))
    except Exception as e:
        print("  OPEN FOUT:", e); continue
    paths=set(); blobs=set()
    for o in bpy.data.objects:
        if o.type!='MESH' or not len(o.data.vertices): continue
        mats=[s.material for s in o.material_slots if s.material]
        for m in mats:
            flat=is_flat(m); bc=basecol(m)
            # vreselijk pad: path-naam met PLAT materiaal (geen textuur)
            if PATH_RE.search(o.name) and flat:
                paths.add((m.name, str(bc), o.name));
            # groene blob: PLAT + groenig + plat van vorm (zext<0.25), niet de grote ground
            if flat and bc and bc[1] > 0.06 and bc[1] >= bc[0] and bc[1] >= bc[2] and (bc[1]-bc[0])>=-0.02:
                try: ze=zext(o)
                except: ze=9
                if ze < 0.25 and 'Ground' not in o.name and o.name.lower() not in ('mist','fog'):
                    blobs.add((m.name, str(bc), o.name, round(ze,2)))
            # moss/sedum-naam altijd flaggen
            if MOSS_RE.search(o.name) and flat:
                blobs.add((m.name, str(bc), o.name, 'name'))
    print("  PADEN (plat materiaal):")
    for mt,bc,on in sorted(paths)[:12]: print(f"    mat={mt} base={bc} obj={on}")
    if not paths: print("    (geen)")
    print("  GROENE BLOBS (plat groen, vlak):")
    seenm=set()
    for mt,bc,on,ze in sorted(blobs):
        if mt in seenm: continue
        seenm.add(mt); print(f"    mat={mt} base={bc} bv.obj={on} zext={ze}")
    if not blobs: print("    (geen)")
print("\nAUDIT_DONE")
