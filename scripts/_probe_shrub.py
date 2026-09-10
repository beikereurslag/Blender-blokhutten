import bpy
from mathutils import Vector
base = r"C:\Users\beike\Documents\Blender-blokhutten\assets\polyhaven\models"
for nm in ['shrub_01','shrub_02','shrub_03','shrub_04']:
    p = base + "\\" + nm + "_2k.blend"
    with bpy.data.libraries.load(p, link=False) as (s, d):
        d.objects = list(s.objects)
    objs = [o for o in d.objects if o]
    for o in objs:
        bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.update()
    cs = []
    for o in objs:
        if o.type == 'MESH' and len(o.data.vertices):
            cs += [o.matrix_world @ Vector(c) for c in o.bound_box]
    if cs:
        xs = [c.x for c in cs]; ys = [c.y for c in cs]; zs = [c.z for c in cs]
        print('SHRUBINFO', nm, 'n=', len(objs), 'dx', round(max(xs)-min(xs), 2),
              'dy', round(max(ys)-min(ys), 2), 'dz', round(max(zs)-min(zs), 2))
    for o in objs:
        bpy.data.objects.remove(o)
