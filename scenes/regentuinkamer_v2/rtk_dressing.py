"""Helpers voor de dressing-lagen van Renders 2.0, pilot De Regentuinkamer (stap2..stap4).

Naast rtk_lib (anker-helpers, niet gewijzigd op .exr in fix_image_ext na). Hier:
- soort_donor: een plant/steen/meubel uit een asset-blend als donorcollectie, transformaties
  ingebakken en gecentreerd (voet op z=0), zodat een GN-instance precies op zijn punt staat;
- plaats_soort: een vaste lijst punten (x, y, z, draaiing, schaal, variant) als GN-instancer.
  De punten staan als attributen op de mesh; de audit leest ze daar terug;
- bekken-bodem (reliëf met twee kommen), waterplassen per kom (flood fill, nooit overlappend);
- toetsen voor de dressing: instances op de echte GN-uitvoer (zwevend, ondergestopt, in de hut,
  op pad/schort/kapvloer, ondersteboven) en een kloon-/rijencheck;
- render_diag: videokaart-controle, GPU_BEZET.txt zetten en weghalen, geheugenpiek via nvidia-smi.

Tuinframe zoals rtk_lib: X 0-14 oost, Y 0-12 noord, meters.
"""
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

SCENE_DIR = Path(r"D:\Blender-blokhutten\scenes\regentuinkamer_v2")
sys.path.insert(0, str(SCENE_DIR))
import rtk_lib as rl  # noqa: E402

cl = rl.cl
ROOT = rl.ROOT
ASSETS = ROOT / "assets"
PH_MODELS = ASSETS / "polyhaven" / "models"
PH_TEX = ASSETS / "polyhaven" / "textures"
BK = ASSETS / "blenderkit"
GPU_BEZET = Path(r"D:\Beeldherkenning\GPU_BEZET.txt")
ANKER_VERSIE = os.environ.get("RTK_ANKER", "v5")
ANKER_AUDIT = SCENE_DIR / "previews" / "_werk" / f"anker_{ANKER_VERSIE}" / "audit.json"
PREVIEW_RES, PREVIEW_SAMPLES = (960, 540), 24
RtkFout = rl.RtkFout


def log(*a):
    print("[dressing]", *a, flush=True)


def meting_anker():
    """Hutmeting uit de audit van het goedgekeurde anker (deur, envelop, binnenruimte)."""
    if not ANKER_AUDIT.exists():
        raise RtkFout(f"anker-audit ontbreekt: {ANKER_AUDIT}")
    return json.loads(ANKER_AUDIT.read_text(encoding="utf-8"))["hut"]


def open_invoer(pad):
    pad = Path(pad)
    if not pad.exists():
        raise RtkFout(f"invoerbestand ontbreekt: {pad} (vorige laag eerst draaien)")
    if Path(bpy.data.filepath) != pad:
        bpy.ops.wm.open_mainfile(filepath=str(pad))
    log("geopend:", pad.name)


def verwijder_vorige(prefixen):
    """Herhaalbaar: objecten van deze laag uit een eerdere run weghalen (alleen eigen prefixen)."""
    weg = [o for o in bpy.data.objects if o.name.startswith(tuple(prefixen))]
    for o in weg:
        bpy.data.objects.remove(o, do_unlink=True)
    return len(weg)


def schrijf_json(pad, data):
    pad.parent.mkdir(parents=True, exist_ok=True)
    pad.write_text(json.dumps(data, indent=1, ensure_ascii=False, default=str), encoding="utf-8")


