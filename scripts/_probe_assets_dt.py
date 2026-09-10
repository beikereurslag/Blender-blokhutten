import bpy
from mathutils import Vector
print("AST_START")
for path,label in [
    (r"assets\sketchfab\furniture\office_desk.blend","office_desk"),
    (r"assets\sketchfab\lighting\garden_lamp.blend","garden_lamp")]:
    full=r"C:\Users\beike\Documents\Blender-blokhutten\\"+path
    try:
        with bpy.data.libraries.load(full,link=False) as (src,dst):
            dst.objects=list(src.objects)
        objs=[o for o in dst.objects if o]
        for o in objs:
            if o.name not in bpy.context.scene.collection.objects:
                bpy.context.scene.collection.objects.link(o)
        bpy.context.view_layer.update()
        cs=[]
        tops=[o.name for o in objs if o.parent is None]
        for o in objs:
            if o.type=='MESH' and len(o.data.vertices):
                cs+=[o.matrix_world@Vector(c) for c in o.bound_box]
        if cs:
            xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
            print(f"{label}: {len(objs)} objs  dims X{max(xs)-min(xs):.2f} Y{max(ys)-min(ys):.2f} Z{max(zs)-min(zs):.2f}  tops={tops[:4]}")
        for o in objs:
            try: bpy.context.scene.collection.objects.unlink(o)
            except: pass
    except Exception as e:
        print(label,"ERR",e)
print("AST_END")
