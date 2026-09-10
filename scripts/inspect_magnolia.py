import bpy, math, sys
from mathutils import Vector
OUT=r'C:/Users/beike/Documents/Blender-blokhutten/scripts/inspect_magnolia_out.txt'
_f=open(OUT,'w',encoding='utf-8')
def print(*a, **k):
    _f.write(" ".join(str(x) for x in a)+"\n"); _f.flush()
# scene is already loaded via -b <blend> on the command line

def rm(o):
    out=[];st=[o]
    while st:
        x=st.pop()
        if x.type=='MESH': out.append(x)
        st.extend(x.children)
    return out
def wbb(ms):
    pts=[(m.matrix_world @ Vector(c)) for m in ms for c in m.bound_box]
    if not pts: return None
    return (min(p.x for p in pts),max(p.x for p in pts),min(p.y for p in pts),max(p.y for p in pts),min(p.z for p in pts),max(p.z for p in pts))

print('=== PROP TREES (children, world bb) ===')
for nm in ['Bank','Lantaarn_root','Vacht']:
    o=bpy.data.objects.get(nm)
    if not o:
        print(nm,'MISSING'); continue
    print('--',nm,'loc',tuple(round(v,2) for v in o.location),'rot_deg',tuple(round(math.degrees(v),1) for v in o.rotation_euler))
    for c in o.children_recursive:
        if c.type=='MESH':
            bb=wbb([c])
            if bb: print('    %-26s x[%.2f,%.2f] y[%.2f,%.2f] z[%.2f,%.2f]'%((c.name,)+bb))
        else:
            print('    %-26s %s'%(c.name,c.type))

print()
print('=== Footprint loc ===')
for nm in ['Terras','Stap_0','Stap_1','Stap_2','Stap_3','Stap_4','shed']:
    o=bpy.data.objects.get(nm)
    if o: print(nm,'loc',tuple(round(v,2) for v in o.location))

print()
print('=== round disc / well / stone objects ===')
KEYS=['disc','well','put','round','steen','stone','grind','wadi','vijver','firepit','vuur','schaal','schijf','plate','manhole','rond','cirkel']
for o in bpy.data.objects:
    nl=o.name.lower()
    if any(k in nl for k in KEYS):
        ms=rm(o); bb=wbb(ms) if ms else None
        print('%-26s %-7s bb %s hr=%s'%(o.name,o.type,('x[%.2f,%.2f] y[%.2f,%.2f] z[%.2f,%.2f]'%bb if bb else 'none'),o.hide_render))

print()
print('=== ALL root mesh/empty NOT struct/tree/hedge (props) with bb ===')
SKIP=('treering','pine_tree','berk','hedge','sketchfab','sun','herocam','altcam','ground','wall','roof','pole','foundation','shed')
for o in sorted(bpy.data.objects,key=lambda x:x.name):
    if o.parent is not None: continue
    nl=o.name.lower()
    if any(k in nl for k in SKIP): continue
    if o.type in ('LIGHT','CAMERA'): continue
    ms=rm(o); bb=wbb(ms) if ms else None
    if bb: print('%-26s %-7s x[%.2f,%.2f] y[%.2f,%.2f] z[%.2f,%.2f] hr=%s'%((o.name,o.type)+bb+(o.hide_render,)))

print("=== END ===")
_f.close()
