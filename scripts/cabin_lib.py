"""Gedeelde bouw-bibliotheek voor cabin-hero-scenes (bewezen patronen
uit Dahlia Oogsttuin + Zonnebloem Zomeravond, 2026-06-12).

Gebruik in build-scripts:
    import sys; sys.path.insert(0, ROOT + r"\\scripts")
    import cabin_lib as cl
"""
import bpy, math, os, random
from mathutils import Vector

ROOT = r"C:\Users\beike\Documents\Blender-blokhutten"
BWTEX = ROOT + r"\assets\blokhutwinkel-textures\8192"
PHTEX = ROOT + r"\assets\polyhaven\textures"
MODELS = ROOT + r"\assets\polyhaven\models"
HDRI_DIR = ROOT + r"\assets\polyhaven\hdri"
SF = ROOT + r"\assets\sketchfab"
AI3D = ROOT + r"\assets\3daistudio"

import sys
sys.path.insert(0, ROOT + r"\scripts")
import extend_scene_real as esr


# ---------------------------------------------------------------- basis
def scene():
    return bpy.context.scene

def open_base(path, outdir):
    bpy.ops.wm.open_mainfile(filepath=path)
    os.makedirs(outdir, exist_ok=True)

def delete_glb_cameras():
    for o in list(bpy.data.objects):
        if o.type == 'CAMERA':
            bpy.data.objects.remove(o, do_unlink=True)

def wbbox_meshes(meshes):
    pts = [(m.matrix_world @ Vector(c)) for m in meshes for c in m.bound_box]
    if not pts: return None
    return (min(p.x for p in pts), max(p.x for p in pts),
            min(p.y for p in pts), max(p.y for p in pts),
            min(p.z for p in pts), max(p.z for p in pts))


# ---------------------------------------------------------------- materialen
def _img(folder, fn):
    i = bpy.data.images.load(os.path.join(folder, fn), check_existing=True)
    try: i.reload()
    except Exception: pass
    return i

def build_clean_wood(matname, fn, scale=0.6, rough=0.6, desat=0.0, valmul=1.0,
                     bump=0.20, hue=0.5):
    """Producttexture -> Principled met BOX/Object-mapping (bewezen patroon)."""
    mat = bpy.data.materials.get(matname) or bpy.data.materials.new(matname)
    mat.use_nodes = True; nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (700, 0)
    b = nt.nodes.new('ShaderNodeBsdfPrincipled'); b.location = (400, 0)
    b.inputs['Roughness'].default_value = rough
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location = (-800, 0)
    mp = nt.nodes.new('ShaderNodeMapping'); mp.location = (-600, 0)
    mp.inputs['Scale'].default_value = (scale, scale, scale)
    tx = nt.nodes.new('ShaderNodeTexImage'); tx.location = (-380, 0)
    tx.image = _img(BWTEX, fn)
    tx.projection = 'BOX'; tx.projection_blend = 0.3
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    nt.links.new(mp.outputs['Vector'], tx.inputs['Vector'])
    col = tx.outputs['Color']
    if desat > 0 or valmul != 1.0 or hue != 0.5:
        hs = nt.nodes.new('ShaderNodeHueSaturation'); hs.location = (-120, 160)
        hs.inputs['Hue'].default_value = hue
        hs.inputs['Saturation'].default_value = max(0.0, 1.0 - desat)
        hs.inputs['Value'].default_value = valmul
        nt.links.new(col, hs.inputs['Color']); col = hs.outputs['Color']
    nt.links.new(col, b.inputs['Base Color'])
    bm = nt.nodes.new('ShaderNodeBump'); bm.location = (150, -250)
    bm.inputs['Strength'].default_value = bump
    nt.links.new(tx.outputs['Color'], bm.inputs['Height'])
    nt.links.new(bm.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return mat

def fix_glass_chrome():
    def bsdf_of(mat):
        return next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    mat = bpy.data.materials.get('glass')
    b = bsdf_of(mat) if mat else None
    if b:
        b.inputs['Roughness'].default_value = 0.05
        for s in ('Transmission Weight', 'Transmission'):
            if s in b.inputs:
                b.inputs[s].default_value = 1.0; break
        if 'IOR' in b.inputs: b.inputs['IOR'].default_value = 1.45
    mat = bpy.data.materials.get('chrome')
    b = bsdf_of(mat) if mat else None
    if b:
        b.inputs['Metallic'].default_value = 1.0
        b.inputs['Roughness'].default_value = 0.25
        b.inputs['Base Color'].default_value = (0.8, 0.8, 0.82, 1.0)

def pbr_from_folder(name, folder, scale=1.0, rough_fallback=0.8, hue=0.5, sat=1.0, val=1.0):
    """Principled uit polyhaven/megascans texture-map (diff/rough/normal), BOX-mapping."""
    mat = bpy.data.materials.get(name)
    if mat: return mat
    mat = bpy.data.materials.new(name); mat.use_nodes = True
    nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (800, 0)
    b = nt.nodes.new('ShaderNodeBsdfPrincipled'); b.location = (500, 0)
    b.inputs['Roughness'].default_value = rough_fallback
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (scale, scale, scale)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    files = os.listdir(folder)
    def find(*keys):
        for f in files:
            fl = f.lower()
            if any(k in fl for k in keys) and fl.endswith(('.png', '.jpg', '.jpeg')):
                return os.path.join(folder, f)
        return None
    fp = find('diff', 'col', '_b.')
    if fp:
        tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = bpy.data.images.load(fp, check_existing=True)
        tx.projection = 'BOX'; tx.projection_blend = 0.3
        nt.links.new(mp.outputs['Vector'], tx.inputs['Vector'])
        col = tx.outputs['Color']
        if hue != 0.5 or sat != 1.0 or val != 1.0:
            hs = nt.nodes.new('ShaderNodeHueSaturation')
            hs.inputs['Hue'].default_value = hue; hs.inputs['Saturation'].default_value = sat
            hs.inputs['Value'].default_value = val
            nt.links.new(col, hs.inputs['Color']); col = hs.outputs['Color']
        nt.links.new(col, b.inputs['Base Color'])
    rp = find('rough')
    if rp:
        rx = nt.nodes.new('ShaderNodeTexImage'); rx.image = bpy.data.images.load(rp, check_existing=True)
        rx.image.colorspace_settings.name = 'Non-Color'
        rx.projection = 'BOX'; rx.projection_blend = 0.3
        nt.links.new(mp.outputs['Vector'], rx.inputs['Vector'])
        nt.links.new(rx.outputs['Color'], b.inputs['Roughness'])
    np_ = find('nor_gl', 'normal', '_n.')
    if np_:
        nx = nt.nodes.new('ShaderNodeTexImage'); nx.image = bpy.data.images.load(np_, check_existing=True)
        nx.image.colorspace_settings.name = 'Non-Color'
        nx.projection = 'BOX'; nx.projection_blend = 0.3
        nm = nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = 0.8
        nt.links.new(mp.outputs['Vector'], nx.inputs['Vector'])
        nt.links.new(nx.outputs['Color'], nm.inputs['Color'])
        nt.links.new(nm.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return mat

def uv_board_textures(prefixes=("basetexture-firstLayer",), only_box=True):
    """Blokhut-cladding: de GLB-import zet de plank-textuur op BOX-projectie /
    Object-coords, waardoor de potdeksel-nerf 90 graden verkeerd loopt (verticaal
    i.p.v. met de plank mee). Zet 'm op de mesh-UVMap (FLAT) zodat de planken
    kloppen. Returnt het aantal aangepaste materialen."""
    n = 0
    for m in bpy.data.materials:
        if not m.use_nodes:
            continue
        if prefixes and not any(m.name.startswith(p) for p in prefixes):
            continue
        nt = m.node_tree
        teximgs = [x for x in nt.nodes if x.type == 'TEX_IMAGE']
        if only_box and not any(t.projection == 'BOX' for t in teximgs):
            continue
        coord = next((x for x in nt.nodes if x.type == 'TEX_COORD'), None)
        mapn = next((x for x in nt.nodes if x.type == 'MAPPING'), None)
        for t in teximgs:
            if t.projection == 'BOX':
                t.projection = 'FLAT'
        if coord and mapn:
            for l in list(mapn.inputs['Vector'].links):
                nt.links.remove(l)
            nt.links.new(coord.outputs['UV'], mapn.inputs['Vector'])
        elif coord:
            for t in teximgs:
                for l in list(t.inputs['Vector'].links):
                    nt.links.remove(l)
                nt.links.new(coord.outputs['UV'], t.inputs['Vector'])
        n += 1
    return n

def simple_mat(name, color, rough=0.6, metallic=0.0, emission=None, emission_strength=0.0):
    mat = bpy.data.materials.get(name)
    if mat: return mat
    mat = bpy.data.materials.new(name); mat.use_nodes = True
    nt = mat.node_tree
    if emission is not None:
        nt.nodes.clear()
        out = nt.nodes.new('ShaderNodeOutputMaterial')
        em = nt.nodes.new('ShaderNodeEmission')
        em.inputs['Color'].default_value = (*emission, 1.0)
        em.inputs['Strength'].default_value = emission_strength
        nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
        return mat
    b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    b.inputs['Base Color'].default_value = (*color, 1.0)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metallic
    return mat


# ---------------------------------------------------------------- omgeving
def add_ground(size=30, name="Ground_Grass", mat=None):
    gmat = mat or esr.mat_grass_rock()
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
    g = bpy.context.active_object; g.name = name
    g.data.materials.append(gmat)
    return g

def setup_hdri(hdri_file, strength=0.9, rot_z_deg=235):
    world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    scene().world = world; world.use_nodes = True
    wn = world.node_tree; wn.nodes.clear()
    wo = wn.nodes.new('ShaderNodeOutputWorld')
    bg = wn.nodes.new('ShaderNodeBackground'); bg.inputs['Strength'].default_value = strength
    env = wn.nodes.new('ShaderNodeTexEnvironment')
    env.image = bpy.data.images.load(os.path.join(HDRI_DIR, hdri_file), check_existing=True)
    mpw = wn.nodes.new('ShaderNodeMapping'); tcw = wn.nodes.new('ShaderNodeTexCoord')
    mpw.inputs['Rotation'].default_value = (0, 0, math.radians(rot_z_deg))
    wn.links.new(tcw.outputs['Generated'], mpw.inputs['Vector'])
    wn.links.new(mpw.outputs['Vector'], env.inputs['Vector'])
    wn.links.new(env.outputs['Color'], bg.inputs['Color'])
    wn.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    return env

def add_sun(energy=3.0, color=(1.0, 0.90, 0.78), elev_deg=17, azim_deg=35, angle_deg=1.5):
    sun = bpy.data.lights.new("Sun", 'SUN')
    suno = bpy.data.objects.new("Sun", sun)
    scene().collection.objects.link(suno)
    sun.energy = energy; sun.color = color; sun.angle = math.radians(angle_deg)
    suno.rotation_euler = (math.radians(90 - elev_deg), 0, math.radians(azim_deg))
    return suno

def add_camera(loc, target, lens=35, shift_y=-0.045, name="HeroCam"):
    cam = bpy.data.cameras.new(name); cam.lens = lens
    cam.clip_start = 0.02; cam.clip_end = 2000.0
    camo = bpy.data.objects.new(name, cam)
    scene().collection.objects.link(camo)
    camo.location = loc
    d = Vector((target[0], target[1], loc[2])) - Vector(loc)   # level: geen kantelende verticalen
    camo.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    cam.shift_y = shift_y
    scene().camera = camo
    return camo

def point_light(name, loc, power, color=(1.0, 0.55, 0.25), size=0.06):
    li = bpy.data.lights.new(name, 'POINT'); li.energy = power; li.color = color
    li.shadow_soft_size = size
    o = bpy.data.objects.new(name, li); scene().collection.objects.link(o)
    o.location = loc
    return o

def area_light(name, loc, power, color=(1.0, 0.72, 0.45), size=1.4, rot=(0, 0, 0)):
    ar = bpy.data.lights.new(name, 'AREA'); ar.energy = power; ar.color = color; ar.size = size
    o = bpy.data.objects.new(name, ar); scene().collection.objects.link(o)
    o.location = loc; o.rotation_euler = rot
    return o

def render_setup(samples=64, res=(960, 540), exposure=0.3, look='Medium High Contrast',
                 transform='Filmic'):
    s = scene()
    s.render.engine = 'CYCLES'
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        _gpu = 'CUDA'
        for _t in ('OPTIX', 'CUDA'):
            prefs.compute_device_type = _t; prefs.get_devices()
            if any(d.type == _t for d in prefs.devices): _gpu = _t; break
        for dv in prefs.devices: dv.use = (dv.type == _gpu)
        print("[gpu]", _gpu)
        s.cycles.device = 'GPU'
    except Exception as e:
        print(e)
    s.cycles.samples = samples
    s.cycles.use_denoising = True
    s.cycles.denoiser = 'OPENIMAGEDENOISE'
    s.cycles.texture_limit_render = '2048'
    s.render.use_persistent_data = False
    s.view_settings.view_transform = transform
    s.view_settings.look = look
    s.view_settings.exposure = exposure
    s.render.resolution_x, s.render.resolution_y = res

def save_and_diag(blend, png, res=(1280, 720), samples=64):
    esr.remap_broken_image_paths()
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    s = scene()
    s.render.resolution_x, s.render.resolution_y = res
    s.cycles.samples = samples
    s.render.filepath = png
    bpy.ops.render.render(write_still=True)


# ---------------------------------------------------------------- geometrie
def add_box(name, xmin, xmax, ymin, ymax, ztop, zbot=0.0, mat=None):
    cx = (xmin+xmax)/2; cy = (ymin+ymax)/2; cz = (zbot+ztop)/2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, cz))
    o = bpy.context.active_object; o.name = name
    o.scale = (xmax-xmin, ymax-ymin, ztop-zbot)
    bpy.ops.object.transform_apply(scale=True)
    if mat: o.data.materials.append(mat)
    return o

