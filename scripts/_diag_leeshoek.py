import bpy, math
from mathutils import Vector
F=r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Dahlia-250x250-300-zijwand\style-scandi\dahlia_leeshoek.blend"
bpy.ops.wm.open_mainfile(filepath=F)
def cen(o):
    ms=[c for c in [o]+list(o.children_recursive) if c.type=='MESH' and len(c.data.vertices)]
    cs=[c.matrix_world@Vector(v) for c in ms for v in c.bound_box]
    if not cs: return None
    xs=[p.x for p in cs];ys=[p.y for p in cs];zs=[p.z for p in cs]
    return ((min(xs)+max(xs))/2,(min(ys)+max(ys))/2,(min(zs)+max(zs))/2),(min(xs),max(xs),min(ys),max(ys),min(zs),max(zs))
print("LS_START")
print("CAMERA", bpy.context.scene.camera.name if bpy.context.scene.camera else None,
      tuple(round(v,2) for v in bpy.context.scene.camera.location) if bpy.context.scene.camera else None)
keys=('stoel','chair','fauteuil','relax','arm','lees','werkstoel','tafel','table','coffee','round','zit')
for o in sorted(bpy.data.objects,key=lambda x:x.name):
    n=o.name.lower()
    if any(k in n for k in keys):
        c=cen(o)
        rot=tuple(round(math.degrees(r),1) for r in o.rotation_euler)
        if c: print(f"  {o.name:30s} {o.type:6s} center({c[0][0]:.2f},{c[0][1]:.2f},{c[0][2]:.2f}) rotZ={rot[2]} rotXY={rot[0]},{rot[1]} bboxXY x[{c[1][0]:.2f},{c[1][1]:.2f}] y[{c[1][2]:.2f},{c[1][3]:.2f}]")
        else: print(f"  {o.name:30s} {o.type:6s} loc{tuple(round(v,2) for v in o.location)} rotZ={rot[2]}")
print("-- collections:", [(c.name,len(c.objects)) for c in bpy.data.collections])
print("LS_END")
