"""Scene-14 pot/plant locatie-probe: world-translation + subtree min_z van potten,
olijven en bistro, plus alle losse voorgrond-plant-meshes (om de 'losse plant bij de
heg' te vinden). Run met scene-14 v3.
"""
import bpy
from mathutils import Vector

def sub_minz(o):
    ms = [c for c in o.children_recursive if c.type == 'MESH' and len(c.data.vertices)]
    if o.type == 'MESH' and len(o.data.vertices): ms.append(o)
    cs = []
    for m in ms: cs += [m.matrix_world @ Vector(c) for c in m.bound_box]
    return (min(c.z for c in cs) if cs else None), len(ms)

NAMES = ["OlijfPot", "OlijfPot_R", "Pot_0_root", "Pot_1", "Pot_2",
         "SM_plant_pot.001", "SM_plant_pot.002", "SM_plant_pot.003",
         "Bistroset_root", "bistrot_table_low"]
print("\n==== POTS/OLIVE world positions ====")
for nm in NAMES:
    o = bpy.data.objects.get(nm)
    if not o:
        print(f"  {nm:<24} MISSING"); continue
    w = o.matrix_world.translation
    mz, nms = sub_minz(o)
    print(f"  {nm:<24} world=({w.x:6.2f},{w.y:6.2f},{w.z:6.2f}) subtree_min_z={mz} meshes={nms}")

# alle losse plant-achtige voorgrond-meshes (mogelijke 'losse plant bij heg')
print("\n==== LOSSE PLANT-MESHES (parent=None, plant-mat, voorgrond) ====")
PK = ("plant", "leaf", "blad", "flower", "bloem", "periwinkle", "sorrel", "weed",
      "shrub", "lavender", "lavendel", "fern", "rozemarijn", "herb", "kruid", "petal")
for o in bpy.data.objects:
    if o.parent is not None or o.type != 'MESH' or not len(o.data.vertices):
        continue
    mats = " ".join(s.material.name.lower() for s in o.material_slots if s.material)
    if not any(k in (o.name.lower()+" "+mats) for k in PK):
        continue
    w = o.matrix_world.translation
    if w.x > 990 or w.y > 990:  # parked donors
        continue
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    minz = min(c.z for c in cs)
    print(f"  {o.name:<28} world=({w.x:6.2f},{w.y:6.2f}) minz={minz:5.2f} v={len(o.data.vertices)} mat=[{mats[:40]}]")
print("==== end\n")
