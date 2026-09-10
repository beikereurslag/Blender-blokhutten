import bpy
F = r"C:\Users\beike\Documents\Blender-blokhutten\assets\polyhaven\models\shrub_02_2k.blend"
with bpy.data.libraries.load(F, link=False) as (s, d):
    d.materials = list(s.materials)
print("NODES_START")
for m in d.materials:
    if not m: continue
    print("MAT", m.name, "use_nodes", m.use_nodes, "blend", getattr(m, 'blend_method', '?'),
          "shadow", getattr(m, 'shadow_method', '?'))
    nt = m.node_tree
    for n in nt.nodes:
        extra = ""
        if n.type == 'TEX_IMAGE' and n.image:
            extra = f" img={n.image.name} cs={n.image.colorspace_settings.name}"
        print(f"  NODE {n.type:18s} '{n.name}'{extra}")
    print("  --- links into Material Output:")
    for l in nt.links:
        if l.to_node.type == 'OUTPUT_MATERIAL':
            print(f"    {l.from_node.type}.{l.from_socket.name} -> OUTPUT.{l.to_socket.name}")
    # show what feeds the surface shader's alpha if any
    for n in nt.nodes:
        if n.type in ('BSDF_PRINCIPLED', 'BSDF_DIFFUSE', 'BSDF_TRANSLUCENT', 'GROUP'):
            for inp in n.inputs:
                if inp.name in ('Alpha', 'Base Color', 'Color') and inp.is_linked:
                    fl = inp.links[0]
                    print(f"    [{n.type}].{inp.name} <- {fl.from_node.type}.{fl.from_socket.name}")
print("NODES_END")
