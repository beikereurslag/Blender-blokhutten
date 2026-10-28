"""Diepe geometrie-audit van een cabin-scene. Detecteert objectief:
floaters, gezonken props, gekantelde meubels, props in gesloten cabinevolume,
hardscape z-fighting, diepe prop-prop-intersecties, bomen/heg in de cabin.

Run: blender -b --python audit_scene_deep.py -- <blend> <cx0> <cx1> <cy0> <cy1>
Print DEFECT-regels + SUMMARY.
"""
import bpy, sys, math, itertools
from mathutils import Vector

argv = sys.argv[sys.argv.index("--")+1:]
BLEND = argv[0]
CX0, CX1, CY0, CY1 = map(float, argv[1:5])

bpy.ops.wm.open_mainfile(filepath=BLEND)
deps = bpy.context.evaluated_depsgraph_get()

STRUCT = ('wall-','parentboard','roof','deur','pole-','foundation','trim','fascia',
          'flatroof','.scharnier','.doorhandle','door_pot','ground','sun','herocam',
          'altcam','camera','mist','rake','karesansui')
TREEHEDGE = ('hedge_','beukblok','beukenblok','beukblok_','rozemarijn_','snoeiwolk',
             'treering','treefull','treerepl','treefill','treeedge','bosden','bosfill',
             'ringpine','gappine','backbirch','birch_','berk_','parasolden','tuinden',
             'framemaple','statementmaple','anchormaple','zenmaple','acer','olijfpot',
             'jacaranda','den_')
HARDSCAPE = ('terras','pad','stoep','deck','vlonder','slab','maaipad','loopplaat',
             'wadi','grindvlak','engawa','apron')
LIGHTISH = ('l_','light','glow')

def is_struct(n): return any(k in n for k in STRUCT)
def is_treehedge(n): return any(k in n for k in TREEHEDGE)
def is_hardscape(n): return any(n.startswith(k) or k in n for k in HARDSCAPE)
def is_light(o): return o.type in ('LIGHT','CAMERA') or any(k in o.name.lower() for k in LIGHTISH)

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

# verzamel prop-roots
props=[]   # (name, bbox, obj)
for o in bpy.data.objects:
    if o.parent is not None: continue
    if is_light(o): continue
    n=o.name.lower()
    if is_struct(n) or is_treehedge(n): continue
    ms=root_meshes(o)
    if not ms: continue
    if o.hide_render: continue
    bb=wbb(ms)
    if not bb: continue
    props.append((o.name, bb, o))

defects=[]
def D(*a): defects.append(" ".join(str(x) for x in a))

# floaters / sunk — alleen voor echte grondstaande props (composiet-onderdelen uitsluiten)
GROUND=('bistro','fauteuil','chair','stoel','bench','bank','table','tafel','pot',
        'mand','basket','vogelbad','birdbath','fiets','bike','picnic','picknick',
        'dining','regenton','boulder','steen','stone','stapsteen','lavendel',
        'hortensia','rozen','spiraea','vlinder','gazania','kruid','olijf','feeder')
EXCL=('band','rand','trede','water','duig','binnenwand','handdoek','rek_','houtblok',
      'hout_','slinger','bulb','festo','hang','bord','karaf','glas','mok','kan_','boek',
      'theekom','laptop','scherm','plaid','vacht','arm','boog')
for name,bb,o in props:
    nl=name.lower()
    if is_hardscape(nl): continue
    if not any(g in nl for g in GROUND): continue
    if any(e in nl for e in EXCL): continue
    minz=bb[4]
    if minz>0.15:
        D("DEFECT floater", name, "minz=%.2f"%minz)
    if minz<-0.07:
        D("DEFECT sunk", name, "minz=%.2f"%minz)

# tilted meubels/props (verwacht rechtop)
UPRIGHT=('bistro','fauteuil','stoel','chair','bank','bench','tafel','table','pot_',
         'mand','basket','lantaarn','lantern','vogelbad','birdbath','fiets','bike',
         'picknick','picnic','dining','regenton','bureau','werkstoel')
for name,bb,o in props:
    nl=name.lower()
    if not any(k in nl for k in UPRIGHT): continue
    rx=math.degrees(o.rotation_euler.x)%90
    ry=math.degrees(o.rotation_euler.y)%90
    rxm=min(rx,90-rx); rym=min(ry,90-ry)
    if rxm>6 or rym>6:
        D("DEFECT tilt", name, "rx=%.0f ry=%.0f"%(math.degrees(o.rotation_euler.x),math.degrees(o.rotation_euler.y)))

# in gesloten cabinevolume
for name,bb,o in props:
    nl=name.lower()
    if is_hardscape(nl): continue
    cx=(bb[0]+bb[1])/2; cy=(bb[2]+bb[3])/2
    if CX0<cx<CX1 and CY0<cy<CY1 and bb[5]>0.25:
        D("DEFECT in_cabin", name, "c=(%.2f,%.2f) top=%.2f"%(cx,cy,bb[5]))

# hardscape z-fight (vlakke platen die in XY overlappen op ~zelfde z)
hard=[(name,bb) for name,bb,o in props if is_hardscape(name.lower())]
for (na,ba),(nb,bb) in itertools.combinations(hard,2):
    ox=min(ba[1],bb[1])-max(ba[0],bb[0])
    oy=min(ba[3],bb[3])-max(ba[2],bb[2])
    if ox>0.05 and oy>0.05:
        dz=abs(ba[5]-bb[5])
        if dz<0.025:
            D("DEFECT zfight", na, nb, "dz=%.3f ovXY=%.2fx%.2f"%(dz,ox,oy))

# diepe prop-prop intersectie (zelfde naam-prefix overslaan: stapels/duigen/rijen)
def prefix(n):
    import re
    return re.sub(r'[_\.\-]?\d+.*$','',n).lower()
big=[(name,bb) for name,bb,o in props if not is_hardscape(name.lower())
     and (bb[1]-bb[0])>0.25 and (bb[3]-bb[2])>0.25]
for (na,ba),(nb,bb) in itertools.combinations(big,2):
    if prefix(na)==prefix(nb): continue
    ox=min(ba[1],bb[1])-max(ba[0],bb[0])
    oy=min(ba[3],bb[3])-max(ba[2],bb[2])
    oz=min(ba[5],bb[5])-max(ba[4],bb[4])
    if ox>0.28 and oy>0.28 and oz>0.28:
        D("DEFECT overlap", na, nb, "ov=%.2fx%.2fx%.2f"%(ox,oy,oz))

# bomen/heg in gesloten cabinevolume
for o in bpy.data.objects:
    if o.parent is not None: continue
    n=o.name.lower()
    if not is_treehedge(n): continue
    ms=root_meshes(o)
    if not ms or o.hide_render: continue
    bb=wbb(ms)
    if not bb: continue
    cx=(bb[0]+bb[1])/2; cy=(bb[2]+bb[3])/2
    if CX0<cx<CX1 and CY0<cy<CY1 and bb[5]>0.3:
        D("DEFECT tree_in_cabin", o.name, "c=(%.2f,%.2f)"%(cx,cy))

print("=== AUDIT %s ===" % BLEND.split("\\")[-1])
for d in defects: print(d)
print("SUMMARY props=%d defects=%d" % (len(props), len(defects)))
