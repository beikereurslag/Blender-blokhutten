import bpy
with open(r'C:/Users/beike/Documents/Blender-blokhutten/scripts/probe_out.txt','w') as f:
    f.write("objects=%d\n" % len(bpy.data.objects))
    t=bpy.data.objects.get('Terras')
    if t:
        me=t.data
        f.write("Terras verts=%d polys=%d mats=%s\n"%(len(me.vertices),len(me.polygons),[m.name if m else None for m in me.materials]))
    f.flush()
