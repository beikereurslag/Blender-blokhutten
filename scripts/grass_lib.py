"""Herbruikbare gras-module: gekruiste-blad-sprietjes + GN-scatter die ALLEEN op
echte grond valt (raycast omlaag: hardscape/deck/pad/water/grind/hut -> geen gras).

S1 gras-mix (9 jul): 3 clump-varianten (pick instance), random scale 0.6-1.4,
tilt, per-instance kleurvariatie (3 groentinten + ~7% droog geel), density-noise
voor kale plekjes, zachte fade aan de scene-randen, alles INSTANCED (geen realize).

Gebruik:
    import grass_lib as gl
    gl.add_grass(scene, area=(-10,10,-4,9), density=180)
"""
import bpy, bmesh, math, random
from mathutils import Vector

GRASS_MAT = "MAT_GrassBlade"
TUFTS_COLL = "GrassTufts"
EMITTER = "GrassEmitter"
NG = "GN_GrassMasked"

# VEILIG: gras ALLEEN waar de bovenste geraakte vlak de echte grondplaat is.
# Zo komt er nooit gras op een ANDER vloer-oppervlak (deck/terras/hottub/pad/water),
# ook niet op vloeren die niet bij naam bekend zijn (die raakt de ray i.p.v. de grond).
GROUND_KW = ("ground", "grass", "gras", "terrain", "grond", "lawn", "gazon", "weide", "veld")


