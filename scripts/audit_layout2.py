"""Layout-dump bovenop de BEWEZEN deep-audit-loader. Schrijft naar OUTTXT.
Run: blender -b --python audit_layout2.py -- <blend> <outtxt>
"""
import bpy, sys
from mathutils import Vector

argv = sys.argv[sys.argv.index("--")+1:]
BLEND = argv[0]
OUTTXT = argv[1]

bpy.ops.wm.open_mainfile(filepath=BLEND)
deps = bpy.context.evaluated_depsgraph_get()

lines=[]
def P(*a):
    s=" ".join(str(x) for x in a)
    lines.append(s)

def root_meshes(o):
    out=[]; st=[o]
    while st:
        x=st.pop()
        if x.type=='MESH': out.append(x)
        st.extend(x.children)
    return out
def wbb(meshes):
    pts=[(m.matrix_world @ Vector(c)) for m in meshes for c in m.bound_box]
    if not pts: return None
    return (min(p.x for p in pts),max(p.x for p in pts),
            min(p.y for p in pts),max(p.y for p in pts),
            min(p.z for p in pts),max(p.z for p in pts))

rows=[]
for o in bpy.data.objects:
    if o.parent is not None: continue
    if o.type in ('LIGHT','CAMERA'): continue
    ms=root_meshes(o)
    if not ms: continue
    if o.hide_render: continue
    bb=wbb(ms)
    if not bb: continue
    rows.append((o.name,bb,o))

P("=== LAYOUT MAP ===")
for name,bb,o in sorted(rows,key=lambda r:(r[1][0])):
    cx=(bb[0]+bb[1])/2; cy=(bb[2]+bb[3])/2
    P("OBJ %-30s x[%6.2f,%6.2f] y[%6.2f,%6.2f] z[%6.2f,%6.2f] c(%5.2f,%5.2f)"%(
        name,bb[0],bb[1],bb[2],bb[3],bb[4],bb[5],cx,cy))

HARD=('terras','pad','stoep','deck','vlonder','slab','engawa','apron','tegel','grind','klinker','loop')
hard=[(n,bb) for n,bb,o in rows if any(k in n.lower() for k in HARD)]
P("--- HARDSCAPE ---")
for n,bb in hard: P("HARD %-30s x[%6.2f,%6.2f] y[%6.2f,%6.2f] z=%.3f"%(n,bb[0],bb[1],bb[2],bb[3],bb[5]))

def on_hard(bb):
    cx=(bb[0]+bb[1])/2; cy=(bb[2]+bb[3])/2
    for n,hb in hard:
        if hb[0]<=cx<=hb[1] and hb[2]<=cy<=hb[3]:
            inside = (bb[0]>=hb[0]-0.05 and bb[1]<=hb[1]+0.05 and bb[2]>=hb[2]-0.05 and bb[3]<=hb[3]+0.05)
            return ('full' if inside else 'partial', n)
    return ('off', None)
GP=('bistro','fauteuil','chair','stoel','bench','bank','table','tafel','pot',
    'mand','basket','bak','planter','kruid','olijf','lavendel','rozemarijn','plant')
P("--- PROP PLACEMENT vs HARDSCAPE ---")
for name,bb,o in rows:
    nl=name.lower()
    if not any(g in nl for g in GP): continue
    st,hn=on_hard(bb)
    P("PLACE %-30s -> %-7s %s  minz=%.2f"%(name,st,hn or "",bb[4]))
P("SUMMARY rows=%d hard=%d"%(len(rows),len(hard)))

with open(OUTTXT,"w",encoding="utf-8") as f:
    f.write("\n".join(lines)+"\n")
print("\n".join(lines))
print("[WROTE] "+OUTTXT)
