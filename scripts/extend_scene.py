"""Extend an already-built scene with extra elements (boxwoods, grass scatter, schutting, etc).

Run AFTER build_scene.py has created the base file.

Usage:
    blender --background <built_scene>.blend --python scripts/extend_scene.py -- <extension>.json

The extension JSON specifies which extras to add. Each extension is idempotent — re-running
it on the same scene replaces existing extras rather than duplicating.
"""
import bpy
import os
import sys
import math
import json
import random
from mathutils import Vector


def log(msg, level="INFO"):
    print(f"[{level}] {msg}")


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
# HETZ_MIDGET source loader (creates clean joined source on first call)
# =============================================================================

def get_or_create_boxwood_source():
    """Boxwood source: SKIP fragile imports, use procedural icosphere directly.

    Earlier attempts with GLTF Hetz and Polyhaven shrub both had texture/path issues
    causing purple/pink rendering or headless hangs. Procedural is fully reliable.
    """
    existing = bpy.data.objects.get("Boxwood_Source")
    if existing:
        return existing

    # Procedural icosphere with boxwood material (always works)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=0.4, location=(40, 40, 0.4))
    obj = bpy.context.active_object
    obj.name = "Boxwood_Source"

    # Boxwood material (procedural green with noise variation + bump)
    mat = bpy.data.materials.new("M_Boxwood")
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location=(800,0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location=(500,0)
    noise = nt.nodes.new('ShaderNodeTexNoise'); noise.location=(0,0)
    noise.inputs['Scale'].default_value = 60.0
    noise.inputs['Detail'].default_value = 8.0
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location=(250,0)
    ramp.color_ramp.elements[0].position = 0.4
    ramp.color_ramp.elements[0].color = (0.05, 0.13, 0.04, 1.0)
    ramp.color_ramp.elements[1].position = 0.7
    ramp.color_ramp.elements[1].color = (0.14, 0.26, 0.09, 1.0)
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.92
    bsdf.inputs['Subsurface Weight'].default_value = 0.08
    bump = nt.nodes.new('ShaderNodeBump'); bump.location=(250,-200)
    bump.inputs['Strength'].default_value = 1.0
    bump.inputs['Distance'].default_value = 0.015
    nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    obj.data.materials.append(mat)
    bpy.ops.object.shade_smooth()

    obj.hide_render = True
    log("Boxwood_Source created as procedural icosphere (Polyhaven unavailable)")
    return obj


# Keep old name as alias for backward compat
def get_or_create_hetz_source():
    return get_or_create_boxwood_source()


# =============================================================================
# EXTENSION: boxwoods at door
# =============================================================================

def add_boxwoods_at_door(plan, cabin):
    """Place 2 boxwood balls in front of door."""
    remove_collection_if_exists("Boxwoods_Door")

    hetz_src = get_or_create_hetz_source()
    if not hetz_src:
        return

    boxwood_coll = bpy.data.collections.new("Boxwoods_Door")
    bpy.context.scene.collection.children.link(boxwood_coll)

    door = cabin["door_pos"]
    # Door direction: which axis is the door on relative to cabin center?
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2

    dx = door[0] - cx
    dy = door[1] - cy

    if abs(dy) > abs(dx):
        # Door on Y axis
        front_y = door[1] + (0.9 if dy > 0 else -0.9)  # 90cm out from door
        x_offsets = [-1.2, 1.2]  # left and right of door
        positions = [(door[0] + ox, front_y, -0.04) for ox in x_offsets]
    else:
        # Door on X axis
        front_x = door[0] + (0.9 if dx > 0 else -0.9)
        y_offsets = [-1.2, 1.2]
        positions = [(front_x, door[1] + oy, -0.04) for oy in y_offsets]

    scale = plan.get("scale", 1.0)
    for i, pos in enumerate(positions):
        dup = bpy.data.objects.new(f"Boxwood_Door_{i}", hetz_src.data)
        dup.location = pos
        dup.scale = (scale, scale, scale)
        dup.rotation_euler = (0, 0, random.uniform(0, math.tau))
        boxwood_coll.objects.link(dup)

    log(f"Added 2 boxwoods at door positions: {positions}")


# =============================================================================
# EXTENSION: grass scatter
# =============================================================================

def add_grass_scatter(plan, cabin):
    """Add 3D grass blade scatter on ground plane, mask cabin footprint."""
    ground = bpy.data.objects.get("Ground_Plane") or bpy.data.objects.get("Ground")
    if not ground:
        log("No ground plane — can't add grass scatter", "ERROR")
        return

    # Remove existing
    for mod in list(ground.modifiers):
        if mod.name == "GrassScatter":
            ground.modifiers.remove(mod)
    blade_existing = bpy.data.objects.get("GrassBlade")
    if blade_existing:
        bpy.data.objects.remove(blade_existing, do_unlink=True)

    # Create grass blade mesh
    gmesh = bpy.data.meshes.new("GrassBlade")
    h = plan.get("blade_height", 0.045)
    verts = [
        (-0.004, 0, 0), (0.004, 0, 0),
        (-0.0025, 0, h*0.33), (0.0025, 0, h*0.33),
        (-0.001, 0, h*0.66), (0.001, 0, h*0.66),
        (0, 0, h),
    ]
    faces = [(0,1,3,2), (2,3,5,4), (4,5,6)]
    gmesh.from_pydata(verts, [], faces); gmesh.update()
    blade = bpy.data.objects.new("GrassBlade", gmesh)
    bpy.context.scene.collection.objects.link(blade)
    blade.location = (50, 50, 0)
    blade.hide_render = True
    blade.hide_viewport = True

    # Material
    gmat = bpy.data.materials.get("M_GrassBlade")
    if gmat is None:
        gmat = bpy.data.materials.new("M_GrassBlade")
        gmat.use_nodes = True
        gnt = gmat.node_tree
        for n in list(gnt.nodes): gnt.nodes.remove(n)
        g_out = gnt.nodes.new('ShaderNodeOutputMaterial'); g_out.location=(800,0)
        g_bsdf = gnt.nodes.new('ShaderNodeBsdfPrincipled'); g_bsdf.location=(500,0)
        g_info = gnt.nodes.new('ShaderNodeObjectInfo'); g_info.location=(-400,200)
        g_ramp = gnt.nodes.new('ShaderNodeValToRGB'); g_ramp.location=(-100,200)
        g_ramp.color_ramp.elements[0].color = (0.13, 0.27, 0.06, 1.0)
        g_ramp.color_ramp.elements[1].color = (0.22, 0.40, 0.11, 1.0)
        gnt.links.new(g_info.outputs['Random'], g_ramp.inputs['Fac'])
        gnt.links.new(g_ramp.outputs['Color'], g_bsdf.inputs['Base Color'])
        g_bsdf.inputs['Roughness'].default_value = 0.85
        g_bsdf.inputs['Subsurface Weight'].default_value = 0.20
        g_bsdf.inputs['Subsurface Radius'].default_value = (0.05, 0.02, 0.005)
        gmat.use_backface_culling = False
        gnt.links.new(g_bsdf.outputs['BSDF'], g_out.inputs['Surface'])
    blade.data.materials.append(gmat)

    # GN scatter
    ng = bpy.data.node_groups.get("GN_GrassScatter")
    if ng:
        bpy.data.node_groups.remove(ng)
    ng = bpy.data.node_groups.new("GN_GrassScatter", 'GeometryNodeTree')
    ng.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    nodes = ng.nodes; links = ng.links

    n_in = nodes.new('NodeGroupInput'); n_in.location=(-1200, 0)
    n_out = nodes.new('NodeGroupOutput'); n_out.location=(1400, 0)
    distrib = nodes.new('GeometryNodeDistributePointsOnFaces'); distrib.location=(-600, 0)

    # Cabin footprint mask
    pos = nodes.new('GeometryNodeInputPosition'); pos.location=(-1400, -400)
    sep = nodes.new('ShaderNodeSeparateXYZ'); sep.location=(-1200, -400)
    links.new(pos.outputs['Position'], sep.inputs['Vector'])

    cx_half = (cabin["bbox_x"][1] - cabin["bbox_x"][0]) / 2 + 0.3
    cy_half = (cabin["bbox_y"][1] - cabin["bbox_y"][0]) / 2 + 0.3

    abs_x = nodes.new('ShaderNodeMath'); abs_x.location=(-1000,-300); abs_x.operation='ABSOLUTE'
    links.new(sep.outputs['X'], abs_x.inputs[0])
    abs_y = nodes.new('ShaderNodeMath'); abs_y.location=(-1000,-450); abs_y.operation='ABSOLUTE'
    links.new(sep.outputs['Y'], abs_y.inputs[0])

    x_out = nodes.new('FunctionNodeCompare'); x_out.location=(-800,-300)
    x_out.data_type='FLOAT'; x_out.operation='GREATER_THAN'; x_out.inputs[1].default_value = cx_half
    links.new(abs_x.outputs['Value'], x_out.inputs[0])
    y_out = nodes.new('FunctionNodeCompare'); y_out.location=(-800,-450)
    y_out.data_type='FLOAT'; y_out.operation='GREATER_THAN'; y_out.inputs[1].default_value = cy_half
    links.new(abs_y.outputs['Value'], y_out.inputs[0])

    out_or = nodes.new('FunctionNodeBooleanMath'); out_or.location=(-600,-400); out_or.operation='OR'
    links.new(x_out.outputs['Result'], out_or.inputs[0])
    links.new(y_out.outputs['Result'], out_or.inputs[1])

    dens_mult = nodes.new('ShaderNodeMath'); dens_mult.location=(-400,-400); dens_mult.operation='MULTIPLY'
    dens_mult.inputs[1].default_value = plan.get("density_per_m2", 1200)
    links.new(out_or.outputs['Boolean'], dens_mult.inputs[0])
    links.new(dens_mult.outputs['Value'], distrib.inputs['Density'])

    ioP = nodes.new('GeometryNodeInstanceOnPoints'); ioP.location=(0, 0)
    obj_info = nodes.new('GeometryNodeObjectInfo'); obj_info.location=(-400, 200)
    obj_info.transform_space = 'ORIGINAL'
    obj_info.inputs['Object'].default_value = blade

    rotate_inst = nodes.new('GeometryNodeRotateInstances'); rotate_inst.location=(400, 0)
    rand_yaw = nodes.new('FunctionNodeRandomValue'); rand_yaw.location=(100, -200)
    rand_yaw.data_type = 'FLOAT_VECTOR'
    rand_yaw.inputs[0].default_value = (0, 0, -math.pi)
    rand_yaw.inputs[1].default_value = (0, 0, math.pi)

    scale_inst = nodes.new('GeometryNodeScaleInstances'); scale_inst.location=(700, 0)
    rand_scale = nodes.new('FunctionNodeRandomValue'); rand_scale.location=(400, -200)
    rand_scale.data_type = 'FLOAT'
    rand_scale.inputs[2].default_value = 0.7
    rand_scale.inputs[3].default_value = 1.2

    join = nodes.new('GeometryNodeJoinGeometry'); join.location=(1100, 0)

    links.new(n_in.outputs['Geometry'], distrib.inputs['Mesh'])
    links.new(distrib.outputs['Points'], ioP.inputs['Points'])
    links.new(obj_info.outputs['Geometry'], ioP.inputs['Instance'])
    links.new(ioP.outputs['Instances'], rotate_inst.inputs['Instances'])
    links.new(rand_yaw.outputs['Value'], rotate_inst.inputs['Rotation'])
    links.new(rotate_inst.outputs['Instances'], scale_inst.inputs['Instances'])
    links.new(rand_scale.outputs['Value'], scale_inst.inputs['Scale'])
    links.new(scale_inst.outputs['Instances'], join.inputs['Geometry'])
    links.new(n_in.outputs['Geometry'], join.inputs['Geometry'])
    links.new(join.outputs['Geometry'], n_out.inputs['Geometry'])

    mod = ground.modifiers.new("GrassScatter", type='NODES')
    mod.node_group = ng

    log(f"Grass scatter added: {plan.get('density_per_m2', 1200)}/m², blade {h*100:.0f}cm")


# =============================================================================
# EXTENSION: cedar schutting behind cabin
# =============================================================================

def make_cedar_material():
    """Cedar plank material with grain bump."""
    mat = bpy.data.materials.get("M_Cedar_Schutting")
    if mat:
        return mat
    mat = bpy.data.materials.new("M_Cedar_Schutting")
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location=(800,0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location=(500,0)
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location=(-600,0)
    mapp = nt.nodes.new('ShaderNodeMapping'); mapp.location=(-400,0)
    mapp.inputs['Scale'].default_value = (6.0, 1.0, 1.0)
    nt.links.new(tc.outputs['Object'], mapp.inputs['Vector'])
    wave = nt.nodes.new('ShaderNodeTexWave'); wave.location=(-200,0)
    wave.wave_type='BANDS'; wave.bands_direction='X'
    wave.inputs['Scale'].default_value = 6.0
    nt.links.new(mapp.outputs['Vector'], wave.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location=(50,0)
    ramp.color_ramp.elements[0].position = 0.45
    ramp.color_ramp.elements[0].color = (0.32, 0.20, 0.12, 1.0)
    ramp.color_ramp.elements[1].position = 0.55
    ramp.color_ramp.elements[1].color = (0.42, 0.27, 0.16, 1.0)
    nt.links.new(wave.outputs['Color'], ramp.inputs['Fac'])
    # Noise grain overlay
    noise = nt.nodes.new('ShaderNodeTexNoise'); noise.location=(-200,-300)
    noise.inputs['Scale'].default_value = 20.0
    noise.inputs['Detail'].default_value = 8.0
    nt.links.new(mapp.outputs['Vector'], noise.inputs['Vector'])
    grain = nt.nodes.new('ShaderNodeValToRGB'); grain.location=(50,-300)
    grain.color_ramp.elements[0].position = 0.4
    grain.color_ramp.elements[0].color = (0.85, 0.85, 0.85, 1.0)
    grain.color_ramp.elements[1].position = 0.7
    grain.color_ramp.elements[1].color = (1.10, 1.10, 1.10, 1.0)
    nt.links.new(noise.outputs['Fac'], grain.inputs['Fac'])
    mix = nt.nodes.new('ShaderNodeMixRGB'); mix.location=(300,0); mix.blend_type='MULTIPLY'
    mix.inputs['Fac'].default_value = 1.0
    nt.links.new(ramp.outputs['Color'], mix.inputs['Color1'])
    nt.links.new(grain.outputs['Color'], mix.inputs['Color2'])
    nt.links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.75
    bump = nt.nodes.new('ShaderNodeBump'); bump.location=(300,-200)
    bump.inputs['Strength'].default_value = 0.5
    bump.inputs['Distance'].default_value = 0.008
    nt.links.new(wave.outputs['Color'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def add_schutting(plan, cabin):
    """Cedar schutting wall behind cabin (opposite of door)."""
    remove_collection_if_exists("Schutting")

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2

    # Determine back direction (opposite of door)
    dx = door[0] - cx
    dy = door[1] - cy

    height = plan.get("height", 2.0)
    thickness = plan.get("thickness", 0.04)
    back_length = plan.get("back_length", 14.0)
    side_length = plan.get("side_length", 9.5)

    mat = make_cedar_material()

    schutting_coll = bpy.data.collections.new("Schutting")
    bpy.context.scene.collection.children.link(schutting_coll)

    if abs(dy) > abs(dx):
        # Door on Y axis — schutting back wall is opposite Y
        back_y = -5.5 if dy > 0 else 5.5  # 4m behind cabin
        side_x_left = -7.0
        side_x_right = 7.0
        side_y_mid = back_y - (3.5 if dy > 0 else -3.5)  # extends partway forward

        # Back wall
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, back_y, height/2))
        wall = bpy.context.active_object
        wall.name = "Schutting_Back"
        wall.scale = (back_length, thickness, height)
        bpy.ops.object.transform_apply(scale=True)
        wall.data.materials.append(mat)

        # Optional left/right side walls
        if plan.get("side_walls", True):
            for x_pos, name in [(side_x_left, "Schutting_Left"), (side_x_right, "Schutting_Right")]:
                bpy.ops.mesh.primitive_cube_add(size=1, location=(x_pos, side_y_mid, height/2))
                w = bpy.context.active_object
                w.name = name
                w.scale = (thickness, side_length, height)
                bpy.ops.object.transform_apply(scale=True)
                w.data.materials.append(mat)
    else:
        # Door on X axis — schutting back wall is opposite X
        back_x = -5.5 if dx > 0 else 5.5
        side_y_left = -7.0
        side_y_right = 7.0
        side_x_mid = back_x - (3.5 if dx > 0 else -3.5)

        bpy.ops.mesh.primitive_cube_add(size=1, location=(back_x, 0, height/2))
        wall = bpy.context.active_object
        wall.name = "Schutting_Back"
        wall.scale = (thickness, back_length, height)
        bpy.ops.object.transform_apply(scale=True)
        wall.data.materials.append(mat)

        if plan.get("side_walls", True):
            for y_pos, name in [(side_y_left, "Schutting_Front"), (side_y_right, "Schutting_Rear")]:
                bpy.ops.mesh.primitive_cube_add(size=1, location=(side_x_mid, y_pos, height/2))
                w = bpy.context.active_object
                w.name = name
                w.scale = (side_length, thickness, height)
                bpy.ops.object.transform_apply(scale=True)
                w.data.materials.append(mat)

    # Move all to schutting collection
    for obj in [o for o in bpy.data.objects if o.name.startswith("Schutting_")]:
        for c in obj.users_collection:
            if c != schutting_coll:
                c.objects.unlink(obj)
        if obj.name not in schutting_coll.objects:
            schutting_coll.objects.link(obj)

    log(f"Cedar schutting added (back+sides, {height}m tall, opposite of door direction)")


# =============================================================================
# EXTENSION: 3-layer plant border (hortensia/lavender/sedum) along schutting
# =============================================================================

def make_hortensia_material():
    mat = bpy.data.materials.get("M_Hortensia")
    if mat: return mat
    mat = bpy.data.materials.new("M_Hortensia")
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location=(800,0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location=(500,0)
    # Voronoi → distinct bloom CLUSTERS over green leaf base (more like real hortensia)
    vor = nt.nodes.new('ShaderNodeTexVoronoi'); vor.location=(-400,0)
    vor.feature = 'F1'
    vor.inputs['Scale'].default_value = 8.0
    vor_ramp = nt.nodes.new('ShaderNodeValToRGB'); vor_ramp.location=(-150,0)
    vor_ramp.color_ramp.elements[0].position = 0.0
    vor_ramp.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)
    vor_ramp.color_ramp.elements[1].position = 0.20
    vor_ramp.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)
    nt.links.new(vor.outputs['Distance'], vor_ramp.inputs['Fac'])
    # Mix: leaf green (default) vs bloom cluster (highlighted)
    mix = nt.nodes.new('ShaderNodeMixRGB'); mix.location=(150,0)
    mix.inputs['Color1'].default_value = (0.10, 0.22, 0.05, 1.0)  # leaf green
    mix.inputs['Color2'].default_value = (0.88, 0.72, 0.78, 1.0)  # pink-white bloom (saturated)
    nt.links.new(vor_ramp.outputs['Color'], mix.inputs['Fac'])
    nt.links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.92
    bsdf.inputs['Subsurface Weight'].default_value = 0.10
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def make_lavender_material():
    mat = bpy.data.materials.get("M_Lavender")
    if mat: return mat
    mat = bpy.data.materials.new("M_Lavender")
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location=(800,0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location=(500,0)
    # Voronoi clusters with more PURPLE dominance (visible from distance)
    vor = nt.nodes.new('ShaderNodeTexVoronoi'); vor.location=(-400,0)
    vor.feature = 'F1'
    vor.inputs['Scale'].default_value = 12.0
    vor_ramp = nt.nodes.new('ShaderNodeValToRGB'); vor_ramp.location=(-150,0)
    vor_ramp.color_ramp.elements[0].position = 0.0
    vor_ramp.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)
    vor_ramp.color_ramp.elements[1].position = 0.35
    vor_ramp.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)
    nt.links.new(vor.outputs['Distance'], vor_ramp.inputs['Fac'])
    mix = nt.nodes.new('ShaderNodeMixRGB'); mix.location=(150,0)
    mix.inputs['Color1'].default_value = (0.14, 0.20, 0.08, 1.0)  # silver-green foliage
    mix.inputs['Color2'].default_value = (0.42, 0.22, 0.58, 1.0)  # saturated purple
    nt.links.new(vor_ramp.outputs['Color'], mix.inputs['Fac'])
    nt.links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.95
    bsdf.inputs['Subsurface Weight'].default_value = 0.15
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def make_sedum_material():
    mat = bpy.data.materials.get("M_Sedum")
    if mat: return mat
    mat = bpy.data.materials.new("M_Sedum")
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location=(800,0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location=(500,0)
    noise = nt.nodes.new('ShaderNodeTexNoise'); noise.location=(-200,0)
    noise.inputs['Scale'].default_value = 120.0
    noise.inputs['Detail'].default_value = 10.0
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location=(100,0)
    ramp.color_ramp.elements[0].color = (0.18, 0.22, 0.10, 1.0)  # yellow-green
    ramp.color_ramp.elements[1].position = 0.7
    ramp.color_ramp.elements[1].color = (0.28, 0.32, 0.14, 1.0)
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.85
    bsdf.inputs['Subsurface Weight'].default_value = 0.05
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def _make_clumped_plant(name, base_radius, height_scale, material):
    """Create an irregular clumped sphere (not perfect ball) for plant volumes."""
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=base_radius, location=(50, 50, 0))
    obj = bpy.context.active_object
    obj.name = name
    # Squash + add noise displacement via Displace modifier
    obj.scale = (1.0, 1.0, height_scale)
    bpy.ops.object.transform_apply(scale=True)
    # Add noise texture for displacement
    tex = bpy.data.textures.new(f"T_{name}", 'CLOUDS')
    tex.noise_scale = 0.35
    disp = obj.modifiers.new("Displace", 'DISPLACE')
    disp.texture = tex
    disp.strength = base_radius * 0.4
    # Subsurf for smoother result
    subs = obj.modifiers.new("Subsurf", 'SUBSURF')
    subs.levels = 1
    subs.render_levels = 2
    obj.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    obj.hide_render = True
    return obj


def add_plant_border(plan, cabin):
    """Three-layer plant border along schutting back wall.

    Layer 1 (back, against schutting): Hortensia — tall round bushes
    Layer 2 (middle): Lavender — purple stripes
    Layer 3 (front): Sedum — low groundcover patches
    """
    remove_collection_if_exists("Plant_Border")

    coll = bpy.data.collections.new("Plant_Border")
    bpy.context.scene.collection.children.link(coll)

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    # Schutting back position (must match add_schutting logic)
    if abs(dy) > abs(dx):
        back_y = -5.5 if dy > 0 else 5.5
        back_axis = 'Y'
    else:
        back_x = -5.5 if dx > 0 else 5.5
        back_axis = 'X'

    border_length = plan.get("length", 12.0)  # along schutting
    center = plan.get("center", 0.0)  # center along the axis

    # Source objects (hidden)
    hortensia_src = _make_clumped_plant("Hortensia_Source", 0.65, 0.95, make_hortensia_material())
    lavender_src = _make_clumped_plant("Lavender_Source", 0.35, 0.55, make_lavender_material())
    sedum_src = _make_clumped_plant("Sedum_Source", 0.22, 0.35, make_sedum_material())

    # Hortensia at back (y_offset from schutting: +0.6)
    # Lavender middle (+1.2)
    # Sedum front (+1.8)
    n_hortensia = plan.get("n_hortensia", 6)
    n_lavender = plan.get("n_lavender", 12)
    n_sedum = plan.get("n_sedum", 18)

    def place_row(src, offset_from_wall, n_items, name_prefix, scale_range=(0.9, 1.1)):
        for i in range(n_items):
            t = i / max(1, n_items - 1)  # 0..1 along border
            pos_along = center + (t - 0.5) * border_length
            jitter_perp = random.uniform(-0.15, 0.15)
            scale = random.uniform(*scale_range)

            if back_axis == 'Y':
                if dy > 0:  # door at +Y, schutting at -Y
                    pos = (pos_along, back_y + offset_from_wall + jitter_perp, -0.04)
                else:
                    pos = (pos_along, back_y - offset_from_wall - jitter_perp, -0.04)
            else:
                if dx > 0:
                    pos = (back_x + offset_from_wall + jitter_perp, pos_along, -0.04)
                else:
                    pos = (back_x - offset_from_wall - jitter_perp, pos_along, -0.04)

            dup = bpy.data.objects.new(f"{name_prefix}_{i}", src.data)
            dup.location = pos
            dup.scale = (scale, scale, scale)
            dup.rotation_euler = (0, 0, random.uniform(0, math.tau))
            coll.objects.link(dup)

    place_row(hortensia_src, 0.55, n_hortensia, "Hortensia", (0.85, 1.20))
    place_row(lavender_src, 1.15, n_lavender, "Lavender", (0.85, 1.15))
    place_row(sedum_src, 1.70, n_sedum, "Sedum", (0.70, 1.10))

    log(f"Plant border: {n_hortensia} hortensia + {n_lavender} lavender + {n_sedum} sedum")

    # Optional: side borders (along schutting side walls, around cabin sides)
    if plan.get("side_borders", False):
        side_length = plan.get("side_length", 5.5)
        n_side_h = plan.get("n_side_hortensia", 3)
        n_side_l = plan.get("n_side_lavender", 5)

        side_xs = [-7.0, 7.0]  # matches schutting side walls at X=±7

        def place_side_row(src, offset_from_wall, n_items, name_prefix, scale_range=(0.85, 1.15)):
            for side_x in side_xs:
                inner_sign = -1 if side_x > 0 else 1  # offset toward cabin
                for i in range(n_items):
                    t = i / max(1, n_items - 1)
                    if back_axis == 'Y':
                        # side walls extend along Y from schutting back forward
                        y_pos = back_y + (0.0 if dy < 0 else 0.0) + (t * side_length if dy > 0 else -t * side_length)
                        # Wait, side walls extend FROM back wall AWAY from door direction
                        # Actually they extend in the +door direction (so from back wall toward door front)
                        if dy > 0:  # door at +Y, side walls extend from back_y=-5.5 toward door
                            y_pos = back_y + 1.0 + t * (side_length - 1.0)  # skip back corner overlap
                        else:
                            y_pos = back_y - 1.0 - t * (side_length - 1.0)
                        x_pos = side_x + inner_sign * offset_from_wall + random.uniform(-0.15, 0.15)
                    else:
                        if dx > 0:
                            x_pos = back_x + 1.0 + t * (side_length - 1.0)
                        else:
                            x_pos = back_x - 1.0 - t * (side_length - 1.0)
                        y_pos = side_x + inner_sign * offset_from_wall + random.uniform(-0.15, 0.15)

                    scale = random.uniform(*scale_range)
                    dup = bpy.data.objects.new(f"{name_prefix}_side_{side_x:.0f}_{i}", src.data)
                    dup.location = (x_pos, y_pos, -0.04)
                    dup.scale = (scale, scale, scale)
                    dup.rotation_euler = (0, 0, random.uniform(0, math.tau))
                    coll.objects.link(dup)

        place_side_row(hortensia_src, 0.55, n_side_h, "Hortensia", (0.80, 1.10))
        place_side_row(lavender_src, 1.15, n_side_l, "Lavender", (0.85, 1.10))
        log(f"Side borders: {n_side_h*2} hortensia + {n_side_l*2} lavender")


# =============================================================================
# EXTENSION: birch backdrop (behind schutting)
# =============================================================================

def make_birch_trunk_material():
    mat = bpy.data.materials.get("M_BirchTrunk")
    if mat: return mat
    mat = bpy.data.materials.new("M_BirchTrunk")
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location=(800,0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location=(500,0)
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location=(-600,0)
    mapp = nt.nodes.new('ShaderNodeMapping'); mapp.location=(-400,0)
    mapp.inputs['Scale'].default_value = (1.0, 1.0, 8.0)
    nt.links.new(tc.outputs['Object'], mapp.inputs['Vector'])
    # Black streaks on white via Voronoi
    vor = nt.nodes.new('ShaderNodeTexVoronoi'); vor.location=(-200,0)
    vor.feature = 'F1'
    vor.inputs['Scale'].default_value = 2.0
    nt.links.new(mapp.outputs['Vector'], vor.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location=(100,0)
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (0.04, 0.03, 0.03, 1.0)  # black streak
    ramp.color_ramp.elements[1].position = 0.15
    ramp.color_ramp.elements[1].color = (0.92, 0.90, 0.86, 1.0)  # white bark
    nt.links.new(vor.outputs['Distance'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.85
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def make_cherry_blossom_material():
    """Force-delete + recreate so iterations pick up changes."""
    existing = bpy.data.materials.get("M_CherryBlossom")
    if existing:
        bpy.data.materials.remove(existing)
    mat = bpy.data.materials.new("M_CherryBlossom")
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location=(800,0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location=(500,0)
    noise = nt.nodes.new('ShaderNodeTexNoise'); noise.location=(-200,0)
    noise.inputs['Scale'].default_value = 25.0
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location=(100,0)
    ramp.color_ramp.elements[0].position = 0.15
    ramp.color_ramp.elements[0].color = (0.78, 0.30, 0.45, 1.0)  # saturated pink
    ramp.color_ramp.elements.new(0.5)
    ramp.color_ramp.elements[1].color = (0.92, 0.55, 0.68, 1.0)  # mid pink
    ramp.color_ramp.elements[2].position = 0.85
    ramp.color_ramp.elements[2].color = (0.95, 0.78, 0.82, 1.0)  # light pink
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.90
    bsdf.inputs['Subsurface Weight'].default_value = 0.05  # reduce glow
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def make_birch_foliage_material():
    mat = bpy.data.materials.get("M_BirchFoliage")
    if mat: return mat
    mat = bpy.data.materials.new("M_BirchFoliage")
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location=(800,0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location=(500,0)
    noise = nt.nodes.new('ShaderNodeTexNoise'); noise.location=(-200,0)
    noise.inputs['Scale'].default_value = 30.0
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location=(100,0)
    ramp.color_ramp.elements[0].color = (0.10, 0.22, 0.05, 1.0)
    ramp.color_ramp.elements[1].position = 0.7
    ramp.color_ramp.elements[1].color = (0.28, 0.42, 0.12, 1.0)
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.92
    bsdf.inputs['Subsurface Weight'].default_value = 0.12
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def add_birch_backdrop(plan, cabin):
    """Tall slim birches behind the schutting for vertical backdrop."""
    remove_collection_if_exists("Birch_Backdrop")
    coll = bpy.data.collections.new("Birch_Backdrop")
    bpy.context.scene.collection.children.link(coll)

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    n = plan.get("count", 4)
    height_range = plan.get("height_range", [4.5, 7.5])
    spread = plan.get("spread", 12.0)
    distance_behind = plan.get("distance_behind_schutting", 1.5)

    trunk_mat = make_birch_trunk_material()
    foliage_style = plan.get("foliage", "birch")  # "birch" or "cherry_blossom"
    if foliage_style == "cherry_blossom":
        foliage_mat = make_cherry_blossom_material()
    else:
        foliage_mat = make_birch_foliage_material()

    # Schutting back at -5.5 (or +5.5 if door at -Y)
    if abs(dy) > abs(dx):
        back_y = -5.5 if dy > 0 else 5.5
        wall_axis = 'Y'
    else:
        back_x = -5.5 if dx > 0 else 5.5
        wall_axis = 'X'

    winter = plan.get("winter", False)
    for i in range(n):
        t = i / max(1, n - 1)
        pos_along = (t - 0.5) * spread + random.uniform(-0.5, 0.5)
        h = random.uniform(height_range[0], height_range[1])
        # Real birch proportions: slim trunk, tall narrow crown starting ~55% up
        trunk_radius = h * 0.022  # slim
        crown_radius = h * 0.18   # narrower (was 0.35 = broccoli)
        crown_start_z = h * 0.55  # foliage starts at 55% — trunk visible above schutting!
        crown_top_z = h * 0.92    # foliage tapers to top

        if wall_axis == 'Y':
            if dy > 0:
                trunk_y = back_y - distance_behind - random.uniform(0, 1.5)
            else:
                trunk_y = back_y + distance_behind + random.uniform(0, 1.5)
            trunk_x = pos_along
        else:
            if dx > 0:
                trunk_x = back_x - distance_behind - random.uniform(0, 1.5)
            else:
                trunk_x = back_x + distance_behind + random.uniform(0, 1.5)
            trunk_y = pos_along

        # Trunk (full height, foliage will hide upper portion partially)
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=10, radius=trunk_radius, depth=h,
            location=(trunk_x, trunk_y, h/2 - 0.05))
        trunk = bpy.context.active_object
        trunk.name = f"Birch_Trunk_{i}"
        trunk.data.materials.append(trunk_mat)
        coll.objects.link(trunk)
        bpy.context.scene.collection.objects.unlink(trunk)

        if winter:
            continue  # Bare branches — no foliage clusters added

        # Crown — multi-cluster of MORE irregular spheres with stronger displacement
        crown_actual_height = crown_top_z - crown_start_z
        n_clusters = 6  # more clusters
        for k in range(n_clusters):
            kt = (k + 0.5) / n_clusters  # 0..1 vertical position in crown
            # Taper at top, fuller in middle
            taper = math.sin(kt * math.pi) * 0.5 + 0.55  # 0.55..1.05 envelope
            clust_radius = crown_radius * taper * random.uniform(0.75, 1.25)
            z_in_crown = crown_start_z + kt * crown_actual_height + random.uniform(-0.3, 0.3)
            x_off = trunk_x + random.uniform(-clust_radius*0.5, clust_radius*0.5)
            y_off = trunk_y + random.uniform(-clust_radius*0.5, clust_radius*0.5)

            bpy.ops.mesh.primitive_ico_sphere_add(
                subdivisions=3, radius=clust_radius,
                location=(x_off, y_off, z_in_crown))
            cluster = bpy.context.active_object
            cluster.name = f"Birch_Crown_{i}_{k}"
            # Two stacked noise displacements for more organic edge
            tex1 = bpy.data.textures.new(f"T_BirchCl1_{i}_{k}", 'CLOUDS')
            tex1.noise_scale = 0.5  # large variations
            disp1 = cluster.modifiers.new("Displace1", 'DISPLACE')
            disp1.texture = tex1
            disp1.strength = clust_radius * 0.4

            tex2 = bpy.data.textures.new(f"T_BirchCl2_{i}_{k}", 'CLOUDS')
            tex2.noise_scale = 0.15  # finer detail
            disp2 = cluster.modifiers.new("Displace2", 'DISPLACE')
            disp2.texture = tex2
            disp2.strength = clust_radius * 0.15

            cluster.data.materials.append(foliage_mat)
            bpy.ops.object.shade_smooth()
            coll.objects.link(cluster)
            bpy.context.scene.collection.objects.unlink(cluster)

    log(f"Birch backdrop: {n} trees behind schutting")


# =============================================================================
# EXTENSION: stepping path
# =============================================================================

def make_paving_material():
    mat = bpy.data.materials.get("M_Paving")
    if mat: return mat
    mat = bpy.data.materials.new("M_Paving")
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location=(800,0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location=(500,0)
    noise = nt.nodes.new('ShaderNodeTexNoise'); noise.location=(-200,0)
    noise.inputs['Scale'].default_value = 50.0
    noise.inputs['Detail'].default_value = 12.0
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location=(100,0)
    ramp.color_ramp.elements[0].position = 0.3
    ramp.color_ramp.elements[0].color = (0.36, 0.34, 0.32, 1.0)
    ramp.color_ramp.elements[1].position = 0.7
    ramp.color_ramp.elements[1].color = (0.55, 0.53, 0.50, 1.0)
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.90
    bump = nt.nodes.new('ShaderNodeBump'); bump.location=(300,-200)
    bump.inputs['Strength'].default_value = 0.4
    bump.inputs['Distance'].default_value = 0.005
    nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def add_stepping_path(plan, cabin):
    """Row of rectangular stepping stones leading to door."""
    remove_collection_if_exists("Stepping_Path")
    coll = bpy.data.collections.new("Stepping_Path")
    bpy.context.scene.collection.children.link(coll)

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    n_stones = plan.get("count", 5)
    stone_size = plan.get("stone_size", [0.50, 0.35])  # along axis x perp
    spacing = plan.get("spacing", 0.65)
    start_offset = plan.get("start_offset_from_door", 1.6)

    mat = make_paving_material()

    # Stones must sit ABOVE grass (~4.5cm). Place at z=0.025 so top at 0.05 above ground.
    stone_z = 0.025
    if abs(dy) > abs(dx):
        # Door on Y axis
        sign = 1 if dy > 0 else -1
        for i in range(n_stones):
            y_pos = door[1] + sign * (start_offset + i * spacing)
            x_pos = door[0] + random.uniform(-0.08, 0.08)
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x_pos, y_pos, stone_z))
            stone = bpy.context.active_object
            stone.name = f"Stone_{i}"
            stone.scale = (stone_size[1], stone_size[0], 0.05)  # length along Y
            bpy.ops.object.transform_apply(scale=True)
            stone.rotation_euler = (0, 0, random.uniform(-0.08, 0.08))
            stone.data.materials.append(mat)
            coll.objects.link(stone)
            bpy.context.scene.collection.objects.unlink(stone)
    else:
        sign = 1 if dx > 0 else -1
        for i in range(n_stones):
            x_pos = door[0] + sign * (start_offset + i * spacing)
            y_pos = door[1] + random.uniform(-0.08, 0.08)
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x_pos, y_pos, stone_z))
            stone = bpy.context.active_object
            stone.name = f"Stone_{i}"
            stone.scale = (stone_size[0], stone_size[1], 0.05)
            bpy.ops.object.transform_apply(scale=True)
            stone.rotation_euler = (0, 0, random.uniform(-0.08, 0.08))
            stone.data.materials.append(mat)
            coll.objects.link(stone)
            bpy.context.scene.collection.objects.unlink(stone)

    log(f"Stepping path: {n_stones} stones to door")


# =============================================================================
# EXTENSION: varied boxwoods (multiple sizes, not just 2 at door)
# =============================================================================

def add_varied_boxwoods(plan, cabin):
    """Multiple boxwoods at varied positions with size variation.

    Replaces the simple 2-at-door pattern. Uses preset arrangements:
    - flanking_door: 2 large at door (back to v4 behavior)
    - corner_accents: small ones at cabin corners
    - border_dots: scattered medium ones along plant border front
    """
    remove_collection_if_exists("Boxwoods_Varied")
    coll = bpy.data.collections.new("Boxwoods_Varied")
    bpy.context.scene.collection.children.link(coll)

    src = get_or_create_boxwood_source()
    if not src: return

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    positions = []  # list of (x, y, scale)

    arrangements = plan.get("arrangements", ["flanking_door", "border_dots"])

    if "flanking_door" in arrangements:
        flank_scale = plan.get("flank_scale", 1.5)
        if abs(dy) > abs(dx):
            front_y = door[1] + (0.9 if dy > 0 else -0.9)
            positions.append((door[0] - 1.2, front_y, flank_scale))
            positions.append((door[0] + 1.2, front_y, flank_scale))
        else:
            front_x = door[0] + (0.9 if dx > 0 else -0.9)
            positions.append((front_x, door[1] - 1.2, flank_scale))
            positions.append((front_x, door[1] + 1.2, flank_scale))

    if "corner_accents" in arrangements:
        corner_scale = plan.get("corner_scale", 0.9)
        # Small boxwoods at the 2 corners visible from camera (front of cabin)
        if abs(dy) > abs(dx):
            front_y = cy + (1.5 if dy > 0 else -1.5)  # at cabin front edge
            if dy > 0:
                door_y_extreme = cabin["bbox_y"][1] + 0.5
                positions.append((cabin["bbox_x"][0] - 0.4, door_y_extreme, corner_scale))
                positions.append((cabin["bbox_x"][1] + 0.4, door_y_extreme, corner_scale))
            else:
                door_y_extreme = cabin["bbox_y"][0] - 0.5
                positions.append((cabin["bbox_x"][0] - 0.4, door_y_extreme, corner_scale))
                positions.append((cabin["bbox_x"][1] + 0.4, door_y_extreme, corner_scale))

    if "border_dots" in arrangements:
        # 4-6 medium boxwoods near front of plant border (visible from camera)
        n_dots = plan.get("border_dot_count", 5)
        dot_scale = plan.get("dot_scale", 0.7)
        if abs(dy) > abs(dx):
            border_y = (-5.5 + 1.7) if dy > 0 else (5.5 - 1.7)  # front of plant border
            for i in range(n_dots):
                t = i / max(1, n_dots - 1)
                x_pos = (t - 0.5) * 9.0  # span 9m along border
                positions.append((x_pos + random.uniform(-0.2, 0.2), border_y + random.uniform(-0.15, 0.15), dot_scale))
        else:
            border_x = (-5.5 + 1.7) if dx > 0 else (5.5 - 1.7)
            for i in range(n_dots):
                t = i / max(1, n_dots - 1)
                y_pos = (t - 0.5) * 9.0
                positions.append((border_x + random.uniform(-0.15, 0.15), y_pos + random.uniform(-0.2, 0.2), dot_scale))

    for i, (x, y, sc) in enumerate(positions):
        dup = bpy.data.objects.new(f"Boxwood_V_{i}", src.data)
        dup.location = (x, y, -0.04 + sc * 0.05)  # sink slightly into ground
        # PYRAMIDAL boxwood: taller than wide (modern topiary buxus look)
        # Random slight variation between instances
        h_stretch = random.uniform(1.15, 1.35)  # taller
        w_var = random.uniform(0.85, 1.05)
        dup.scale = (sc * w_var, sc * w_var, sc * h_stretch)
        dup.rotation_euler = (0, 0, random.uniform(0, math.tau))
        coll.objects.link(dup)

    log(f"Varied boxwoods: {len(positions)} placed across arrangements {arrangements}")


# =============================================================================
# EXTENSION: front terrace (paved area in front of door)
# =============================================================================

def add_front_terrace(plan, cabin):
    """Paved terrace area directly in front of cabin door — grounds the cabin visually."""
    remove_collection_if_exists("Front_Terrace")
    coll = bpy.data.collections.new("Front_Terrace")
    bpy.context.scene.collection.children.link(coll)

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    width = plan.get("width", 4.0)  # along cabin face
    depth = plan.get("depth", 2.0)  # away from cabin
    paver_size = plan.get("paver_size", 0.5)  # individual paver

    mat = make_paving_material()

    # Terrace center position: just in front of door
    if abs(dy) > abs(dx):
        # Door at +Y or -Y
        sign = 1 if dy > 0 else -1
        terrace_y = cabin["bbox_y"][1] + depth/2 if dy > 0 else cabin["bbox_y"][0] - depth/2
        terrace_x = door[0]
        # Paver grid: along X (width), along Y (depth)
        n_x = max(1, int(width / paver_size))
        n_y = max(1, int(depth / paver_size))
        for i in range(n_x):
            for j in range(n_y):
                px = terrace_x - width/2 + (i + 0.5) * (width / n_x)
                py = terrace_y - sign * depth/2 + sign * (j + 0.5) * (depth / n_y)
                bpy.ops.mesh.primitive_cube_add(size=1, location=(px, py, 0.025))
                paver = bpy.context.active_object
                paver.name = f"Paver_{i}_{j}"
                paver.scale = (width / n_x - 0.02, depth / n_y - 0.02, 0.05)  # 2cm gap
                bpy.ops.object.transform_apply(scale=True)
                paver.data.materials.append(mat)
                coll.objects.link(paver)
                bpy.context.scene.collection.objects.unlink(paver)
    else:
        # Door at +X or -X
        sign = 1 if dx > 0 else -1
        terrace_x = cabin["bbox_x"][1] + depth/2 if dx > 0 else cabin["bbox_x"][0] - depth/2
        terrace_y = door[1]
        n_x = max(1, int(depth / paver_size))
        n_y = max(1, int(width / paver_size))
        for i in range(n_x):
            for j in range(n_y):
                px = terrace_x - sign * depth/2 + sign * (i + 0.5) * (depth / n_x)
                py = terrace_y - width/2 + (j + 0.5) * (width / n_y)
                bpy.ops.mesh.primitive_cube_add(size=1, location=(px, py, 0.025))
                paver = bpy.context.active_object
                paver.name = f"Paver_{i}_{j}"
                paver.scale = (depth / n_x - 0.02, width / n_y - 0.02, 0.05)
                bpy.ops.object.transform_apply(scale=True)
                paver.data.materials.append(mat)
                coll.objects.link(paver)
                bpy.context.scene.collection.objects.unlink(paver)

    log(f"Front terrace: {width}×{depth}m paved with ~{paver_size}m pavers")


# =============================================================================
# EXTENSION: foreground planter (color accent + scale reference)
# =============================================================================

def make_terracotta_material():
    mat = bpy.data.materials.get("M_Terracotta")
    if mat: return mat
    mat = bpy.data.materials.new("M_Terracotta")
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location=(800,0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location=(500,0)
    noise = nt.nodes.new('ShaderNodeTexNoise'); noise.location=(-200,0)
    noise.inputs['Scale'].default_value = 25.0
    noise.inputs['Detail'].default_value = 8.0
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location=(100,0)
    ramp.color_ramp.elements[0].position = 0.3
    ramp.color_ramp.elements[0].color = (0.52, 0.24, 0.15, 1.0)
    ramp.color_ramp.elements[1].position = 0.7
    ramp.color_ramp.elements[1].color = (0.70, 0.38, 0.22, 1.0)
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.85
    bump = nt.nodes.new('ShaderNodeBump'); bump.location=(300,-200)
    bump.inputs['Strength'].default_value = 0.3
    bump.inputs['Distance'].default_value = 0.003
    nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def make_dark_planter_material():
    mat = bpy.data.materials.get("M_DarkPlanter")
    if mat: return mat
    mat = bpy.data.materials.new("M_DarkPlanter")
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location=(800,0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location=(500,0)
    bsdf.inputs['Base Color'].default_value = (0.06, 0.06, 0.07, 1.0)  # near-black
    bsdf.inputs['Roughness'].default_value = 0.70
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def add_foreground_planter(plan, cabin):
    """Decorative planter pot(s) in foreground with plants — color/scale accent.

    Supports `planters` array for multiple positions, else single planter.
    """
    remove_collection_if_exists("Foreground_Planter")
    coll = bpy.data.collections.new("Foreground_Planter")
    bpy.context.scene.collection.children.link(coll)

    door = cabin["door_pos"]
    cx = (cabin["bbox_x"][0] + cabin["bbox_x"][1]) / 2
    cy = (cabin["bbox_y"][0] + cabin["bbox_y"][1]) / 2
    dx = door[0] - cx
    dy = door[1] - cy

    # Determine planters list
    if "planters" in plan:
        planters_list = plan["planters"]
    else:
        planters_list = [plan]

    for p_idx, p in enumerate(planters_list):
        planter_style = p.get("style", "dark")
        plant_type = p.get("plant", "hortensia")
        radius = p.get("radius", 0.30)
        height = p.get("height", 0.45)
        position = p.get("position", None)

        if position:
            pos = position
        else:
            # Default placement (left of cabin or right alternating)
            if abs(dy) > abs(dx):
                sign_y = 1 if dy > 0 else -1
                side_x = cabin["bbox_x"][1] + 1.5 if p_idx % 2 == 0 else cabin["bbox_x"][0] - 1.5
                pos = (side_x, cy + sign_y * 0.5, 0)
            else:
                sign_x = 1 if dx > 0 else -1
                side_y = cabin["bbox_y"][1] + 1.5 if p_idx % 2 == 0 else cabin["bbox_y"][0] - 1.5
                pos = (cx + sign_x * 0.5, side_y, 0)

        _add_single_planter(coll, pos, radius, height, planter_style, plant_type, p_idx)


def _add_single_planter(coll, pos, radius, height, planter_style, plant_type, p_idx):
    """Inner helper: create one planter at given position."""

    # Planter pot (cylinder)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=20, radius=radius, depth=height,
        location=(pos[0], pos[1], height/2 - 0.02))
    pot = bpy.context.active_object
    pot.name = f"Planter_Pot_{p_idx}"
    # Slight taper at bottom (scale top a bit)
    # Skip for simplicity — straight cylinder is fine for "modern" style

    mat_planter = make_dark_planter_material() if planter_style == "dark" else make_terracotta_material()
    pot.data.materials.append(mat_planter)
    coll.objects.link(pot)
    bpy.context.scene.collection.objects.unlink(pot)

    # Plant on top
    if plant_type == "lavender":
        # Use SOLID PURPLE material for visibility (not subtle voronoi)
        plant_mat = bpy.data.materials.get("M_FlowerPurpleSolid")
        if not plant_mat:
            plant_mat = bpy.data.materials.new("M_FlowerPurpleSolid")
            plant_mat.use_nodes = True
            pnt = plant_mat.node_tree
            for n in list(pnt.nodes): pnt.nodes.remove(n)
            p_out = pnt.nodes.new('ShaderNodeOutputMaterial'); p_out.location=(800,0)
            p_bsdf = pnt.nodes.new('ShaderNodeBsdfPrincipled'); p_bsdf.location=(500,0)
            p_noise = pnt.nodes.new('ShaderNodeTexNoise'); p_noise.location=(-200,0)
            p_noise.inputs['Scale'].default_value = 15.0
            p_ramp = pnt.nodes.new('ShaderNodeValToRGB'); p_ramp.location=(100,0)
            p_ramp.color_ramp.elements[0].color = (0.32, 0.16, 0.45, 1.0)  # deep purple
            p_ramp.color_ramp.elements[1].position = 0.8
            p_ramp.color_ramp.elements[1].color = (0.55, 0.32, 0.78, 1.0)  # bright purple
            pnt.links.new(p_noise.outputs['Fac'], p_ramp.inputs['Fac'])
            pnt.links.new(p_ramp.outputs['Color'], p_bsdf.inputs['Base Color'])
            p_bsdf.inputs['Roughness'].default_value = 0.95
            pnt.links.new(p_bsdf.outputs['BSDF'], p_out.inputs['Surface'])
        plant_radius = radius * 0.95
        plant_height = 0.55
    else:  # hortensia
        # Solid white/pink material for visibility
        plant_mat = bpy.data.materials.get("M_FlowerWhiteSolid")
        if not plant_mat:
            plant_mat = bpy.data.materials.new("M_FlowerWhiteSolid")
            plant_mat.use_nodes = True
            pnt = plant_mat.node_tree
            for n in list(pnt.nodes): pnt.nodes.remove(n)
            p_out = pnt.nodes.new('ShaderNodeOutputMaterial'); p_out.location=(800,0)
            p_bsdf = pnt.nodes.new('ShaderNodeBsdfPrincipled'); p_bsdf.location=(500,0)
            p_noise = pnt.nodes.new('ShaderNodeTexNoise'); p_noise.location=(-200,0)
            p_noise.inputs['Scale'].default_value = 15.0
            p_ramp = pnt.nodes.new('ShaderNodeValToRGB'); p_ramp.location=(100,0)
            p_ramp.color_ramp.elements[0].color = (0.78, 0.58, 0.62, 1.0)  # rose
            p_ramp.color_ramp.elements[1].position = 0.6
            p_ramp.color_ramp.elements[1].color = (0.92, 0.85, 0.82, 1.0)  # white
            pnt.links.new(p_noise.outputs['Fac'], p_ramp.inputs['Fac'])
            pnt.links.new(p_ramp.outputs['Color'], p_bsdf.inputs['Base Color'])
            p_bsdf.inputs['Roughness'].default_value = 0.92
            pnt.links.new(p_bsdf.outputs['BSDF'], p_out.inputs['Surface'])
        plant_radius = radius * 1.2
        plant_height = 0.55

    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=3, radius=plant_radius,
        location=(pos[0], pos[1], height + plant_height/2 - 0.05))
    plant = bpy.context.active_object
    plant.name = f"Planter_Plant_{p_idx}"
    plant.scale = (1.0, 1.0, plant_height / (2 * plant_radius))
    bpy.ops.object.transform_apply(scale=True)
    # Noise displacement (stronger for less ball-like, more organic)
    tex = bpy.data.textures.new(f"T_PlanterPlant_{p_idx}", 'CLOUDS')
    tex.noise_scale = 0.25
    disp = plant.modifiers.new("Displace", 'DISPLACE')
    disp.texture = tex
    disp.strength = plant_radius * 0.55
    plant.data.materials.append(plant_mat)
    bpy.ops.object.shade_smooth()
    coll.objects.link(plant)
    bpy.context.scene.collection.objects.unlink(plant)

    log(f"Planter {p_idx}: {planter_style} pot with {plant_type} at {pos[:2]}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    argv = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    if not argv:
        print("Usage: blender --background <scene>.blend --python extend_scene.py -- <extension>.json")
        return

    plan_path = argv[0]
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    log(f"Loaded extension plan: {plan.get('name', '?')}")

    cabin = get_cabin_info()
    if not cabin:
        log("No cabin info", "ERROR")
        return

    extensions = plan.get("extensions", {})

    if extensions.get("boxwoods_at_door", {}).get("enabled", False):
        add_boxwoods_at_door(extensions["boxwoods_at_door"], cabin)

    if extensions.get("grass_scatter", {}).get("enabled", False):
        add_grass_scatter(extensions["grass_scatter"], cabin)

    if extensions.get("schutting", {}).get("enabled", False):
        add_schutting(extensions["schutting"], cabin)

    if extensions.get("plant_border", {}).get("enabled", False):
        add_plant_border(extensions["plant_border"], cabin)

    if extensions.get("birch_backdrop", {}).get("enabled", False):
        add_birch_backdrop(extensions["birch_backdrop"], cabin)

    if extensions.get("stepping_path", {}).get("enabled", False):
        add_stepping_path(extensions["stepping_path"], cabin)

    if extensions.get("varied_boxwoods", {}).get("enabled", False):
        add_varied_boxwoods(extensions["varied_boxwoods"], cabin)

    if extensions.get("foreground_planter", {}).get("enabled", False):
        add_foreground_planter(extensions["foreground_planter"], cabin)

    if extensions.get("front_terrace", {}).get("enabled", False):
        add_front_terrace(extensions["front_terrace"], cabin)

    # Save
    out_blend = plan.get("output_blend")
    if out_blend:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(out_blend))
        log(f"Saved to {out_blend}")
    else:
        bpy.ops.wm.save_mainfile()

    # Optional re-render
    if plan.get("render_now", False):
        render_path = plan.get("output_render")
        if render_path:
            bpy.context.scene.render.filepath = os.path.abspath(render_path)
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            log("Re-rendering...")
            bpy.ops.render.render(write_still=True)
            log(f"Render complete: {render_path}")


if __name__ == "__main__":
    main()
