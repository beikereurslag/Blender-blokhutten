import bpy, sys
from mathutils import Vector
argv = sys.argv[sys.argv.index("--")+1:]
BLEND = argv[0]
bpy.ops.wm.open_mainfile(filepath=BLEND)
deps = bpy.context.evaluated_depsgraph_get()

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

import math
OUTTXT = r"C:\Users\beike\Documents\Blender-blokhutten\_placement.txt"
LINES=["=== PLACEMENT DUMP ==="]
print("=== PLACEMENT DUMP ===")
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
    rotx=math.degrees(o.rotation_euler.x); roty=math.degrees(o.rotation_euler.y); rotz=math.degrees(o.rotation_euler.z)
    rows.append((o.name,cx,cy,bb[4],bb[5],sx,sy,sz,rotx,roty,rotz,o.hide_render))
rows.sort(key=lambda r:(r[2],r[1]))
for r in rows:
    s="OBJ %-26s cx=%6.2f cy=%6.2f minz=%6.3f maxz=%6.3f dim=%5.2fx%5.2fx%5.2f rot=(%5.1f,%5.1f,%5.1f)%s"%(
        r[0][:26],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10]," HIDDEN" if r[11] else "")
    print(s); LINES.append(s)
LINES.append("COUNT %d"%len(rows))
print("COUNT %d"%len(rows))
with open(OUTTXT,"w",encoding="utf-8") as f:
    f.write("\n".join(LINES))
