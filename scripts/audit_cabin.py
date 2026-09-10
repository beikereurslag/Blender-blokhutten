"""Audit cabin orientation — door + window positions for all blokhutten templates.

Outputs: cabin_orientations.json met per cabin door position, front direction, dimensions.

Run:
    blender --background --python scripts/audit_cabin.py

Or load specific cabin:
    blender --background pilots/base/Lavendel-400x300.blend --python scripts/audit_cabin.py -- audit-single
"""
import bpy
import os
import json
import sys
import math
from mathutils import Vector


def audit_cabin(blend_path):
    """Open cabin blend, locate door + windows, determine front direction."""
    try:
        bpy.ops.wm.open_mainfile(filepath=blend_path)
    except Exception as e:
        return {"error": f"open failed: {e}"}

    # Force depsgraph evaluation
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()

    # Find shed root
    shed = bpy.data.objects.get("shed")
    if not shed:
        return {"error": "no shed empty"}

    # Get all cabin mesh children
    all_children = [shed] + shed.children_recursive

    # Compute overall cabin bbox
    all_xs, all_ys, all_zs = [], [], []
    for o in all_children:
        if o.type == 'MESH':
            try:
                o_eval = o.evaluated_get(depsgraph)
                for c in o_eval.bound_box:
                    wp = o_eval.matrix_world @ Vector(c)
                    all_xs.append(wp.x)
                    all_ys.append(wp.y)
                    all_zs.append(wp.z)
            except:
                continue

    if not all_xs:
        return {"error": "no mesh bounds"}

    cabin_bb = {
        "x": [min(all_xs), max(all_xs)],
        "y": [min(all_ys), max(all_ys)],
        "z": [min(all_zs), max(all_zs)],
        "width_x": max(all_xs) - min(all_xs),
        "depth_y": max(all_ys) - min(all_ys),
        "height_z": max(all_zs) - min(all_zs),
        "center": [(min(all_xs)+max(all_xs))/2, (min(all_ys)+max(all_ys))/2, (min(all_zs)+max(all_zs))/2]
    }

    # Find door objects
    door_objs = [o for o in all_children if o.type == 'MESH' and
                 any(k in o.name.lower() for k in ['deur', 'door']) and
                 'handle' not in o.name.lower() and
                 'scharnier' not in o.name.lower()]

    door_data = []
    for d in door_objs[:5]:
        d_eval = d.evaluated_get(depsgraph)
        bb = [d_eval.matrix_world @ Vector(c) for c in d_eval.bound_box]
        cx = sum(v.x for v in bb) / 8
        cy = sum(v.y for v in bb) / 8
        cz = sum(v.z for v in bb) / 8
        door_data.append({
            "name": d.name,
            "center": [round(cx, 2), round(cy, 2), round(cz, 2)],
        })

    # Find windows (no separate window mesh in Lavendel — they're holes in walls)
    # Window may be detected as "raam" or transparent glass material
    window_objs = [o for o in all_children if o.type == 'MESH' and
                   any(k in o.name.lower() for k in ['raam', 'window', 'glass'])]

    window_data = []
    for w in window_objs[:5]:
        w_eval = w.evaluated_get(depsgraph)
        bb = [w_eval.matrix_world @ Vector(c) for c in w_eval.bound_box]
        cx = sum(v.x for v in bb) / 8
        cy = sum(v.y for v in bb) / 8
        cz = sum(v.z for v in bb) / 8
        window_data.append({
            "name": w.name,
            "center": [round(cx, 2), round(cy, 2), round(cz, 2)],
        })

    # Determine front direction
    # Door avg position relative to cabin center
    if door_data:
        avg_door_y = sum(d["center"][1] for d in door_data) / len(door_data)
        avg_door_x = sum(d["center"][0] for d in door_data) / len(door_data)
        center_y = cabin_bb["center"][1]
        center_x = cabin_bb["center"][0]

        # Find dominant axis
        dy = avg_door_y - center_y
        dx = avg_door_x - center_x

        if abs(dy) > abs(dx):
            front_dir = "+Y" if dy > 0 else "-Y"
        else:
            front_dir = "+X" if dx > 0 else "-X"
    else:
        front_dir = "unknown"

    # Recommended camera position based on front_dir
    # Camera at 3/4 angle, eye level 1.7m, distance ~max(w,d)*1.5+3
    max_dim = max(cabin_bb["width_x"], cabin_bb["depth_y"])
    cam_dist = max_dim * 1.5 + 3

    if front_dir == "+Y":
        cam_pos = [cam_dist * 0.6, cam_dist, 1.7]
    elif front_dir == "-Y":
        cam_pos = [cam_dist * 0.6, -cam_dist, 1.7]
    elif front_dir == "+X":
        cam_pos = [cam_dist, cam_dist * 0.6, 1.7]
    else:  # -X
        cam_pos = [-cam_dist, cam_dist * 0.6, 1.7]

    return {
        "file": os.path.basename(blend_path),
        "bbox": cabin_bb,
        "doors": door_data,
        "windows": window_data,
        "front_direction": front_dir,
        "suggested_camera_position": [round(v, 2) for v in cam_pos],
        "suggested_camera_target": [round(v, 2) for v in cabin_bb["center"]],
    }


def main():
    base_dir = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\base"
    output_path = r"C:\Users\beike\Documents\Blender-blokhutten\training\cabin_orientations.json"

    if not os.path.isdir(base_dir):
        print(f"Base dir not found: {base_dir}")
        return

    # Detect 'audit-single' arg
    argv = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    single_mode = "audit-single" in argv

    if single_mode:
        # Audit currently open file only
        result = audit_cabin(bpy.data.filepath)
        print(json.dumps(result, indent=2))
        return

    # Audit all base cabins
    results = {}
    cabins = sorted([f for f in os.listdir(base_dir) if f.endswith('.blend') and not f.endswith('.blend1')])
    print(f"Auditing {len(cabins)} cabins...")

    for cabin in cabins:
        path = os.path.join(base_dir, cabin)
        print(f"  {cabin}...", end=" ")
        try:
            r = audit_cabin(path)
            results[cabin.replace('.blend', '')] = r
            print(f"door {r.get('front_direction', '?')}")
        except Exception as e:
            results[cabin.replace('.blend', '')] = {"error": str(e)}
            print(f"ERROR: {e}")

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"\n=== Cabin orientations saved to {output_path} ===")
    print(f"Audited {len(results)} cabins")

    # Summary
    front_counts = {}
    for r in results.values():
        d = r.get('front_direction', 'error')
        front_counts[d] = front_counts.get(d, 0) + 1
    print(f"Front direction distribution: {front_counts}")


if __name__ == "__main__":
    main()
