"""DEEP QUALITY extension — uses REAL Polyhaven .blend assets.

Photo-real garden render with:
- pine_tree_01 (real geometry + materials) instead of procedural spheres
- shrub_01 (real shrub mesh) for boxwoods
- potted_plant_01 (real terracotta pot + plant) for accents
- wild_rooibos_bush (real bush + purple flowers) for border
- PBR brown_planks_09 wood texture for schutting
- PBR dark_planks wood texture for terrace deck
- PBR aerial_grass_rock for ground

Usage:
    blender --background built_scene.blend --python scripts/extend_scene_real.py -- plan.json
"""
import bpy
import os
import sys
import math
import json
import random
from pathlib import Path
from mathutils import Vector

ASSETS = Path("C:/Users/beike/Documents/Blender-blokhutten/assets/polyhaven")


def log(msg, level="INFO"):
    print(f"[{level}] {msg}")


# =============================================================================
# UTILS: texture remap + scale
# =============================================================================

def remap_broken_image_paths():
    """Fix Polyhaven .jpg→.png filepath mismatches after asset import."""
    fixed = 0
    for img in bpy.data.images:
        if img.name in ("Render Result", "Viewer Node"):
            continue
        abspath = bpy.path.abspath(img.filepath)
        if not os.path.exists(abspath):
            base, ext = os.path.splitext(abspath)
            for try_ext in ['.png', '.jpg', '.exr', '.hdr', '.tif']:
                alt = base + try_ext
                if os.path.exists(alt):
                    img.filepath = alt
                    try:
                        img.reload()
                        fixed += 1
                    except: pass
                    break
    if fixed > 0:
        log(f"Remapped {fixed} broken texture paths")
    return fixed


def scale_heavy_textures(max_size=1024):
    """Downscale large textures (in-memory) to fit VRAM budget."""
    scaled = 0
    for img in bpy.data.images:
        if img.name in ("Render Result", "Viewer Node"):
            continue
        try:
            _ = img.pixels[0]
            if img.has_data and (img.size[0] > max_size or img.size[1] > max_size):
                img.scale(max_size, max_size)
                scaled += 1
        except Exception:
            pass
    if scaled > 0:
        log(f"Scaled {scaled} textures to {max_size}px")
    return scaled


def remove_collection_if_exists(name):
    coll = bpy.data.collections.get(name)
    if coll:
        for obj in list(coll.objects):
            mesh = obj.data if obj.type == 'MESH' else None
            bpy.data.objects.remove(obj, do_unlink=True)
            if mesh and mesh.users == 0:
                bpy.data.meshes.remove(mesh)
        bpy.data.collections.remove(coll)


def get_cabin_info():
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    shed = bpy.data.objects.get("shed")
    if not shed:
        return None
    all_children = [shed] + shed.children_recursive
    all_xs, all_ys, all_zs = [], [], []
    for o in all_children:
        if o.type == 'MESH':
            try:
                o_eval = o.evaluated_get(depsgraph)
                for c in o_eval.bound_box:
                    wp = o_eval.matrix_world @ Vector(c)
                    all_xs.append(wp.x); all_ys.append(wp.y); all_zs.append(wp.z)
            except: pass
    door_objs = [o for o in all_children if o.type == 'MESH' and
                 any(k in o.name.lower() for k in ['deur', 'door']) and
                 'handle' not in o.name.lower() and 'scharnier' not in o.name.lower()]
    door_pos = None
    if door_objs:
        d = door_objs[0]
        d_eval = d.evaluated_get(depsgraph)
        bb = [d_eval.matrix_world @ Vector(c) for c in d_eval.bound_box]
        door_pos = [sum(v.x for v in bb)/8, sum(v.y for v in bb)/8, sum(v.z for v in bb)/8]
    return {
        "bbox_x": [min(all_xs), max(all_xs)],
        "bbox_y": [min(all_ys), max(all_ys)],
        "bbox_z": [min(all_zs), max(all_zs)],
        "door_pos": door_pos,
    }


# =============================================================================
# ASSET LOADERS (collection-based, linked-data duplicates)
# =============================================================================

def _load_blend_as_collection(blend_path, coll_name):
    existing = bpy.data.collections.get(coll_name)
    if existing:
        return existing

    with bpy.data.libraries.load(str(blend_path), link=False) as (data_from, data_to):
        data_to.objects = data_from.objects

    new_coll = bpy.data.collections.new(coll_name)
    bpy.context.scene.collection.children.link(new_coll)

    HIDE_OFFSET = Vector((1000, 1000, 0))
    for obj in data_to.objects:
        if obj is not None and obj.type == 'MESH':
            obj.location = obj.location + HIDE_OFFSET
            obj.hide_render = True
            obj.hide_viewport = True
            try:
                new_coll.objects.link(obj)
            except RuntimeError:
                pass
            try:
                bpy.context.scene.collection.objects.unlink(obj)
            except RuntimeError:
                pass
    return new_coll


def _duplicate_collection_at(src_coll, name_prefix, location, scale=1.0, rotation_z=0.0):
    HIDE_OFFSET = Vector((1000, 1000, 0))
    dest = bpy.context.scene.collection
    src_objs = [o for o in src_coll.objects if o.type == 'MESH']
    if not src_objs:
        return []
    centroid = sum((o.location for o in src_objs), Vector((0, 0, 0))) / len(src_objs)

    copies = []
    for i, src_obj in enumerate(src_objs):
        new_obj = src_obj.copy()
        new_obj.name = f"{name_prefix}_{i}"
        relative_pos = src_obj.location - centroid
        new_obj.location = Vector(location) + relative_pos
        new_obj.scale = (scale, scale, scale)
        new_obj.rotation_euler = (0, 0, rotation_z)
        new_obj.hide_render = False
        new_obj.hide_viewport = False
        dest.objects.link(new_obj)
        copies.append(new_obj)
    return copies


