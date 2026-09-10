import bpy
with open(r"C:\Users\beike\Documents\Blender-blokhutten\sentinel.txt", "w") as f:
    f.write("BLENDER_PYTHON_RAN objects=%d\n" % len(bpy.data.objects))
bpy.ops.wm.quit_blender()
