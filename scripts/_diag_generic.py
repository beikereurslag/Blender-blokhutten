"""Generieke read-only scene-inventaris. Geen save.
Gebruik: blender --background --python _diag_generic.py -- <scene.blend>
"""
import bpy, sys
from mathutils import Vector
argv = sys.argv
F = argv[argv.index("--") + 1] if "--" in argv else argv[-1]
bpy.ops.wm.open_mainfile(filepath=F)
scn = bpy.context.scene

def bb(o):
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs]; ys=[c.y for c in cs]; zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
def matkind(o):
    out=[]
    for s in getattr(o,"material_slots",[]):
        m=s.material
        if not m: out.append("<none>"); continue
        imgs=[n.image.name for n in m.node_tree.nodes if m.use_nodes and n.type=='TEX_IMAGE' and n.image]
        out.append(f"{m.name}:{('img['+','.join(imgs)+']') if imgs else 'flat'}")
    return out

print("INV_START", F)
cam=scn.camera
print("CAMERA:", cam.name if cam else None,
      (str(tuple(round(v,2) for v in cam.location))+f" lens={cam.data.lens:.0f}") if cam else "")
print("RENDER:", scn.render.engine, scn.view_settings.view_transform, "look=", scn.view_settings.look,
      "exp=", round(scn.view_settings.exposure,2), "res", scn.render.resolution_x, scn.render.resolution_y)
print("COLLECTIONS:", [(c.name, len(c.objects)) for c in bpy.data.collections])
keys=('deck','vlonder','terras','engawa','pad','path','stap','tegel','klink','grind','gravel',
      'slab','steen','stone','flag','tobi','bak','planter','corten','kruid','herb','zand','sand',
      'pot','bollard','lamp','lantaarn','lantern','regenton','barrel','vat','wadi','mos','moss',
      'tsukubai','water','fontein','fountain','vacht','throw','sheep','tafel','table','plate','bord',
      'mok','mug','glas','glass','fles','wijn','wine','thee','tea','lavend','roos','rose','hortensia',
      'bank','bench','stoel','chair','sedum','rake','karesansui','boulder','rock','loop','plank')
print("--- KEY OBJECTS (procedureel kandidaat) + materiaal ---")
seen=set()
for o in sorted(bpy.data.objects, key=lambda x:x.name):
    n=o.name.lower()
    if any(k in n for k in keys) and id(o) not in seen:
        seen.add(id(o))
        if o.type=='MESH' and len(o.data.vertices):
            b=bb(o); print(f"  {o.name:30s} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}] v={len(o.data.vertices)} {matkind(o)}")
        elif o.type=='MESH':
            print(f"  {o.name:30s} MESH(empty-data)")
        else:
            print(f"  {o.name:30s} {o.type} loc{tuple(round(v,2) for v in o.location)}")
print("--- ALL top-level mesh objects (naam) ---")
tops=sorted(o.name for o in bpy.data.objects if o.type=='MESH' and not o.parent)
print("  count:", len(tops), tops)
print("INV_END", F)
