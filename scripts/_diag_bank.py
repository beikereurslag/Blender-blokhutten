import bpy, math
from mathutils import Vector
F=r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Lavendel-400x300-400-zijwand\style-boerderij\lavendel_pluktuin.blend"
bpy.ops.wm.open_mainfile(filepath=F)
print("BANK_START")
for nm in ("Bank_root","bench","bench.fbx","bench_bench_0"):
    o=bpy.data.objects.get(nm)
    if not o: print(f"  {nm}: -"); continue
    p=o.parent.name if o.parent else None
    print(f"  {nm:16s} type={o.type} parent={p} loc={tuple(round(v,2) for v in o.location)} rotZdeg={round(math.degrees(o.rotation_euler.z),1)} scale={tuple(round(v,3) for v in o.scale)}")
b=bpy.data.objects.get("Bank_root")
if b:
    print("  Bank_root children_recursive:")
    for c in b.children_recursive:
        if c.type=='MESH':
            cs=[c.matrix_world@Vector(v) for v in c.bound_box];xs=[p.x for p in cs];ys=[p.y for p in cs]
            print(f"    {c.name} parent={c.parent.name if c.parent else None} worldX[{min(xs):.2f},{max(xs):.2f}] worldY[{min(ys):.2f},{max(ys):.2f}]")
# is bench_bench_0 onder Bank_root?
bb=bpy.data.objects.get("bench_bench_0")
if bb:
    chain=[];x=bb
    while x: chain.append(x.name);x=x.parent
    print("  bench_bench_0 parent-chain:",chain)
print("  PotRoos objs:",[o.name for o in bpy.data.objects if o.name.startswith("PotRoos")][:6])
print("BANK_END")
