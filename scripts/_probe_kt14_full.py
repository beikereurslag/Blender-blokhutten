"""Grondige scene-14 probe (Roosmarijn Kruidenterras, mediterraan).
Dumpt camera, overkapping-structuur, potten/olijf/planten (world-pos + subtree bbox),
floaters, heg/bomen. Run: blender -b <blend> --python scripts/_probe_kt14_full.py
"""
import bpy, math
from mathutils import Vector

def sub_bb(o):
    ms = [c for c in o.children_recursive if c.type == 'MESH' and len(c.data.vertices)]
    if o.type == 'MESH' and len(o.data.vertices): ms.append(o)
    cs = []
    for m in ms:
        cs += [m.matrix_world @ Vector(c) for c in m.bound_box]
    if not cs: return None
    return (min(c.x for c in cs), max(c.x for c in cs),
            min(c.y for c in cs), max(c.y for c in cs),
            min(c.z for c in cs), max(c.z for c in cs), len(ms))

print("\n########## CAMERA ##########")
scn = bpy.context.scene
for cam in [o for o in bpy.data.objects if o.type == 'CAMERA']:
    w = cam.matrix_world
    loc = w.translation
    fwd = w.to_3x3() @ Vector((0, 0, -1))
    rot = [math.degrees(a) for a in cam.rotation_euler]
    act = " <ACTIVE>" if scn.camera == cam else ""
    print(f"  {cam.name}{act} loc=({loc.x:.2f},{loc.y:.2f},{loc.z:.2f}) "
          f"lens={cam.data.lens:.0f}mm rot_deg=({rot[0]:.0f},{rot[1]:.0f},{rot[2]:.0f}) "
          f"fwd=({fwd.x:.2f},{fwd.y:.2f},{fwd.z:.2f})")

print("\n########## TOP-LEVEL OBJECTS (parent=None) by keyword ##########")
KW = ("pot", "olij", "olive", "plant", "kruid", "herb", "bak", "bed", "bistro", "stoel",
      "chair", "tafel", "table", "terras", "patio", "overkap", "veranda", "canopy", "luifel",
      "dak", "roof", "post", "paal", "stoep", "deur", "door", "hedge", "heg", "pine", "boom",
      "tree", "jac", "lavend", "rozemarijn", "rosemary", "thyme", "tijm", "basil", "sorrel",
      "periwinkle", "weed", "shrub", "grond", "ground", "gras", "grass", "cabin", "wall", "wand",
      "sm_plant", "flower", "bloem", "lamp", "light")
rows = []
for o in bpy.data.objects:
    if o.parent is not None: continue
    nm = o.name.lower()
    if not any(k in nm for k in KW): continue
    w = o.matrix_world.translation
    if abs(w.x) > 900 or abs(w.y) > 900:
        tag = " [PARKED]"
    else:
        tag = ""
    bb = sub_bb(o)
    if bb:
        print(f"  {o.name:<30} {o.type:<7} w=({w.x:6.2f},{w.y:6.2f},{w.z:6.2f}) "
              f"bb_x[{bb[0]:6.2f},{bb[1]:6.2f}] y[{bb[2]:6.2f},{bb[3]:6.2f}] z[{bb[4]:6.2f},{bb[5]:6.2f}] m={bb[6]}{tag}")
    else:
        print(f"  {o.name:<30} {o.type:<7} w=({w.x:6.2f},{w.y:6.2f},{w.z:6.2f}) (no-mesh){tag}")

print("\n########## FLOATERS (top-level mesh subtree min_z > 0.08, not parked) ##########")
for o in bpy.data.objects:
    if o.parent is not None: continue
    if abs(o.matrix_world.translation.x) > 900: continue
    bb = sub_bb(o)
    if not bb: continue
    if bb[4] > 0.08:
        # skip obvious canopy/lamp by height
        span_z = bb[5]-bb[4]
        print(f"  FLOAT {o.name:<28} min_z={bb[4]:.2f} max_z={bb[5]:.2f} type={o.type}")

print("\n########## COLLECTIONS ##########")
for c in bpy.data.collections:
    n = len([o for o in c.objects])
    if n: print(f"  {c.name:<28} objs={n}")

print("\n########## RENDER/VIEW ##########")
print(f"  engine={scn.render.engine} res=({scn.render.resolution_x}x{scn.render.resolution_y}) "
      f"view={scn.view_settings.view_transform}/{scn.view_settings.look} exp={scn.view_settings.exposure}")
w = bpy.context.scene.world
print("\n==== PROBE END ====")
