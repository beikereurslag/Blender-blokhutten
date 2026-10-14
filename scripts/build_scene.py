"""YAML-driven scene builder for showroom garden + cabin scenes.

Stable, reproducible, no MCP-state issues. Run via:

    blender --background pilots/base/Lavendel-400x300.blend --python scripts/build_scene.py -- plan.yaml

Plan YAML format: see PLAN_TEMPLATE.md for the structure.
"""
import bpy
import os
import sys
import math
import json
import random
from mathutils import Vector


# =============================================================================
# UTILITIES
# =============================================================================

def log(msg, level="INFO"):
    print(f"[{level}] {msg}")


def safe_pixel_load_all_images():
    """Force lazy-loaded images into memory."""
    for img in bpy.data.images:
        if img.name in ("Render Result", "Viewer Node"):
            continue
        try:
            _ = img.pixels[0]
        except Exception:
            pass


def remap_broken_image_paths():
    """Fix Polyhaven .jpg→.png filepath mismatches."""
    fixed = 0
    for img in bpy.data.images:
        if img.name in ("Render Result", "Viewer Node"):
            continue
        abspath = bpy.path.abspath(img.filepath)
        if not os.path.exists(abspath):
            base, ext = os.path.splitext(abspath)
            for try_ext in ['.png', '.jpg', '.exr', '.hdr']:
                alt = base + try_ext
                if os.path.exists(alt):
                    img.filepath = alt
                    try:
                        img.reload()
                        fixed += 1
                    except: pass
                    break
    return fixed


def scale_heavy_textures(max_size=2048):
    """Downscale large textures to fit VRAM budget."""
    scaled = 0
    for img in bpy.data.images:
        if img.name in ("Render Result", "Viewer Node"):
            continue
        try:
            _ = img.pixels[0]  # trigger load
            if img.has_data and (img.size[0] > max_size or img.size[1] > max_size):
                img.scale(max_size, max_size)
                scaled += 1
        except Exception as e:
            log(f"scale fail on {img.name}: {e}", "WARN")
    return scaled


# =============================================================================
# CABIN ORIENTATION
# =============================================================================

def get_cabin_info():
    """Return cabin bbox + door position for currently-loaded file."""
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

    if not all_xs:
        return None

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
        "center": [(min(all_xs)+max(all_xs))/2, (min(all_ys)+max(all_ys))/2, (min(all_zs)+max(all_zs))/2],
        "door_pos": door_pos,
    }


# =============================================================================
# SCENE BUILDERS
# =============================================================================

def setup_render_settings(plan):
    """Apply render settings from plan."""
    scene = bpy.context.scene
    rs = plan.get("render", {})

    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    scene.render.resolution_x = rs.get("width", 1920)
    scene.render.resolution_y = rs.get("height", 1080)
    scene.cycles.samples = rs.get("samples", 128)
    scene.cycles.adaptive_threshold = rs.get("noise_threshold", 0.005)
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'
    scene.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
    scene.cycles.max_bounces = 6
    scene.cycles.texture_limit_render = rs.get("texture_limit", '1024')
    scene.cycles.texture_limit = '512'
    scene.render.use_persistent_data = False
    scene.view_settings.view_transform = rs.get("view_transform", 'AgX')
    scene.view_settings.look = rs.get("look", 'AgX - Punchy')
    scene.view_settings.exposure = rs.get("exposure", 0.0)
    scene.render.use_simplify = True
    scene.render.simplify_subdivision = 1
    scene.render.simplify_subdivision_render = 6


def setup_world_hdri(hdri_path, rotation_z_deg, strength=1.0):
    """Set up world HDRI."""
    scene = bpy.context.scene
    world = scene.world
    if world is None:
        world = bpy.data.worlds.new("World")
        scene.world = world
    world.use_nodes = True
    wt = world.node_tree
    for n in list(wt.nodes):
        wt.nodes.remove(n)
    w_out = wt.nodes.new('ShaderNodeOutputWorld'); w_out.location=(400,0)
    w_bg = wt.nodes.new('ShaderNodeBackground'); w_bg.location=(200,0)
    w_env = wt.nodes.new('ShaderNodeTexEnvironment'); w_env.location=(-200,0)
    w_env.image = bpy.data.images.load(hdri_path, check_existing=True)
    w_map = wt.nodes.new('ShaderNodeMapping'); w_map.location=(-500,0)
    w_map.inputs['Rotation'].default_value[2] = math.radians(rotation_z_deg)
    w_coord = wt.nodes.new('ShaderNodeTexCoord'); w_coord.location=(-800,0)
    wt.links.new(w_coord.outputs['Generated'], w_map.inputs['Vector'])
    wt.links.new(w_map.outputs['Vector'], w_env.inputs['Vector'])
    wt.links.new(w_env.outputs['Color'], w_bg.inputs['Color'])
    w_bg.inputs['Strength'].default_value = strength
    wt.links.new(w_bg.outputs['Background'], w_out.inputs['Surface'])


