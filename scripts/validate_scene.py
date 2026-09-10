"""
Blender scene validator voor Blokhutwinkel marketing visuals.

Detecteert visuele fouten die anders pas in een render of screenshot zichtbaar worden:
- Bomen / planten / meubels die door cabin-wanden snijden
- Objecten boven of onder de grond (floating / underground)
- Objecten met origin op (0,0,0) die nooit verplaatst zijn
- Tree origin niet op grondniveau (boom hangt)

Gebruik via Blender MCP:

    import sys
    sys.path.insert(0, r"C:\\Users\\beike\\Documents\\Blender-blokhutten\\scripts")
    import validate_scene
    result = validate_scene.run()

Of stand-alone in Blender's Text editor / Script tab:

    exec(open(r"...\\validate_scene.py").read())
    result = validate_scene_run()

`result` is een dict met 'flags' (lijst van problemen) en 'cabin_bbox'.
"""

import bpy
from mathutils import Vector


CABIN_KEYWORDS = (
    "shed", "pole", "wall", "roof", "roofbeam", "roofboard", "roofplate",
    "foundationbeam", "board", "deur", "door", "raam", "window",
    "FlatRoof", "scharnier", "doorhandle", "trim", "epdm",
)

PLANT_TREE_KEYWORDS = (
    "tree", "fern", "anthurium", "shrub", "grass", "flower", "plant",
    "dandelion", "celandine", "empodium", "weed", "moss", "calathea",
    "pachira", "jacaranda", "fir", "pine", "boom", "boulder",
)

FURNITURE_KEYWORDS = (
    "chair", "sofa", "table", "bench", "lantern", "lantaarn", "pot",
    "lounge", "deck", "hottub", "fence", "pad", "patio",
)

# Objecten die LEGITIEM hoger dan 0.5m kunnen zijn (geen floating-flag).
ALLOWED_FLOATING_KEYWORDS = (
    "tree", "fir", "pine", "jacaranda", "lantern", "lantaarn",
    "roof", "wall", "shed", "pole", "roofbeam", "scharnier", "doorhandle",
    "door", "window", "raam", "board", "trim", "epdm",
    "camera", "light", "lamp", "sun",
    "hot_tub_water", "hottub_water", "tub_water",  # water in hottub op ~Z=1m
)

# Bounding-box buffer voor "binnen cabin volume" check (m).
# Cabin AABB shrinkt met deze waarde — voorkomt false positives van planten
# direct tegen de buitenwand.
CABIN_INTERIOR_SHRINK = 0.15


def get_world_bbox(obj):
    """Wereld-coords AABB voor 1 object."""
    coords = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    xs = [c.x for c in coords]
    ys = [c.y for c in coords]
    zs = [c.z for c in coords]
    return (
        Vector((min(xs), min(ys), min(zs))),
        Vector((max(xs), max(ys), max(zs))),
    )


def name_matches(name, keywords):
    n = name.lower()
    return any(k in n for k in keywords)


def is_cabin_part(obj):
    return name_matches(obj.name, CABIN_KEYWORDS)


def is_plant_or_tree(obj):
    return name_matches(obj.name, PLANT_TREE_KEYWORDS)


def is_furniture(obj):
    return name_matches(obj.name, FURNITURE_KEYWORDS)


def is_tree(obj):
    n = obj.name.lower()
    return any(k in n for k in ("tree", "fir", "pine", "jacaranda", "boom"))


def allowed_to_float(obj):
    return name_matches(obj.name, ALLOWED_FLOATING_KEYWORDS)


def compute_cabin_bbox():
    """AABB van alle cabin-parts samen."""
    cabin_objs = [
        o for o in bpy.data.objects
        if o.type == "MESH" and is_cabin_part(o) and not o.hide_get()
    ]
    if not cabin_objs:
        return None
    mn = Vector((float("inf"),) * 3)
    mx = Vector((float("-inf"),) * 3)
    for o in cabin_objs:
        omn, omx = get_world_bbox(o)
        for i in range(3):
            mn[i] = min(mn[i], omn[i])
            mx[i] = max(mx[i], omx[i])
    return mn, mx, len(cabin_objs)


def bboxes_overlap(a_min, a_max, b_min, b_max, shrink=0.0):
    """Check of twee AABB's overlappen. `shrink` krimpt de eerste box."""
    for i in range(3):
        if a_max[i] - shrink < b_min[i]:
            return False
        if a_min[i] + shrink > b_max[i]:
            return False
    return True


def origin_inside_xy(origin, bbox_min, bbox_max, shrink=0.0):
    """Check of (origin.x, origin.y) binnen XY-footprint van bbox valt."""
    return (
        bbox_min.x + shrink <= origin.x <= bbox_max.x - shrink
        and bbox_min.y + shrink <= origin.y <= bbox_max.y - shrink
    )