def _remove_instances_starting_with(prefix):
    for obj in list(bpy.data.objects):
        if obj.name.startswith(prefix):
            bpy.data.objects.remove(obj, do_unlink=True)


def _get_collection_bbox_height(coll):
    max_z = float('-inf')
    min_z = float('inf')
    for o in coll.objects:
        if o.type == 'MESH':
            for c in o.bound_box:
                wp = o.matrix_world @ Vector(c)
                max_z = max(max_z, wp.z)
                min_z = min(min_z, wp.z)
    if max_z == float('-inf'):
        return 1.0
    return max_z - min_z


def get_pine_tree():
    return _load_blend_as_collection(ASSETS / "models" / "pine_tree_01_2k.blend", "Asset_Pine")


def get_shrub(variant=1):
    return _load_blend_as_collection(
        ASSETS / "models" / f"shrub_0{variant}_2k.blend", f"Asset_Shrub_{variant}")


def get_potted_plant():
    return _load_blend_as_collection(ASSETS / "models" / "potted_plant_01_2k.blend", "Asset_Potted")


def get_rooibos_bush():
    return _load_blend_as_collection(ASSETS / "models" / "wild_rooibos_bush_2k.blend", "Asset_Rooibos")


def get_flower_gazania():
    return _load_blend_as_collection(ASSETS / "models" / "flower_gazania_2k.blend", "Asset_Gazania")


def get_periwinkle():
    return _load_blend_as_collection(ASSETS / "models" / "periwinkle_plant_2k.blend", "Asset_Periwinkle")


# =============================================================================
# PBR MATERIALS
# =============================================================================

