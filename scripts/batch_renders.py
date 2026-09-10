"""Production batch renderer — generates multiple cabin × mood combinations.

Usage:
    python scripts/batch_renders.py [--cabins lavendel,magnolia] [--moods hero,dawn] [--dry-run]

Default: renders all listed cabins × all listed moods to training/renders/batch_<cabin>_<mood>.png

Each render:
1. Builds base from plans/<mood>_template_full.json (with cabin override)
2. Runs extension from plans/<mood>_template_ext.json
3. Saves render to training/renders/batch_<cabin>_<mood>.png

Templates currently defined: midday, hero, dawn, overcast, cherry, winter
"""
import os
import sys
import json
import subprocess
import argparse

PROJECT_ROOT = "C:/Users/beike/Documents/Blender-blokhutten"
PLANS_DIR = os.path.join(PROJECT_ROOT, "training", "plans")
RENDERS_DIR = os.path.join(PROJECT_ROOT, "training", "renders")
BUILDS_DIR = os.path.join(PROJECT_ROOT, "training", "builds")
PILOTS_DIR = os.path.join(PROJECT_ROOT, "pilots", "base")
BLENDER = "C:/Program Files/Blender Foundation/Blender 5.1/blender.exe"


# Per-cabin parameters (size-tuned extensions)
CABINS = {
    "lavendel": {
        "file": "Lavendel-400x300.blend",
        "camera": {"position": [4.5, 8.5, 1.55], "target": [-0.2, 0.0, 1.15]},
        "ext": {
            "schutting": {"back_length": 16.0, "side_length": 8.0},
            "front_terrace": {"width": 4.5, "depth": 2.2},
            "varied_boxwoods": {"flank_scale": 1.5},
            "foreground_planter": [
                {"plant": "lavender", "position": [3.5, 1.0, 0]},
                {"plant": "hortensia", "position": [-3.5, 1.0, 0]},
            ],
            "plant_border": {"length": 14.0, "n_hortensia": 6, "n_lavender": 12, "n_sedum": 16,
                             "n_side_hortensia": 3, "n_side_lavender": 4, "side_borders": True, "side_length": 6.0},
            "birch_backdrop": {"count": 5, "height_range": [6.0, 8.5], "spread": 14.0},
        },
    },
    "magnolia": {
        "file": "Magnolia-300x200.blend",
        "camera": {"position": [3.8, 7.5, 1.45], "target": [-0.1, 0.0, 1.0]},
        "ext": {
            "schutting": {"back_length": 14.0, "side_length": 7.0},
            "front_terrace": {"width": 3.6, "depth": 1.8},
            "varied_boxwoods": {"flank_scale": 1.3},
            "foreground_planter": [
                {"plant": "lavender", "position": [3.0, 0.8, 0]},
                {"plant": "hortensia", "position": [-3.0, 0.8, 0]},
            ],
            "plant_border": {"length": 12.0, "n_hortensia": 5, "n_lavender": 10, "n_sedum": 14,
                             "n_side_hortensia": 3, "n_side_lavender": 4, "side_borders": True, "side_length": 5.0},
            "birch_backdrop": {"count": 4, "height_range": [5.5, 7.5], "spread": 12.0},
        },
    },
}


# Mood = lighting + tree foliage style
MOODS = {
    "midday": {
        "hdri": "kloofendal_48d_partly_cloudy_puresky_1k.hdr",
        "hdri_rotation_z": 220, "hdri_strength": 1.0,
        "sun_altitude": 52, "sun_azimuth": 215,
        "sun_energy": 5.0, "sun_temperature": 5200, "sun_angle": 0.6,
        "foliage": "birch",
    },
    "hero": {
        "hdri": "kloofendal_43d_clear_2k.hdr",
        "hdri_rotation_z": 200, "hdri_strength": 1.0,
        "sun_altitude": 35, "sun_azimuth": 220,
        "sun_energy": 6.0, "sun_temperature": 4500, "sun_angle": 0.5,
        "foliage": "birch",
    },
    "dawn": {
        "hdri": "kiara_1_dawn_2k.hdr",
        "hdri_rotation_z": 220, "hdri_strength": 0.8,
        "sun_altitude": 25, "sun_azimuth": 245,
        "sun_energy": 5.5, "sun_temperature": 3800, "sun_angle": 0.7,
        "foliage": "birch",
    },
    "overcast": {
        "hdri": "kloofendal_overcast_puresky_1k.hdr",
        "hdri_rotation_z": 220, "hdri_strength": 1.5,
        "sun_altitude": 65, "sun_azimuth": 220,
        "sun_energy": 2.5, "sun_temperature": 6500, "sun_angle": 5.0,
        "foliage": "birch",
    },
    "cherry": {
        "hdri": "kloofendal_48d_partly_cloudy_puresky_1k.hdr",
        "hdri_rotation_z": 220, "hdri_strength": 1.0,
        "sun_altitude": 52, "sun_azimuth": 215,
        "sun_energy": 5.0, "sun_temperature": 5200, "sun_angle": 0.6,
        "foliage": "cherry_blossom",
    },
}


