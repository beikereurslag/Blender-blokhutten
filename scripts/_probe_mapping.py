import bpy
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Dahlia-250x250-300-zijwand\style-scandi\dahlia_leeshoek.blend"
bpy.ops.wm.open_mainfile(filepath=F)
print("PROBE_START")
m = bpy.data.materials.get("MAT_AshDeck")
nt = m.node_tree
mapping = next((n for n in nt.nodes if n.type=='MAPPING'), None)
img = next((n for n in nt.nodes if n.type=='TEX_IMAGE'), None)
# what feeds the mapping Vector input?
vin = mapping.inputs['Vector']
print("Mapping.Vector from:", [(l.from_node.type, l.from_socket.name) for l in vin.links])
print("Mapping Location:", tuple(round(x,3) for x in mapping.inputs['Location'].default_value))
print("Mapping Rotation:", tuple(round(x,3) for x in mapping.inputs['Rotation'].default_value))
print("Mapping Scale:", tuple(round(x,3) for x in mapping.inputs['Scale'].default_value))
# image vector source
print("Image.Vector from:", [(l.from_node.type, l.from_socket.name) for l in img.inputs['Vector'].links])
print("PROBE_END")