def smoothstep(a, b, x):
    t = min(1.0, max(0.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


# --------------------------------------------------------------------------- bekkenvorm
def bekken_r(th):
    """Straalfactor van de bekkenomtrek op hoek th (zelfde formule als rl.basin_n)."""
    return 1 + 0.18 * math.sin(2 * th + 0.7) + 0.12 * math.sin(3 * th - 1.1) + 0.07 * math.sin(5 * th + 2.0)


def bekken_punt(th, n):
    """Punt op genormaliseerde afstand n (1 = rand) in richting th (0 = oost, pi/2 = noord)."""
    r = bekken_r(th) * n
    return rl.BC[0] + r * math.cos(th) * rl.BRX, rl.BC[1] + r * math.sin(th) * rl.BRY


# Bodemreliëf in de kern (laag 2): twee kommen met een lage drempel ertussen, zodat de twee
# plassen elk een eigen waterlijn hebben en nooit op dezelfde z of in elkaar liggen.
# v5 (opdracht projectsessie): plassen van elk 1-2,5 m2 in het laagste deel, dus ruimere kommen
KOM_A = (4.18, 6.02, 1.00, 0.065)        # x, y, straal, diepte (fix_gazon_v4: straal 0,85 -> 1,00)
KOM_B = (5.33, 4.62, 0.90, 0.060)        # fix_gazon_v4: straal 0,75 -> 0,90
DREMPEL_H, DREMPEL_B, DREMPEL_L = 0.090, 0.20, 1.4   # fix_gazon_v4: 0,065 -> 0,09 (plassen liepen bij ~1,2 m2 al in elkaar)
BODEM_MIN_DIEPTE = 0.010                 # bodemmesh vanaf deze bekkendiepte (rand ligt onder het gras)
BODEM_LIFT = 0.005                       # boven Ground_Tuin (v6: 1,5 mm liet de 0,30-m-vlakken aan de rand doorsteken)


def bodem_relief(x, y):
    ax, ay, ar, ad = KOM_A
    bx, by, br, bd = KOM_B
    rel = -ad * math.exp(-((x - ax) ** 2 + (y - ay) ** 2) / ar ** 2)
    rel -= bd * math.exp(-((x - bx) ** 2 + (y - by) ** 2) / br ** 2)
    mx, my = (ax + bx) / 2, (ay + by) / 2
    ux, uy = bx - ax, by - ay
    ll = math.hypot(ux, uy)
    d = abs((x - mx) * ux / ll + (y - my) * uy / ll)
    rel += DREMPEL_H * math.exp(-(d / DREMPEL_B) ** 2) * math.exp(-(math.hypot(x - mx, y - my) / DREMPEL_L) ** 2)
    rel += 0.0015 * math.sin(7.3 * x + 1.1) * math.sin(6.1 * y + 0.4)      # kleine onregelmatigheid
    return rel


_GROND_BVH = {}


def grond_mesh_z(x, y):
    """Echte hoogte van de Ground_Tuin-mesh (raster 0,30 m). In de holle kom ligt de mesh tot
    enkele mm boven rl.ground_height (koorden boven de kromme): v1 van laag 2 liet daardoor de
    rode aarde van het anker door de nieuwe bodem steken."""
    if "bvh" not in _GROND_BVH:
        from mathutils.bvhtree import BVHTree
        g = bpy.data.objects["Ground_Tuin"]
        _GROND_BVH["bvh"] = BVHTree.FromObject(g, bpy.context.evaluated_depsgraph_get())
        _GROND_BVH["mw"] = g.matrix_world.copy()
        _GROND_BVH["inv"] = g.matrix_world.inverted()
    inv, mw = _GROND_BVH["inv"], _GROND_BVH["mw"]
    o = inv @ Vector((x, y, 5.0))
    d = (inv.to_3x3() @ Vector((0.0, 0.0, -1.0))).normalized()
    hit = _GROND_BVH["bvh"].ray_cast(o, d, 20.0)
    if hit[0] is None:
        return rl.ground_height(x, y)
    return (mw @ hit[0]).z


def bodem_z(x, y):
    """Hoogte van de bekkenbodem (laag 2) of None buiten de bodemmesh."""
    dp = rl.basin_depth(x, y)
    if dp <= BODEM_MIN_DIEPTE:
        return None
    w = smoothstep(0.03, 0.08, dp)
    basis = max(rl.ground_height(x, y), grond_mesh_z(x, y))
    return basis + BODEM_LIFT + bodem_relief(x, y) * w


KAPVLOER_RECT = (10.54, 13.10, 8.003, 10.515)   # oost van de gesloten muur (X 10,538), voor de achterwand (Y 10,519)
KAPVLOER_TOP = 0.033                             # schort-top 0,039 min 6 mm: geen doorsteken bij de naad


def oppervlak_z(x, y):
    """Waar een voet hoort te staan: kapvloer (laag 4), bekkenbodem, borderbed (+0,006) of maaiveld."""
    if "Kapvloer_Steen" in bpy.data.objects and rl.sdf_rect(x, y, KAPVLOER_RECT) < 0.0:
        return KAPVLOER_TOP
    bz = bodem_z(x, y)
    if bz is not None:
        return bz
    for rect in BEDDEN.values():
        if rl.sdf_rect(x, y, rect) < 0.0:
            return rl.ground_height(x, y) + 0.006
    return rl.ground_height(x, y)


BEDDEN = {"Bed_Oost": (10.0, 13.2, 1.2, 5.8), "Bed_West": (1.0, 2.5, 6.5, 10.5)}   # = stap1_anker.BEDDEN


# --------------------------------------------------------------------------- donors
def _bak_in(o):
    """Wereldtransformatie (uit de ouderketen, ook als de collectie uitgesloten is) in de mesh bakken."""
    m = o.matrix_basis.copy()
    p = o
    while p.parent is not None:
        m = p.parent.matrix_basis @ p.matrix_parent_inverse @ m
        p = p.parent
    if o.type == "MESH":
        if o.data.users > 1:
            o.data = o.data.copy()
        o.data.transform(m)
    o.parent = None
    o.matrix_basis = Matrix.Identity(4)


def _bbox_mesh(objs):
    import numpy as np
    alle = []
    for o in objs:
        n = len(o.data.vertices)
        co = np.empty(n * 3, dtype=np.float32)
        o.data.vertices.foreach_get("co", co)
        alle.append(co.reshape(n, 3))
    a = np.concatenate(alle)
    return a.min(axis=0), a.max(axis=0)


def soort_donor(blend, label, kies, geheel=False, verwacht_h=None):
    """Asset-blend als donorcollectie onder RTK_Donors.

    kies(naam) -> welke objecten mee. geheel=True: alle gekozen meshes samen vormen één plant
    (één instance); anders is elke mesh een eigen variant. Transformaties worden in de mesh
    gebakken; elke variant (of het geheel) wordt gecentreerd met de voet op z=0.
    verwacht_h = (min, max) in m: anders RtkFout (verkeerde schaal of liggend asset).
    """
    blend = Path(blend)
    if not blend.exists():
        raise RtkFout(f"asset ontbreekt: {blend}")
    with bpy.data.libraries.load(str(blend), link=False) as (src, dst):
        dst.objects = [n for n in src.objects if kies(n)]
    objs = [o for o in dst.objects if o is not None]
    if not objs:
        raise RtkFout(f"{label}: niets gekozen uit {blend.name}")
    coll = bpy.data.collections.new(f"RTK_D_{label}")
    rl.donor_collection().children.link(coll)
    for o in objs:
        coll.objects.link(o)
    for o in objs:
        _bak_in(o)
    meshes = [o for o in objs if o.type == "MESH"]
    for o in objs:
        if o.type != "MESH":
            coll.objects.unlink(o)
    groepen = [meshes] if geheel else [[o] for o in meshes]
    varianten = []
    for g in groepen:
        mn, mx = _bbox_mesh(g)
        t = Matrix.Translation((-(mn[0] + mx[0]) / 2, -(mn[1] + mx[1]) / 2, -mn[2]))
        for o in g:
            o.data.transform(t)
            o.hide_render = False
            o.hide_viewport = False
        h, w = float(mx[2] - mn[2]), float(max(mx[0] - mn[0], mx[1] - mn[1]))
        varianten.append({"naam": g[0].name if not geheel else label, "h": round(h, 3), "w": round(w, 3),
                          "verts": sum(len(o.data.vertices) for o in g)})
        if verwacht_h and not (verwacht_h[0] <= h <= verwacht_h[1]):
            raise RtkFout(f"{label}/{g[0].name}: hoogte {h:.2f} m buiten verwacht {verwacht_h}: "
                          f"liggend of verkeerd geschaald asset")
    gerepareerd = rl.fix_image_ext()
    info = {"label": label, "bestand": str(blend), "coll": coll, "geheel": geheel,
            "varianten": varianten, "objnamen": [o.name for o in meshes], "beeldpad_gerepareerd": gerepareerd}
    log(f"donor {label}: {len(varianten)} variant(en), "
        f"h {[v['h'] for v in varianten]}, verts {sum(v['verts'] for v in varianten)}")
    return info


def donor_info_json(d):
    return {k: v for k, v in d.items() if k != "coll"}


# --------------------------------------------------------------------------- plaatsen
def plaats_soort(naam, donor, punten, attrs=None):
    """punten: lijst dicts met x, y, z, rot, s, v (variant). Eén mesh-object met die punten als
    vertices + attributen (variant/rot/schaal en optioneel extra float-attributen uit attrs:
    {naam: [waarde per punt]}) en een GN-modifier die er de donor op zet."""
    if not punten:
        raise RtkFout(f"{naam}: geen punten")
    cx = sum(p["x"] for p in punten) / len(punten)
    cy = sum(p["y"] for p in punten) / len(punten)
    me = bpy.data.meshes.new(naam)
    me.from_pydata([(p["x"] - cx, p["y"] - cy, p["z"]) for p in punten], [], [])
    for an, typ, waarden in (("variant", "INT", [int(p["v"]) for p in punten]),
                             ("rot", "FLOAT", [float(p["rot"]) for p in punten]),
                             ("schaal", "FLOAT", [float(p["s"]) for p in punten])):
        me.attributes.new(an, typ, "POINT").data.foreach_set("value", waarden)
    for an, waarden in (attrs or {}).items():
        me.attributes.new(an, "FLOAT", "POINT").data.foreach_set("value", [float(w) for w in waarden])
    ob = bpy.data.objects.new(naam, me)
    ob.location = (cx, cy, 0.0)
    bpy.context.scene.collection.objects.link(ob)

    n_var = len(donor["varianten"])
    ng = bpy.data.node_groups.new(f"RTK_Plaats_{naam}", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    nd, lk = ng.nodes, ng.links
    gi, go = nd.new("NodeGroupInput"), nd.new("NodeGroupOutput")
    mp = nd.new("GeometryNodeMeshToPoints")
    iop = nd.new("GeometryNodeInstanceOnPoints")
    ci = nd.new("GeometryNodeCollectionInfo")
    ci.inputs["Collection"].default_value = donor["coll"]
    ci.inputs["Separate Children"].default_value = n_var > 1
    ci.inputs["Reset Children"].default_value = n_var > 1
    lk.new(gi.outputs[0], mp.inputs["Mesh"])
    lk.new(mp.outputs["Points"], iop.inputs["Points"])
    lk.new(ci.outputs[0], iop.inputs["Instance"])

    def attr(an, typ):
        a = nd.new("GeometryNodeInputNamedAttribute")
        a.data_type = typ
        a.inputs["Name"].default_value = an
        return a.outputs["Attribute"]
    if n_var > 1:
        iop.inputs["Pick Instance"].default_value = True
        lk.new(attr("variant", "INT"), iop.inputs["Instance Index"])
    cz = nd.new("ShaderNodeCombineXYZ")
    lk.new(attr("rot", "FLOAT"), cz.inputs["Z"])
    lk.new(cz.outputs["Vector"], iop.inputs["Rotation"])
    lk.new(attr("schaal", "FLOAT"), iop.inputs["Scale"])
    lk.new(iop.outputs["Instances"], go.inputs[0])
    m = ob.modifiers.new("Plaats", "NODES")
    m.node_group = ng
    ob["rtk_donor"] = donor["label"]
    ob["rtk_dressing"] = True
    return ob


def punten_van(ob):
    """De punten zoals ze echt op de mesh staan (wereld-xy, z, rot, schaal, variant)."""
    me = ob.data
    n = len(me.vertices)
    uit = []
    rot = [0.0] * n
    sch = [0.0] * n
    var = [0] * n
    me.attributes["rot"].data.foreach_get("value", rot)
    me.attributes["schaal"].data.foreach_get("value", sch)
    me.attributes["variant"].data.foreach_get("value", var)
    for i, v in enumerate(me.vertices):
        w = ob.matrix_world @ v.co
        uit.append({"x": w.x, "y": w.y, "z": w.z, "rot": rot[i], "s": sch[i], "v": var[i]})
    return uit


# --------------------------------------------------------------------------- materialen
def instancer_nat(mat, donker=0.5, ruw_min=0.45):
    """Materiaal leest het instance-attribuut 'nat' (0 droog .. 1 nat): donkerder en gladder."""
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    at = nt.nodes.new("ShaderNodeAttribute")
    at.attribute_type = "INSTANCER"
    at.attribute_name = "nat"
    for lk in list(bsdf.inputs["Base Color"].links):
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.blend_type = "MULTIPLY"
        nt.links.new(at.outputs["Fac"], mix.inputs[0])
        mix.inputs[7].default_value = (donker, donker, donker * 0.96, 1.0)
        nt.links.new(lk.from_socket, mix.inputs[6])
        nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    nt.links.new(at.outputs["Fac"], mr.inputs["Value"])
    mr.inputs["To Min"].default_value = 1.0
    mr.inputs["To Max"].default_value = ruw_min
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    nt.links.new(mr.outputs["Result"], mul.inputs[1])
    links = list(bsdf.inputs["Roughness"].links)
    if links:
        nt.links.new(links[0].from_socket, mul.inputs[0])
    else:
        mul.inputs[0].default_value = bsdf.inputs["Roughness"].default_value
    nt.links.new(mul.outputs["Value"], bsdf.inputs["Roughness"])
    return mat


def kleur_bijstellen(mat, beeld_sleutel, hue=0.5, sat=1.0, val=1.0):
    """HueSat achter elke beeldnode waarvan de naam beeld_sleutel bevat (Base Color-pad)."""
    nt = mat.node_tree
    n_aangepast = 0
    for n in [n for n in nt.nodes if n.type == "TEX_IMAGE" and n.image
              and beeld_sleutel.lower() in n.image.name.lower()]:
        for lk in list(n.outputs["Color"].links):
            hs = nt.nodes.new("ShaderNodeHueSaturation")
            hs.inputs["Hue"].default_value = hue
            hs.inputs["Saturation"].default_value = sat
            hs.inputs["Value"].default_value = val
            doel = lk.to_socket
            nt.links.remove(lk)
            nt.links.new(n.outputs["Color"], hs.inputs["Color"])
            nt.links.new(hs.outputs["Color"], doel)
            n_aangepast += 1
    return n_aangepast


def basiskleur_bijstellen(mat, hue=0.5, sat=1.0, val=1.0):
    """HueSat vlak voor Base Color van de Principled (na alle eigen kleurnodes van het asset)."""
    nt = mat.node_tree
    bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if bsdf is None or not bsdf.inputs["Base Color"].is_linked:
        return 0
    lk = bsdf.inputs["Base Color"].links[0]
    hs = nt.nodes.new("ShaderNodeHueSaturation")
    hs.inputs["Hue"].default_value = hue
    hs.inputs["Saturation"].default_value = sat
    hs.inputs["Value"].default_value = val
    bron = lk.from_socket
    nt.links.remove(lk)
    nt.links.new(bron, hs.inputs["Color"])
    nt.links.new(hs.outputs["Color"], bsdf.inputs["Base Color"])
    return 1


def bloemen_herkleuren(mat, beeld_sleutel, hue=0.56, sat=0.35, val=1.15, drempel=(0.04, 0.20), vaste_kleur=None):
    """Alleen de bloemen in een gecombineerde blad+bloem-textuur herkleuren (PH periwinkle is roze;
    ontwerp vraagt wit/lichtviolet). Masker = R - G: blad is groen (R < G), roze bloem R >> G.
    Het blad blijft zoals het is."""
    nt = mat.node_tree
    n_aangepast = 0
    for n in [n for n in nt.nodes if n.type == "TEX_IMAGE" and n.image
              and beeld_sleutel.lower() in n.image.name.lower()]:
        for lk in list(n.outputs["Color"].links):
            sep = nt.nodes.new("ShaderNodeSeparateColor")
            nt.links.new(n.outputs["Color"], sep.inputs["Color"])
            sub = nt.nodes.new("ShaderNodeMath")
            sub.operation = "SUBTRACT"
            nt.links.new(sep.outputs[0], sub.inputs[0])
            nt.links.new(sep.outputs[1], sub.inputs[1])
            mr = nt.nodes.new("ShaderNodeMapRange")
            mr.inputs["From Min"].default_value, mr.inputs["From Max"].default_value = drempel
            nt.links.new(sub.outputs["Value"], mr.inputs["Value"])
            hs = nt.nodes.new("ShaderNodeHueSaturation")
            hs.inputs["Hue"].default_value = hue
            hs.inputs["Saturation"].default_value = sat
            hs.inputs["Value"].default_value = val
            nt.links.new(n.outputs["Color"], hs.inputs["Color"])
            mix = nt.nodes.new("ShaderNodeMix")
            mix.data_type = "RGBA"
            nt.links.new(mr.outputs["Result"], mix.inputs[0])
            nt.links.new(n.outputs["Color"], mix.inputs[6])
            if vaste_kleur is None:
                nt.links.new(hs.outputs["Color"], mix.inputs[7])
            else:                          # bv. bladgroen: bodembedekker zonder bloemen
                mix.inputs[7].default_value = (*vaste_kleur, 1.0)
            doel = lk.to_socket
            nt.links.remove(lk)
            nt.links.new(mix.outputs[2], doel)
            n_aangepast += 1
    return n_aangepast


def ruwheid_minimaal(mat, minimum):
    """Roughness nooit onder `minimum` (teak-fauteuil: lak glom te veel, handoff G1)."""
    nt = mat.node_tree
    bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if bsdf is None:
        return False
    links = list(bsdf.inputs["Roughness"].links)
    if not links:
        bsdf.inputs["Roughness"].default_value = max(minimum, bsdf.inputs["Roughness"].default_value)
        return True
    mx = nt.nodes.new("ShaderNodeMath")
    mx.operation = "MAXIMUM"
    mx.inputs[1].default_value = minimum
    nt.links.new(links[0].from_socket, mx.inputs[0])
    nt.links.new(mx.outputs["Value"], bsdf.inputs["Roughness"])
    return True


# --------------------------------------------------------------------------- toetsen dressing
def _wbbox_inst(inst):
    m = inst.matrix_world
    pts = [m @ Vector(c) for c in inst.object.bound_box]
    return (min(p.x for p in pts), max(p.x for p in pts), min(p.y for p in pts),
            max(p.y for p in pts), min(p.z for p in pts), max(p.z for p in pts))


def _overlap(a, b):
    return not (a[1] < b[0] or a[0] > b[1] or a[3] < b[2] or a[2] > b[3] or a[5] < b[4] or a[4] > b[5])


def audit_dressing(instancers, route_sdf, meting, regels):
    """Toets op de echte GN-uitvoer (depsgraph-instances) van de opgegeven instancer-objecten.

    regels per instancer-naam: dict met
      pad_marge: minimale afstand van de voet tot Route_Steen (m; None = niet toetsen)
      kap_vrij:  voet niet onder de kap / op de kapvloer
      zinken:    toegestane diepte van de bbox-onderkant onder het oppervlak (m)
    Algemeen: niets in de gesloten ruimte (bbox raakt de hutmuren-bbox niet), niet zwevend
    (> 5 cm), niet ondersteboven.
    """
    scn = bpy.context.scene
    gras = [m for o in scn.objects if o.name.startswith(("Gazon", "Bodemlaag", "Struiklaag"))
            for m in o.modifiers if m.type == "NODES"]
    for m in gras:
        m.show_viewport = False
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    gb = meting["gesloten_ruimte_bbox"]
    hut_box = (gb[0], gb[1], gb[2], gb[3], -1.0, 3.0)
    eb = meting["envelop"]
    kap_rect = (gb[1], eb[1], gb[2], eb[3])                    # onder het kapdak, oost van de muur
    namen = {o.name for o in instancers}
    tel = {n: 0 for n in namen}
    fouten = []
    per = {n: {"zwevend": [], "ondergestopt": [], "in_hut": [], "op_pad": [], "onder_kap": [],
               "ondersteboven": []} for n in namen}
    # Een plant uit een 'geheel'-donor (bv. lavendel: 67 losse meshes) geeft per punt meerdere
    # depsgraph-instances met dezelfde transformatie: per punt samenvoegen tot één bbox.
    groepen = {}
    for inst in dg.object_instances:
        if not inst.is_instance or inst.parent is None:
            continue
        pn = inst.parent.original.name
        if pn not in namen:
            continue
        mwi = inst.matrix_world
        t = mwi.translation
        sleutel = (pn, round(t.x, 4), round(t.y, 4), round(t.z, 4))
        bb = _wbbox_inst(inst)
        if sleutel in groepen:
            o = groepen[sleutel][0]
            bb = (min(o[0], bb[0]), max(o[1], bb[1]), min(o[2], bb[2]), max(o[3], bb[3]),
                  min(o[4], bb[4]), max(o[5], bb[5]))
        groepen[sleutel] = (bb, t.copy(), mwi.col[2].xyz.normalized())
    for (pn, *_), (bb, t, zas) in groepen.items():
        tel[pn] += 1
        r = regels.get(pn, {})
        oz = oppervlak_z(t.x, t.y)
        p = per[pn]
        if bb[4] - oz > 0.05:
            p["zwevend"].append([round(t.x, 2), round(t.y, 2), round(bb[4] - oz, 3)])
        if oz - bb[4] > r.get("zinken", 0.06) + 1e-4:
            p["ondergestopt"].append([round(t.x, 2), round(t.y, 2), round(oz - bb[4], 3)])
        if _overlap(bb, hut_box):
            p["in_hut"].append([round(t.x, 2), round(t.y, 2)])
        if r.get("pad_marge") is not None and route_sdf(t.x, t.y) < r["pad_marge"]:
            p["op_pad"].append([round(t.x, 2), round(t.y, 2), round(route_sdf(t.x, t.y), 2)])
        if r.get("kap_vrij", True) and rl.sdf_rect(t.x, t.y, kap_rect) < 0.0:
            p["onder_kap"].append([round(t.x, 2), round(t.y, 2)])
        if zas.z < 0.9:
            p["ondersteboven"].append([round(t.x, 2), round(t.y, 2), round(zas.z, 2)])
    for m in gras:
        m.show_viewport = True
    bpy.context.view_layer.update()
    for n in sorted(namen):
        verwacht = len(bpy.data.objects[n].data.vertices)
        if tel[n] != verwacht:
            fouten.append(f"{n}: {tel[n]} instances, verwacht {verwacht} (GN-uitvoer klopt niet)")
        for soort, lijst in per[n].items():
            if lijst:
                fouten.append(f"{n} {soort}: {len(lijst)}x, bv. {lijst[:3]}")
    return {"ok": not fouten, "fouten": fouten, "instances": tel,
            "details": {n: {k: v[:10] for k, v in d.items() if v} for n, d in per.items()}}


def kloon_check(soorten):
    """Per soort: buren < 1,2 m met dezelfde variant, schaal (+-4%) en draaiing (+-11 gr) =
    kloon; drie punten op een rechte lijn met gelijke afstanden (+-12%) = rij."""
    uit, klonen_tot, rijen_tot = {}, 0, 0
    for naam, pts in soorten.items():
        klonen, rijen = [], []
        for i, a in enumerate(pts):
            for b in pts[i + 1:]:
                d = math.hypot(a["x"] - b["x"], a["y"] - b["y"])
                if d > 1.2 or a["v"] != b["v"]:
                    continue
                dr = abs((a["rot"] - b["rot"] + math.pi) % (2 * math.pi) - math.pi)
                if abs(a["s"] - b["s"]) / max(a["s"], 1e-6) < 0.04 and dr < 0.2:
                    klonen.append([round(a["x"], 2), round(a["y"], 2), round(b["x"], 2), round(b["y"], 2)])
        for a in pts:
            buren = sorted(pts, key=lambda b: math.hypot(a["x"] - b["x"], a["y"] - b["y"]))[1:3]
            if len(buren) < 2:
                continue
            v1 = (buren[0]["x"] - a["x"], buren[0]["y"] - a["y"])
            v2 = (buren[1]["x"] - a["x"], buren[1]["y"] - a["y"])
            l1, l2 = math.hypot(*v1), math.hypot(*v2)
            if l1 < 1e-6 or l2 < 1e-6:
                continue
            cos = (v1[0] * v2[0] + v1[1] * v2[1]) / (l1 * l2)
            if cos < -0.99 and abs(l1 - l2) / max(l1, l2) < 0.12:
                rijen.append([round(a["x"], 2), round(a["y"], 2)])
        uit[naam] = {"aantal": len(pts), "klonen": klonen[:6], "rijen": rijen[:6],
                     "schaal_min_max": [round(min(p["s"] for p in pts), 2), round(max(p["s"] for p in pts), 2)]
                     if pts else None,
                     "varianten": sorted({p["v"] for p in pts})}
        klonen_tot += len(klonen)
        rijen_tot += len(rijen)
    return {"ok": klonen_tot == 0 and rijen_tot <= 2, "klonen": klonen_tot, "rijen": rijen_tot,
            "eis": "0 klonen, hooguit 2 toevallige rij-drietallen", "per_soort": uit}


def dicht_genoeg(x, y, r, bestaande, factor=0.75):
    """True als (x, y) met straal r te dicht bij een bestaande plant (x, y, r) staat."""
    return any(math.hypot(x - bx, y - by) < factor * (r + br) for bx, by, br in bestaande)


# --------------------------------------------------------------------------- camera's + render
def zet_camera(naam, loc, doel, lens, shift_y=0.0, dof_focus=None, fstop=5.6):
    oud = bpy.data.objects.get(naam)
    if oud is not None:
        bpy.data.objects.remove(oud, do_unlink=True)
    cam = cl.add_camera(loc, doel, lens=lens, shift_y=shift_y, name=naam)
    if dof_focus is not None:
        cl.set_camera_dof(naam, fstop=fstop, focus_xyz=dof_focus)
    bpy.context.scene.camera = bpy.data.objects["HeroCam"]
    return cam


def gpu_status():
    """(vrij, reden). Bezet = GPU_BEZET.txt van een ander, of een ander Blender/python-proces op de GPU."""
    if GPU_BEZET.exists():
        tekst = GPU_BEZET.read_text(encoding="utf-8", errors="replace").strip()
        if not tekst.startswith("Renders 2.0"):
            return False, f"GPU_BEZET.txt: {tekst[:120]}"
    return True, ""


def _gpu_mb():
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=15)
        return float(r.stdout.strip().splitlines()[0])
    except (OSError, ValueError, IndexError, subprocess.TimeoutExpired) as e:
        log("nvidia-smi faalde:", e)
        return None


def render_diag(cams, werk, verwacht_min=5):
    """Rendert de camera's (960x540/24, denoise) naar werk/<cam>.png.

    Vooraf: GPU_BEZET.txt van een ander -> RtkFout (niet renderen). Tijdens de render staat ons
    eigen GPU_BEZET.txt; het wordt altijd weer weggehaald (finally). Geheugen: nvidia-smi elke
    0,5 s in een apart proces; piek en nullijn gaan naar render.json.
    """
    vrij, reden = gpu_status()
    if not vrij:
        raise RtkFout(f"videokaart bezet, niet gerenderd: {reden}")
    werk.mkdir(parents=True, exist_ok=True)
    scn = bpy.context.scene
    # In een losse 'blender -b' staat compute_device_type op NONE: dan rendert Cycles stil op de
    # processor, ook met scene.cycles.device = 'GPU' (gemeten 26-10). Daarom hier expliciet OPTIX.
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "OPTIX"
    prefs.get_devices()
    for dv in prefs.devices:
        dv.use = dv.type == "OPTIX"
    if not any(dv.use for dv in prefs.devices):
        raise RtkFout("geen OPTIX-videokaart gevonden; niet stil op de processor renderen")
    scn.cycles.device = "GPU"
    log(f"render-apparaat: {[(dv.name, dv.type) for dv in prefs.devices if dv.use]}")
    scn.render.resolution_x, scn.render.resolution_y = PREVIEW_RES
    scn.render.resolution_percentage = 100
    scn.cycles.samples = PREVIEW_SAMPLES
    scn.cycles.use_denoising = True
    scn.cycles.texture_limit_render = "1024"
    scn.render.image_settings.file_format = "PNG"
    basis = _gpu_mb()
    nu = time.strftime("%H:%M")
    eind = time.strftime("%H:%M", time.localtime(time.time() + 60 * max(verwacht_min, len(cams) * 1.5)))
    eigen = False
    sampler = None
    memlog = werk / "gpu_mem.txt"
    tijden = {}
    cycles_mem = {"max_mb": 0.0}

    def stats(tekst, *_):
        # Cycles meldt "Mem: 5431M | Sample 1/24" (geen "Peak": daarom gaf stap1 0,0)
        import re
        for m in re.finditer(r"Mem:\s*([\d.]+)([MG])", str(tekst)):
            mb = float(m.group(1)) * (1024 if m.group(2) == "G" else 1)
            cycles_mem["max_mb"] = max(cycles_mem["max_mb"], mb)
    bpy.app.handlers.render_stats.append(stats)
    try:
        GPU_BEZET.write_text(f"Renders 2.0 (regentuinkamer_v2) — begin {nu} — verwacht klaar {eind}\n",
                             encoding="utf-8")
        eigen = True
        memf = open(memlog, "w")
        sampler = subprocess.Popen(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits",
                                    "-lms", "500"], stdout=memf, stderr=subprocess.DEVNULL)
        for naam in cams:
            scn.camera = bpy.data.objects[naam]
            scn.render.filepath = str(werk / f"{naam}.png")
            t = time.time()
            bpy.ops.render.render(write_still=True)
            tijden[naam] = round(time.time() - t, 1)
            log(f"render {naam}: {tijden[naam]} s")
    finally:
        if sampler is not None:
            sampler.terminate()
            try:
                sampler.wait(timeout=10)
            except subprocess.TimeoutExpired:
                sampler.kill()
            memf.close()
        if eigen and GPU_BEZET.exists():
            GPU_BEZET.unlink()
        if stats in bpy.app.handlers.render_stats:
            bpy.app.handlers.render_stats.remove(stats)
        scn.camera = bpy.data.objects["HeroCam"]
    waarden = []
    for regel in memlog.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            waarden.append(float(regel.strip()))
        except ValueError:
            continue
    piek = max(waarden) if waarden else None
    # maat = wat Cycles zelf meldt; nvidia-smi (hele kaart, ook andere programma's) staat ernaast
    uit = {"rendertijden_s": tijden, "cycles_mem_max_mb": round(cycles_mem["max_mb"], 0),
           "gpu_mb_voor_render": basis, "gpu_mb_piek_totaal_kaart": piek,
           "metingen_nvidia_smi": len(waarden), "grens_mb": 6.5 * 1024,
           "geheugen_ok": 0 < cycles_mem["max_mb"] <= 6.5 * 1024}
    schrijf_json(werk / "render.json", uit)
    log(f"renders klaar: {uit}")
    return uit


def standaard_toetsen(meting):
    """validate_scene + cl.audit + audit_extra + schaduw- + luchttoets: precies stap1_anker.toetsen."""
    import stap1_anker as s1
    return s1.toetsen(meting, rl.route_sdf_from_meta(bpy.data.objects["Route_Steen"]))


def main_wrapper(main, label):
    try:
        code = main()
    except RtkFout as e:
        print(f"[{label}] STOP: {e}", flush=True)
        code = 1
    except Exception:   # noqa: BLE001 - volledige traceback naar de log, en exitcode 2
        import traceback
        traceback.print_exc()
        print(f"[{label}] STOP: onverwachte fout (traceback hierboven)", flush=True)
        code = 2
    sys.stdout.flush()
    os._exit(code)
