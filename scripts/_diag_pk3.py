import bpy
from mathutils import Vector
F=r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Lavendel-400x300-400-zijwand\style-boerderij\lavendel_pluktuin.blend"
bpy.ops.wm.open_mainfile(filepath=F)
def wbb(o):
    ms=[c for c in [o]+list(o.children_recursive) if c.type=='MESH' and len(c.data.vertices)]
    cs=[c.matrix_world@Vector(v) for c in ms for v in c.bound_box]
    if not cs: return None
    xs=[p.x for p in cs];ys=[p.y for p in cs];zs=[p.z for p in cs]
    return ((min(xs)+max(xs))/2,(min(ys)+max(ys))/2,min(zs),max(zs))
print("PK3_START  (alles in/op cabin+patio+overkapping: x[-4,3] y[-1.7,4.6])")
for o in sorted(bpy.data.objects,key=lambda x:x.name):
    if o.type not in ('EMPTY','MESH'): continue
    if o.parent and o.type=='MESH': continue
    n=o.name.lower()
    if any(k in n for k in ('plant','flower','bloem','pot','basket','mand','wicker','struik','bush','hortensia','hydrang','roos','rose','spiraea','lavender','azalea','kalmia','butterfly','goldmound','optim','fern','varen','potted')):
        w=wbb(o)
        if w and -4<w[0]<3 and -1.7<w[1]<4.6:
            print(f"  {o.name:30s} {o.type:6s} center({w[0]:.2f},{w[1]:.2f}) z[{w[2]:.2f},{w[3]:.2f}]")
print("PK3_END")