def setup_sun(rotation_alt_deg, rotation_az_deg, energy=4.5, temperature=4500, angle_deg=1.0):
    """Add sun light."""
    sun = bpy.data.objects.get("Sun_Scene")
    if sun is None:
        bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
        sun = bpy.context.active_object
        sun.name = "Sun_Scene"
    sun.data.energy = energy
    sun.data.angle = math.radians(angle_deg)

    # Kelvin → RGB (Tannenbaum)
    t = temperature / 100.0
    if t <= 66:
        r, g, b = 255, 99.4708 * math.log(t) - 161.1196 if t > 0 else 0, 0 if t <= 19 else 138.5177 * math.log(t-10) - 305.0448
    else:
        r = 329.6987 * (t-60)**-0.1332
        g = 288.1222 * (t-60)**-0.0755
        b = 255
    sun.data.color = tuple(max(0, min(255, c))/255.0 for c in (r, g, b))

    sun.rotation_euler = (math.radians(90 - rotation_alt_deg), 0, math.radians(rotation_az_deg))
    return sun


def setup_camera(position, target, lens=35, f_stop=5.6, shift_y=0.05):
    """Position camera with track-to target."""
    cam = bpy.data.objects.get("camera") or bpy.data.objects.get("Camera_Scene")
    if cam is None:
        bpy.ops.object.camera_add(location=position)
        cam = bpy.context.active_object
        cam.name = "Camera_Scene"
    cam.location = position
    cam.rotation_euler = (0, 0, 0)
    cam.data.lens = lens
    cam.data.sensor_width = 36
    cam.data.shift_y = shift_y
    cam.data.dof.use_dof = True
    cam.data.dof.aperture_fstop = f_stop

    target_obj = bpy.data.objects.get("Cam_Target")
    if target_obj is None:
        target_obj = bpy.data.objects.new("Cam_Target", None)
        target_obj.empty_display_type = 'PLAIN_AXES'
        bpy.context.scene.collection.objects.link(target_obj)
    target_obj.location = target

    # Replace any existing constraint
    for c in list(cam.constraints):
        cam.constraints.remove(c)
    tc = cam.constraints.new('TRACK_TO')
    tc.target = target_obj
    tc.track_axis = 'TRACK_NEGATIVE_Z'
    tc.up_axis = 'UP_Y'

    # Auto focus_distance = camera-to-target
    cam.data.dof.focus_distance = (Vector(position) - Vector(target)).length

    bpy.context.scene.camera = cam
    return cam


def add_ground_plane(size=30, lawn_material=None):
    """Add ground plane with lawn material."""
    # Remove old ground
    for o in list(bpy.data.objects):
        if o.name in ("Ground", "Ground_Plane"):
            bpy.data.objects.remove(o, do_unlink=True)

    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
    ground = bpy.context.active_object
    ground.name = "Ground_Plane"
    if lawn_material is None:
        lawn_material = make_lawn_material()
    ground.data.materials.append(lawn_material)
    return ground


