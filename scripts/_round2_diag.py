"""Ronde-2 diagnose-dump. Open een .blend headless en print gericht wat voor de
ronde-2 feedback relevant is: camera, lampen, zwevende objecten, dak-hoogte, en
objecten waarvan de naam een feedback-trefwoord bevat (bank/plant/pot/bloem/boom/
lamp/zand/grind/moss/karesansui/wit). Geen render. Run:
  blender --background <scene>.blend --python scripts/_round2_diag.py
"""
import bpy
from mathutils import Vector

def wbb(o):
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    xs = [c.x for c in cs]; ys = [c.y for c in cs]; zs = [c.z for c in cs]
    return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))

def colls_of(o):
    return ",".join(c.name for c in o.users_collection)

KW = ("bank", "bench", "sofa", "chair", "stoel", "plant", "pot", "bloem", "flower",
      "hortensia", "hydrang", "boom", "tree", "pine", "berk", "birch", "lamp", "light",
      "zand", "sand", "grind", "gravel", "karesansui", "moss", "mos", "wit", "white",
      "deck", "vlonder", "patio", "terras", "overkap", "pergola", "rake", "hark",
      "tsukubai", "lantern", "festoon", "string")

scn = bpy.context.scene
print("\n================ DIAG:", bpy.data.filepath)
print("OBJECTS_TOTAL:", len(bpy.data.objects))
print("COLLECTIONS:", ", ".join(c.name for c in bpy.data.collections))

# camera
cam = scn.camera
if cam:
    e = cam.rotation_euler
    print(f"CAMERA {cam.name} loc=({cam.location.x:.2f},{cam.location.y:.2f},{cam.location.z:.2f}) "
          f"rot=({e.x:.2f},{e.y:.2f},{e.z:.2f}) lens={getattr(cam.data,'lens','?')}")

# roof / cabin height reference
roof_top = None
for o in bpy.data.objects:
    if o.type == 'MESH' and any(k in o.name.lower() for k in ("dak", "roof", "wand", "muur", "wall", "cabin", "blokhut")):
        b = wbb(o)
        roof_top = b[5] if roof_top is None else max(roof_top, b[5])
print("CABIN/ROOF_MAX_Z:", round(roof_top, 3) if roof_top is not None else "?")

# lights
print("\n--- LIGHTS ---")
for o in bpy.data.objects:
    if o.type == 'LIGHT':
        L = o.data
        print(f"  {o.name:<28} z={o.location.z:6.2f}  {L.type:<5} energy={getattr(L,'energy','?')}")

# floating objects (mesh bbox bottom well above ground, not a known hanging element)
print("\n--- FLOATING (bbox min_z > 0.08) ---")
floats = []
for o in bpy.data.objects:
    if o.type != 'MESH' or not len(o.data.vertices):
        continue
    if len(o.users_collection) and any("scatter" in c.name.lower() or "instance" in c.name.lower() for c in o.users_collection):
        continue
    b = wbb(o)
    if b[4] > 0.08 and (b[5] - b[4]) < 6.0:  # bottom above ground, not a huge wall
        floats.append((b[4], o.name, colls_of(o), len(o.data.vertices)))
for minz, nm, cc, nv in sorted(floats)[-40:]:
    print(f"  {nm:<32} min_z={minz:6.2f}  verts={nv:<7} [{cc}]")

# keyword-relevant objects
print("\n--- KEYWORD OBJECTS (feedback-relevant) ---")
seen = 0
for o in sorted(bpy.data.objects, key=lambda x: x.name):
    nl = o.name.lower()
    if not any(k in nl for k in KW):
        continue
    if o.type == 'MESH' and len(o.data.vertices):
        b = wbb(o)
        nv = len(o.data.vertices)
        mat = o.material_slots[0].material.name if o.material_slots and o.material_slots[0].material else "-"
        print(f"  {o.name:<34} {o.type:<5} loc=({o.location.x:6.2f},{o.location.y:6.2f},{o.location.z:6.2f}) "
              f"z[{b[4]:.2f},{b[5]:.2f}] verts={nv:<6} mat={mat}")
    else:
        print(f"  {o.name:<34} {o.type:<5} loc=({o.location.x:6.2f},{o.location.y:6.2f},{o.location.z:6.2f})")
    seen += 1
    if seen > 120:
        print("  ...(truncated)")
        break
print("================ END DIAG\n")
