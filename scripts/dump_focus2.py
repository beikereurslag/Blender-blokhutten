"""Focus-dump v2 zonder evaluated geometry (geen OOM). Schrijft naar file.
Run: blender -b --python dump_focus2.py -- <blend> <outtxt>
"""
import bpy, sys, math
from mathutils import Vector
argv = sys.argv[sys.argv.index("--")+1:]
BLEND = argv[0]
OUT = argv[1]
bpy.ops.wm.open_mainfile(filepath=BLEND)
lines=[]
def P(*a): lines.append(" ".join(str(x) for x in a))

def wbb(o):
    pts=[(o.matrix_world @ Vector(c)) for c in o.bound_box]
    return (min(p.x for p in pts),max(p.x for p in pts),
            min(p.y for p in pts),max(p.y for p in pts),
            min(p.z for p in pts),max(p.z for p in pts))

shed=bpy.data.objects.get('shed')
P("=== SHED CHILDREN ===")
if shed:
    P("shed self: children=%d type=%s"%(len(shed.children),shed.type))
    def walk(o,d=0):
        bb=wbb(o)
        nm=o.name.lower()
        flag=''
        if any(k in nm for k in ('deur','door','raam','window','glas','glass','kozijn','opening')): flag=' <-- OPENING'
        P("%s%-32s [%s] c=(%6.2f,%6.2f) z=[%5.2f..%5.2f] sz=(%4.2f,%4.2f,%4.2f)%s"%(
            "  "*d,o.name[:32],o.type[:4],(bb[0]+bb[1])/2,(bb[2]+bb[3])/2,bb[4],bb[5],
            bb[1]-bb[0],bb[3]-bb[2],bb[5]-bb[4],flag))
        for c in sorted(o.children,key=lambda x:x.name): walk(c,d+1)
    walk(shed)

P("=== ALLE MESH met deur/raam/glas/opening in naam ===")
for o in sorted(bpy.data.objects,key=lambda x:x.name):
    nm=o.name.lower()
    if o.type!='MESH': continue
    if any(k in nm for k in ('deur','door','raam','window','glas','glass','kozijn','opening','overkap','carport','veranda','luifel')):
        bb=wbb(o)
        P("%-30s parent=%-14s c=(%6.2f,%6.2f) z=[%5.2f..%5.2f]"%(
            o.name[:30],(o.parent.name if o.parent else "-")[:14],(bb[0]+bb[1])/2,(bb[2]+bb[3])/2,bb[4],bb[5]))

P("=== CAMERA ===")
for o in bpy.data.objects:
    if o.type=='CAMERA':
        P("%-20s loc=(%6.2f,%6.2f,%6.2f) rotdeg=(%5.1f,%5.1f,%5.1f) scene_cam=%s"%(
            o.name,o.location.x,o.location.y,o.location.z,
            math.degrees(o.rotation_euler.x),math.degrees(o.rotation_euler.y),
            math.degrees(o.rotation_euler.z),o==bpy.context.scene.camera))
P("=== END ===")
open(OUT,"w",encoding="utf-8").write("\n".join(lines))
print("WROTE",OUT,len(lines),"lines")