def make_lawn_material():
    """Procedural showroom-clean lawn."""
    mat = bpy.data.materials.get("M_Lawn")
    if mat is None:
        mat = bpy.data.materials.new("M_Lawn")
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location=(600,0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location=(400,0)
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location=(-600,0)
    noise = nt.nodes.new('ShaderNodeTexNoise'); noise.location=(-400,0)
    noise.inputs['Scale'].default_value = 0.8
    noise.inputs['Detail'].default_value = 2.0
    nt.links.new(tc.outputs['Generated'], noise.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location=(-150,0)
    ramp.color_ramp.elements[0].position = 0.4
    ramp.color_ramp.elements[0].color = (0.14, 0.28, 0.07, 1.0)
    ramp.color_ramp.elements[1].position = 0.6
    ramp.color_ramp.elements[1].color = (0.19, 0.34, 0.10, 1.0)
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.95
    bsdf.inputs['Subsurface Weight'].default_value = 0.06
    bsdf.inputs['Subsurface Radius'].default_value = (0.03, 0.015, 0.005)
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


# =============================================================================
# YAML PLAN LOADER (simplified — no actual YAML lib, JSON-style)
# =============================================================================

def load_plan(path):
    """Load plan from JSON or simple YAML-like file."""
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    if path.endswith('.json'):
        return json.loads(text)
    else:
        # Try yaml if available
        try:
            import yaml
            return yaml.safe_load(text)
        except ImportError:
            print("PyYAML not available — use .json plans only")
            return None


# =============================================================================
# MAIN
# =============================================================================

def main():
    argv = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    if not argv:
        print("Usage: blender --background <cabin>.blend --python build_scene.py -- <plan.json>")
        return

    plan_path = argv[0]
    plan = load_plan(plan_path)
    if not plan:
        log("Plan load failed", "ERROR")
        return

    log(f"Loaded plan: {plan.get('name', '?')}")

    # Step 0: Fix any broken textures from cabin
    fixed = remap_broken_image_paths()
    if fixed:
        log(f"Remapped {fixed} broken texture paths")
    scaled = scale_heavy_textures(max_size=plan.get("render", {}).get("max_texture_size", 2048))
    if scaled:
        log(f"Scaled {scaled} oversized textures")

    # Step 1: Cabin info
    cabin = get_cabin_info()
    if not cabin:
        log("No cabin in scene — abort", "ERROR")
        return
    log(f"Cabin bbox: x={cabin['bbox_x']}, y={cabin['bbox_y']}")
    log(f"Door at: {cabin['door_pos']}")

    # Step 2: Render settings
    setup_render_settings(plan)
    log("Render settings applied")

    # Step 3: World + Sun
    light_plan = plan.get("lighting", {})
    setup_world_hdri(light_plan["hdri_path"], light_plan.get("hdri_rotation_z", 140),
                     light_plan.get("hdri_strength", 1.0))
    setup_sun(light_plan.get("sun_altitude", 55),
              light_plan.get("sun_azimuth", 140),
              light_plan.get("sun_energy", 4.5),
              light_plan.get("sun_temperature", 4500),
              light_plan.get("sun_angle", 1.0))
    log("HDRI + Sun configured")

    # Step 4: Camera (auto from cabin info if not specified)
    cam_plan = plan.get("camera", {})
    cam_pos = cam_plan.get("position")
    cam_target = cam_plan.get("target") or cabin["center"]

    if not cam_pos:
        # Auto-derive based on door direction (works for +X, -X, +Y, -Y doors)
        door_x = cabin["door_pos"][0]
        door_y = cabin["door_pos"][1]
        center_x = cabin["center"][0]
        center_y = cabin["center"][1]
        dx = door_x - center_x
        dy = door_y - center_y
        max_dim = max(cabin["bbox_x"][1] - cabin["bbox_x"][0],
                      cabin["bbox_y"][1] - cabin["bbox_y"][0])
        dist = max_dim * 1.5 + 3
        if abs(dy) > abs(dx):
            # Door on Y axis
            sign_y = 1 if dy > 0 else -1
            cam_pos = [dist * 0.6, sign_y * dist, 1.7]
        else:
            # Door on X axis
            sign_x = 1 if dx > 0 else -1
            cam_pos = [sign_x * dist, dist * 0.6, 1.7]
        log(f"Auto-derived camera based on door direction (dx={dx:.2f}, dy={dy:.2f})")

    setup_camera(cam_pos, cam_target,
                 lens=cam_plan.get("lens", 35),
                 f_stop=cam_plan.get("f_stop", 5.6),
                 shift_y=cam_plan.get("shift_y", 0.05))
    log(f"Camera at {cam_pos} → target {cam_target}")

    # Step 5: Ground
    add_ground_plane(size=plan.get("ground", {}).get("size", 30))
    log("Ground plane added")

    # Step 6: Save modified blend
    out_blend = plan.get("output_blend", "training/builds/scene.blend")
    out_dir = os.path.dirname(out_blend)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(out_blend))
    log(f"Saved blend to {out_blend}")

    # Step 7: Render
    render_path = plan.get("output_render", "training/renders/scene")
    bpy.context.scene.render.filepath = os.path.abspath(render_path)
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.color_depth = '16'

    if plan.get("render_now", True):
        log("Starting render...")
        bpy.ops.render.render(write_still=True)
        log(f"Render complete: {render_path}")


if __name__ == "__main__":
    main()
