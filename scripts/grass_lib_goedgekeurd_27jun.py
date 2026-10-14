"""Herbruikbare gras-module: gekruiste-blad-sprietjes + GN-scatter die ALLEEN op
echte grond valt (raycast omlaag: hardscape/deck/pad/water/grind/hut -> geen gras).
Gebruik:
    import grass_lib as gl
    gl.add_grass(scene, area=(-10,10,-4,9), density=180)
"""
import bpy, bmesh, math, random
from mathutils import Vector

GRASS_MAT = "MAT_GrassBlade"
TUFT = "GrassTuft_X"
EMITTER = "GrassEmitter"
NG = "GN_GrassMasked"

# VEILIG: gras ALLEEN waar de bovenste geraakte vlak de echte grondplaat is.
# Zo komt er nooit gras op een ANDER vloer-oppervlak (deck/terras/hottub/pad/water),
# ook niet op vloeren die niet bij naam bekend zijn (die raakt de ray i.p.v. de grond).
GROUND_KW = ("ground", "grass", "gras", "terrain", "grond", "lawn", "gazon", "weide", "veld")

def grass_material():
    m = bpy.data.materials.get(GRASS_MAT)
    if m: return m
    m = bpy.data.materials.new(GRASS_MAT); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Roughness'].default_value = 0.85
    # donkere wortel -> frisser groene tip via object-Z
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Generated'], sep.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[0].color = (0.035, 0.115, 0.022, 1)
    ramp.color_ramp.elements[1].position = 1.0; ramp.color_ramp.elements[1].color = (0.115, 0.255, 0.060, 1)
    nt.links.new(sep.outputs['Z'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return m

def make_tuft():
    old = bpy.data.objects.get(TUFT)
    if old: bpy.data.objects.remove(old, do_unlink=True)
    me = bpy.data.meshes.new(TUFT); bm = bmesh.new(); rr = random.Random(7)
    for _ in range(8):
        ang = rr.uniform(0, 6.283); lean = rr.uniform(0.004, 0.028); h = rr.uniform(0.035, 0.075); w = 0.007
        cx, cy = math.cos(ang) * 0.011, math.sin(ang) * 0.011
        tx, ty = cx + math.cos(ang) * lean, cy + math.sin(ang) * lean
        for (ox, oy) in ((math.cos(ang) * w, math.sin(ang) * w), (-math.sin(ang) * w, math.cos(ang) * w)):
            v1 = bm.verts.new((cx - ox, cy - oy, 0)); v2 = bm.verts.new((cx + ox, cy + oy, 0))
            v3 = bm.verts.new((tx, ty, h))
            bm.faces.new((v1, v2, v3))   # gekruiste bladen (2 vlakken per spriet, alle hoeken zichtbaar)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(TUFT, me); bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(grass_material()); o.hide_render = True; o.hide_viewport = True
    return o

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

def grass_nodegroup(tuft, density):
    old = bpy.data.node_groups.get(NG)
    if old: bpy.data.node_groups.remove(old)
    ng = bpy.data.node_groups.new(NG, 'GeometryNodeTree')
    ng.interface.new_socket("Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket("Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    nd = ng.nodes; lk = ng.links
    gin = nd.new('NodeGroupInput'); gout = nd.new('NodeGroupOutput')
    na = nd.new('GeometryNodeInputNamedAttribute'); na.data_type = 'FLOAT'; na.inputs['Name'].default_value = "grass"
    cmp = nd.new('FunctionNodeCompare'); cmp.data_type = 'FLOAT'; cmp.operation = 'GREATER_THAN'
    cmp.inputs[1].default_value = 0.5
    dist = nd.new('GeometryNodeDistributePointsOnFaces'); dist.distribute_method = 'RANDOM'
    dist.inputs['Density'].default_value = float(density)
    oi = nd.new('GeometryNodeObjectInfo'); oi.inputs['Object'].default_value = tuft
    iop = nd.new('GeometryNodeInstanceOnPoints')
    rv = nd.new('FunctionNodeRandomValue'); rv.data_type = 'FLOAT_VECTOR'
    rv.inputs[0].default_value = (0, 0, -3.14159); rv.inputs[1].default_value = (0, 0, 3.14159)
    rs = nd.new('FunctionNodeRandomValue'); rs.data_type = 'FLOAT'; rs.inputs[2].default_value = 0.7; rs.inputs[3].default_value = 1.4
    real = nd.new('GeometryNodeRealizeInstances')
    lk.new(gin.outputs['Geometry'], dist.inputs['Mesh'])
    lk.new(na.outputs['Attribute'], cmp.inputs[0])
    lk.new(cmp.outputs['Result'], dist.inputs['Selection'])
    lk.new(dist.outputs['Points'], iop.inputs['Points'])
    lk.new(oi.outputs['Geometry'], iop.inputs['Instance'])
    lk.new(rv.outputs['Value'], iop.inputs['Rotation'])
    lk.new(rs.outputs['Value'], iop.inputs['Scale'])
    lk.new(iop.outputs['Instances'], real.inputs['Geometry'])
    lk.new(real.outputs['Geometry'], gout.inputs['Geometry'])
    return ng

def add_grass(scene, area=(-10, 10, -4, 9), density=420, cell=0.40):
    """Voeg gemaskeerd gras toe; idempotent (verwijdert ALLE vorige gras-objecten/NG,
    ook van eerdere handmatige scripts: GrassField/GrassTuft/GrassEmitter/GN_Grass*)."""
    for o in list(bpy.data.objects):
        if o.name.startswith(("GrassEmitter", "GrassField", "GrassTuft")):
            bpy.data.objects.remove(o, do_unlink=True)
    for ng in list(bpy.data.node_groups):
        if ng.name.startswith("GN_Grass"):
            bpy.data.node_groups.remove(ng)
    tuft = make_tuft()
    em = build_emitter(scene, area, cell)
    ng = grass_nodegroup(tuft, density)
    mod = em.modifiers.new("Grass", 'NODES'); mod.node_group = ng
    print("[grass] gemaskeerd gras toegevoegd (alleen op echte grond)")
    return em
