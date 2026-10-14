"""Focus-dump: deur/wand-segmenten van 'shed', + analyse bench/path/boulder.
Run: blender -b --python dump_focus.py -- <blend>
"""
import bpy, sys
from mathutils import Vector
argv = sys.argv[sys.argv.index("--")+1:]
BLEND = argv[0]
bpy.ops.wm.open_mainfile(filepath=BLEND)
dg=bpy.context.evaluated_depsgraph_get()

def wbb_obj(o):
    oe=o.evaluated_get(dg)
    me=oe.to_mesh() if oe.type=='MESH' else None
    pts=[(o.matrix_world @ Vector(c)) for c in o.bound_box]
    return (min(p.x for p in pts),max(p.x for p in pts),
            min(p.y for p in pts),max(p.y for p in pts),
            min(p.z for p in pts),max(p.z for p in pts))

# shed is een hierarchie? dump children/onderdelen
shed=bpy.data.objects.get('shed')
print("=== SHED HIERARCHY ===")
if shed:
    def walk(o,d=0):
        try: bb=wbb_obj(o)
        except: bb=None
        nm=o.name.lower()
        flag=''
        if any(k in nm for k in ('deur','door','raam','window','glas','glass','kozijn')): flag=' <-- OPENING'
        if bb:
            print("%s%-30s c=(%6.2f,%6.2f) z=[%5.2f..%5.2f] sz=(%4.2f,%4.2f,%4.2f)%s"%(
                "  "*d,o.name[:30],(bb[0]+bb[1])/2,(bb[2]+bb[3])/2,bb[4],bb[5],bb[1]-bb[0],bb[3]-bb[2],bb[5]-bb[4],flag))
        for c in o.children: walk(c,d+1)
    walk(shed)

# alle objects met deur/door/raam/glas in naam, ongeacht parent
print("=== ALLE OPENINGEN (deur/raam/glas) ===")
for o in bpy.data.objects:
    nm=o.name.lower()
    if any(k in nm for k in ('deur','door','raam','window','glas','glass','kozijn','frame')) and o.type=='MESH':
        bb=wbb_obj(o)
        print("%-30s parent=%s c=(%6.2f,%6.2f) z=[%5.2f..%5.2f]"%(
            o.name[:30],o.parent.name if o.parent else "-",(bb[0]+bb[1])/2,(bb[2]+bb[3])/2,bb[4],bb[5]))

# camera
print("=== CAMERA ===")
for o in bpy.data.objects:
    if o.type=='CAMERA':
        print("%-20s loc=(%6.2f,%6.2f,%6.2f) rot=(%5.1f,%5.1f,%5.1f) scene_cam=%s"%(
            o.name,o.location.x,o.location.y,o.location.z,
            __import__('math').degrees(o.rotation_euler.x),
            __import__('math').degrees(o.rotation_euler.y),
            __import__('math').degrees(o.rotation_euler.z),
            o==bpy.context.scene.camera))
print("=== END ===")
