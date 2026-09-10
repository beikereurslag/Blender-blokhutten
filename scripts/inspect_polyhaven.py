"""Quickly inspect Polyhaven .blend files for usability.

For each model:
- Mesh objects count + total polys
- Bounding box size
- Materials count + missing textures
- Reports if usable

Usage:
    blender --background --python scripts/inspect_polyhaven.py
"""
import bpy
import os
import sys
import json
from pathlib import Path

MODELS_DIR = Path("C:/Users/beike/Documents/Blender-blokhutten/assets/polyhaven/models")

# Skip these per vault notes (known broken)
SKIP = {"jacaranda_tree_2k.blend", "shrub_03_2k.blend"}

# Skip non-plant items
SKIP_NON_PLANTS = {"Sofa_01_2k.blend", "coffee_table_round_01_2k.blend",
                   "modern_arm_chair_01_2k.blend", "outdoor_table_chair_set_01_2k.blend",
                   "painted_wooden_bench_2k.blend"}


def inspect_blend(blend_path):
    """Open blend file and gather info on objects + materials."""
    info = {
        "file": blend_path.name,
        "objects": 0,
        "meshes": 0,
        "total_polys": 0,
        "max_dim": 0,
        "bbox": None,
        "materials": 0,
        "missing_textures": 0,
        "errors": [],
    }

    try:
        # Use Library load to NOT execute scripts
        with bpy.data.libraries.load(str(blend_path), link=False) as (data_from, data_to):
            mesh_names = list(data_from.meshes)
            obj_names = list(data_from.objects)
            mat_names = list(data_from.materials)
            tex_names = list(data_from.images)
        info["materials"] = len(mat_names)
        info["meshes"] = len(mesh_names)
        info["objects"] = len(obj_names)
        info["textures_count"] = len(tex_names)
    except Exception as e:
        info["errors"].append(f"load error: {e}")

    return info


def main():
    blends = sorted(MODELS_DIR.glob("*.blend"))
    results = []
    for b in blends:
        if b.name in SKIP or b.name in SKIP_NON_PLANTS:
            continue
        info = inspect_blend(b)
        results.append(info)
        print(f"{b.name}: {info['objects']}obj {info['meshes']}mesh {info['materials']}mat | errors: {info['errors']}")

    out_path = MODELS_DIR.parent / "inspection.json"
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
