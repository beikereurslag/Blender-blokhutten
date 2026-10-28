"""Dump alle root-object posities/bboxes voor placement-analyse zonder render."""
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

print("=== ROOT OBJECTS ===")
rows=[]
for o in bpy.data.objects:
    if o.parent is not None: continue
    if o.type=='LIGHT':
        print("LIGHT %-28s loc=(%.2f,%.2f,%.2f) energy=%.0f type=%s"%(o.name,o.location.x,o.location.y,o.location.z,getattr(o.data,'energy',0),getattr(o.data,'type','')))
        continue
    if o.type=='CAMERA':
        print("CAMERA %-27s loc=(%.2f,%.2f,%.2f) rot=(%.0f,%.0f,%.0f)"%(o.name,o.location.x,o.location.y,o.location.z,
              __import__('math').degrees(o.rotation_euler.x),__import__('math').degrees(o.rotation_euler.y),__import__('math').degrees(o.rotation_euler.z)))
        continue
    ms=root_meshes(o)
    if not ms: 
        print("EMPTY %-28s loc=(%.2f,%.2f,%.2f) children=%d"%(o.name,o.location.x,o.location.y,o.location.z,len(o.children)))
        continue
    bb=wbb(ms)
    if not bb: continue
    cx=(bb[0]+bb[1])/2; cy=(bb[2]+bb[3])/2
    hr="HIDE" if o.hide_render else "    "
    rows.append((o.name,bb,cx,cy,hr))
rows.sort(key=lambda r:(r[2],r[3]))
for name,bb,cx,cy,hr in rows:
    print("%s %-30s X[%.2f,%.2f] Y[%.2f,%.2f] Z[%.2f,%.2f] c=(%.2f,%.2f)"%(hr,name,bb[0],bb[1],bb[2],bb[3],bb[4],bb[5],cx,cy))
print("=== CAMERA ACTIVE: %s ==="%(bpy.context.scene.camera.name if bpy.context.scene.camera else "NONE"))
