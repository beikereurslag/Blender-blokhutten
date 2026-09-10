import bpy
from mathutils import Vector
F=r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Lavendel-400x300-400-zijwand\style-boerderij\lavendel_pluktuin.blend"
bpy.ops.wm.open_mainfile(filepath=F)
def wbb(o):
    ms=[c for c in [o]+list(o.children_recursive) if c.type=='MESH' and len(c.data.vertices)]
    cs=[c.matrix_world@Vector(v) for c in ms for v in c.bound_box]
    if not cs: return None
    xs=[p.x for p in cs];ys=[p.y for p in cs];zs=[p.z for p in cs]
    return (min(xs),max(xs),min(ys),max(ys),min(zs),max(zs))
print("ROZEN_START  (RoseArch/Rozenboog op ~(2.95,6.6))")
for o in sorted(bpy.data.objects,key=lambda x:x.name):
    n=o.name.lower()
    if any(k in n for k in ('roos','rose','boog','arch','poort')):
        if o.parent and o.type!='EMPTY': continue
        w=wbb(o)
        if w: print(f"  {o.name:30s} {o.type:6s} x[{w[0]:.2f},{w[1]:.2f}] y[{w[2]:.2f},{w[3]:.2f}] z[{w[4]:.3f},{w[5]:.3f}]{'  <-- ZWEEFT' if w[4]>0.15 else ''}")
        else: print(f"  {o.name:30s} {o.type}")
print("ROZEN_END")
