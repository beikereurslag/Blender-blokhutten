import bpy
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Camelia-250x300-300-zijwand\style-mediterraan\camelia_wijnterras.blend"
bpy.ops.wm.open_mainfile(filepath=F)
print("TM_START")
m=bpy.data.materials.get("MAT_Travertine")
if m and m.use_nodes:
    for n in m.node_tree.nodes:
        line=f"  node {n.type:18s} {n.name}"
        if n.type=='TEX_IMAGE':
            line+=f"  img={n.image.name if n.image else None}  src={[l.from_node.type for l in n.inputs['Vector'].links]}"
        if n.type=='TEX_COORD':
            line+="  (coord)"
        if n.type=='MAPPING':
            sc=n.inputs['Scale'].default_value
            line+=f"  scale=({sc[0]:.2f},{sc[1]:.2f},{sc[2]:.2f}) in={[l.from_socket.name for l in n.inputs['Vector'].links]}"
        if n.type=='BSDF_PRINCIPLED':
            bc=n.inputs['Base Color'].default_value
            line+=f"  baseRGBA=({bc[0]:.2f},{bc[1]:.2f},{bc[2]:.2f}) roughIn={[l.from_node.type for l in n.inputs['Roughness'].links]}"
        print(line)
else:
    print("  MAT_Travertine missing or no nodes")
print("TM_END")
