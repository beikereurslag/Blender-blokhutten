import bpy
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Dahlia-250x250-300-zijwand\style-scandi\dahlia_leeshoek.blend"
bpy.ops.wm.open_mainfile(filepath=F)
print("PROBE_START")
m = bpy.data.materials.get("MAT_AshDeck")
print("nodes:", [(n.type, n.name) for n in m.node_tree.nodes])
b = next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'), None)
if b:
    bc = b.inputs['Base Color']
    print("BaseColor links:", [(l.from_node.type, l.from_node.name) for l in bc.links])
for n in m.node_tree.nodes:
    if n.type in ('TEX_IMAGE','TEX_NOISE','TEX_WAVE','TEX_MUSGRAVE','TEX_VORONOI'):
        img = getattr(n,'image',None)
        print("  texnode", n.type, n.name, "image=", img.name if img else None)
v = bpy.data.objects.get("Vlonder")
print("Vlonder verts:", len(v.data.vertices), "polys:", len(v.data.polygons), "uv_layers:", [u.name for u in v.data.uv_layers])
print("Vlonder dims:", tuple(round(x,2) for x in v.dimensions))
print("PROBE_END")