def ribbon_path(name, ctrl_xy, width=1.04, z=0.045, mat=None, clamp_x_min=None, clamp_below_y=4.0):
    """Gebogen pad: Catmull-Rom door ctrl-punten -> platte ribbon-mesh."""
    ctrl = [Vector(c) for c in ctrl_xy]
    def catmull(p0, p1, p2, p3, t):
        t2 = t*t; t3 = t2*t
        return 0.5 * ((2*p1) + (-p0 + p2)*t + (2*p0 - 5*p1 + 4*p2 - p3)*t2 + (-p0 + 3*p1 - 3*p2 + p3)*t3)
    samples = []
    for i in range(1, len(ctrl) - 2):
        for s in range(12):
            samples.append(catmull(ctrl[i-1], ctrl[i], ctrl[i+1], ctrl[i+2], s/12.0))
    samples.append(ctrl[-2])
    W = width / 2
    verts = []; faces = []
    for i, p in enumerate(samples):
        if i == 0: tang = (samples[1] - samples[0]).normalized()
        elif i == len(samples) - 1: tang = (samples[-1] - samples[-2]).normalized()
        else: tang = (samples[i+1] - samples[i-1]).normalized()
        nrm = Vector((-tang.y, tang.x))
        l = p + nrm * W; r = p - nrm * W
        if clamp_x_min is not None and p.y < clamp_below_y:
            if l.x < clamp_x_min: l.x = clamp_x_min
            if r.x < clamp_x_min: r.x = clamp_x_min
        verts.append((l.x, l.y, z)); verts.append((r.x, r.y, z))
        if i > 0:
            a = 2*i; faces.append((a-2, a-1, a+1, a))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces); me.update()
    ob = bpy.data.objects.new(name, me)
    scene().collection.objects.link(ob)
    if mat: ob.data.materials.append(mat)
    return ob, samples


