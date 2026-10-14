import bpy
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Camelia-250x300-300-zijwand\style-mediterraan\camelia_wijnterras.blend"
bpy.ops.wm.open_mainfile(filepath=F)
print("IMG_START")
total=0
rows=[]
for im in bpy.data.images:
    w,h = im.size[0], im.size[1]
    packed = im.packed_file is not None
    psize = im.packed_file.size if im.packed_file else 0
    total += psize
    users = im.users
    rows.append((psize, im.name, w, h, packed, users, im.filepath))
rows.sort(reverse=True)
for psize,name,w,h,packed,users,fp in rows:
    print(f"  {psize/1e6:7.1f}MB  {w}x{h:<5} packed={packed} users={users}  {name}")
print(f"--- total packed ~ {total/1e6:.0f} MB across {len(rows)} images")
print("IMG_END")
