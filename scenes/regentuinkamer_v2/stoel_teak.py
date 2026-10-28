r"""Teak loungefauteuil, volledig in script gebouwd (geen Meshy, geen betaald asset).

Vervangt de GLB Creator-fauteuil (Beike 28-10: "doe het liever zonder dat want het is betaald").
Herbruikbaar in andere scènes:

    import stoel_teak
    root = stoel_teak.bouw_stoel("Zit_Fauteuil_A", (x, y, z), rot_z)

Lokaal assenstelsel: front = -Y (zitkant), voet op z=0, midden op x=y=0. Maat ~0,72 x 0,80 x 0,77 m (rugkussen bovenaan).
Onderdelen (allemaal echte geometrie, geen kale boxen):
- frame: schuine voor- en achterpoten, armleuningen, zijregels, lattenzijkant (7 liggende latten),
  zitregels en zitlatten, schuine rugstijlen met rugregels; alle latten afgerond (Bevel, 3 segmenten);
- houttextuur PolyHaven teak_veneer (CC0, 2k), UV per lat langs de lengte (nerf loopt mee), per lat
  een eigen willekeurige verschuiving zodat geen twee latten hetzelfde stuk textuur tonen;
- zit- en rugkussen: subdivision met een naad rondom, ingezakt in het midden, bollend naast de naad;
  bies (9 mm) als buisje langs de naad (ronde extra 28-10); stof is procedureel (antraciet, weefsel van
  ~3 mm, slubs, kleurvariatie), dus geen extra textuur in het videogeheugen.
"""
import math
import random
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

TEAK_DIR = Path(r"D:\Blender-blokhutten\assets\polyhaven\textures\teak_veneer")
TEX_M = 1.0          # teak_veneer is 1 x 1 m (api.polyhaven.com/info/teak_veneer: dimensions 1000 mm)

# maten (m)
B = 0.72             # buitenbreedte over de armleuningen (0,74 stak in stap4 v6 buiten de kapvloer)
D = 0.80             # diepte over de poten
ARM_TOP = 0.585      # bovenkant armleuning
ZIT_TOP = 0.285      # bovenkant zitlatten
ZIJ_X = B / 2 - 0.035          # hart van het zijframe
KUSSEN_ZIT = (0.565, 0.60, 0.13)   # breed, diep, dik
KUSSEN_RUG = (0.565, 0.12, 0.36)   # breed, dik, hoog
KUSSEN_BOL = 0.012   # ronde extra: zoveel bolt de stof naast de naad op (m)
BIES_STRAAL = 0.0045  # bies 9 mm dik: in de close-up ~6 px, in de HeroCam ~2 px


