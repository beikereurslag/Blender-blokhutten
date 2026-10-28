import bpy
from mathutils import Vector
print("PP_START")
for pp in ("potted_plant_01_2k","potted_plant_02_2k","potted_plant_04_2k","shrub_02_2k"):
    path=fr"C:\Users\beike\Documents\Blender-blokhutten\assets\polyhaven\models\{pp}.blend"
    try:
        with bpy.data.libraries.load(path, link=False) as (src,dst):
            dst.objects=list(src.objects)
        objs=[o for o in dst.objects if o]
        for o in objs:
            if o.name not in bpy.context.scene.collection.objects:
                bpy.context.scene.collection.objects.link(o)
        bpy.context.view_layer.update()
        cs=[]
        for o in objs:
            if o.type=='MESH' and len(o.data.vertices):
                cs+=[o.matrix_world@Vector(c) for c in o.bound_box]
        if cs:
            xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
            print(f"{pp}: {len(objs)} objs  dims X{max(xs)-min(xs):.2f} Y{max(ys)-min(ys):.2f} Z{max(zs)-min(zs):.2f}  meshes={[o.name for o in objs if o.type=='MESH'][:6]}")
        # unlink to keep clean
        for o in objs:
            try: bpy.context.scene.collection.objects.unlink(o)
            except: pass
    except Exception as e:
        print(pp,"ERR",e)
print("PP_END")