def build_full_plan(cabin_name, mood_name):
    cab = CABINS[cabin_name]
    mood = MOODS[mood_name]
    plan = {
        "name": f"batch_{cabin_name}_{mood_name}_full",
        "cabin_file": f"{PILOTS_DIR}/{cab['file']}",
        "output_blend": f"{BUILDS_DIR}/batch_{cabin_name}_{mood_name}.blend",
        "output_render": f"{RENDERS_DIR}/batch_{cabin_name}_{mood_name}",
        "render_now": True,
        "render": {
            "width": 1920, "height": 1080,
            "samples": 128, "noise_threshold": 0.008,
            "texture_limit": "1024",
            "view_transform": "AgX", "look": "AgX - Punchy",
            "exposure": 0.1, "max_texture_size": 2048,
        },
        "lighting": {
            "hdri_path": f"{PROJECT_ROOT}/assets/polyhaven/hdri/{mood['hdri']}",
            "hdri_rotation_z": mood["hdri_rotation_z"],
            "hdri_strength": mood["hdri_strength"],
            "sun_altitude": mood["sun_altitude"],
            "sun_azimuth": mood["sun_azimuth"],
            "sun_energy": mood["sun_energy"],
            "sun_temperature": mood["sun_temperature"],
            "sun_angle": mood["sun_angle"],
        },
        "camera": {
            **cab["camera"],
            "lens": 35, "f_stop": 5.6, "shift_y": 0.03,
        },
        "ground": {"size": 30},
    }
    return plan


def build_ext_plan(cabin_name, mood_name):
    cab = CABINS[cabin_name]
    mood = MOODS[mood_name]
    ext = cab["ext"]
    plan = {
        "name": f"batch_{cabin_name}_{mood_name}_ext",
        "output_blend": f"{BUILDS_DIR}/batch_{cabin_name}_{mood_name}.blend",
        "output_render": f"{RENDERS_DIR}/batch_{cabin_name}_{mood_name}",
        "render_now": True,
        "extensions": {
            "schutting": {
                "enabled": True,
                "height": 2.1, "thickness": 0.04,
                "back_length": ext["schutting"]["back_length"],
                "side_length": ext["schutting"]["side_length"],
                "side_walls": True,
            },
            "plant_border": {
                "enabled": True,
                **ext["plant_border"],
                "center": 0.0,
            },
            "birch_backdrop": {
                "enabled": True,
                "foliage": mood["foliage"],
                **ext["birch_backdrop"],
                "distance_behind_schutting": 1.0,
            },
            "front_terrace": {
                "enabled": True,
                "width": ext["front_terrace"]["width"],
                "depth": ext["front_terrace"]["depth"],
                "paver_size": 0.55,
            },
            "grass_scatter": {
                "enabled": True,
                "density_per_m2": 600, "blade_height": 0.045,
            },
            "varied_boxwoods": {
                "enabled": True,
                "arrangements": ["flanking_door"],
                "flank_scale": ext["varied_boxwoods"]["flank_scale"],
            },
            "foreground_planter": {
                "enabled": True,
                "planters": [
                    {**p, "style": "dark", "radius": 0.42, "height": 0.62}
                    for p in ext["foreground_planter"]
                ],
            },
        },
    }
    return plan


def render_combination(cabin_name, mood_name, dry_run=False):
    cab = CABINS[cabin_name]

    # Build plans
    full_plan = build_full_plan(cabin_name, mood_name)
    ext_plan = build_ext_plan(cabin_name, mood_name)

    # Save plans
    full_path = f"{PLANS_DIR}/batch_{cabin_name}_{mood_name}_full.json"
    ext_path = f"{PLANS_DIR}/batch_{cabin_name}_{mood_name}_ext.json"
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(full_plan, f, indent=2)
    with open(ext_path, 'w', encoding='utf-8') as f:
        json.dump(ext_plan, f, indent=2)

    if dry_run:
        print(f"[DRY] Would render {cabin_name} × {mood_name}")
        return True

    print(f"\n=== Rendering {cabin_name} × {mood_name} ===")

    # Run build
    cabin_blend = f"{PILOTS_DIR}/{cab['file']}"
    cmd_build = [
        BLENDER, "--background", cabin_blend,
        "--python", f"{PROJECT_ROOT}/scripts/build_scene.py",
        "--", full_path,
    ]
    res = subprocess.run(cmd_build, capture_output=True, text=True, timeout=300)
    if res.returncode != 0:
        print(f"BUILD FAILED: {res.stderr[-500:]}")
        return False

    # Run extension
    built_blend = full_plan["output_blend"]
    cmd_ext = [
        BLENDER, "--background", built_blend,
        "--python", f"{PROJECT_ROOT}/scripts/extend_scene.py",
        "--", ext_path,
    ]
    res = subprocess.run(cmd_ext, capture_output=True, text=True, timeout=300)
    if res.returncode != 0:
        print(f"EXT FAILED: {res.stderr[-500:]}")
        return False

    output_png = full_plan["output_render"] + ".png"
    if os.path.exists(output_png):
        size = os.path.getsize(output_png)
        print(f"  ✓ {output_png} ({size//1024} KB)")
        return True
    print(f"  ✗ No output PNG")
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cabins", default="lavendel,magnolia", help="Comma-separated cabin names")
    parser.add_argument("--moods", default="midday,hero,dawn,overcast,cherry", help="Comma-separated mood names")
    parser.add_argument("--dry-run", action="store_true", help="Just write plans, don't render")
    args = parser.parse_args()

    cabin_names = args.cabins.split(",")
    mood_names = args.moods.split(",")

    print(f"Batch rendering {len(cabin_names)} cabins × {len(mood_names)} moods = {len(cabin_names)*len(mood_names)} renders")
    print(f"Cabins: {cabin_names}")
    print(f"Moods: {mood_names}")

    success_count = 0
    fail_count = 0
    for cabin in cabin_names:
        if cabin not in CABINS:
            print(f"ERROR: unknown cabin '{cabin}'")
            continue
        for mood in mood_names:
            if mood not in MOODS:
                print(f"ERROR: unknown mood '{mood}'")
                continue
            ok = render_combination(cabin, mood, dry_run=args.dry_run)
            if ok:
                success_count += 1
            else:
                fail_count += 1

    print(f"\n=== Summary: {success_count} ok, {fail_count} failed ===")


if __name__ == "__main__":
    main()
