import bpy
from mathutils import Vector
F=r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Lavendel-400x300-400-zijwand\style-boerderij\lavendel_pluktuin.blend"
bpy.ops.wm.open_mainfile(filepath=F)
def wbb(o):
    ms=[c for c in [o]+list(o.children_recursive) if c.type=='MESH' and len(c.data.vertices)]
    cs=[c.matrix_world@Vector(v) for c in ms for v in c.bound_box]
    if not cs: return None
    xs=[p.x for p in cs];ys=[p.y for p in cs];zs=[p.z for p in cs]
    return ((min(xs)+max(xs))/2,(min(ys)+max(ys))/2,min(zs),max(zs),min(xs),max(xs),min(ys),max(ys))
print("PK2_START")
print("== FURNITURE / props (root-empties + losse mesh) ==")
for o in sorted(bpy.data.objects,key=lambda x:x.name):
    n=o.name.lower()
    if any(k in n for k in ('tafel','table','picknick','picnic','dining','eet','bank','bench','basket','mand','wicker','korf','pot','plant','stoel','chair')):
        if o.parent is None or o.type=='EMPTY':
            w=wbb(o)
            if w: print(f"  {o.name:26s} {o.type:6s} center({w[0]:.2f},{w[1]:.2f}) z[{w[2]:.2f},{w[3]:.2f}] x[{w[4]:.2f},{w[5]:.2f}] y[{w[6]:.2f},{w[7]:.2f}]")
            else: print(f"  {o.name:26s} {o.type}")
print("== PLANTEN OP DE PATIO (binnen x[-3.7,2.7] y[1.2,4.2]) ==")
for o in bpy.data.objects:
    if o.parent is not None and o.type!='EMPTY': continue
    n=o.name.lower()
    if any(k in n for k in ('hortensia','hydrangea','roos','rose','bloem','flower','struik','bush','spiraea','lavender','azalea','kalmia','butterfly','goldmound','plant')):
        w=wbb(o)
        if w and -3.7<w[0]<2.7 and 1.2<w[1]<4.2:
            print(f"  OP-PATIO: {o.name:26s} center({w[0]:.2f},{w[1]:.2f}) z[{w[2]:.2f},{w[3]:.2f}]")
print("PK2_END")