def _pbr_material(name, tex_folder, prefix=None, scale=1.0):
    existing = bpy.data.materials.get(name)
    if existing:
        return existing
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)

    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (1000, 0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location = (700, 0)
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location = (-800, 0)
    mapp = nt.nodes.new('ShaderNodeMapping'); mapp.location = (-600, 0)
    mapp.inputs['Scale'].default_value = (scale, scale, scale)
    nt.links.new(tc.outputs['UV'], mapp.inputs['Vector'])

    p_prefix = prefix or ""
    p_sep = "_" if prefix else ""

    def try_load(suffix, slot=None, colorspace=None, y_off=0):
        for path in [tex_folder / f"{p_prefix}{p_sep}{suffix}_2k.jpg",
                     tex_folder / f"{suffix}_2k.jpg"]:
            if path.exists() and path.stat().st_size > 10000:
                try:
                    tex = nt.nodes.new('ShaderNodeTexImage'); tex.location = (-400, y_off)
                    img = bpy.data.images.load(str(path), check_existing=True)
                    if img.size[0] > 0:
                        tex.image = img
                        if colorspace == 'Non-Color':
                            img.colorspace_settings.name = 'Non-Color'
                        nt.links.new(mapp.outputs['Vector'], tex.inputs['Vector'])
                        if slot:
                            nt.links.new(tex.outputs['Color'], bsdf.inputs[slot])
                        return tex
                    nt.nodes.remove(tex)
                except Exception:
                    pass
        return None

    try_load("diff", slot="Base Color", y_off=200)
    try_load("rough", slot="Roughness", colorspace='Non-Color', y_off=-50)
    nor_tex = try_load("nor_gl", colorspace='Non-Color', y_off=-300)
    if nor_tex:
        nor_map = nt.nodes.new('ShaderNodeNormalMap'); nor_map.location = (-100, -300)
        nor_map.inputs['Strength'].default_value = 1.0
        nt.links.new(nor_tex.outputs['Color'], nor_map.inputs['Color'])
        nt.links.new(nor_map.outputs['Normal'], bsdf.inputs['Normal'])

    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def mat_planks_brown():
    return _pbr_material("M_PBR_Planks_Brown", ASSETS / "textures" / "brown_planks_09",
                         prefix="brown_planks_09", scale=1.5)


def mat_planks_dark():
    return _pbr_material("M_PBR_Planks_Dark", ASSETS / "textures" / "dark_planks",
                         prefix="dark_planks", scale=2.0)


def mat_grass_rock():
    return _pbr_material("M_PBR_GrassRock", ASSETS / "textures" / "aerial_grass_rock",
                         prefix=None, scale=4.0)


# =============================================================================
# EXTENSIONS
# =============================================================================

def upgrade_ground():
    ground = bpy.data.objects.get("Ground_Plane") or bpy.data.objects.get("Ground")
    if not ground:
        return
    mat = mat_grass_rock()
    ground.data.materials.clear()
    ground.data.materials.append(mat)
    log("Ground -> PBR aerial_grass_rock")


# =============================================================================
# GARDEN DESIGN PRINCIPLES — zones, beds, edges, paths
# =============================================================================

def mat_mulch_dark():
    """Dark mulch material — wood chips/dark soil for plant beds."""
    name = "M_Mulch_Dark"
    existing = bpy.data.materials.get(name)
    if existing:
        return existing
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (800, 0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location = (500, 0)
    noise = nt.nodes.new('ShaderNodeTexNoise'); noise.location = (-200, 0)
    noise.inputs['Scale'].default_value = 60.0
    noise.inputs['Detail'].default_value = 12.0
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location = (100, 0)
    ramp.color_ramp.elements[0].color = (0.04, 0.03, 0.02, 1.0)  # very dark brown
    ramp.color_ramp.elements[1].position = 0.7
    ramp.color_ramp.elements[1].color = (0.10, 0.07, 0.05, 1.0)
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.95
    bump = nt.nodes.new('ShaderNodeBump'); bump.location = (300, -200)
    bump.inputs['Strength'].default_value = 0.5
    bump.inputs['Distance'].default_value = 0.01
    nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def mat_concrete_edge():
    """Concrete material for mowing strips + edging."""
    name = "M_ConcreteEdge"
    existing = bpy.data.materials.get(name)
    if existing:
        return existing
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (800, 0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location = (500, 0)
    noise = nt.nodes.new('ShaderNodeTexNoise'); noise.location = (-200, 0)
    noise.inputs['Scale'].default_value = 80.0
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location = (100, 0)
    ramp.color_ramp.elements[0].color = (0.45, 0.44, 0.42, 1.0)  # warm grey
    ramp.color_ramp.elements[1].color = (0.55, 0.54, 0.52, 1.0)
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.85
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def add_plant_bed(plan, cabin):
    """Add a defined plant bed with dark mulch material (against schutting back).

    Real garden design: planten staan IN BED, niet drijven in gras.
    Bed has edging (mowing strip) on lawn side.
    """
    remove_collection_if_exists("Plant_Bed")
    coll = bpy.data.collections.new("Plant_Bed")
    bpy.context.scene.collection.children.link(coll)

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    # Bed dimensions
    width = plan.get("width", 12.0)
    depth = plan.get("depth", 1.5)  # how far from schutting toward lawn
    center_offset = plan.get("center_offset", 0.0)  # along schutting

    mulch_mat = mat_mulch_dark()
    edge_mat = mat_concrete_edge()

    # Plant bed sits against schutting (Y=-5.5 typically) extending into lawn
    if abs(dy) > abs(dx):
        back_y = -5.5 if dy > 0 else 5.5
        sign = -1 if dy > 0 else 1  # bed extends from schutting toward door (positive direction)
        # Bed: from back_y to back_y - sign*depth
        bed_y_back = back_y - sign * 0.05  # 5cm from wall
        bed_y_front = back_y - sign * depth
        bed_center_y = (bed_y_back + bed_y_front) / 2
        bed_center_x = center_offset
        bed_size_x = width
        bed_size_y = abs(bed_y_back - bed_y_front)
    else:
        back_x = -5.5 if dx > 0 else 5.5
        sign = -1 if dx > 0 else 1
        bed_x_back = back_x - sign * 0.05
        bed_x_front = back_x - sign * depth
        bed_center_x = (bed_x_back + bed_x_front) / 2
        bed_center_y = center_offset
        bed_size_x = abs(bed_x_back - bed_x_front)
        bed_size_y = width

    # Create mulch bed plane (slightly above ground to avoid z-fight)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(bed_center_x, bed_center_y, 0.012))
    bed_plane = bpy.context.active_object
    bed_plane.scale = (bed_size_x, bed_size_y, 1)
    bpy.ops.object.transform_apply(scale=True)
    bed_plane.name = "PlantBed_Mulch"
    bed_plane.data.materials.append(mulch_mat)
    coll.objects.link(bed_plane)
    bpy.context.scene.collection.objects.unlink(bed_plane)

    # Mowing edge strip on lawn-facing side (20cm concrete strip)
    if plan.get("mowing_strip", True):
        strip_w = 0.20
        if abs(dy) > abs(dx):
            strip_y = bed_y_front + sign * 0.02  # at front edge of bed
            bpy.ops.mesh.primitive_cube_add(size=1, location=(bed_center_x, strip_y, 0.018))
            strip = bpy.context.active_object
            strip.scale = (bed_size_x + 0.05, strip_w, 0.03)
        else:
            strip_x = bed_x_front + sign * 0.02
            bpy.ops.mesh.primitive_cube_add(size=1, location=(strip_x, bed_center_y, 0.018))
            strip = bpy.context.active_object
            strip.scale = (strip_w, bed_size_y + 0.05, 0.03)
        bpy.ops.object.transform_apply(scale=True)
        strip.name = "PlantBed_MowingStrip"
        strip.data.materials.append(edge_mat)
        coll.objects.link(strip)
        bpy.context.scene.collection.objects.unlink(strip)

    log(f"Plant bed: {bed_size_x:.1f}×{bed_size_y:.1f}m with mulch + mowing strip")
    return {"bed_x": bed_center_x, "bed_y": bed_center_y,
            "bed_w": bed_size_x, "bed_d": bed_size_y,
            "back_axis": 'Y' if abs(dy) > abs(dx) else 'X'}


def add_path_to_door(plan, cabin):
    """Stepping path of bluestone pavers from deck out toward the lawn or schutting.

    Real garden = path leads somewhere, not random stones.
    """
    remove_collection_if_exists("Garden_Path")
    coll = bpy.data.collections.new("Garden_Path")
    bpy.context.scene.collection.children.link(coll)

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    # Path starts from deck edge, goes perpendicular out
    n_stones = plan.get("count", 5)
    paver_size_x = plan.get("paver_x", 0.60)
    paver_size_y = plan.get("paver_y", 0.40)
    spacing = plan.get("spacing", 0.75)
    start_offset = plan.get("start_offset", 3.0)  # from cabin face
    direction = plan.get("direction", "side")  # "side" = perpendicular to door, "forward"

    mat = mat_planks_dark()  # match deck or use bluestone if available

    # Path goes from deck side toward right edge of garden
    if abs(dy) > abs(dx):
        sign_y = 1 if dy > 0 else -1
        path_start_y = door[1] + sign_y * start_offset
        if direction == "side":
            # Path extends along X (perpendicular to door axis)
            for i in range(n_stones):
                px = door[0] + 1.5 + i * spacing  # to the right of door
                py = path_start_y + random.uniform(-0.04, 0.04)
                _make_paver(coll, px, py, paver_size_x, paver_size_y, mat, i, sign=1)
        else:
            for i in range(n_stones):
                px = door[0] + random.uniform(-0.04, 0.04)
                py = path_start_y + sign_y * i * spacing
                _make_paver(coll, px, py, paver_size_x, paver_size_y, mat, i, sign=sign_y)
    else:
        sign_x = 1 if dx > 0 else -1
        path_start_x = door[0] + sign_x * start_offset
        for i in range(n_stones):
            px = path_start_x + sign_x * i * spacing
            py = door[1] + random.uniform(-0.04, 0.04)
            _make_paver(coll, px, py, paver_size_x, paver_size_y, mat, i, sign=sign_x)

    log(f"Garden path: {n_stones} pavers ({direction} direction)")


def _make_paver(coll, px, py, sx, sy, mat, i, sign):
    """Helper: create one paver cube."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(px, py, 0.025))
    paver = bpy.context.active_object
    paver.name = f"Path_Paver_{i}"
    paver.scale = (sx, sy, 0.05)
    bpy.ops.object.transform_apply(scale=True)
    paver.rotation_euler = (0, 0, random.uniform(-0.04, 0.04))
    paver.data.materials.append(mat)
    coll.objects.link(paver)
    bpy.context.scene.collection.objects.unlink(paver)


def add_focal_tree(plan, cabin):
    """ONE large focal tree at specified position. Not a row — single statement.

    Real garden = focal point, niet rij.
    """
    _remove_instances_starting_with("FocalTree_")
    coll = get_pine_tree()
    if not coll:
        return

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    target_h = plan.get("height", 11.0)  # slightly taller than tree row
    src_h = _get_collection_bbox_height(coll) or 20.0
    scale_factor = target_h / src_h

    # Default: place in BACK-LEFT corner of garden (opposite of camera-side)
    position = plan.get("position", None)
    if not position:
        if abs(dy) > abs(dx):
            back_y = -5.5 if dy > 0 else 5.5
            sign = -1 if dy > 0 else 1
            position = (-5.5, back_y + sign * 0.5, 0)  # back-left
        else:
            back_x = -5.5 if dx > 0 else 5.5
            sign = -1 if dx > 0 else 1
            position = (back_x + sign * 0.5, -5.5, 0)

    _duplicate_collection_at(coll, "FocalTree", location=tuple(position),
                             scale=scale_factor, rotation_z=random.uniform(0, math.tau))
    log(f"Focal tree at {position[:2]}, height {target_h}m")


def add_gravel_zone(plan, cabin):
    """Gravel/crushed-stone zone — defines transition between deck and lawn.

    Real garden design: hardscape zones (paving, gravel, deck) define spaces.
    Lawn comes AFTER a hardscape edge, not directly against cabin.
    """
    remove_collection_if_exists("Gravel_Zone")
    coll = bpy.data.collections.new("Gravel_Zone")
    bpy.context.scene.collection.children.link(coll)

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    width = plan.get("width", 6.5)
    depth = plan.get("depth", 1.0)
    offset_from_deck = plan.get("offset_from_deck", 0.0)  # gap or no gap
    extend_beyond_deck = plan.get("extend_beyond_deck", 1.0)  # extra width past deck

    # Gravel material: crushed stone look
    mat = bpy.data.materials.get("M_Gravel")
    if not mat:
        mat = bpy.data.materials.new("M_Gravel")
        mat.use_nodes = True
        nt = mat.node_tree
        for n in list(nt.nodes): nt.nodes.remove(n)
        out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (800, 0)
        bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location = (500, 0)
        noise = nt.nodes.new('ShaderNodeTexNoise'); noise.location = (-200, 0)
        noise.inputs['Scale'].default_value = 200.0
        noise.inputs['Detail'].default_value = 14.0
        ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location = (100, 0)
        ramp.color_ramp.elements[0].color = (0.42, 0.40, 0.36, 1.0)  # warm grey gravel
        ramp.color_ramp.elements[1].position = 0.6
        ramp.color_ramp.elements[1].color = (0.55, 0.53, 0.48, 1.0)
        nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
        nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
        bsdf.inputs['Roughness'].default_value = 0.95
        bump = nt.nodes.new('ShaderNodeBump'); bump.location = (300, -200)
        bump.inputs['Strength'].default_value = 0.8
        bump.inputs['Distance'].default_value = 0.005
        nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
        nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
        nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])

    # Place gravel just past the deck edge
    if abs(dy) > abs(dx):
        sign = 1 if dy > 0 else -1
        deck_front_y = cabin["bbox_y"][1] + 2.2 if dy > 0 else cabin["bbox_y"][0] - 2.2
        gravel_y_back = deck_front_y + sign * offset_from_deck
        gravel_y_front = gravel_y_back + sign * depth
        gravel_center_y = (gravel_y_back + gravel_y_front) / 2
        bpy.ops.mesh.primitive_plane_add(size=1, location=(door[0], gravel_center_y, 0.008))
        plane = bpy.context.active_object
        plane.scale = (width, depth, 1)
    else:
        sign = 1 if dx > 0 else -1
        deck_front_x = cabin["bbox_x"][1] + 2.2 if dx > 0 else cabin["bbox_x"][0] - 2.2
        gravel_x_back = deck_front_x + sign * offset_from_deck
        gravel_x_front = gravel_x_back + sign * depth
        gravel_center_x = (gravel_x_back + gravel_x_front) / 2
        bpy.ops.mesh.primitive_plane_add(size=1, location=(gravel_center_x, door[1], 0.008))
        plane = bpy.context.active_object
        plane.scale = (depth, width, 1)

    bpy.ops.object.transform_apply(scale=True)
    plane.name = "Gravel_Zone"
    plane.data.materials.append(mat)
    coll.objects.link(plane)
    bpy.context.scene.collection.objects.unlink(plane)
    log(f"Gravel zone: {width}×{depth}m beyond deck")


def add_side_bed(plan, cabin):
    """Plant bed ALONG SIDE of cabin (foundation planting).

    Real garden tradition: narrow bed against house/cabin wall.
    Highly visible from front camera angle.
    """
    remove_collection_if_exists("Side_Bed")
    coll = bpy.data.collections.new("Side_Bed")
    bpy.context.scene.collection.children.link(coll)

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    bed_depth = plan.get("depth", 0.8)  # narrow — against wall
    side = plan.get("side", "left")  # which side of cabin

    mulch_mat = mat_mulch_dark()

    # Determine bed position along cabin wall
    if abs(dy) > abs(dx):
        # Door at +Y or -Y, cabin walls run along X
        # Side bed is at either +X or -X wall
        if side == "left":
            bed_x_in = cabin["bbox_x"][0]  # cabin left wall
            bed_x_out = bed_x_in - bed_depth
        else:
            bed_x_in = cabin["bbox_x"][1]
            bed_x_out = bed_x_in + bed_depth
        bed_center_x = (bed_x_in + bed_x_out) / 2
        bed_size_x = bed_depth
        # Bed runs along Y, from back to front of cabin
        bed_y_front = cabin["bbox_y"][1] if dy > 0 else cabin["bbox_y"][0]
        bed_y_back = cabin["bbox_y"][0] if dy > 0 else cabin["bbox_y"][1]
        bed_center_y = (bed_y_back + bed_y_front) / 2
        bed_size_y = abs(bed_y_back - bed_y_front)
    else:
        # Door at +X or -X, cabin walls along Y
        if side == "left":
            bed_y_in = cabin["bbox_y"][0]
            bed_y_out = bed_y_in - bed_depth
        else:
            bed_y_in = cabin["bbox_y"][1]
            bed_y_out = bed_y_in + bed_depth
        bed_center_y = (bed_y_in + bed_y_out) / 2
        bed_size_y = bed_depth
        bed_x_front = cabin["bbox_x"][1] if dx > 0 else cabin["bbox_x"][0]
        bed_x_back = cabin["bbox_x"][0] if dx > 0 else cabin["bbox_x"][1]
        bed_center_x = (bed_x_back + bed_x_front) / 2
        bed_size_x = abs(bed_x_back - bed_x_front)

    bpy.ops.mesh.primitive_plane_add(size=1, location=(bed_center_x, bed_center_y, 0.012))
    bed_plane = bpy.context.active_object
    bed_plane.scale = (bed_size_x, bed_size_y, 1)
    bpy.ops.object.transform_apply(scale=True)
    bed_plane.name = "SideBed_Mulch"
    bed_plane.data.materials.append(mulch_mat)
    coll.objects.link(bed_plane)
    bpy.context.scene.collection.objects.unlink(bed_plane)

    # Scatter small plants in the bed
    if plan.get("with_plants", True):
        coll_shrub = get_shrub(variant=4)
        if coll_shrub:
            n = plan.get("plant_count", 5)
            src_h = _get_collection_bbox_height(coll_shrub) or 0.28
            target_h = 0.35
            scale_factor = target_h / src_h

            for i in range(n):
                if abs(dy) > abs(dx):
                    py = bed_y_back + (i + 0.5) * (bed_size_y / n) + random.uniform(-0.1, 0.1)
                    px = bed_center_x + random.uniform(-bed_depth*0.3, bed_depth*0.3)
                else:
                    px = bed_x_back + (i + 0.5) * (bed_size_x / n) + random.uniform(-0.1, 0.1)
                    py = bed_center_y + random.uniform(-bed_depth*0.3, bed_depth*0.3)
                s = scale_factor * random.uniform(0.85, 1.15)
                _duplicate_collection_at(coll_shrub, f"SideBedPlant_{i}",
                                         location=(px, py, 0), scale=s,
                                         rotation_z=random.uniform(0, math.tau))

    log(f"Side bed ({side}): {bed_size_x:.1f}×{bed_size_y:.1f}m foundation planting")


def add_clipped_hedge_row(plan, cabin):
    """Clipped boxwood hedge as rectangle (not balls). Real Dutch garden = strakke hedge.

    Uses cube primitive with green material — looks like trimmed buxus.
    """
    remove_collection_if_exists("Clipped_Hedge")
    coll = bpy.data.collections.new("Clipped_Hedge")
    bpy.context.scene.collection.children.link(coll)

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    length = plan.get("length", 6.0)
    height = plan.get("height", 0.6)
    thickness = plan.get("thickness", 0.5)
    position = plan.get("position", None)

    if not position:
        # Default: along front edge of plant bed, parallel to schutting
        if abs(dy) > abs(dx):
            back_y = -5.5 if dy > 0 else 5.5
            sign = -1 if dy > 0 else 1
            position = (0, back_y - sign * 1.5, 0)
        else:
            back_x = -5.5 if dx > 0 else 5.5
            sign = -1 if dx > 0 else 1
            position = (back_x - sign * 1.5, 0, 0)

    # Build hedge as box with rounded top via bevel
    bpy.ops.mesh.primitive_cube_add(size=1, location=(position[0], position[1], height/2))
    hedge = bpy.context.active_object
    hedge.name = "ClippedHedge"
    # Orient along axis (along X if door at Y, along Y if door at X)
    if abs(dy) > abs(dx):
        hedge.scale = (length, thickness, height)
    else:
        hedge.scale = (thickness, length, height)
    bpy.ops.object.transform_apply(scale=True)

    # Add slight bevel via subdivision + simple smoothing
    bpy.ops.object.modifier_add(type='BEVEL')
    hedge.modifiers["Bevel"].width = 0.06
    hedge.modifiers["Bevel"].segments = 3

    # Green material — slightly darker dense leaf look
    mat_name = "M_ClippedHedge"
    hedge_mat = bpy.data.materials.get(mat_name)
    if not hedge_mat:
        hedge_mat = bpy.data.materials.new(mat_name)
        hedge_mat.use_nodes = True
        nt = hedge_mat.node_tree
        for n in list(nt.nodes): nt.nodes.remove(n)
        out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (800, 0)
        bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location = (500, 0)
        noise = nt.nodes.new('ShaderNodeTexNoise'); noise.location = (-200, 0)
        noise.inputs['Scale'].default_value = 120.0
        noise.inputs['Detail'].default_value = 12.0
        ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location = (100, 0)
        ramp.color_ramp.elements[0].color = (0.06, 0.14, 0.04, 1.0)
        ramp.color_ramp.elements[1].position = 0.6
        ramp.color_ramp.elements[1].color = (0.12, 0.24, 0.07, 1.0)
        nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
        nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
        bsdf.inputs['Roughness'].default_value = 0.95
        bump = nt.nodes.new('ShaderNodeBump'); bump.location = (300, -200)
        bump.inputs['Strength'].default_value = 0.6
        bump.inputs['Distance'].default_value = 0.015
        nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
        nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
        nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    hedge.data.materials.append(hedge_mat)
    coll.objects.link(hedge)
    bpy.context.scene.collection.objects.unlink(hedge)
    log(f"Clipped hedge: {length}×{thickness}m, height {height}m at {position[:2]}")


def add_schutting(plan, cabin):
    remove_collection_if_exists("PBR_Schutting")

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    height = plan.get("height", 2.1)
    thickness = plan.get("thickness", 0.04)
    back_length = plan.get("back_length", 16.0)
    side_length = plan.get("side_length", 8.0)
    style = plan.get("style", "brown")
    mat = mat_planks_dark() if style == "dark" else mat_planks_brown()

    coll = bpy.data.collections.new("PBR_Schutting")
    bpy.context.scene.collection.children.link(coll)

    if abs(dy) > abs(dx):
        back_y = -5.5 if dy > 0 else 5.5
        side_y_mid = back_y - (3.5 if dy > 0 else -3.5)

        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, back_y, height/2))
        wall = bpy.context.active_object
        wall.name = "PBR_Schutting_Back"
        wall.scale = (back_length, thickness, height)
        bpy.ops.object.transform_apply(scale=True)
        wall.data.materials.append(mat)

        if plan.get("side_walls", True):
            for x_pos, name in [(-7.0, "PBR_Schutting_Left"), (7.0, "PBR_Schutting_Right")]:
                bpy.ops.mesh.primitive_cube_add(size=1, location=(x_pos, side_y_mid, height/2))
                w = bpy.context.active_object
                w.name = name
                w.scale = (thickness, side_length, height)
                bpy.ops.object.transform_apply(scale=True)
                w.data.materials.append(mat)
    else:
        back_x = -5.5 if dx > 0 else 5.5
        bpy.ops.mesh.primitive_cube_add(size=1, location=(back_x, 0, height/2))
        wall = bpy.context.active_object
        wall.name = "PBR_Schutting_Back"
        wall.scale = (thickness, back_length, height)
        bpy.ops.object.transform_apply(scale=True)
        wall.data.materials.append(mat)

    for obj in [o for o in bpy.data.objects if o.name.startswith("PBR_Schutting_")]:
        for c in obj.users_collection:
            if c != coll:
                c.objects.unlink(obj)
        if obj.name not in coll.objects:
            coll.objects.link(obj)
    log(f"Schutting: {style} planks, {height}m tall")


def add_terrace(plan, cabin):
    remove_collection_if_exists("PBR_Terrace")
    coll = bpy.data.collections.new("PBR_Terrace")
    bpy.context.scene.collection.children.link(coll)

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    width = plan.get("width", 4.5)
    depth = plan.get("depth", 2.2)
    mat = mat_planks_dark()

    if abs(dy) > abs(dx):
        sign = 1 if dy > 0 else -1
        terrace_y = cabin["bbox_y"][1] + depth/2 if dy > 0 else cabin["bbox_y"][0] - depth/2
        terrace_x = door[0]
        bpy.ops.mesh.primitive_plane_add(size=1, location=(terrace_x, terrace_y, 0.005))
        plane = bpy.context.active_object
        plane.scale = (width, depth, 1)
    else:
        sign = 1 if dx > 0 else -1
        terrace_x = cabin["bbox_x"][1] + depth/2 if dx > 0 else cabin["bbox_x"][0] - depth/2
        terrace_y = door[1]
        bpy.ops.mesh.primitive_plane_add(size=1, location=(terrace_x, terrace_y, 0.005))
        plane = bpy.context.active_object
        plane.scale = (depth, width, 1)

    bpy.ops.object.transform_apply(scale=True)
    plane.name = "PBR_Terrace_Plane"
    plane.data.materials.append(mat)
    coll.objects.link(plane)
    bpy.context.scene.collection.objects.unlink(plane)
    log(f"Terrace: {width}×{depth}m wood deck")


def add_trees(plan, cabin):
    _remove_instances_starting_with("RealTree_")
    coll = get_pine_tree()
    if not coll:
        return

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    if abs(dy) > abs(dx):
        back_y = -5.5 if dy > 0 else 5.5
        wall_axis = 'Y'
    else:
        back_x = -5.5 if dx > 0 else 5.5
        wall_axis = 'X'

    n = plan.get("count", 4)
    target_h = plan.get("height", 9.0)
    src_h = _get_collection_bbox_height(coll) or 20.0
    scale_factor = target_h / src_h
    spread = plan.get("spread", 14.0)
    distance_behind = plan.get("distance_behind_schutting", 1.5)

    for i in range(n):
        t = i / max(1, n - 1)
        pos_along = (t - 0.5) * spread + random.uniform(-0.8, 0.8)

        if wall_axis == 'Y':
            pos_y = back_y - distance_behind - random.uniform(0, 1.5) if dy > 0 else back_y + distance_behind + random.uniform(0, 1.5)
            pos_x = pos_along
        else:
            pos_x = back_x - distance_behind - random.uniform(0, 1.5) if dx > 0 else back_x + distance_behind + random.uniform(0, 1.5)
            pos_y = pos_along

        s = scale_factor * random.uniform(0.85, 1.15)
        _duplicate_collection_at(coll, f"RealTree_{i}",
                                 location=(pos_x, pos_y, 0), scale=s,
                                 rotation_z=random.uniform(0, math.tau))

    log(f"Trees: {n} pines, scale {scale_factor:.3f}")


def add_boxwoods(plan, cabin):
    _remove_instances_starting_with("RealBoxwood_")
    variant = plan.get("variant", 1)
    coll = get_shrub(variant=variant)
    if not coll:
        return

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    target_h = plan.get("height", 0.55)
    src_h = _get_collection_bbox_height(coll) or 0.4
    scale_factor = target_h / src_h

    if abs(dy) > abs(dx):
        front_y = door[1] + (0.9 if dy > 0 else -0.9)
        positions = [(door[0] - 1.2, front_y, 0), (door[0] + 1.2, front_y, 0)]
    else:
        front_x = door[0] + (0.9 if dx > 0 else -0.9)
        positions = [(front_x, door[1] - 1.2, 0), (front_x, door[1] + 1.2, 0)]

    for i, pos in enumerate(positions):
        s = scale_factor * random.uniform(0.95, 1.10)
        _duplicate_collection_at(coll, f"RealBoxwood_{i}",
                                 location=pos, scale=s,
                                 rotation_z=random.uniform(0, math.tau))
    log(f"Boxwoods: 2 shrubs")


def add_potted_plants(plan, cabin):
    _remove_instances_starting_with("RealPotted_")
    coll = get_potted_plant()
    if not coll:
        return

    positions = plan.get("positions", [[3.0, 1.5, 0], [-3.0, 1.5, 0]])
    target_h = plan.get("height", 1.25)
    src_h = _get_collection_bbox_height(coll) or 1.3
    scale_factor = target_h / src_h

    for i, pos in enumerate(positions):
        s = scale_factor * random.uniform(0.95, 1.05)
        _duplicate_collection_at(coll, f"RealPotted_{i}",
                                 location=tuple(pos), scale=s,
                                 rotation_z=random.uniform(0, math.tau))
    log(f"Potted plants: {len(positions)}")


def add_bushes_border(plan, cabin):
    _remove_instances_starting_with("RealBush_")
    coll = get_rooibos_bush()
    if not coll:
        return

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    if abs(dy) > abs(dx):
        back_y = -5.5 if dy > 0 else 5.5
        back_axis = 'Y'
    else:
        back_x = -5.5 if dx > 0 else 5.5
        back_axis = 'X'

    n = plan.get("count", 6)
    border_length = plan.get("length", 13.0)
    offset_from_wall = plan.get("offset_from_wall", 1.2)
    target_h = plan.get("height", 0.65)
    src_h = _get_collection_bbox_height(coll) or 0.54
    scale_factor = target_h / src_h

    for i in range(n):
        t = i / max(1, n - 1)
        pos_along = (t - 0.5) * border_length + random.uniform(-0.4, 0.4)
        jitter = random.uniform(-0.25, 0.25)

        if back_axis == 'Y':
            pos = (pos_along, back_y + offset_from_wall + jitter, 0) if dy > 0 else (pos_along, back_y - offset_from_wall - jitter, 0)
        else:
            pos = (back_x + offset_from_wall + jitter, pos_along, 0) if dx > 0 else (back_x - offset_from_wall - jitter, pos_along, 0)

        s = scale_factor * random.uniform(0.7, 1.3)
        _duplicate_collection_at(coll, f"RealBush_{i}",
                                 location=pos, scale=s,
                                 rotation_z=random.uniform(0, math.tau))
    log(f"Bushes border: {n}")


def add_flower_bed(plan, cabin):
    """Add cluster of real flowers in foreground for color pop."""
    _remove_instances_starting_with("RealFlower_")
    coll = get_flower_gazania()
    if not coll:
        return

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    n = plan.get("count", 5)
    target_h = plan.get("height", 0.25)
    src_h = _get_collection_bbox_height(coll) or 0.20
    scale_factor = target_h / src_h

    # Cluster near front corner of cabin (foreground accent)
    if abs(dy) > abs(dx):
        sign = 1 if dy > 0 else -1
        center_x = plan.get("center_x", cabin["bbox_x"][0] - 1.2)
        center_y = cabin["bbox_y"][1 if dy > 0 else 0] + sign * 0.5
    else:
        sign = 1 if dx > 0 else -1
        center_x = cabin["bbox_x"][1 if dx > 0 else 0] + sign * 0.5
        center_y = plan.get("center_y", cabin["bbox_y"][0] - 1.2)

    for i in range(n):
        angle = (i / n) * math.tau + random.uniform(-0.3, 0.3)
        radius = plan.get("cluster_radius", 0.5) * random.uniform(0.3, 1.0)
        px = center_x + math.cos(angle) * radius
        py = center_y + math.sin(angle) * radius
        s = scale_factor * random.uniform(0.85, 1.15)
        _duplicate_collection_at(coll, f"RealFlower_{i}",
                                 location=(px, py, 0), scale=s,
                                 rotation_z=random.uniform(0, math.tau))
    log(f"Flower bed: {n} gazania clusters at ({center_x:.1f}, {center_y:.1f})")


def push_render_quality(plan):
    scene = bpy.context.scene
    cy = scene.cycles
    cy.samples = plan.get("samples", 192)
    cy.adaptive_threshold = plan.get("noise_threshold", 0.005)
    cy.use_denoising = True
    cy.denoiser = 'OPENIMAGEDENOISE'
    cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
    try:
        scene.render.use_persistent_data = False
    except AttributeError:
        pass
    try:
        scene.world.light_settings.use_ambient_occlusion = True
        scene.world.light_settings.ao_factor = 0.4
    except AttributeError:
        pass
    try:
        cy.texture_limit_render = str(plan.get("texture_limit", 1024))
    except Exception:
        pass
    log(f"Render quality: {cy.samples} samples")


# =============================================================================
# MAIN
# =============================================================================

def main():
    argv = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    if not argv:
        return

    plan_path = argv[0]
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    log(f"Loaded plan: {plan.get('name', '?')}")

    cabin = get_cabin_info()
    if not cabin:
        log("No cabin info", "ERROR")
        return

    extensions = plan.get("extensions", {})

    if extensions.get("pbr_ground", {}).get("enabled", False):
        upgrade_ground()

    if extensions.get("render_quality", {}).get("enabled", False):
        push_render_quality(extensions["render_quality"])

    if extensions.get("schutting", {}).get("enabled", False):
        add_schutting(extensions["schutting"], cabin)

    if extensions.get("terrace", {}).get("enabled", False):
        add_terrace(extensions["terrace"], cabin)

    if extensions.get("trees", {}).get("enabled", False):
        add_trees(extensions["trees"], cabin)

    if extensions.get("boxwoods", {}).get("enabled", False):
        add_boxwoods(extensions["boxwoods"], cabin)

    if extensions.get("potted_plants", {}).get("enabled", False):
        add_potted_plants(extensions["potted_plants"], cabin)

    if extensions.get("bushes_border", {}).get("enabled", False):
        add_bushes_border(extensions["bushes_border"], cabin)

    if extensions.get("flower_bed", {}).get("enabled", False):
        add_flower_bed(extensions["flower_bed"], cabin)

    # NEW: Real garden design extensions
    if extensions.get("plant_bed", {}).get("enabled", False):
        add_plant_bed(extensions["plant_bed"], cabin)

    if extensions.get("path_to_door", {}).get("enabled", False):
        add_path_to_door(extensions["path_to_door"], cabin)

    if extensions.get("focal_tree", {}).get("enabled", False):
        add_focal_tree(extensions["focal_tree"], cabin)

    if extensions.get("clipped_hedge", {}).get("enabled", False):
        add_clipped_hedge_row(extensions["clipped_hedge"], cabin)

    if extensions.get("side_bed", {}).get("enabled", False):
        add_side_bed(extensions["side_bed"], cabin)

    if extensions.get("gravel_zone", {}).get("enabled", False):
        add_gravel_zone(extensions["gravel_zone"], cabin)

    # ALWAYS fix paths + downscale textures (VRAM safety!)
    remap_broken_image_paths()
    max_tex = plan.get("max_texture_size", 1024)
    scale_heavy_textures(max_size=max_tex)

    # Save
    out_blend = plan.get("output_blend")
    if out_blend:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(out_blend))

    # Render
    if plan.get("render_now", False):
        render_path = plan.get("output_render")
        if render_path:
            bpy.context.scene.render.filepath = os.path.abspath(render_path)
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            log("Rendering...")
            bpy.ops.render.render(write_still=True)
            log(f"Done: {render_path}")


if __name__ == "__main__":
    main()
