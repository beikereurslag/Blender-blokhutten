"""Peek in asset-.blends: lijst object- en collectie-namen zonder te importeren."""
import bpy, os
ROOT = r"C:\Users\beike\Documents\Blender-blokhutten"
PATHS = [
    r"assets\polyhaven\models\modern_arm_chair_01_2k.blend",
    r"assets\polyhaven\models\coffee_table_round_01_2k.blend",
    r"assets\polyhaven\models\painted_wooden_bench_2k.blend",
    r"assets\polyhaven\models\outdoor_table_chair_set_01_2k.blend",
    r"assets\polyhaven\models\Sofa_01_2k.blend",
    r"assets\polyhaven\models\potted_plant_01_2k.blend",
    r"assets\polyhaven\models\potted_plant_02_2k.blend",
    r"assets\polyhaven\models\shrub_01_2k.blend",
    r"assets\polyhaven\models\shrub_03_2k.blend",
]
for p in PATHS:
    full = os.path.join(ROOT, p)
    if not os.path.exists(full):
        print(f"\n### MISSING {p}"); continue
    with bpy.data.libraries.load(full) as (src, dst):
        objs = list(src.objects); colls = list(src.collections)
    print(f"\n### {os.path.basename(p)}")
    print("  collections:", colls)
    print("  objects:", objs[:30])
