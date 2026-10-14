import bpy, sys, math
from mathutils import Vector
argv = sys.argv[sys.argv.index("--")+1:]
BLEND = argv[0]
bpy.ops.wm.open_mainfile(filepath=BLEND)
deps = bpy.context.evaluated_depsgraph_get()

def wbb(o):
    pts=[o.matrix_world @ Vector(c) for c in o.bound_box]
    return (min(p.x for p in pts),max(p.x for p in pts),
            min(p.y for p in pts),max(p.y for p in pts),
            min(p.z for p in pts),max(p.z for p in pts))

lines = ["=== OBJECTS ==="]
for o in sorted(bpy.data.objects, key=lambda x:x.name):
    if o.type != 'MESH':
        lines.append("%-26s TYPE=%s par=%s" % (o.name, o.type, o.parent.name if o.parent else '-'))
        continue
    b = wbb(o)
    lines.append("%-26s X[%6.2f,%6.2f] Y[%6.2f,%6.2f] Z[%6.2f,%6.2f] rot=(%.0f,%.0f,%.0f) par=%s%s" % (
        o.name, b[0], b[1], b[2], b[3], b[4], b[5],
        math.degrees(o.rotation_euler.x), math.degrees(o.rotation_euler.y), math.degrees(o.rotation_euler.z),
        o.parent.name if o.parent else '-',
        ' HIDE' if o.hide_render else ''))
with open(r"C:/Users/beike/Documents/Blender-blokhutten/scripts/_bbox_result.txt", "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))
print("WROTE %d lines" % len(lines))
