"""Query HedgeSprig GN-koppeling + BeukBlok + Drift/weed op het dek. Read-only."""
import bpy, sys
from mathutils import Vector
argv = sys.argv; F = argv[argv.index("--")+1]
bpy.ops.wm.open_mainfile(filepath=F)

def bb(o):
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs]; ys=[c.y for c in cs]; zs=[c.z for c in cs]
    return (min(xs),max(xs),min(ys),max(ys),min(zs),max(zs))

print("Q_START")
for nm in ("HedgeSprig","Hedge_Back","BeukBlok_0","BeukBlok_1","BeukBlok_2"):
    o = bpy.data.objects.get(nm)
    if not o: print(nm, "MISSING"); continue
    mods = []
    for m in o.modifiers:
        if m.type == 'NODES':
            ng = m.node_group.name if m.node_group else None
            inp = {}
            try:
                for k in m.keys():
                    v = m[k]
                    if hasattr(v, 'name'): inp[k] = f"{type(v).__name__}:{v.name}"
                    else: inp[k] = v
            except Exception as e:
                inp = {"err": str(e)}
            mods.append(("NODES", ng, inp))
        else:
            mods.append((m.type, getattr(m,'name',''), {}))
    print(f"{nm}: parent={o.parent.name if o.parent else None} mods={mods}")
    print(f"   children={[c.name for c in o.children]}")

# Drift_/weed/BakGras parts overlapping the deck footprint x[-3.5,3.5] y[1.72,4.5]
print("--- PLANT PARTS ON/IN DECK (x[-3.5,3.5] y[1.72,4.5]) ---")
import re
for o in bpy.data.objects:
    if o.type!='MESH' or not len(o.data.vertices): continue
    if not re.search(r'(Drift_|BakGras_|weed_plant)', o.name): continue
    b = bb(o)
    cx=(b[0]+b[1])/2; cy=(b[2]+b[3])/2
    if -3.6<cx<3.6 and 1.6<cy<4.6:
        print(f"  {o.name:18s} c=({cx:.2f},{cy:.2f}) z[{b[4]:.2f},{b[5]:.2f}] parent={o.parent.name if o.parent else None}")
# Drift roots summary
print("--- Drift_ ROOTS (empties) ---")
for o in sorted(bpy.data.objects, key=lambda x:x.name):
    if o.name.startswith("Drift_") and o.parent is None:
        kids=[c for c in o.children_recursive if c.type=='MESH']
        if kids:
            xs=[];ys=[]
            for k in kids:
                b=bb(k); xs+=[b[0],b[1]]; ys+=[b[2],b[3]]
            print(f"  {o.name:14s} kids={len(kids)} xspan[{min(xs):.1f},{max(xs):.1f}] yspan[{min(ys):.1f},{max(ys):.1f}]")
print("Q_END")