# --------------------------------------------------------------------------- materialen
def _teak_materiaal():
    mat = bpy.data.materials.get("MAT_Stoel_Teak")
    if mat is not None:
        return mat
    for kaart in ("diff", "rough", "nor_gl"):
        if not (TEAK_DIR / f"teak_veneer_{kaart}_2k.jpg").exists():
            raise FileNotFoundError(f"teaktextuur ontbreekt: {TEAK_DIR / f'teak_veneer_{kaart}_2k.jpg'}")
    mat = bpy.data.materials.new("MAT_Stoel_Teak")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]

    def beeld(kaart, kleur):
        n = nt.nodes.new("ShaderNodeTexImage")
        n.image = bpy.data.images.load(str(TEAK_DIR / f"teak_veneer_{kaart}_2k.jpg"), check_existing=True)
        n.image.colorspace_settings.name = "sRGB" if kleur else "Non-Color"
        return n
    diff, rough, nor = beeld("diff", True), beeld("rough", False), beeld("nor_gl", False)
    # geoliede tuin-teak: honingkleur zoals de vorige fauteuil en de PH-bijzettafel
    hs = nt.nodes.new("ShaderNodeHueSaturation")
    hs.inputs["Hue"].default_value = 0.515      # v1 (0,49) trok naar roze; iets naar geel = honingteak
    hs.inputs["Saturation"].default_value = 0.95
    hs.inputs["Value"].default_value = 0.88
    nt.links.new(diff.outputs["Color"], hs.inputs["Color"])
    nt.links.new(hs.outputs["Color"], bsdf.inputs["Base Color"])
    # ruwheid nooit onder 0,5 (handoff G1: glimmende teak las als plastic)
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["To Min"].default_value = 0.52
    mr.inputs["To Max"].default_value = 0.78
    nt.links.new(rough.outputs["Color"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], bsdf.inputs["Roughness"])
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nm.inputs["Strength"].default_value = 0.7
    nt.links.new(nor.outputs["Color"], nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def _stof_materiaal():
    """Buitenstof (antraciet). Ronde extra 28-10: de vorige versie (albedo 0,03, weefsel van 1,5 mm,
    zwakke bump) las op 2560x1440 als vlak grijs blok. Nu: iets lichter zodat de vorm schaduw krijgt,
    weefsel van ~3 mm dat in de close-up leesbaar is, langgerekte 'slubs' (dikkere draden) in bump en
    kleur, en vlekkerige kleurvariatie. Alles procedureel: geen extra textuur in het videogeheugen."""
    mat = bpy.data.materials.get("MAT_Stoel_Kussen")
    if mat is not None:
        return mat
    mat = bpy.data.materials.new("MAT_Stoel_Kussen")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    # weefsel: twee haaks op elkaar staande golven (draad ~3 mm: Blender-golf = sin(10 x schaal x coord))
    golven = []
    for richting in ("X", "Y"):
        w = nt.nodes.new("ShaderNodeTexWave")
        w.wave_type = "BANDS"
        w.bands_direction = richting
        w.inputs["Scale"].default_value = 210.0
        w.inputs["Distortion"].default_value = 1.0
        nt.links.new(tc.outputs["Object"], w.inputs["Vector"])
        golven.append(w)
    weefsel = nt.nodes.new("ShaderNodeMath")
    weefsel.operation = "MULTIPLY"
    nt.links.new(golven[0].outputs["Fac"], weefsel.inputs[0])
    nt.links.new(golven[1].outputs["Fac"], weefsel.inputs[1])
    # slubs: ruis die in X sterk is uitgerekt (draden van enkele cm lang, ~1 mm dik)
    rek = nt.nodes.new("ShaderNodeMapping")
    rek.inputs["Scale"].default_value = (6.0, 260.0, 260.0)
    nt.links.new(tc.outputs["Object"], rek.inputs["Vector"])
    slub = nt.nodes.new("ShaderNodeTexNoise")
    slub.inputs["Scale"].default_value = 1.0
    slub.inputs["Detail"].default_value = 2.0
    nt.links.new(rek.outputs["Vector"], slub.inputs["Vector"])
    hoogte = nt.nodes.new("ShaderNodeMath")
    hoogte.operation = "MULTIPLY_ADD"                 # weefsel + 0,6 x slub
    nt.links.new(slub.outputs["Fac"], hoogte.inputs[0])
    hoogte.inputs[1].default_value = 0.6
    nt.links.new(weefsel.outputs["Value"], hoogte.inputs[2])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.45
    bump.inputs["Distance"].default_value = 0.0006
    nt.links.new(hoogte.outputs["Value"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    # kleur: vlekkerig (grove ruis) en de slubs iets lichter
    ruis = nt.nodes.new("ShaderNodeTexNoise")
    ruis.inputs["Scale"].default_value = 7.0
    ruis.inputs["Detail"].default_value = 4.0
    nt.links.new(tc.outputs["Object"], ruis.inputs["Vector"])
    kleur = nt.nodes.new("ShaderNodeMix")
    kleur.data_type = "RGBA"
    kleur.inputs[6].default_value = (0.046, 0.046, 0.048, 1.0)    # antraciet, iets warm
    kleur.inputs[7].default_value = (0.070, 0.068, 0.066, 1.0)
    nt.links.new(ruis.outputs["Fac"], kleur.inputs[0])
    draad = nt.nodes.new("ShaderNodeMix")
    draad.data_type = "RGBA"
    draad.blend_type = "SCREEN"
    draad.inputs[7].default_value = (0.05, 0.05, 0.05, 1.0)
    nt.links.new(slub.outputs["Fac"], draad.inputs[0])
    nt.links.new(kleur.outputs[2], draad.inputs[6])
    nt.links.new(draad.outputs[2], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.9
    bsdf.inputs["Sheen Weight"].default_value = 0.25
    bsdf.inputs["Sheen Roughness"].default_value = 0.5
    return mat


def _bies_materiaal():
    """Bies (piping) rond de kussens: zelfde stof, een tint lichter zodat de naad op 2560x1440 leest."""
    mat = bpy.data.materials.get("MAT_Stoel_Bies")
    if mat is not None:
        return mat
    mat = bpy.data.materials.new("MAT_Stoel_Bies")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.105, 0.100, 0.094, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.85
    bsdf.inputs["Sheen Weight"].default_value = 0.3
    bsdf.inputs["Sheen Roughness"].default_value = 0.5
    return mat


# --------------------------------------------------------------------------- hout
def _lat(bm, uv, p0, p1, breed, dik, boven=Vector((0, 0, 1)), rng=None):
    """Balk van p0 naar p1 (lengteas), doorsnede breed x dik. `boven` bepaalt waar de 'dik'-kant
    naar wijst. UV: U langs de lengte (nerf), V rondom; per lat een willekeurige verschuiving."""
    p0, p1 = Vector(p0), Vector(p1)
    u = (p1 - p0).normalized()
    w = (boven - boven.dot(u) * u).normalized()
    v = w.cross(u).normalized()
    hb, hd = breed / 2, dik / 2
    hoeken = []
    for p in (p0, p1):
        for sv, sw in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            hoeken.append(bm.verts.new(p + v * (sv * hb) + w * (sw * hd)))
    a, b = hoeken[:4], hoeken[4:]
    vlakken = [bm.faces.new((a[3], a[2], a[1], a[0])), bm.faces.new((b[0], b[1], b[2], b[3]))]
    for i in range(4):
        j = (i + 1) % 4
        vlakken.append(bm.faces.new((a[i], a[j], b[j], b[i])))
    ou, ov = (rng.random(), rng.random()) if rng else (0.0, 0.0)
    for f in vlakken:
        f.smooth = True
        n = f.normal
        for lp in f.loops:
            d = lp.vert.co - p0
            if abs(n.dot(u)) > 0.7:        # kopshout: dwarsdoorsnede
                lp[uv].uv = (d.dot(v) / TEX_M + ou, d.dot(w) / TEX_M + ov)
            elif abs(n.dot(w)) > 0.7:      # brede kant
                lp[uv].uv = (d.dot(u) / TEX_M + ou, d.dot(v) / TEX_M + ov)
            else:                          # smalle kant
                lp[uv].uv = (d.dot(u) / TEX_M + ou, d.dot(w) / TEX_M + ov + 0.37)
    return vlakken


def _frame_mesh(naam, seed):
    rng = random.Random(seed)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    X = Vector((1, 0, 0))
    y_v, y_a = -D / 2 + 0.03, D / 2 - 0.06          # voorpoot / achterpoot (boven)
    for s in (-1, 1):
        x = s * ZIJ_X
        # schuine poten (voet staat iets verder uit dan de bovenkant)
        _lat(bm, uv, (x, -D / 2 + 0.02, 0.0), (x, y_v + 0.05, ARM_TOP - 0.03), 0.048, 0.05, X, rng)
        _lat(bm, uv, (x, D / 2 - 0.02, 0.0), (x, y_a - 0.04, ARM_TOP - 0.03), 0.048, 0.05, X, rng)
        # armleuning: breed, plat, steekt voor iets uit
        _lat(bm, uv, (x - s * 0.006, -D / 2 - 0.005, ARM_TOP - 0.015), (x - s * 0.006, D / 2 - 0.04, ARM_TOP - 0.015),
             0.030, 0.075, X, rng)
        # zijregel onder (zit-hoogte) en een lage regel als voetverbinding
        _lat(bm, uv, (x, y_v - 0.005, ZIT_TOP - 0.05), (x, y_a + 0.03, ZIT_TOP - 0.05), 0.07, 0.04, X, rng)
        _lat(bm, uv, (x, -D / 2 + 0.05, 0.10), (x, D / 2 - 0.05, 0.10), 0.035, 0.03, X, rng)
        # lattenzijkant: 7 liggende latten tussen zijregel en armleuning
        n, onder, boven = 7, ZIT_TOP - 0.01, ARM_TOP - 0.035
        stap = (boven - onder) / n
        for i in range(n):
            z = onder + stap * (i + 0.5)
            _lat(bm, uv, (x, y_v + 0.025, z), (x, y_a - 0.005, z),
                 0.026, 0.022, X, rng)
    # zitregels voor en achter, zitlatten dwars
    _lat(bm, uv, (-ZIJ_X + 0.02, y_v + 0.01, ZIT_TOP - 0.045), (ZIJ_X - 0.02, y_v + 0.01, ZIT_TOP - 0.045),
         0.07, 0.035, Vector((0, -1, 0)), rng)
    _lat(bm, uv, (-ZIJ_X + 0.02, y_a - 0.01, ZIT_TOP - 0.045), (ZIJ_X - 0.02, y_a - 0.01, ZIT_TOP - 0.045),
         0.06, 0.035, Vector((0, 1, 0)), rng)
    for i in range(6):
        y = y_v + 0.06 + i * (y_a - y_v - 0.10) / 5
        _lat(bm, uv, (-ZIJ_X + 0.03, y, ZIT_TOP - 0.01), (ZIJ_X - 0.03, y, ZIT_TOP - 0.01), 0.07, 0.018,
             Vector((0, 0, 1)), rng)
    # rug: schuine stijlen (~16 graden achterover) met liggende rugregels
    rug_x = ZIJ_X - 0.045
    r0, r1 = Vector((0, y_a - 0.07, ZIT_TOP - 0.06)), Vector((0, D / 2, 0.72))
    rug_dir = (r1 - r0).normalized()
    rug_n = Vector((0, -rug_dir.z, rug_dir.y))       # loodrecht op de rug, naar voren-boven
    for s in (-1, 1):
        _lat(bm, uv, r0 + Vector((s * rug_x, 0, 0)), r1 + Vector((s * rug_x, 0, 0)), 0.045, 0.04, rug_n, rng)
    for i in range(5):
        t = 0.16 + i * 0.19
        p = r0.lerp(r1, t) + rug_n * 0.012
        _lat(bm, uv, p + Vector((-rug_x - 0.02, 0, 0)), p + Vector((rug_x + 0.02, 0, 0)), 0.065, 0.018, rug_n, rng)
    me = bpy.data.meshes.new(naam)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(_teak_materiaal())
    return me, (r0, r1, rug_dir, rug_n)


# --------------------------------------------------------------------------- kussens
def _kussen_mesh(naam, maat, zak, seed):
    """Kussen: box met 6 x 6 x 2 vlakken, rondom een naad op halve dikte (crease) en Subdivision.
    zak = hoeveel het midden van de bovenkant inzakt (m)."""
    rng = random.Random(seed)
    bx, by, bz = maat
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(bx, by, bz), verts=bm.verts)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=5, use_grid_fill=True)
    # naad: de rand van boven- en ondervlak hard houden zodat er een bies ontstaat
    crease = bm.edges.layers.float.new("crease_edge")
    for e in bm.edges:
        a, b = e.verts
        if abs(abs(a.co.z) - bz / 2) < 1e-4 and abs(abs(b.co.z) - bz / 2) < 1e-4:
            buiten = all(abs(abs(v.co.x) - bx / 2) < 1e-4 or abs(abs(v.co.y) - by / 2) < 1e-4 for v in e.verts)
            if buiten:
                e[crease] = 1.0
    # naad: de randlus van boven- en ondervlak 4 mm naar buiten, zodat er een bies (lip) ontstaat
    for v in bm.verts:
        if abs(abs(v.co.z) - bz / 2) < 1e-4 and (abs(abs(v.co.x) - bx / 2) < 1e-4 or abs(abs(v.co.y) - by / 2) < 1e-4):
            v.co.x += math.copysign(0.004, v.co.x) if abs(abs(v.co.x) - bx / 2) < 1e-4 else 0.0
            v.co.y += math.copysign(0.004, v.co.y) if abs(abs(v.co.y) - by / 2) < 1e-4 else 0.0
    # randlussen (de naad) onthouden voor de bies; volgorde rondom = hoek rond het midden
    randen = {+1: [], -1: []}
    for v in bm.verts:
        if abs(abs(v.co.z) - bz / 2) < 1e-4 and (abs(v.co.x) > bx / 2 + 1e-3 or abs(v.co.y) > by / 2 + 1e-3):
            randen[1 if v.co.z > 0 else -1].append(v)
    for v in bm.verts:
        nx, ny = 2 * v.co.x / bx, 2 * v.co.y / by
        midden = max(0.0, 1 - nx * nx) * max(0.0, 1 - ny * ny)
        # ronde extra: bolling naast de naad (de stof rolt over de bies heen); 0 op de naad zelf
        rand = min(1.0, max(abs(nx), abs(ny)))
        bol = KUSSEN_BOL * (1 - rand ** 6)
        if v.co.z > 0:                       # bovenkant zakt in waar je zit
            v.co.z += bol - zak * midden - rng.uniform(0, 0.003)
        else:
            v.co.z += 0.25 * zak * midden - 0.3 * bol
        # zijkanten bollen op (ronde extra: 0,03 -> 0,055)
        zf = 1 - (2 * v.co.z / bz) ** 2
        v.co.x *= 1 + 0.055 * max(0.0, zf)
        v.co.y *= 1 + 0.055 * max(0.0, zf)
    lussen = []
    for kant in (1, -1):
        lus = sorted(randen[kant], key=lambda v: math.atan2(v.co.y / by, v.co.x / bx))
        lussen.append([v.co.copy() for v in lus])
    for f in bm.faces:
        f.smooth = True
    me = bpy.data.meshes.new(naam)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(_stof_materiaal())
    return me, lussen


def _bies_curve(naam, lus):
    """Bies als buisje langs de naad. Cyclische NURBS van orde 4 door de randlus: dat is precies de
    limietkromme van een volledig gecreasede lus onder Subdivision, dus de bies volgt de naad."""
    cu = bpy.data.curves.new(naam, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = BIES_STRAAL
    cu.bevel_resolution = 2
    cu.resolution_u = 4
    sp = cu.splines.new("NURBS")
    sp.points.add(len(lus) - 1)
    for p, co in zip(sp.points, lus):
        p.co = (co.x, co.y, co.z, 1.0)
    sp.use_cyclic_u = True
    sp.order_u = 4
    sp.use_smooth = True
    cu.materials.append(_bies_materiaal())
    return cu


# --------------------------------------------------------------------------- samenstellen
def bouw_stoel(naam, loc, rot_z, collectie=None, seed=1):
    """Bouwt de fauteuil onder een lege root `naam` op loc (voet op loc.z), gedraaid rot_z (rad).
    Geeft de root terug; de meshes heten <naam>_Frame, <naam>_Kussen_Zit, <naam>_Kussen_Rug; de biezen
    (curves) <naam>_Kussen_Zit_Bies0/1 en <naam>_Kussen_Rug_Bies0/1."""
    coll = collectie or bpy.context.scene.collection
    root = bpy.data.objects.new(naam, None)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.3
    coll.objects.link(root)
    obs = []
    me, (r0, r1, rug_dir, rug_n) = _frame_mesh(f"{naam}_Frame", seed)
    frame = bpy.data.objects.new(f"{naam}_Frame", me)
    bev = frame.modifiers.new("Afronding", "BEVEL")
    bev.width = 0.005
    bev.segments = 3
    bev.limit_method = "ANGLE"
    bev.harden_normals = True
    obs.append(frame)

    zit_me, zit_lussen = _kussen_mesh(f"{naam}_Kussen_Zit", KUSSEN_ZIT, 0.022, seed + 7)
    zit = bpy.data.objects.new(f"{naam}_Kussen_Zit", zit_me)
    zit.location = (0.0, -0.035, ZIT_TOP + KUSSEN_ZIT[2] / 2 - 0.004)
    obs.append(zit)
    # rugkussen: staat op het zitkussen en leunt tegen de rugregels
    bx, dik, h = KUSSEN_RUG
    rug_me, rug_lussen = _kussen_mesh(f"{naam}_Kussen_Rug", (bx, h, dik), 0.018, seed + 11)
    rug = bpy.data.objects.new(f"{naam}_Kussen_Rug", rug_me)
    hoek = math.atan2(rug_dir.y, rug_dir.z)          # helling van de rug t.o.v. verticaal
    # onderkant op het zitkussen (3 cm ingedrukt), voorkant van de rugregels + halve dikte (1 cm ingedrukt)
    t0 = (ZIT_TOP + KUSSEN_ZIT[2] - 0.03 - r0.z) / (r1.z - r0.z)
    midden = r0.lerp(r1, t0) + rug_dir * (h / 2) + rug_n * (0.021 + dik / 2 - 0.01)
    # lokaal: kussen-z = dikte; +90 graden om X zet de (ingezakte) bovenkant naar voren (-Y),
    # daarna -hoek om X: achterover hellen zoals de rug
    rug.matrix_basis = Matrix.Translation(midden) @ Matrix.Rotation(math.pi / 2 - hoek, 4, "X")
    obs.append(rug)
    for k in (zit, rug):
        sub = k.modifiers.new("Zacht", "SUBSURF")
        sub.levels = 2
        sub.render_levels = 2
    for o in obs:
        coll.objects.link(o)
        o.parent = root
    # bies langs de naad boven en onder, als kind van het kussen (lokaal = kussenmaat)
    for kussen, lussen in ((zit, zit_lussen), (rug, rug_lussen)):
        for i, lus in enumerate(lussen):
            b = bpy.data.objects.new(f"{kussen.name}_Bies{i}", _bies_curve(f"{kussen.name}_Bies{i}", lus))
            coll.objects.link(b)
            b.parent = kussen
    root.location = loc
    root.rotation_euler = (0.0, 0.0, rot_z)
    return root


def info(root):
    """Polycount (na modifiers) en materialen, voor de audit."""
    dg = bpy.context.evaluated_depsgraph_get()
    tris, mats = 0, set()
    for o in root.children_recursive:
        if o.type not in ("MESH", "CURVE"):
            continue
        e = o.evaluated_get(dg)
        m = e.to_mesh()
        tris += sum(len(p.vertices) - 2 for p in m.polygons)
        e.to_mesh_clear()
        mats |= {s.material.name for s in o.material_slots if s.material}
    return {"driehoeken": tris, "materialen": sorted(mats)}
