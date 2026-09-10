"""Dump XY/Z-posities van props + struct + hardscape voor placement-diagnose.
Geen render -> geen VRAM-blowup. Print compacte top-down kaart-data.
Run: blender -b --python dump_placement.py -- <blend>
"""
import bpy, sys
from mathutils import Vector
argv = sys.argv[sys.argv.index("--")+1:]
BLEND = argv[0]
bpy.ops.wm.open_mainfile(filepath=BLEND)

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

HARDSCAPE=('terras','pad','stoep','deck','vlonder','slab','maaipad','loopplaat',
           'wadi','grindvlak','engawa','apron','step','staptegel','stapsteen')
STRUCT=('wall','parentboard','roof','deur','door','pole','foundation','trim','fascia',
        'flatroof','shed','veranda','carport','overkap','post','beam','balk','gevel')

rows=[]
for o in bpy.data.objects:
    if o.parent is not None: continue
    if o.type in ('LIGHT','CAMERA'): continue
    ms=root_meshes(o)
    if not ms: continue
    bb=wbb(ms)
    if not bb: continue
    cx=(bb[0]+bb[1])/2; cy=(bb[2]+bb[3])/2
    sx=bb[1]-bb[0]; sy=bb[3]-bb[2]; sz=bb[5]-bb[4]
    nl=o.name.lower()
    kind='prop'
    if any(k in nl for k in HARDSCAPE): kind='HARD'
    elif any(k in nl for k in STRUCT): kind='STRUCT'
    rows.append((kind,o.name,cx,cy,bb[4],bb[5],sx,sy,sz,o.hide_render))

rows.sort(key=lambda r:(r[0],r[1]))
print("=== PLACEMENT ===")
print("KIND NAME cx cy minz maxz sx sy sz hidden")
for k,n,cx,cy,mnz,mxz,sx,sy,sz,h in rows:
    print("%-6s %-26s c=(%6.2f,%6.2f) z=[%5.2f..%5.2f] sz=(%4.2f,%4.2f,%4.2f) %s"%(
        k,n[:26],cx,cy,mnz,mxz,sx,sy,sz,"HIDDEN" if h else ""))
print("=== END ===")
