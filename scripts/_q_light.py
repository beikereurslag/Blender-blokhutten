import bpy, sys, math
F=sys.argv[sys.argv.index("--")+1]
bpy.ops.wm.open_mainfile(filepath=F)
scn=bpy.context.scene
print("Q_START")
for o in bpy.data.objects:
    if o.type=='LIGHT':
        L=o.data
        rot=tuple(round(math.degrees(a),1) for a in o.rotation_euler)
        extra=f"angle={math.degrees(getattr(L,'angle',0)):.2f}deg" if L.type=='SUN' else f"size={getattr(L,'size',0)}"
        print(f"LIGHT {o.name} type={L.type} energy={L.energy} color={tuple(round(c,2) for c in L.color)} rot={rot} {extra}")
w=scn.world
print("WORLD:", w.name if w else None, "use_nodes=", w.use_nodes if w else None)
if w and w.use_nodes:
    for n in w.node_tree.nodes:
        if n.type=='BACKGROUND':
            print("  BG strength=", round(n.inputs['Strength'].default_value,3), "color=", tuple(round(c,2) for c in n.inputs['Color'].default_value))
        if n.type=='TEX_ENVIRONMENT':
            print("  ENV image=", n.image.name if n.image else None)
        if n.type=='TEX_SKY':
            print("  SKY type=", getattr(n,'sky_type','?'))
print("view_transform=", scn.view_settings.view_transform, "look=", scn.view_settings.look, "exposure=", round(scn.view_settings.exposure,2))
# fog/volume
for o in bpy.data.objects:
    if o.type=='MESH':
        for s in o.material_slots:
            if s.material and ('fog' in s.material.name.lower() or 'mist' in s.material.name.lower()):
                print("VOLUME obj:", o.name, "mat:", s.material.name)
print("Q_END")