def grass_material(dry_frac=0.07, sat_mul=1.0, val_mul=1.0):
    """Per-instance kleurvariatie: ObjectInfo.Random -> ramp met 3 groentinten
    + smalle droog-geel-zone bovenin; vermenigvuldigd met wortel->tip-gradient.
    Grote wereld-noise mengt richting warmer/droger voor vlek-variatie."""
    m = bpy.data.materials.get(GRASS_MAT)
    if m:
        bpy.data.materials.remove(m)
    m = bpy.data.materials.new(GRASS_MAT); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Roughness'].default_value = 0.92
    for key in ('Specular IOR Level', 'Specular'):
        if key in b.inputs:
            b.inputs[key].default_value = 0.06; break

    def c(rgb):  # sat/val-shift voor scene-varianten (mediterraan droger enz.)
        r, g, bl = rgb
        avg = (r + g + bl) / 3
        return tuple(min(1.0, (avg + (v - avg) * sat_mul) * val_mul) for v in (r, g, bl)) + (1.0,)

    # per-instance variatie (Cycles: Object Info Random is per GN-instance)
    oi = nt.nodes.new('ShaderNodeObjectInfo')
    var = nt.nodes.new('ShaderNodeValToRGB')
    cr = var.color_ramp
    cr.elements[0].position = 0.0;  cr.elements[0].color = c((0.030, 0.095, 0.020))
    cr.elements[1].position = 0.40; cr.elements[1].color = c((0.058, 0.155, 0.033))
    e = cr.elements.new(0.78);      e.color = c((0.098, 0.215, 0.050))
    e = cr.elements.new(1.0 - dry_frac - 0.01); e.color = c((0.105, 0.205, 0.052))
    e = cr.elements.new(1.0 - dry_frac);        e.color = c((0.240, 0.190, 0.055))  # droog
    e = cr.elements.new(1.0);       e.color = c((0.320, 0.245, 0.075))
    nt.links.new(oi.outputs['Random'], var.inputs['Fac'])

    # vlek-variatie op wereldpositie: sommige zones warmer/droger
    geo = nt.nodes.new('ShaderNodeNewGeometry')
    noi = nt.nodes.new('ShaderNodeTexNoise')
    noi.inputs['Scale'].default_value = 0.16; noi.inputs['Detail'].default_value = 2.0
    nt.links.new(geo.outputs['Position'], noi.inputs['Vector'])
    mrn = nt.nodes.new('ShaderNodeMapRange')
    mrn.inputs['From Min'].default_value = 0.42; mrn.inputs['From Max'].default_value = 0.68
    mrn.inputs['To Min'].default_value = 0.0;   mrn.inputs['To Max'].default_value = 0.28
    nt.links.new(noi.outputs['Fac'], mrn.inputs['Value'])
    warm = nt.nodes.new('ShaderNodeMixRGB'); warm.blend_type = 'MULTIPLY'
    warm.inputs['Color2'].default_value = (1.35, 1.05, 0.55, 1.0)  # gelig-droge zweem
    nt.links.new(var.outputs['Color'], warm.inputs['Color1'])
    nt.links.new(mrn.outputs['Result'], warm.inputs['Fac'])

    # donkere wortel -> frissere tip via object-Z
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Generated'], sep.inputs['Vector'])
    zr = nt.nodes.new('ShaderNodeValToRGB')
    zr.color_ramp.elements[0].position = 0.0; zr.color_ramp.elements[0].color = (0.32, 0.32, 0.32, 1)
    zr.color_ramp.elements[1].position = 1.0; zr.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1)
    nt.links.new(sep.outputs['Z'], zr.inputs['Fac'])
    root = nt.nodes.new('ShaderNodeMixRGB'); root.blend_type = 'MULTIPLY'
    root.inputs['Fac'].default_value = 1.0
    nt.links.new(warm.outputs['Color'], root.inputs['Color1'])
    nt.links.new(zr.outputs['Color'], root.inputs['Color2'])

    nt.links.new(root.outputs['Color'], b.inputs['Base Color'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return m


def _tuft(name, seed, blades, h_range, lean_range, h_mul, mat):
    old = bpy.data.objects.get(name)
    if old: bpy.data.objects.remove(old, do_unlink=True)
    me = bpy.data.meshes.new(name); bm = bmesh.new(); rr = random.Random(seed)
    for _ in range(blades):
        ang = rr.uniform(0, 6.283)
        lean = rr.uniform(*lean_range)
        h = rr.uniform(*h_range) * h_mul
        w = rr.uniform(0.006, 0.008)
        cx, cy = math.cos(ang) * 0.012, math.sin(ang) * 0.012
        tx, ty = cx + math.cos(ang) * lean, cy + math.sin(ang) * lean
        for (ox, oy) in ((math.cos(ang) * w, math.sin(ang) * w), (-math.sin(ang) * w, math.cos(ang) * w)):
            v1 = bm.verts.new((cx - ox, cy - oy, 0)); v2 = bm.verts.new((cx + ox, cy + oy, 0))
            v3 = bm.verts.new((tx, ty, h))
            bm.faces.new((v1, v2, v3))   # gekruiste bladen (2 vlakken per spriet)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    o.data.materials.append(mat)
    return o


def make_tufts(h_mul=1.0, mat=None):
    """3 clump-varianten in een (niet aan de scene gelinkte) collectie:
    A = standaard gazonpol, B = hoger + schever weidepolletje, C = kort + dicht.
    h_mul < 1 = korter gemaaid gazon (v5-les: 1.0 leest als weidegras)."""
    coll = bpy.data.collections.get(TUFTS_COLL)
    if coll:
        for o in list(coll.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(coll)
    coll = bpy.data.collections.new(TUFTS_COLL)
    mat = mat or grass_material()
    specs = (("GrassTuft_A", 7, 9, (0.032, 0.070), (0.004, 0.028)),
             ("GrassTuft_B", 13, 6, (0.050, 0.095), (0.012, 0.055)),
             ("GrassTuft_C", 23, 13, (0.020, 0.045), (0.003, 0.020)))
    for name, seed, blades, hr, lr in specs:
        coll.objects.link(_tuft(name, seed, blades, hr, lr, h_mul, mat))
    return coll


def build_emitter(scene, area, cell=0.45):
    """Grid-plane over 'area' (x0,x1,y0,y1) op z=0.03 met float-attribuut 'grass' (1=grond, 0=hardscape)."""
    old = bpy.data.objects.get(EMITTER)
    if old: bpy.data.objects.remove(old, do_unlink=True)
    x0, x1, y0, y1 = area
    nx = max(2, int((x1 - x0) / cell)); ny = max(2, int((y1 - y0) / cell))
    bm = bmesh.new(); verts = {}
    for i in range(nx + 1):
        for j in range(ny + 1):
            x = x0 + (x1 - x0) * i / nx; y = y0 + (y1 - y0) * j / ny
            verts[(i, j)] = bm.verts.new((x, y, 0.03))
    bm.verts.ensure_lookup_table()
    for i in range(nx):
        for j in range(ny):
            bm.faces.new((verts[(i, j)], verts[(i + 1, j)], verts[(i + 1, j + 1)], verts[(i, j + 1)]))
    me = bpy.data.meshes.new(EMITTER); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(EMITTER, me); scene.collection.objects.link(o)
    # wereld-XY per vertex vastleggen, dan emitter verbergen zodat de raycast hem niet raakt
    world_xy = [(o.matrix_world @ v.co).xy for v in me.vertices]
    o.hide_viewport = True
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    attr = me.attributes.new("grass", 'FLOAT', 'POINT')
    ngrass = 0
    for vi, xy in enumerate(world_xy):
        hit, loc, nor, idx, obj, mat = scene.ray_cast(dg, (xy.x, xy.y, 0.45), (0, 0, -1), distance=0.80)
        # gras = de bovenste geraakte vlak IS de echte grondplaat (veilig: nooit op andere vloeren)
        is_grass = 1.0 if (hit and obj is not None and any(k in obj.name.lower() for k in GROUND_KW)) else 0.0
        attr.data[vi].value = is_grass; ngrass += int(is_grass)
    o.hide_viewport = False
    print(f"[grass] emitter {nx}x{ny}, grass-cellen {ngrass}/{len(me.vertices)}")
    return o


def grass_nodegroup(coll, density, area, fade=1.6, tilt=0.30, bare=True):
    """Scatter: mask-selectie + density-noise (kale plekjes) + rand-fade,
    pick-instance uit 3 tuft-varianten, random Z-rot + tilt + scale 0.6-1.4.
    GEEN RealizeInstances: alles blijft instanced (VRAM)."""
    old = bpy.data.node_groups.get(NG)
    if old: bpy.data.node_groups.remove(old)
    ng = bpy.data.node_groups.new(NG, 'GeometryNodeTree')
    ng.interface.new_socket("Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket("Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    nd = ng.nodes; lk = ng.links
    gin = nd.new('NodeGroupInput'); gout = nd.new('NodeGroupOutput')

    # selectie: alleen echte grond (raycast-attribuut)
    na = nd.new('GeometryNodeInputNamedAttribute'); na.data_type = 'FLOAT'; na.inputs['Name'].default_value = "grass"
    cmp = nd.new('FunctionNodeCompare'); cmp.data_type = 'FLOAT'; cmp.operation = 'GREATER_THAN'
    cmp.inputs[1].default_value = 0.5

    # density-veld: basis * noise (kale plekjes) * rand-fade
    pos = nd.new('GeometryNodeInputPosition')
    sep = nd.new('ShaderNodeSeparateXYZ')
    lk.new(pos.outputs['Position'], sep.inputs['Vector'])
    dens = nd.new('ShaderNodeValue'); dens.outputs[0].default_value = float(density) * 1.45
    field = dens.outputs[0]
    if bare:
        noi = nd.new('ShaderNodeTexNoise')
        noi.inputs['Scale'].default_value = 0.35; noi.inputs['Detail'].default_value = 3.0
        lk.new(pos.outputs['Position'], noi.inputs['Vector'])
        mr = nd.new('ShaderNodeMapRange')
        mr.inputs['From Min'].default_value = 0.34; mr.inputs['From Max'].default_value = 0.66
        mr.inputs['To Min'].default_value = 0.40;  mr.inputs['To Max'].default_value = 1.15
        lk.new(noi.outputs['Fac'], mr.inputs['Value'])
        m1 = nd.new('ShaderNodeMath'); m1.operation = 'MULTIPLY'
        lk.new(field, m1.inputs[0]); lk.new(mr.outputs['Result'], m1.inputs[1])
        field = m1.outputs[0]
    x0, x1, y0, y1 = area
    for lo, hi, out_idx in ((x0, x1, 'X'), (y0, y1, 'Y')):
        for a, bnd, rev in ((lo, lo + fade, False), (hi - fade, hi, True)):
            f = nd.new('ShaderNodeMapRange'); f.interpolation_type = 'SMOOTHSTEP'
            f.inputs['From Min'].default_value = a; f.inputs['From Max'].default_value = bnd
            f.inputs['To Min'].default_value = 1.0 if rev else 0.0
            f.inputs['To Max'].default_value = 0.0 if rev else 1.0
            lk.new(sep.outputs[out_idx], f.inputs['Value'])
            mm = nd.new('ShaderNodeMath'); mm.operation = 'MULTIPLY'
            lk.new(field, mm.inputs[0]); lk.new(f.outputs['Result'], mm.inputs[1])
            field = mm.outputs[0]

    dist = nd.new('GeometryNodeDistributePointsOnFaces'); dist.distribute_method = 'RANDOM'
    lk.new(gin.outputs['Geometry'], dist.inputs['Mesh'])
    lk.new(na.outputs['Attribute'], cmp.inputs[0])
    lk.new(cmp.outputs['Result'], dist.inputs['Selection'])
    lk.new(field, dist.inputs['Density'])

    # 3 varianten, pick instance
    ci = nd.new('GeometryNodeCollectionInfo'); ci.transform_space = 'ORIGINAL'
    ci.inputs['Collection'].default_value = coll
    ci.inputs['Separate Children'].default_value = True
    ci.inputs['Reset Children'].default_value = True
    iop = nd.new('GeometryNodeInstanceOnPoints')
    iop.inputs['Pick Instance'].default_value = True
    ridx = nd.new('FunctionNodeRandomValue'); ridx.data_type = 'INT'
    ridx.inputs[4].default_value = 0; ridx.inputs[5].default_value = len(coll.objects) - 1  # int-min/max (naam 'Min' pakt vector-socket!)
    rv = nd.new('FunctionNodeRandomValue'); rv.data_type = 'FLOAT_VECTOR'
    rv.inputs[0].default_value = (-tilt, -tilt, -3.14159)
    rv.inputs[1].default_value = (tilt, tilt, 3.14159)
    rs = nd.new('FunctionNodeRandomValue'); rs.data_type = 'FLOAT'
    rs.inputs[2].default_value = 0.6; rs.inputs[3].default_value = 1.4

    lk.new(dist.outputs['Points'], iop.inputs['Points'])
    lk.new(ci.outputs['Instances'], iop.inputs['Instance'])
    lk.new(ridx.outputs['Value'], iop.inputs['Instance Index'])
    lk.new(rv.outputs['Value'], iop.inputs['Rotation'])
    lk.new(rs.outputs['Value'], iop.inputs['Scale'])
    lk.new(iop.outputs['Instances'], gout.inputs['Geometry'])
    return ng


def add_grass(scene, area=(-10, 10, -4, 9), density=420, cell=0.40, h_mul=1.0,
              dry_frac=0.07, sat_mul=1.0, val_mul=1.0, fade=1.6, bare=True):
    """Voeg gemaskeerd gras-mix toe; idempotent (verwijdert ALLE vorige gras-
    objecten/NG, ook van eerdere handmatige scripts: GrassField/GrassTuft/
    GrassEmitter/GN_Grass*). Scene-smaak: dry_frac/sat_mul/val_mul (mediterraan:
    dry_frac 0.15, sat_mul 0.8; avond: val_mul 0.7)."""
    for o in list(bpy.data.objects):
        if o.name.startswith(("GrassEmitter", "GrassField", "GrassTuft")):
            bpy.data.objects.remove(o, do_unlink=True)
    for ngr in list(bpy.data.node_groups):
        if ngr.name.startswith("GN_Grass"):
            bpy.data.node_groups.remove(ngr)
    mat = grass_material(dry_frac=dry_frac, sat_mul=sat_mul, val_mul=val_mul)
    coll = make_tufts(h_mul, mat)
    em = build_emitter(scene, area, cell)
    ng = grass_nodegroup(coll, density, area, fade=fade)
    mod = em.modifiers.new("Grass", 'NODES'); mod.node_group = ng
    print("[grass] gras-mix toegevoegd (3 varianten, kleur/scale/tilt-variatie, kale plekjes, rand-fade)")
    return em