# ---------------------------------------------------------------- heg (GN, dicht)
def build_hedge_system(density=700, sprig_h=0.25, hue=0.54, sat=1.40, val=0.52):
    """Sprig uit shrub_03 + HedgeGN nodegroup. Returnt add_hedge(name, cm-box)."""
    def dims(o):
        cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
        return [max(c[i] for c in cs) - min(c[i] for c in cs) for i in range(3)]
    with bpy.data.libraries.load(os.path.join(MODELS, "shrub_03_2k.blend"), link=False) as (src, dst):
        dst.objects = list(src.objects)
    subs = [o for o in dst.objects if o and o.type == 'MESH']
    for o in subs: scene().collection.objects.link(o)
    bpy.context.view_layer.update()
    subs_sorted = sorted(subs, key=lambda o: len(o.data.vertices))
    sprig = subs_sorted[len(subs_sorted)//2]
    for o in subs:
        if o is not sprig: bpy.data.objects.remove(o, do_unlink=True)
    sprig.name = "HedgeSprig"
    bpy.ops.object.select_all(action='DESELECT')
    sprig.select_set(True); bpy.context.view_layer.objects.active = sprig
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    sh = max(dims(sprig)[2], 0.01); base_scale = sprig_h / sh
    sprig.location = (25, 25, 0); sprig.hide_render = True; sprig.hide_viewport = True
    esr.remap_broken_image_paths()
    for m in sprig.data.materials:
        if not m: continue
        m.blend_method = 'HASHED'
        nt = m.node_tree
        diff = next((n for n in nt.nodes if n.type == 'TEX_IMAGE' and n.image
                     and 'diff' in n.image.name.lower()), None)
        if diff and diff.outputs['Color'].is_linked:
            targets = [l.to_socket for l in diff.outputs['Color'].links]
            hsv = nt.nodes.new('ShaderNodeHueSaturation')
            hsv.inputs['Hue'].default_value = hue
            hsv.inputs['Saturation'].default_value = sat
            hsv.inputs['Value'].default_value = val
            nt.links.new(diff.outputs['Color'], hsv.inputs['Color'])
            for ts in targets: nt.links.new(hsv.outputs['Color'], ts)
    core = bpy.data.materials.new("MAT_HedgeCore"); core.use_nodes = True
    cb = next(n for n in core.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    cb.inputs['Base Color'].default_value = (0.02, 0.05, 0.015, 1.0)
    cb.inputs['Roughness'].default_value = 1.0
    ng = bpy.data.node_groups.new("HedgeGN", 'GeometryNodeTree')
    ng.interface.new_socket("Geometry", in_out='INPUT',  socket_type='NodeSocketGeometry')
    ng.interface.new_socket("Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    nd = ng.nodes
    gi = nd.new("NodeGroupInput"); go = nd.new("NodeGroupOutput")
    dp = nd.new("GeometryNodeDistributePointsOnFaces")
    dp.distribute_method = 'RANDOM'; dp.inputs["Density"].default_value = float(density)
    oi = nd.new("GeometryNodeObjectInfo"); oi.transform_space = 'ORIGINAL'
    oi.inputs["Object"].default_value = sprig; oi.inputs["As Instance"].default_value = True
    rv = nd.new("FunctionNodeRandomValue"); rv.data_type = 'FLOAT'
    rv.inputs[2].default_value = base_scale*0.75; rv.inputs[3].default_value = base_scale*1.3
    iop = nd.new("GeometryNodeInstanceOnPoints")
    rvz = nd.new("FunctionNodeRandomValue"); rvz.data_type = 'FLOAT'
    rvz.inputs[2].default_value = 0.0; rvz.inputs[3].default_value = 6.283
    cz = nd.new("ShaderNodeCombineXYZ")
    ri = nd.new("GeometryNodeRotateInstances")
    ng.links.new(gi.outputs[0], dp.inputs["Mesh"])
    ng.links.new(dp.outputs["Points"], iop.inputs["Points"])
    ng.links.new(dp.outputs["Rotation"], iop.inputs["Rotation"])
    ng.links.new(oi.outputs["Geometry"], iop.inputs["Instance"])
    ng.links.new(rv.outputs[1], iop.inputs["Scale"])
    ng.links.new(rvz.outputs[1], cz.inputs["Z"])
    ng.links.new(iop.outputs["Instances"], ri.inputs["Instances"])
    ng.links.new(cz.outputs["Vector"], ri.inputs["Rotation"])
    ng.links.new(ri.outputs["Instances"], go.inputs[0])

    def add_hedge(name, xmin, xmax, ymin, ymax, ztop):
        cx = (xmin+xmax)/200; cy = (ymin+ymax)/200; cz_ = ztop/200
        bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, cz_))
        o = bpy.context.active_object; o.name = name
        o.scale = ((xmax-xmin)/100, (ymax-ymin)/100, ztop/100)
        bpy.ops.object.transform_apply(scale=True)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.subdivide(number_cuts=16)
        bpy.ops.object.mode_set(mode='OBJECT')
        bev = o.modifiers.new("Bevel", 'BEVEL'); bev.width = 0.10; bev.segments = 3
        bpy.ops.object.shade_smooth()
        o.data.materials.append(core)
        m = o.modifiers.new("HedgeScatter", 'NODES'); m.node_group = ng
        return o
    return add_hedge, ng, sprig


# ---------------------------------------------------------------- bomen
def pine_rings(ring_spots, rnd=None):
    """ring_spots: lijst (x_cm, y_cm, h_cm). Let op: dennen achter de cabin in
    zone x +-4m moeten <=550cm hoog of >=900cm naar achteren (kroon-over-daklijn-les)."""
    rnd = rnd or random
    pine = bpy.data.collections.get("Asset_Pine") or esr._load_blend_as_collection(
        os.path.join(MODELS, "pine_tree_01_2k.blend"), "Asset_Pine")
    src_h = (esr._get_collection_bbox_height(pine) or 20.0) * 100
    for i, (x, y, h) in enumerate(ring_spots):
        esr._duplicate_collection_at(pine, f"RingPine_{i}", (x/100, y/100, 0),
                                     scale=h/src_h, rotation_z=rnd.uniform(0, 6.28))
    return len(ring_spots)

def default_ring_spots(rnd, back_y=(-780, -620), n_flanks=True,
                       cabin_safe_x=4.0, near_h=(450, 540), far_h=(680, 880)):
    """Standaard 3 ringen + flanken. Ring-1 dennen binnen cabin_safe_x blijven laag."""
    spots = []
    for x in range(-8, 9, 3):
        xx = x*100 + rnd.randint(-60, 60)
        h = rnd.randint(*near_h) if abs(xx) < cabin_safe_x*100 else rnd.randint(520, 680)
        spots.append((xx, rnd.randint(*back_y), h))
    for x in range(-10, 11, 3):
        spots.append((x*100 + rnd.randint(-80, 80), rnd.randint(-1180, -920), rnd.randint(*far_h)))
    for x in range(-12, 13, 4):
        spots.append((x*100 + rnd.randint(-100, 100), rnd.randint(-1750, -1380), rnd.randint(850, 1080)))
    if n_flanks:
        for y in range(-3, 7, 2):
            spots.append((rnd.randint(-1300, -1050), y*100 + rnd.randint(-60, 60), rnd.randint(600, 850)))
        for y in range(-4, 3, 2):
            spots.append((rnd.randint(1000, 1250), y*100 + rnd.randint(-60, 60), rnd.randint(550, 750)))
    return spots


# ---------------------------------------------------------------- props
def _strip_lods(new):
    for o in list(new):
        if any(t in o.name for t in ("LOD1", "LOD2", "LOD3", "LOD_1", "LOD_2", "LOD_3")):
            bpy.data.objects.remove(o, do_unlink=True); new.remove(o)
    return new

def import_gltf_prop(path, target_dim, loc, rot_z=0.0, name="Prop", by_dim='Z'):
    """GLTF importeren, schalen op as-dimensie, gronden op min-z."""
    before = set(bpy.data.objects)
    try:
        bpy.ops.import_scene.gltf(filepath=path)
    except Exception as e:
        print(f"[cabin_lib] gltf import FAILED {path}: {e}"); return None
    new = _strip_lods([o for o in bpy.data.objects if o not in before])
    meshes = [o for o in new if o.type == 'MESH']
    bpy.ops.object.empty_add(location=(0, 0, 0))
    root = bpy.context.active_object; root.name = name + "_root"
    bpy.context.view_layer.update()
    bb = wbbox_meshes(meshes)
    if not bb:
        print(f"[cabin_lib] {name}: no meshes"); return root
    axis = {'X': (0, 1), 'Y': (2, 3), 'Z': (4, 5)}[by_dim]
    dim = bb[axis[1]] - bb[axis[0]]
    minz = bb[4]
    for o in new:
        if o.parent is None and o is not root: o.parent = root
    sc = target_dim / max(dim, 0.001)
    root.scale = (sc,)*3
    root.location = (loc[0], loc[1], -minz*sc + (loc[2] if len(loc) > 2 else 0))
    root.rotation_euler = (0, 0, rot_z)
    bpy.context.view_layer.update()
    return root

def import_obj_prop(path, target_h, loc, rot_z=0.0, name="Prop"):
    """OBJ (3daistudio) importeren, op hoogte schalen, gronden."""
    before = set(bpy.data.objects)
    try:
        bpy.ops.wm.obj_import(filepath=path)
    except Exception as e:
        print(f"[cabin_lib] obj import FAILED {path}: {e}"); return None
    new = [o for o in bpy.data.objects if o not in before]
    meshes = [o for o in new if o.type == 'MESH']
    bpy.ops.object.empty_add(location=(0, 0, 0))
    root = bpy.context.active_object; root.name = name + "_root"
    bpy.context.view_layer.update()
    bb = wbbox_meshes(meshes)
    if not bb: return root
    h = bb[5] - bb[4]
    for o in new:
        if o.parent is None and o is not root: o.parent = root
    sc = target_h / max(h, 0.001)
    root.scale = (sc,)*3
    root.location = (loc[0], loc[1], -bb[4]*sc)
    root.rotation_euler = (0, 0, rot_z)
    bpy.context.view_layer.update()
    return root

def dup_hierarchy(src_root, name, loc, rot_z=None, scale_mul=1.0):
    dup = src_root.copy()
    scene().collection.objects.link(dup)
    stack = [(src_root, dup)]
    while stack:
        s, d = stack.pop()
        for ch in s.children:
            c = ch.copy()
            if ch.data: c.data = ch.data
            c.parent = d
            scene().collection.objects.link(c)
            stack.append((ch, c))
    dup.name = name
    dup.location = (loc[0], loc[1], dup.location.z if len(loc) < 3 else loc[2])
    if rot_z is not None:
        dup.rotation_euler = (dup.rotation_euler[0], dup.rotation_euler[1], rot_z)
    if scale_mul != 1.0:
        dup.scale = [v*scale_mul for v in dup.scale]
    return dup

def ground_root(root):
    """Zet root zo dat min-z van zijn meshes op 0 ligt."""
    bpy.context.view_layer.update()
    ms = [c for c in root.children_recursive if c.type == 'MESH']
    bb = wbbox_meshes(ms)
    if bb: root.location.z -= bb[4]


def auto_upright(root, target_h, ground_z=0.0):
    """GLTF-props importeren regelmatig gekanteld (picknicktafel-les).
    Probeert X/Y-rotaties en kiest de stand met minimale bbox-hoogte
    (= rechtop voor meubels), herschaalt naar target_h en grondt."""
    ms = [c for c in root.children_recursive if c.type == 'MESH']
    if not ms: return
    best = None
    for rx, ry in ((0, 0), (math.pi/2, 0), (-math.pi/2, 0), (math.pi, 0),
                   (0, math.pi/2), (0, -math.pi/2)):
        root.rotation_euler.x = rx; root.rotation_euler.y = ry
        bpy.context.view_layer.update()
        bb = wbbox_meshes(ms)
        if not bb: continue
        h = bb[5] - bb[4]
        w = max(bb[1]-bb[0], bb[3]-bb[2])
        # rechtop = hoogte kleiner dan breedste horizontale maat (meubelheuristiek)
        score = h / max(w, 0.001)
        if best is None or score < best[0]:
            best = (score, rx, ry)
    root.rotation_euler.x = best[1]; root.rotation_euler.y = best[2]
    bpy.context.view_layer.update()
    bb = wbbox_meshes(ms)
    h = bb[5] - bb[4]
    f = target_h / max(h, 0.001)
    root.scale = [v * f for v in root.scale]
    bpy.context.view_layer.update()
    bb = wbbox_meshes(ms)
    root.location.z += ground_z - bb[4]
    bpy.context.view_layer.update()


def keep_one_xy_cluster(root, prefer_largest=True):
    """Asset-packs (vogelbad!) bevatten meerdere varianten naast elkaar:
    cluster meshes op XY en houd er één over; rest wordt verwijderd."""
    bpy.context.view_layer.update()
    ms = [c for c in root.children_recursive if c.type == 'MESH']
    if len(ms) < 2: return
    clusters = {}
    for m in ms:
        t = m.matrix_world.translation
        key = (round(t.x), round(t.y))
        clusters.setdefault(key, []).append(m)
    if len(clusters) < 2:
        # varianten exact gestapeld: houd de grootste mesh
        if prefer_largest and len(ms) > 1:
            keep = max(ms, key=lambda m: len(m.data.vertices))
            for m in ms:
                if m is not keep:
                    bpy.data.objects.remove(m, do_unlink=True)
        return
    def size(objs):
        bb = wbbox_meshes(objs)
        return (bb[1]-bb[0]) * (bb[3]-bb[2]) if bb else 0
    keep_key = max(clusters, key=lambda k: size(clusters[k])) if prefer_largest \
        else min(clusters, key=lambda k: Vector((k[0], k[1])).length)
    for k, objs in clusters.items():
        if k == keep_key: continue
        for m in objs:
            bpy.data.objects.remove(m, do_unlink=True)
    # overgebleven cluster naar root-positie centreren
    bpy.context.view_layer.update()
    ms = [c for c in root.children_recursive if c.type == 'MESH']
    bb = wbbox_meshes(ms)
    if bb:
        cx = (bb[0]+bb[1])/2; cy = (bb[2]+bb[3])/2
        root.location.x += root.location.x - cx
        root.location.y += root.location.y - cy

def load_asset_clusters(blend_name, coll_name, min_h=0.04, skip_mats=("scan_",), max_w=6.0):
    """Cluster-donor fix; filtert scan-/reuzen-meshes (gazania-les!)."""
    coll = esr._load_blend_as_collection(os.path.join(MODELS, blend_name), coll_name)
    # all_objects (niet .objects): sommige blends nesten meshes in sub-collecties
    src_objs = list(coll.all_objects) if hasattr(coll, "all_objects") else list(coll.objects)
    meshes = []
    for o in src_objs:
        if o.type != 'MESH': continue
        mats = {sl.material.name for sl in o.material_slots if sl.material}
        if any(m.startswith(p) for m in mats for p in skip_mats): continue
        meshes.append(o)
    clusters = {}
    for o in meshes:
        key = (round(o.location.x / 2.0), round(o.location.y / 2.0))
        clusters.setdefault(key, []).append(o)
    out = []
    for k, objs in clusters.items():
        bb = wbbox_meshes(objs)
        if not bb: continue
        h = bb[5] - bb[4]
        w = max(bb[1]-bb[0], bb[3]-bb[2])
        if h >= min_h and w < max_w:   # reuzen-check
            out.append((h, objs))
    out.sort(key=lambda t: -t[0])
    return out


def full_tree_donors(blend="pine_tree_01_2k.blend", coll="Asset_Pine", top_frac=0.5):
    """Donors gesorteerd op vert-aantal (= bladdichtheid); houdt de volste helft.
    Voorkomt kale-skelet-varianten in beeld (Camelia/Magnolia-les)."""
    donors = load_asset_clusters(blend, coll, min_h=1.0, max_w=99.0)
    if not donors:
        return []
    def dverts(d): return sum(len(m.data.vertices) for m in d[1])
    donors = sorted(donors, key=dverts, reverse=True)
    keep = max(1, int(len(donors) * top_frac))
    return donors[:keep]


def tree_rings_clustered(spots, rnd=None, blend="pine_tree_01_2k.blend",
                         coll="Asset_Pine", prefix="TreeRing", full_only=True):
    """Bomenringen via cluster-donors — de VEILIGE methode.
    NOOIT _duplicate_collection_at op een boom-blend: dat kopieert ALLE 54
    variant-onderdelen verspreid rond het doel (losse stammen tegen de gevel!).
    full_only=True gebruikt alleen volle (bladrijke) donors -> geen kale skeletten.
    spots: (x_cm, y_cm, h_cm)."""
    rnd = rnd or random
    donors = full_tree_donors(blend, coll) if full_only else \
        load_asset_clusters(blend, coll, min_h=1.0, max_w=99.0)
    if not donors:
        print("[cabin_lib] GEEN tree-donors"); return 0
    for i, (x, y, h) in enumerate(spots):
        root = place_cluster(donors[i % len(donors)], f"{prefix}_{i}",
                             (x/100.0, y/100.0, 0), h/100.0, rnd=rnd)
        ground_root(root)
    return len(spots)


def volumetric_fog(name, xmin, xmax, ymin, ymax, zmin, zmax,
                   density=0.012, anisotropy=0.3, color=(0.85, 0.86, 0.88),
                   height_falloff=True):
    """Begrensde mist-box met Principled Volume (Lelie-dageraad).
    height_falloff: dichter bij de grond via gradient(Z) -> density.
    Box bewust BEGRENSD houden (VRAM)."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=((xmin+xmax)/2, (ymin+ymax)/2, (zmin+zmax)/2))
    o = bpy.context.active_object; o.name = name
    o.scale = (xmax-xmin, ymax-ymin, zmax-zmin)
    bpy.ops.object.transform_apply(scale=True)
    o.display_type = 'WIRE'
    mat = bpy.data.materials.new("MAT_Fog"); mat.use_nodes = True
    nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    vol = nt.nodes.new('ShaderNodeVolumePrincipled')
    vol.inputs['Color'].default_value = (*color, 1.0)
    vol.inputs['Anisotropy'].default_value = anisotropy
    if height_falloff:
        # gradient over wereld-Z: onder dichter, boven ijler
        tc = nt.nodes.new('ShaderNodeTexCoord')
        sep = nt.nodes.new('ShaderNodeSeparateXYZ')
        nt.links.new(tc.outputs['Generated'], sep.inputs['Vector'])
        ramp = nt.nodes.new('ShaderNodeMapRange')
        ramp.inputs['From Min'].default_value = 0.0
        ramp.inputs['From Max'].default_value = 1.0
        ramp.inputs['To Min'].default_value = density
        ramp.inputs['To Max'].default_value = density * 0.12
        nt.links.new(sep.outputs['Z'], ramp.inputs['Value'])
        nt.links.new(ramp.outputs['Result'], vol.inputs['Density'])
    else:
        vol.inputs['Density'].default_value = density
    nt.links.new(vol.outputs['Volume'], out.inputs['Volume'])
    o.data.materials.append(mat)
    return o, mat

def place_cluster(donor, name, loc, target_h, rot_z=None, rnd=None):
    rnd = rnd or random
    h_src, objs = donor
    cen = Vector((0, 0, 0))
    for m in objs: cen += m.location
    cen /= len(objs)
    sc = target_h / max(h_src, 0.01)
    bpy.ops.object.empty_add(location=(loc[0], loc[1], loc[2] if len(loc) > 2 else 0))
    root = bpy.context.active_object; root.name = name
    root.scale = (sc,)*3
    root.rotation_euler = (0, 0, rot_z if rot_z is not None else rnd.uniform(0, 6.28))
    for i, m in enumerate(objs):
        d = m.copy(); d.name = f"{name}_m{i}"
        d.hide_render = False; d.hide_viewport = False
        d.location = m.location - cen
        d.parent = root
        scene().collection.objects.link(d)
    return root


# ---------------------------------------------------------------- slinger
def festoon_mats():
    wire = simple_mat("MAT_Draad", (0.02, 0.02, 0.02), rough=0.6)
    bulb = simple_mat("MAT_Bulb", (1, 1, 1), emission=(1.0, 0.62, 0.28), emission_strength=28.0)
    return wire, bulb

def festoon(name, p0, p1, sag=0.32, bulbs=True):
    wire, bulbmat = festoon_mats()
    p0 = Vector(p0); p1 = Vector(p1)
    n = 28
    pts = []
    for i in range(n + 1):
        t = i / n
        p = p0.lerp(p1, t)
        p.z -= sag * 4 * t * (1 - t)
        pts.append(p)
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    sp = cu.splines.new('POLY'); sp.points.add(n)
    for i, p in enumerate(pts):
        sp.points[i].co = (p.x, p.y, p.z, 1)
    cu.bevel_depth = 0.005; cu.bevel_resolution = 2
    ob = bpy.data.objects.new(name, cu); scene().collection.objects.link(ob)
    ob.data.materials.append(wire)
    if bulbs:
        for i in range(1, n, 2):
            p = pts[i]
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.028, segments=12, ring_count=8,
                                                 location=(p.x, p.y, p.z - 0.055))
            b = bpy.context.active_object; b.name = f"{name}_bulb{i}"
            b.data.materials.append(bulbmat)
            bpy.ops.object.shade_smooth()
    return ob


# ---------------------------------------------------------------- validatie
def audit(cabin_x=(0.4, 3.1), cabin_y=(-1.3, 1.3), extra_safe=()):
    issues = []
    SAFE = ['parentboard', 'wall-', 'roof', 'deur', 'pole-', 'foundation', 'door_pot',
            '.scharnier', 'trim-', 'fasciaboard', 'flatroof', '.doorhandle',
            'hedge_', 'ground'] + [s.lower() for s in extra_safe]
    for o in bpy.data.objects:
        if o.type != 'MESH' or o.hide_viewport: continue
        n = o.name.lower()
        if any(k in n for k in SAFE): continue
        pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
        xs = [p.x for p in pts]; ys = [p.y for p in pts]; zs = [p.z for p in pts]
        if not xs: continue
        cx, cy = (min(xs)+max(xs))/2, (min(ys)+max(ys))/2
        if cabin_x[0] < cx < cabin_x[1] and cabin_y[0] < cy < cabin_y[1] and max(zs) > 0.2:
            issues.append(f"IN_CABIN: {o.name} ({cx:.1f},{cy:.1f})")
        w, d, h = max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs)
        if (w > 12 or d > 12 or h > 12):
            issues.append(f"HUGE: {o.name} {w:.0f}x{d:.0f}x{h:.0f}")
    for i in bpy.data.images:
        if i.name in ("Render Result", "Viewer Node"): continue
        ap = bpy.path.abspath(i.filepath) if i.filepath else ""
        if not i.packed_file and ap and not os.path.exists(ap) and i.users > 0:
            issues.append(f"BROKEN_TEX: {i.name}")
    if issues:
        print("=== AUDIT ISSUES ===")
        for i in issues: print("  ! " + i)
    else:
        print("=== AUDIT PASSED ===")
    return issues

def fix_broken_image_materials(plant_kw=('weed', 'leaf', 'poppy', 'shrub', 'plant', 'flower',
                                         'grass', 'fern', 'rooibos', 'sorrel', 'periwinkle',
                                         'dandelion', 'moss', 'heli', 'gazania')):
    """Materialen die een NIET-bestaande image gebruiken herkleuren:
    planten -> procedureel groen, overig -> neutraal grijs. Voorkomt magenta.
    Roept eerst remap aan (lost echte path-mismatches op); pas wat dan nog mist."""
    esr.remap_broken_image_paths()
    bad = set()
    for i in bpy.data.images:
        if i.name in ("Render Result", "Viewer Node"):
            continue
        ap = bpy.path.abspath(i.filepath) if i.filepath else ""
        if not i.packed_file and ap and not os.path.exists(ap):
            bad.add(i)
    if not bad:
        return 0
    fixed = 0
    for m in bpy.data.materials:
        if not m.use_nodes:
            continue
        nt = m.node_tree
        uses = [n for n in nt.nodes if n.type == 'TEX_IMAGE' and n.image in bad]
        if not uses:
            continue
        b = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if not b:
            continue
        tag = (m.name + " " + " ".join(n.image.name for n in uses if n.image)).lower()
        is_plant = any(k in tag for k in plant_kw)
        for l in list(b.inputs['Base Color'].links):
            nt.links.remove(l)
        for l in list(b.inputs['Normal'].links):
            nt.links.remove(l)
        for l in list(b.inputs['Roughness'].links):
            if l.from_node.type == 'TEX_IMAGE' and l.from_node.image in bad:
                nt.links.remove(l)
        if is_plant:
            noi = nt.nodes.new('ShaderNodeTexNoise'); noi.inputs['Scale'].default_value = 13.0
            rmp = nt.nodes.new('ShaderNodeValToRGB')
            rmp.color_ramp.elements[0].color = (0.06, 0.11, 0.04, 1)
            rmp.color_ramp.elements[1].color = (0.15, 0.21, 0.07, 1)
            nt.links.new(noi.outputs['Fac'], rmp.inputs['Fac'])
            nt.links.new(rmp.outputs['Color'], b.inputs['Base Color'])
            b.inputs['Roughness'].default_value = 0.9
        else:
            b.inputs['Base Color'].default_value = (0.40, 0.40, 0.39, 1.0)
            b.inputs['Roughness'].default_value = 0.7
        fixed += 1
    return fixed


def remove_in_cabin(objects_prefix, cabin_x, cabin_y):
    """Verwijder root-objecten (op naam-prefix) waarvan een mesh in het cabinevolume valt."""
    roots = [o for o in bpy.data.objects if o.name.startswith(objects_prefix) and o.parent is None]
    removed = 0
    for r in roots:
        bpy.context.view_layer.update()
        ms = [c for c in r.children_recursive if c.type == 'MESH']
        bb = wbbox_meshes(ms)
        if not bb:
            continue
        if bb[0] < cabin_x[1] and bb[1] > cabin_x[0] and bb[2] < cabin_y[1] and bb[3] > cabin_y[0]:
            nms = [c.name for c in r.children_recursive] + [r.name]
            for nm in nms:
                o = bpy.data.objects.get(nm)
                if o:
                    bpy.data.objects.remove(o, do_unlink=True)
            removed += 1
    return removed


def ground_to(name, z=0.0):
    """Zet root-object zo dat de min-z van zijn meshes op z ligt."""
    o = bpy.data.objects.get(name)
    if not o: return None
    bpy.context.view_layer.update()
    ms = [c for c in o.children_recursive if c.type == 'MESH'] + ([o] if o.type == 'MESH' else [])
    bb = wbbox_meshes(ms)
    if bb: o.location.z += z - bb[4]
    bpy.context.view_layer.update()
    return o

def move_root_to(name, x=None, y=None, ground_z=None):
    """Verplaats root via wereld-bbox-center naar (x,y); optioneel gronden."""
    o = bpy.data.objects.get(name)
    if not o: return None
    bpy.context.view_layer.update()
    ms = [c for c in o.children_recursive if c.type == 'MESH'] + ([o] if o.type == 'MESH' else [])
    bb = wbbox_meshes(ms)
    if not bb: return o
    if x is not None: o.location.x += x - (bb[0]+bb[1])/2
    if y is not None: o.location.y += y - (bb[2]+bb[3])/2
    if ground_z is not None:
        bpy.context.view_layer.update()
        bb = wbbox_meshes(ms); o.location.z += ground_z - bb[4]
    bpy.context.view_layer.update()
    return o

def force_base_color(objnames, color, rough=0.8, only_prefix=None):
    """Hard base-color op de materialen van gegeven objecten; verwijdert alle
    image-links naar Base Color (lost magenta op die fix_broken miste omdat de
    image bestaat/packed is maar verkeerd mapt). objnames = lijst of prefix-string."""
    if isinstance(objnames, str):
        targets = [o for o in bpy.data.objects if o.name.startswith(objnames)]
    else:
        targets = [bpy.data.objects.get(n) for n in objnames if bpy.data.objects.get(n)]
    mats = set()
    for o in targets:
        for c in [o] + list(o.children_recursive):
            for s in c.material_slots:
                if s.material: mats.add(s.material)
    n = 0
    for m in mats:
        if not m.use_nodes: continue
        if only_prefix and only_prefix not in m.name: continue
        b = next((x for x in m.node_tree.nodes if x.type == 'BSDF_PRINCIPLED'), None)
        if not b: continue
        for l in list(b.inputs['Base Color'].links): m.node_tree.links.remove(l)
        b.inputs['Base Color'].default_value = (*color, 1.0)
        b.inputs['Roughness'].default_value = rough
        if 'Emission Strength' in b.inputs: b.inputs['Emission Strength'].default_value = 0.0
        n += 1
    return n

def place_along(names, p0, p1, keep_z=True, z=None, jitter=0.0, rnd=None):
    """Verdeel bestaande stepping-objecten gelijkmatig langs lijn p0->p1 (XY).
    Geen overlap als afstand > steen-grootte; behoudt of zet z."""
    rnd = rnd or random
    objs = [bpy.data.objects.get(n) for n in names if bpy.data.objects.get(n)]
    p0 = Vector(p0); p1 = Vector(p1); k = len(objs)
    for i, o in enumerate(objs):
        t = i / max(k-1, 1)
        p = p0.lerp(p1, t)
        o.location.x = p.x + (rnd.uniform(-jitter, jitter) if jitter else 0)
        o.location.y = p.y + (rnd.uniform(-jitter, jitter) if jitter else 0)
        if z is not None: o.location.z = z
    return objs


def inspect_cams(shots, outdir, res=(800, 600), samples=48):
    """shots: lijst (naam, loc, target). Rendert close-ups, slaat NIET op."""
    s = scene()
    s.render.resolution_x, s.render.resolution_y = res
    s.cycles.samples = samples
    for name, loc, tgt in shots:
        cam = bpy.data.cameras.new(name); cam.lens = 35
        co = bpy.data.objects.new(name, cam); s.collection.objects.link(co)
        co.location = loc
        d = Vector(tgt) - co.location
        co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
        s.camera = co
        s.render.filepath = os.path.join(outdir, name + ".png")
        bpy.ops.render.render(write_still=True)
        print(f"[inspect] {name} done")


# ==================== REALISME-TOOLKIT (2026-06-16) ====================
import bmesh as _bmesh

def bevel_all(obj, w=0.004, seg=2, angle=55):
    """Micro-bevel op scherpe randen (de #1 'echt materiaal'-tell). Laat als modifier."""
    if not obj or obj.type != 'MESH':
        return obj
    m = obj.modifiers.new("Bevel", 'BEVEL')
    m.width = w; m.segments = seg
    m.limit_method = 'ANGLE'; m.angle_limit = math.radians(angle)
    try: m.harden_normals = True
    except Exception: pass
    return obj

def set_agx(look='AgX - Medium High Contrast', exposure=None):
    """AgX i.p.v. Filmic — camera-achtige highlight-rolloff, grootste gratis realisme-winst."""
    s = scene()
    s.view_settings.view_transform = 'AgX'
    for lk in (look, 'AgX - Base Contrast', 'None'):
        try:
            s.view_settings.look = lk; break
        except Exception:
            continue
    if exposure is not None:
        s.view_settings.exposure = exposure

def set_camera_dof(cam_name='HeroCam', fstop=6.0, focus_xyz=(0.0, 0.3, 1.2)):
    """Subtiele DoF (f5.6-8): cabin scherp, voor/achtergrond net zacht."""
    cam = bpy.data.objects.get(cam_name)
    if not cam or cam.type != 'CAMERA':
        return
    cam.data.dof.use_dof = True
    cam.data.dof.aperture_fstop = fstop
    cam.data.dof.focus_distance = (Vector(focus_xyz) - cam.location).length

def stone_mat(name="MAT_Steen", base=(0.42, 0.40, 0.37), rough=0.85):
    """Procedureel grijs-steen materiaal (noise-kleurvariatie + bump). Betrouwbaar, geen 8K."""
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    b.inputs['Roughness'].default_value = rough
    tc = nt.nodes.new('ShaderNodeTexCoord')
    noi = nt.nodes.new('ShaderNodeTexNoise'); noi.inputs['Scale'].default_value = 6.0
    noi.inputs['Detail'].default_value = 8.0
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (base[0]*0.65, base[1]*0.65, base[2]*0.65, 1)
    ramp.color_ramp.elements[1].color = (base[0]*1.18, base[1]*1.16, base[2]*1.12, 1)
    nt.links.new(tc.outputs['Object'], noi.inputs['Vector'])
    nt.links.new(noi.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    noi2 = nt.nodes.new('ShaderNodeTexNoise'); noi2.inputs['Scale'].default_value = 40.0
    bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.35
    nt.links.new(tc.outputs['Object'], noi2.inputs['Vector'])
    nt.links.new(noi2.outputs['Fac'], bm.inputs['Height'])
    nt.links.new(bm.outputs['Normal'], b.inputs['Normal'])
    return m

def plank_deck(name, x0, x1, y0, y1, top_z, mat, plank_w=0.145, gap=0.006,
               thick=0.03, along='Y', fascia_mat=None, rnd=None):
    """Vlonder/terras uit LOSSE planken + donkere voeg-onderlaag + fascia rondom
    (verzonken in de grond). Vervangt de platte add_box-slab."""
    rnd = rnd or random
    objs = []
    dark = simple_mat("MAT_DeckGap", (0.03, 0.025, 0.02), rough=1.0)
    add_box(f"{name}_base", x0, x1, y0, y1, top_z - thick + 0.006, top_z - thick - 0.02, dark)
    if along == 'Y':
        n = int((x1 - x0) / (plank_w + gap))
        for i in range(n):
            px0 = x0 + i * (plank_w + gap); px1 = min(px0 + plank_w, x1)
            o = add_box(f"{name}_p{i}", px0, px1, y0, y1, top_z, top_z - thick, mat)
            o.rotation_euler.z = rnd.uniform(-0.003, 0.003)
            bevel_all(o, 0.003); objs.append(o)
    else:
        n = int((y1 - y0) / (plank_w + gap))
        for i in range(n):
            py0 = y0 + i * (plank_w + gap); py1 = min(py0 + plank_w, y1)
            o = add_box(f"{name}_p{i}", x0, x1, py0, py1, top_z, top_z - thick, mat)
            bevel_all(o, 0.003); objs.append(o)
    fm = fascia_mat or mat
    zt = top_z + 0.003; zb = top_z - thick - 0.10
    add_box(f"{name}_fN", x0-0.015, x1+0.015, y1, y1+0.022, zt, zb, fm)
    add_box(f"{name}_fS", x0-0.015, x1+0.015, y0-0.022, y0, zt, zb, fm)
    add_box(f"{name}_fW", x0-0.022, x0, y0-0.022, y1+0.022, zt, zb, fm)
    add_box(f"{name}_fE", x1, x1+0.022, y0-0.022, y1+0.022, zt, zb, fm)
    for nm in (f"{name}_fN", f"{name}_fS", f"{name}_fW", f"{name}_fE"):
        bevel_all(bpy.data.objects.get(nm), 0.003)
    return objs

def slat_planter(name, x0, x1, y0, y1, h, mat_wall, mat_post, plank_h=0.15,
                 gap=0.006, thick=0.02, post=0.07, post_over=0.03, rnd=None):
    """Plantenbak/bed/zandbak uit losse planken + 4 hoekpalen (uitstekend), bevelled.
    Vervangt de 4-box-of-1-box bak. Returnt (root_empty, binnenmaat-tuple)."""
    rnd = rnd or random
    bpy.ops.object.empty_add(location=((x0+x1)/2, (y0+y1)/2, 0))
    root = bpy.context.active_object; root.name = name + "_root"
    n = max(1, int(round(h / (plank_h + gap))))
    def wall(tag, ax0, ax1, ay0, ay1):
        for i in range(n):
            z0 = i * (plank_h + gap); z1 = z0 + plank_h
            o = add_box(f"{name}_{tag}{i}", ax0, ax1, ay0, ay1, z1, z0, mat_wall)
            o.rotation_euler.z = rnd.uniform(-0.004, 0.004)
            bevel_all(o, 0.004); o.parent = root; o.matrix_parent_inverse = root.matrix_basis.inverted()
    wall("N", x0+post, x1-post, y1-thick, y1)
    wall("S", x0+post, x1-post, y0, y0+thick)
    wall("W", x0, x0+thick, y0, y1)
    wall("E", x1-thick, x1, y0, y1)
    for (px, py) in ((x0+post/2, y0+post/2), (x1-post/2, y0+post/2),
                     (x0+post/2, y1-post/2), (x1-post/2, y1-post/2)):
        o = add_box(f"{name}_post_{px:.2f}_{py:.2f}", px-post/2, px+post/2,
                    py-post/2, py+post/2, h+post_over, 0.0, mat_post)
        bevel_all(o, 0.005); o.parent = root; o.matrix_parent_inverse = root.matrix_basis.inverted()
    return root, (x0+thick, x1-thick, y0+thick, y1-thick)

def _irregular_stone(name, rx, mat, sides=8, jitter=0.20, dome=0.30, rnd=None):
    """Eén onregelmatige, licht bolle natuursteen (geen cilinder). Bevelled."""
    rnd = rnd or random
    bm = _bmesh.new()
    top, bot = [], []
    rs = [rx * (1 + rnd.uniform(-jitter, jitter)) for _ in range(sides)]
    for i in range(sides):
        a = i / sides * 2 * math.pi
        r = rs[i]
        top.append(bm.verts.new((math.cos(a)*r, math.sin(a)*r, rx*dome*rnd.uniform(0.7, 1.0))))
        bot.append(bm.verts.new((math.cos(a)*r*1.03, math.sin(a)*r*1.03, -rx*0.6)))
    ctop = bm.verts.new((rnd.uniform(-0.05,0.05)*rx, rnd.uniform(-0.05,0.05)*rx, rx*dome*1.15))
    for i in range(sides):
        j = (i+1) % sides
        bm.faces.new((top[i], top[j], ctop))
        bm.faces.new((bot[i], bot[j], top[j], top[i]))
    bm.faces.new(list(reversed(bot)))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); scene().collection.objects.link(o)
    if mat: o.data.materials.append(mat)
    bevel_all(o, 0.012)
    return o

def flagstone_path(name, pts, stride=0.62, target=0.46, sink=0.04, mat=None, rnd=None):
    """Echt stapstenenpad: onregelmatige natuurstenen op stride-afstand (55-65cm) langs
    de polyline pts, elk anders van vorm/grootte/rotatie, verzonken in het gras (top ~+1cm).
    Vervangt identieke cilinder-'rondjes'. pts = [(x,y),...] van deur/terras naar tuin."""
    rnd = rnd or random
    mat = mat or stone_mat()
    P = [Vector((p[0], p[1])) for p in pts]
    seg = [(P[k+1]-P[k]).length for k in range(len(P)-1)]
    total = sum(seg)
    samples = [P[0]]
    pos = 0.0
    while pos + stride < total:
        pos += stride
        run = pos; k = 0
        while k < len(seg) and run > seg[k]:
            run -= seg[k]; k += 1
        if k >= len(seg): break
        samples.append(P[k].lerp(P[k+1], run/seg[k]))
    out = []
    for j, s in enumerate(samples):
        rx = target/2 * rnd.uniform(0.82, 1.18)
        o = _irregular_stone(f"{name}_{j}", rx, mat, sides=rnd.choice([7, 8, 9]),
                             jitter=0.20, rnd=rnd)
        o.rotation_euler.z = rnd.uniform(0, 6.28)
        bpy.context.view_layer.update()
        bb = wbbox_meshes([o])
        o.location.x = s.x; o.location.y = s.y
        o.location.z = (0.012 - sink) - bb[4]
        out.append(o)
    return out

def klinker_strip(name, x0, x1, y0, y1, top_z, mat, L=0.21, B=0.07, gap=0.005,
                  thick=0.05, herringbone=False, rnd=None):
    """Klinkerbestrating uit individuele stenen (halfsteens) met voeg + micro-bevel +
    per-steen rot/z-jitter. Vervangt het platte add_box-terras/pad. Donkere voeg-onderlaag."""
    rnd = rnd or random
    dark = simple_mat("MAT_Voegzand", (0.16, 0.14, 0.11), rough=1.0)
    add_box(f"{name}_voeg", x0, x1, y0, y1, top_z - thick + 0.012, top_z - thick - 0.01, dark)
    objs = []
    ny = int((y1 - y0) / (B + gap))
    for r in range(ny):
        py0 = y0 + r * (B + gap)
        off = ((L + gap) / 2) if (r % 2) else 0.0
        x = x0 - off; idx = 0
        while x < x1:
            px1 = min(x + L, x1)
            if px1 - x > 0.04:
                o = add_box(f"{name}_{r}_{idx}", max(x, x0), px1, py0, py0 + B,
                            top_z + rnd.uniform(-0.002, 0.003), top_z - thick, mat)
                o.rotation_euler.z = rnd.uniform(-0.035, 0.035)
                bevel_all(o, 0.0035); objs.append(o)
            x += L + gap; idx += 1
    return objs

def grass_overhang_edge(name, x0, x1, y0, y1, density=900, ng=None, sprig=None, rnd=None):
    """Strook gras-scatter die over een hardscape-rand hangt (breekt de mes-snijlijn).
    Hergebruikt de HedgeGN-scatter op een dunne strook-mesh."""
    if ng is None or sprig is None:
        return None
    o = add_box(name, x0, x1, y0, y1, 0.02, 0.0, None)
    mod = o.modifiers.new("GrassScatter", 'NODES'); mod.node_group = ng
    return o


# ================================================================ RIG A - herbruikbare licht-rig
def _kelvin_rgb(k):
    """Grove blackbody->RGB voor de sun-kleur (lager K = warmer)."""
    presets = {2800: (1.0, 0.64, 0.34), 3000: (1.0, 0.68, 0.38), 3200: (1.0, 0.71, 0.42),
               3500: (1.0, 0.76, 0.50), 4000: (1.0, 0.82, 0.63), 4500: (1.0, 0.86, 0.71),
               5000: (1.0, 0.90, 0.79), 5500: (1.0, 0.93, 0.86), 6000: (0.98, 0.95, 0.94),
               6500: (0.95, 0.96, 1.0)}
    return presets[min(presets, key=lambda x: abs(x - k))]

LIGHT_MOMENTS = {
    'golden_hour': dict(elev=7,  energy=5.0, kelvin=3200, density=0.004, look='AgX - Medium High Contrast', world=0.9, hdri='spaichingen_hill_2k.hdr',           hdri_rot=90),
    'namiddag':    dict(elev=15, energy=4.0, kelvin=4000, density=0.003, look='AgX - Medium High Contrast', world=1.0, hdri='syferfontein_18d_clear_2k.hdr',     hdri_rot=200),
    'ochtend':     dict(elev=10, energy=4.5, kelvin=4500, density=0.004, look='AgX - Base Contrast',        world=1.0, hdri='kiara_1_dawn_2k.hdr',              hdri_rot=130),
    'blue_hour':   dict(elev=6,  energy=1.8, kelvin=6500, density=0.006, look='AgX - Base Contrast',        world=0.7, hdri='moonless_golf_2k.hdr',             hdri_rot=180),
    'sunset':      dict(elev=6,  energy=4.5, kelvin=3000, density=0.005, look='AgX - Medium High Contrast', world=0.9, hdri='venice_sunset_2k.hdr',             hdri_rot=90),
    'overcast':    dict(elev=35, energy=1.5, kelvin=6000, density=0.004, look='AgX - Base Contrast',        world=1.1, hdri='kloofendal_overcast_puresky_1k.hdr', hdri_rot=180),
}

def setup_light(moment='namiddag', azimuth_deg=45, bounds=(-14, 14, -14, 14, 0.0, 9.0), exposure=0.3):
    """RIG A: verwijder oude sun+mist, zet lage warme zon per moment + BEGRENSDE haze-cube
    (nooit World Volume Scatter) + AgX. Compositor uit (anti-zwart). bounds = haze-cube-extent."""
    p = LIGHT_MOMENTS.get(moment, LIGHT_MOMENTS['namiddag'])
    for o in list(bpy.data.objects):
        if o.type == 'LIGHT' and o.data.type == 'SUN':
            bpy.data.objects.remove(o, do_unlink=True)
        elif o.name.lower().startswith(('mist', 'fog', 'haze')):
            bpy.data.objects.remove(o, do_unlink=True)
    add_sun(energy=p['energy'], color=_kelvin_rgb(p['kelvin']), elev_deg=p['elev'], azim_deg=azimuth_deg, angle_deg=1.2)
    x0, x1, y0, y1, z0, z1 = bounds
    hazecol = (0.74, 0.79, 0.92) if moment == 'blue_hour' else (0.86, 0.86, 0.87)
    volumetric_fog("Mist_Rig", x0, x1, y0, y1, z0, z1, density=p['density'], anisotropy=0.5, color=hazecol)
    # echte lucht per moment (fixt warme-zon-vs-verkeerde-lucht mismatch)
    try:
        setup_hdri(p['hdri'], strength=p['world'], rot_z_deg=p.get('hdri_rot', 180))
        print("  HDRI ->", p['hdri'])
    except Exception as e:
        print("  HDRI-swap faalde:", e)
    set_agx(look=p['look'], exposure=exposure)
    scene().use_nodes = False   # geen stiekeme compositor-zwart
    print(f"[RIG A] moment={moment} azim={azimuth_deg} sun(elev={p['elev']},{p['kelvin']}K,E{p['energy']}) haze={p['density']} look={p['look']} world={p['world']}")


# ================================================================ RIG C - hout
def warm_wood_walls(min_rough=0.55):
    """RIG C: nerf mét de plank (uv_board_textures) + plastic-glans doden + bleke/witte
    wanden warm maken. Behoudt basis-textuur en two-tone (zwart KDI buiten / naturel binnen)."""
    uv_board_textures()
    KW = ('wall', 'canopy', 'roofboard', 'cladding', 'plank', 'wand', 'potdeksel', 'rabat',
          'luxehouse', 'hout', 'wood', 'deur', 'door', 'fascia', 'shed')
    n = 0
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        nl = m.name.lower()
        if not any(k in nl for k in KW): continue
        nt = m.node_tree
        b = next((x for x in nt.nodes if x.type == 'BSDF_PRINCIPLED'), None)
        if not b: continue
        r = b.inputs['Roughness']
        if not r.is_linked and r.default_value < min_rough:
            r.default_value = min_rough
        for key in ('Specular IOR Level', 'Specular'):
            if key in b.inputs and not b.inputs[key].is_linked:
                b.inputs[key].default_value = min(b.inputs[key].default_value, 0.3); break
        bc = b.inputs['Base Color']
        if bc.is_linked and any(k in nl for k in ('canopy', 'luxehouse')):
            # bleke onbehandelde binnenwand warm maken (amber-multiply), textuur behouden
            src = bc.links[0].from_socket
            mix = nt.nodes.new('ShaderNodeMixRGB'); mix.blend_type = 'MULTIPLY'
            mix.inputs['Fac'].default_value = 0.32; mix.inputs['Color2'].default_value = (0.87, 0.73, 0.52, 1)
            nt.links.new(src, mix.inputs['Color1'])
            for l in list(bc.links): nt.links.remove(l)
            nt.links.new(mix.outputs['Color'], bc)
        elif not bc.is_linked:
            c = bc.default_value
            if c[0] > 0.6 and c[1] > 0.55:   # bleek/wit hout -> warm
                bc.default_value = (min(c[0], 0.72), c[1] * 0.82, c[2] * 0.58, 1)
        n += 1
    print(f"[RIG C] warm_wood_walls: {n} wand/hout-materialen (nerf FLAT+UV, glans gedood, bleke warm)")
    return n


# ================================================================ S2 - practicals AAN (9 jul)
# Recept uit overkappingen-website/scene_b_spa.py (emissie_mat + Fill_LED): bollen
# emission 2200K sterkte 2 (dag) / 4 (schemer), lantaarns idem + kleine warme point.
PRACTICAL_BULB_KW = ('bulb', 'festoon', 'slinger', 'string_light', 'lichtsnoer', 'fairy')
PRACTICAL_LANTERN_KW = ('lantaarn', 'lantern')
PRACTICAL_GLOW_KW = ('glass', 'glas', 'emit', 'light', 'bulb', 'candle', 'kaars', 'lamp')

def emissie_mat(naam, kleur, sterkte):
    """Puur emissie-materiaal (spa-recept). Idempotent op naam."""
    m = bpy.data.materials.get(naam)
    if m:
        return m
    m = bpy.data.materials.new(naam); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = (*kleur, 1.0)
    em.inputs['Strength'].default_value = sterkte
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
    return m

def _glow_principled(m, color, strength):
    """Laat een bestaand Principled-materiaal gloeien (vorm/textuur blijft)."""
    if not m.use_nodes: return False
    b = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if not b: return False
    for key in ('Emission Color', 'Emission'):
        if key in b.inputs:
            b.inputs[key].default_value = (*color, 1.0); break
    if 'Emission Strength' in b.inputs:
        b.inputs['Emission Strength'].default_value = strength
    return True

def practicals_on(mode='schemer', bulb_kw=PRACTICAL_BULB_KW, lantern_kw=PRACTICAL_LANTERN_KW):
    """S2: alle lichtsnoer-bollen + lantaarns ECHT laten branden.
    mode 'dag' = sterkte 2, 'schemer' = sterkte 4. Lantaarn krijgt bovendien
    een kleine warme point (radius 0.05) in zijn bbox-centrum. Idempotent."""
    strength = 2.0 if mode == 'dag' else 4.0
    warm = (1.0, 0.58, 0.24)  # ~2200K
    n_bulb = 0
    done_mats = set()
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        nl = o.name.lower()
        if not any(k in nl for k in bulb_kw): continue
        for s in o.material_slots:
            m = s.material
            if not m or m.name in done_mats: continue
            ml = m.name.lower()
            if any(k in ml for k in ('wire', 'draad', 'cable', 'cord', 'metal', 'black', 'frame')):
                continue
            if m.name.startswith('MAT_Bulb'):
                # eigen festoon-mat: S2-niveau (2-4; hoger blaast naar wit uit onder AgX)
                em = next((x for x in m.node_tree.nodes if x.type == 'EMISSION'), None)
                if em:
                    em.inputs['Strength'].default_value = strength
                    em.inputs['Color'].default_value = (*warm, 1.0)
                done_mats.add(m.name); n_bulb += 1; continue
            if _glow_principled(m, warm, strength):
                done_mats.add(m.name); n_bulb += 1
    # lantaarns: glas-delen laten gloeien + warme point in het centrum
    n_lan = 0
    roots = {}
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        nl = o.name.lower()
        if not any(k in nl for k in lantern_kw): continue
        top = o
        while top.parent is not None and any(k in top.parent.name.lower() for k in lantern_kw):
            top = top.parent
        roots.setdefault(top.name, []).append(o)
    for rname, objs in roots.items():
        glowed = 0
        for o in objs:
            for s in o.material_slots:
                m = s.material
                if not m or m.name in done_mats: continue
                if any(k in m.name.lower() for k in PRACTICAL_GLOW_KW):
                    if _glow_principled(m, warm, strength * 1.5):
                        done_mats.add(m.name); glowed += 1
        cs = [ob.matrix_world @ Vector(c) for ob in objs for c in ob.bound_box]
        cx = sum(c.x for c in cs) / len(cs); cy = sum(c.y for c in cs) / len(cs)
        cz = (min(c.z for c in cs) + max(c.z for c in cs)) / 2
        pname = f"Practical_{rname}"
        old = bpy.data.objects.get(pname)
        if old: bpy.data.objects.remove(old, do_unlink=True)
        li = bpy.data.lights.new(pname, 'POINT')
        li.energy = 6.0 if mode == 'dag' else 12.0
        li.color = warm; li.shadow_soft_size = 0.05
        po = bpy.data.objects.new(pname, li); scene().collection.objects.link(po)
        po.location = (cx, cy, cz)
        n_lan += 1
        print(f"  [S2] lantaarn '{rname}': {glowed} glow-mats + point @ ({cx:.2f},{cy:.2f},{cz:.2f})")
    print(f"[S2] practicals_on({mode}): {n_bulb} bol/snoer-materialen gloeien, {n_lan} lantaarns met point")
    return n_bulb, n_lan


# ================================================================ RIG E - overkapping-fill
def overhang_fill(loc=(0.0, 0.7, 1.9), energy=45.0, kelvin=2700, size=2.4):
    """RIG E: warme fill-area-light onder het afdak / achter het glas, zodat overkapping en
    interieur nooit als zwart gat lezen (warme binnengloed door de open zijde/glas). Idempotent."""
    for o in list(bpy.data.objects):
        if o.name == 'OverhangFill':
            bpy.data.objects.remove(o, do_unlink=True)
    li = bpy.data.lights.new('OverhangFill', 'AREA'); li.energy = energy; li.size = size
    li.color = _kelvin_rgb(kelvin)
    o = bpy.data.objects.new('OverhangFill', li); scene().collection.objects.link(o)
    o.location = loc; o.rotation_euler = (math.radians(18), 0, 0)
    print(f"[RIG E] overhang fill-light @ {loc} {kelvin}K E{energy}")
    return o

