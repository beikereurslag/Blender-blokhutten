import bpy, os
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Dahlia-250x250-300-zijwand\style-modern-urban-cottage\dahlia_tuinkantoor.blend"
bpy.ops.wm.open_mainfile(filepath=F)
print("DIAG_START")
# find shrub-ish objects
shrubs = [o for o in bpy.data.objects if 'shrub' in o.name.lower() or 'Shrub' in o.name]
print("shrub objects:", [o.name for o in shrubs])
for o in shrubs:
    print(f"  {o.name}: type={o.type} verts={len(o.data.vertices) if o.type=='MESH' else '-'} hide_render={o.hide_render} visible={o.visible_get()}")
    for s in o.material_slots:
        m = s.material
        if not m: continue
        print(f"    MAT {m.name} blend_method={getattr(m,'blend_method','?')}")
        if m.use_nodes:
            for n in m.node_tree.nodes:
                if n.type == 'TEX_IMAGE' and n.image:
                    im = n.image
                    ap = bpy.path.abspath(im.filepath)
                    print(f"      IMG {im.name} packed={bool(im.packed_file)} exists={os.path.exists(ap)} path={im.filepath}")
                if n.type == 'BSDF_PRINCIPLED':
                    a = n.inputs['Alpha']
                    print(f"      BSDF Alpha linked={a.is_linked} val={a.default_value}")
print("DIAG_END")