def run():
    flags = []

    cabin = compute_cabin_bbox()
    if cabin is None:
        flags.append({
            "severity": "ERROR",
            "category": "no_cabin",
            "message": "Geen cabin-parts gevonden (zoekwoord shed/wall/roof/pole). Check of cabin GLB geimporteerd is.",
        })
        return {"flags": flags, "cabin_bbox": None}

    cabin_min, cabin_max, cabin_part_count = cabin

    # Skip objects die NIET renderen: hide_render=True OR hide_viewport=True
    # OR hide_get() (= view layer hide). Wat renderbaar is, telt voor validatie.
    meshes = [
        o for o in bpy.data.objects
        if o.type == "MESH"
        and not o.hide_render
        and not o.hide_viewport
        and not o.hide_get()
        and not is_cabin_part(o)
    ]

    for obj in meshes:
        obj_min, obj_max = get_world_bbox(obj)
        obj_origin = obj.matrix_world.translation

        # 1. Plant/tree origin binnen cabin XY-footprint → boom in huis
        if is_plant_or_tree(obj):
            if origin_inside_xy(obj_origin, cabin_min, cabin_max, shrink=0.0):
                flags.append({
                    "severity": "CRITICAL",
                    "category": "plant_in_cabin",
                    "object": obj.name,
                    "origin": [round(c, 2) for c in obj_origin],
                    "cabin_xy": [
                        round(cabin_min.x, 2), round(cabin_min.y, 2),
                        round(cabin_max.x, 2), round(cabin_max.y, 2),
                    ],
                    "message": f"'{obj.name}' staat binnen cabin XY-footprint",
                })

        # 2. Wall-clip: object AABB overlapt cabin AABB (met shrink-buffer)
        #    Maar alleen flag als object NIET op de grond is verbonden via deck/patio.
        if is_plant_or_tree(obj) or is_furniture(obj):
            if bboxes_overlap(obj_min, obj_max, cabin_min, cabin_max,
                              shrink=CABIN_INTERIOR_SHRINK):
                # Alleen kritiek als origin echt in cabin-volume zit
                if not origin_inside_xy(obj_origin, cabin_min, cabin_max,
                                         shrink=0.0):
                    # AABB raakt cabin maar origin staat buiten — kan tegen muur
                    # leunen, maar als overlap groot is = wall clip
                    overlap_x = min(obj_max.x, cabin_max.x) - max(obj_min.x, cabin_min.x)
                    overlap_y = min(obj_max.y, cabin_max.y) - max(obj_min.y, cabin_min.y)
                    if overlap_x > 0.3 and overlap_y > 0.3:
                        flags.append({
                            "severity": "HIGH",
                            "category": "wall_clip",
                            "object": obj.name,
                            "overlap_xy": [round(overlap_x, 2), round(overlap_y, 2)],
                            "message": f"'{obj.name}' AABB snijdt {overlap_x:.2f}x{overlap_y:.2f}m door cabin-wand",
                        })

        # 3. Floating: object's laagste vertex > 0.5 m boven Z=0
        #    en object is geen hanging-fixture (lantaarn aan paal, dakkant, etc).
        if not allowed_to_float(obj):
            if obj_min.z > 0.5:
                flags.append({
                    "severity": "HIGH",
                    "category": "floating",
                    "object": obj.name,
                    "lowest_z": round(obj_min.z, 2),
                    "message": f"'{obj.name}' zweeft op Z={obj_min.z:.2f}m",
                })

        # 4. Underground: laagste vertex < -0.3 m (boulders/planten 10-25cm
        #    ingegraven is bewuste landscape-keuze; flag pas vanaf 30cm).
        if obj_min.z < -0.3:
            flags.append({
                "severity": "MED",
                "category": "underground",
                "object": obj.name,
                "lowest_z": round(obj_min.z, 2),
                "message": f"'{obj.name}' steekt {abs(obj_min.z):.2f}m onder grond",
            })

        # 5. Tree-origin niet op Z=0 (boom hangt)
        if is_tree(obj):
            if obj_origin.z > 0.3 or obj_origin.z < -0.3:
                flags.append({
                    "severity": "HIGH",
                    "category": "tree_origin_off_ground",
                    "object": obj.name,
                    "origin_z": round(obj_origin.z, 2),
                    "message": f"Tree '{obj.name}' origin op Z={obj_origin.z:.2f} (moet ~0)",
                })

        # 6. Origin op (0,0,0) maar object is geen ground/plane
        if not is_cabin_part(obj):
            o = obj_origin
            on_origin = abs(o.x) < 0.01 and abs(o.y) < 0.01 and abs(o.z) < 0.01
            is_ground = name_matches(obj.name, ("ground", "lawn", "plane", "patio", "deck", "gravel", "floor"))
            if on_origin and not is_ground:
                flags.append({
                    "severity": "MED",
                    "category": "origin_at_zero",
                    "object": obj.name,
                    "message": f"'{obj.name}' origin staat op (0,0,0) — vergeten te verplaatsen?",
                })

    # Sort: CRITICAL > HIGH > MED > LOW
    order = {"CRITICAL": 0, "ERROR": 0, "HIGH": 1, "MED": 2, "LOW": 3}
    flags.sort(key=lambda f: order.get(f["severity"], 4))

    return {
        "flags": flags,
        "flag_counts": {
            sev: sum(1 for f in flags if f["severity"] == sev)
            for sev in ("CRITICAL", "HIGH", "MED", "LOW")
        },
        "cabin_bbox": {
            "min": [round(c, 2) for c in cabin_min],
            "max": [round(c, 2) for c in cabin_max],
            "size": [round(cabin_max[i] - cabin_min[i], 2) for i in range(3)],
            "part_count": cabin_part_count,
        },
        "total_meshes_checked": len(meshes),
    }


def print_report(result):
    """Pretty-print het rapport voor leesbaarheid in MCP output."""
    print("=" * 60)
    print("BLENDER SCENE VALIDATION REPORT")
    print("=" * 60)
    if result.get("cabin_bbox"):
        cb = result["cabin_bbox"]
        print(f"Cabin AABB: {cb['min']} → {cb['max']}  size={cb['size']}")
        print(f"Cabin parts: {cb['part_count']}")
    print(f"Total non-cabin meshes checked: {result.get('total_meshes_checked', 0)}")
    print(f"Flag counts: {result.get('flag_counts', {})}")
    print("-" * 60)
    for f in result["flags"]:
        print(f"[{f['severity']:<8}] {f.get('category', '?'):<20} {f.get('message', '')}")
    if not result["flags"]:
        print("GREEN — no flags")
    print("=" * 60)
    return result


if __name__ == "__main__":
    print_report(run())
