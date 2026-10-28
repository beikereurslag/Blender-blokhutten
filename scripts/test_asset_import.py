"""Test importing key Polyhaven assets — check scale + materials."""
import bpy
import os
import sys
from pathlib import Path
from mathutils import Vector

ASSETS_DIR = Path("C:/Users/beike/Documents/Blender-blokhutten/assets/polyhaven/models")


def append_collection_or_objects(blend_path, location=(0, 0, 0)):
    """Append all mesh objects from a blend file to current scene."""
    with bpy.data.libraries.load(str(blend_path), link=False) as (data_from, data_to):
        data_to.objects = data_from.objects

    imported = []
    for obj in data_to.objects:
        if obj is not None:
            bpy.context.scene.collection.objects.link(obj)
            imported.append(obj)

    return imported


def get_bounds(objects):
    """Get combined bounding box of multiple objects."""
    if not objects:
        return None
    xs, ys, zs = [], [], []
    for o in objects:
        for c in o.bound_box:
            wp = o.matrix_world @ Vector(c)
            xs.append(wp.x); ys.append(wp.y); zs.append(wp.z)
    return {
        "x": (min(xs), max(xs)), "y": (min(ys), max(ys)), "z": (min(zs), max(zs)),
        "width_x": max(xs) - min(xs),
        "depth_y": max(ys) - min(ys),
        "height_z": max(zs) - min(zs),
    }


def main():
    print("Clean scene")
    bpy.ops.wm.read_homefile(use_empty=True)

    assets_to_test = ["pine_tree_01_2k.blend", "shrub_01_2k.blend", "shrub_04_2k.blend",
                      "potted_plant_01_2k.blend", "wild_rooibos_bush_2k.blend"]

    for asset in assets_to_test:
        path = ASSETS_DIR / asset
        print(f"\n=== {asset} ===")
        before_objs = set(o.name for o in bpy.data.objects)
        imported = append_collection_or_objects(path)
        new_objs = [o for o in imported if o.type == 'MESH']
        if not new_objs:
            print(f"  No mesh objects imported")
            continue
        b = get_bounds(new_objs)
        if b:
            print(f"  {len(new_objs)} mesh objects")
            print(f"  Size: {b['width_x']:.2f} × {b['depth_y']:.2f} × {b['height_z']:.2f}m")
            print(f"  Z range: {b['z'][0]:.2f} → {b['z'][1]:.2f}")
            # Materials
            mats = set()
            for o in new_objs:
                for s in o.material_slots:
                    if s.material:
                        mats.add(s.material.name)
            print(f"  Materials: {sorted(mats)}")

        # Remove for next test
        for o in new_objs:
            bpy.data.objects.remove(o, do_unlink=True)


if __name__ == "__main__":
    main()
