import bpy
from mathutils import Vector
F = r"C:\Users\beike\Documents\Blender-blokhutten\assets\sketchfab\decor\firewood_stack.blend"
with bpy.data.libraries.load(F, link=False) as (s, d):
    d.objects = list(s.objects)
objs = [o for o in d.objects if o]
for o in objs:
    bpy.context.scene.collection.objects.link(o)
bpy.context.view_layer.update()
def bb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
print("FW_START n=", len(objs))
for o in sorted(objs, key=lambda o:o.name):
    if o.type=='MESH':
        b=bb(o)
        print(f"  {o.name:30s} par={o.parent.name if o.parent else '-':20s} "
              f"dx{b[1]-b[0]:.2f} dy{b[3]-b[2]:.2f} dz{b[5]-b[4]:.2f} "
              f"c({(b[0]+b[1])/2:.2f},{(b[2]+b[3])/2:.2f},{(b[4]+b[5])/2:.2f})")
    else:
        print(f"  {o.name:30s} EMPTY par={o.parent.name if o.parent else '-'} loc{tuple(round(v,2) for v in o.location)}")
print("FW_END")
