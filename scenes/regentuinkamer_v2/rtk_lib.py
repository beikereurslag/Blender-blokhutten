"""Helpers voor Renders 2.0, pilot De Regentuinkamer (plan: docs/PLAN_renders2_2026-10.md).

Alles wat hier staat hoort bij deze scene. Gedeelde code komt uit scripts/cabin_lib.py
(`import cabin_lib as cl`); die wordt niet gewijzigd (plan §1).

Elke toets (shadow_test, sky_closure, audit_extra) geeft een dict terug met "ok" en de
getallen, zodat stap1 ze in audit.json kan zetten.

Tuinframe (zoals docs/PLAN_astra_garden.md): X 0-14 oost, Y 0-12 noord, meters, Z omhoog.
"""
import math
import random
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

ROOT = Path(r"D:\Blender-blokhutten")
SCENE_DIR = ROOT / "scenes" / "regentuinkamer_v2"
sys.path.insert(0, str(ROOT / "scripts"))
import cabin_lib as cl  # noqa: E402

GARDEN = (0.0, 14.0, 0.0, 12.0)          # x0, x1, y0, y1 (binnenkant hagen)
SCHAAL_MIN, SCHAAL_MAX = 0.8, 1.1         # plan §3: boomschaal nooit buiten 0,8-1,1
MIN_VERTS_BOOM = 50000                    # plan §8.2: minder = kale boom, weigeren
FAR_Z = -0.14                             # Ground_Far (plan §7)


def log(*a):
    print("[rtk]", *a, flush=True)


class RtkFout(RuntimeError):
    """Harde stop met een bruikbare reden (stap1 vangt dit en stopt met exitcode 1)."""


# --------------------------------------------------------------------------- grond
# Bekken: functies uit pilots/G1-regentuinkamer-Jasmijn300x250-250/regentuinkamer_stap1_anker.py
BC = (4.75, 5.30)
BRX, BRY = 1.55, 1.90
BDEPTH = 0.12


def basin_n(x, y):
    """Genormaliseerde afstand tot de bekkenrand (0 = midden, 1 = rand), onregelmatige omtrek."""
    dx, dy = (x - BC[0]) / BRX, (y - BC[1]) / BRY
    th = math.atan2(dy, dx)
    r = 1 + 0.18 * math.sin(2 * th + 0.7) + 0.12 * math.sin(3 * th - 1.1) + 0.07 * math.sin(5 * th + 2.0)
    return math.hypot(dx, dy) / r


def basin_depth(x, y):
    n = basin_n(x, y)
    if n >= 1.0:
        return 0.0
    t = min(1.0, max(0.0, (n - 0.25) / 0.75))
    s = t * t * (3 - 2 * t)
    return BDEPTH * (1 - s)


GROUND_BOUNDS = (-16.0, 30.0, -16.0, 28.0)   # raster uit de oude stap1
GROUND_RAND = 3.0                             # laatste 3 m zakt de rand onder Ground_Far
GROUND_RAND_Z = -0.17


def ground_height(x, y):
    """Hoogte van het maaiveld op (x, y): bodemmesh met bekken en zakkende rand, anders Ground_Far."""
    x0, x1, y0, y1 = GROUND_BOUNDS
    if not (x0 <= x <= x1 and y0 <= y <= y1):
        return FAR_Z
    z = -basin_depth(x, y)
    d = min(x - x0, x1 - x, y - y0, y1 - y)
    if d < GROUND_RAND:
        z = GROUND_RAND_Z + (z - GROUND_RAND_Z) * (d / GROUND_RAND)
    return max(z, FAR_Z)


def make_ground(name, mat, cell=0.30, mat_kern=None, kern_diepte=0.035):
    """Bodemmesh met bekkenkuil. De rand zakt onder Ground_Far zodat er geen trede te zien is."""
    x0, x1, y0, y1 = GROUND_BOUNDS
    nx, ny = int(round((x1 - x0) / cell)), int(round((y1 - y0) / cell))
    bm = bmesh.new()
    grid = {}
    for i in range(nx + 1):
        for j in range(ny + 1):
            x = x0 + (x1 - x0) * i / nx
            y = y0 + (y1 - y0) * j / ny
            d = min(x - x0, x1 - x, y - y0, y1 - y)
            z = -basin_depth(x, y)
            if d < GROUND_RAND:
                z = GROUND_RAND_Z + (z - GROUND_RAND_Z) * (d / GROUND_RAND)
            grid[(i, j)] = bm.verts.new((x, y, z))
    for i in range(nx):
        for j in range(ny):
            bm.faces.new((grid[(i, j)], grid[(i + 1, j)], grid[(i + 1, j + 1)], grid[(i, j + 1)]))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat)
    if mat_kern is not None:      # bekkenkern = vers bewerkte aarde, net als de bedden
        ob.data.materials.append(mat_kern)
        for p in me.polygons:
            c = p.center
            if basin_depth(c.x, c.y) > kern_diepte:
                p.material_index = 1
    diepst = min(v.co.z for v in me.vertices if v.co.x > 0 and v.co.y > 0 and v.co.x < 14 and v.co.y < 12)
    return ob, {"cellen": [nx, ny], "bekken_diepst_m": round(diepst, 3)}


# --------------------------------------------------------------------------- vormen (2D)
def dist_to_rect(x, y, rect):
    x0, x1, y0, y1 = rect
    dx = max(x0 - x, 0.0, x - x1)
    dy = max(y0 - y, 0.0, y - y1)
    return math.hypot(dx, dy)


def sdf_rect(x, y, rect):
    """Signed distance tot een rechthoek (negatief = binnen)."""
    x0, x1, y0, y1 = rect
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    hx, hy = (x1 - x0) / 2, (y1 - y0) / 2
    qx, qy = abs(x - cx) - hx, abs(y - cy) - hy
    buiten = math.hypot(max(qx, 0.0), max(qy, 0.0))
    return buiten + min(max(qx, qy), 0.0)


def sdf_polyline(x, y, pts):
    """Afstand tot een polylijn (altijd >= 0)."""
    best = 1e9
    for (ax, ay), (bx, by) in zip(pts[:-1], pts[1:]):
        vx, vy = bx - ax, by - ay
        ll = vx * vx + vy * vy
        t = 0.0 if ll == 0 else max(0.0, min(1.0, ((x - ax) * vx + (y - ay) * vy) / ll))
        best = min(best, math.hypot(x - (ax + t * vx), y - (ay + t * vy)))
    return best


def route_centerline(ctrl, eind, per_seg=24, recht_stap=0.1):
    """Middenlijn van het pad: Hermite-boog door ctrl (Catmull-raaklijnen binnenin), begin- en
    eindraaklijn recht naar het noorden, daarna een recht stuk van ctrl[-1] naar eind.

    Zo is de overgang naar het rechte laatste stuk vloeiend (geen knik) en loopt het
    laatste stuk exact recht op de deur af (plan §7: laatste 2,2 m recht).
    """
    p = [Vector(c) for c in ctrl]
    n = len(p)
    tang = []
    for i in range(n):
        if i == 0 or i == n - 1:
            buur = p[1] - p[0] if i == 0 else p[-1] - p[-2]
            tang.append(Vector((0.0, buur.length)))
        else:
            tang.append((p[i + 1] - p[i - 1]) * 0.5)
    uit = []
    for i in range(n - 1):
        p0, p1, m0, m1 = p[i], p[i + 1], tang[i], tang[i + 1]
        for s in range(per_seg):
            t = s / per_seg
            h00 = 2 * t ** 3 - 3 * t ** 2 + 1
            h10 = t ** 3 - 2 * t ** 2 + t
            h01 = -2 * t ** 3 + 3 * t ** 2
            h11 = t ** 3 - t ** 2
            uit.append(h00 * p0 + h10 * m0 + h01 * p1 + h11 * m1)
    a, b = p[-1], Vector(eind)
    k = max(1, int((b - a).length / recht_stap))
    for s in range(k + 1):
        uit.append(a.lerp(b, s / k))
    return [(v.x, v.y) for v in uit]


# --------------------------------------------------------------------------- route (pad + schort)
def route_sdf(centerline, half_width, schort_rect, schort_clip=None, start_y=None, eind_y=None):
    """Signed distance tot de vorm van Route_Steen (negatief = op de steen)."""
    def sdf(x, y):
        d_pad = sdf_polyline(x, y, centerline) - half_width
        if start_y is not None:
            d_pad = max(d_pad, start_y - y)
        if eind_y is not None:
            d_pad = max(d_pad, y - eind_y)
        d_schort = sdf_rect(x, y, schort_rect)
        if schort_clip is not None:
            cx0, cx1, cymax = schort_clip
            if cx0 <= x <= cx1:
                d_schort = max(d_schort, y - cymax)
        return min(d_pad, d_schort)
    return sdf


def route_sdf_from_meta(ob):
    """De sdf opnieuw opbouwen uit de vorm die make_route in het object heeft gezet."""
    import json
    m = json.loads(ob["rtk_route"])
    return route_sdf([tuple(p) for p in m["centerline"]], m["half_width"], tuple(m["schort_rect"]),
                     tuple(m["schort_clip"]) if m["schort_clip"] else None, m["start_y"], m["eind_y"])


def make_route(name, centerline, half_width, schort_rect, top_z, mat, disp_image,
               cell=0.015, dikte=0.06, rand_r=0.02, disp_sterkte=0.012, uv_maat=1.8,
               schort_clip=None, start_y=None, eind_y=None):
    """Pad + terras-schort als één mesh (plan §7).

    - bovenvlak = raster van `cell` m binnen de vereniging van pad (afstand tot middenlijn
      <= half_width) en schort; randpunten worden op de echte rand gelegd (geen trapjes);
    - afgeronde rand: binnen `rand_r` van de rand zakt het vlak als een kwartcirkel;
    - Displace-modifier uit de disp-map, uitgefaded naar de rand (vertexgroep);
    - de randranden worden recht naar beneden geëxtrudeerd: `dikte` dik, zonder Solidify
      (die gaf pieken op de schuine randnormalen).
    schort_clip: (x0, x1, ymax) - het schortdeel binnen x0..x1 stopt op ymax (de wand van
    de gesloten ruimte), zodat er geen steen de hut in loopt.
    start_y / eind_y: het pad begint en eindigt recht afgesneden op deze Y (geen ronde kop;
    eind_y = gemeten deurvoorkant).
    """
    sdf = route_sdf(centerline, half_width, schort_rect, schort_clip, start_y, eind_y)

    xs = [p[0] for p in centerline] + [schort_rect[0], schort_rect[1]]
    ys = [p[1] for p in centerline] + [schort_rect[2], schort_rect[3]]
    bx0, bx1 = min(xs) - half_width - cell, max(xs) + half_width + cell
    by0, by1 = min(ys) - half_width - cell, max(ys) + half_width + cell
    nx, ny = int((bx1 - bx0) / cell) + 1, int((by1 - by0) / cell) + 1
    d = [[sdf(bx0 + i * cell, by0 + j * cell) for j in range(ny + 1)] for i in range(nx + 1)]

    bm = bmesh.new()
    verts = {}
    eps = 1e-4

    def vert(i, j):
        if (i, j) in verts:
            return verts[(i, j)]
        x, y = bx0 + i * cell, by0 + j * cell
        s = d[i][j]
        if s > 0:   # buiten de vorm: op de rand projecteren (numerieke gradient)
            for _ in range(4):
                gx = (sdf(x + eps, y) - sdf(x - eps, y)) / (2 * eps)
                gy = (sdf(x, y + eps) - sdf(x, y - eps)) / (2 * eps)
                g = math.hypot(gx, gy) or 1.0
                x, y = x - gx / g * s, y - gy / g * s
                s = sdf(x, y)
                if abs(s) < 1e-4:
                    break
        v = bm.verts.new((x, y, top_z))
        verts[(i, j)] = v
        return v

    for i in range(nx):
        for j in range(ny):
            hoeken = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
            if sum(1 for a, b in hoeken if d[a][b] <= 0) < 2:
                continue
            vs = [vert(a, b) for a, b in hoeken]
            if len(set(vs)) < 3:
                continue
            try:
                bm.faces.new(vs)
            except ValueError:
                pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=cell * 0.25)
    # degenerate vlakken (na samenvoegen) weg
    weg = [f for f in bm.faces if f.calc_area() < (cell * cell) * 0.02]
    bmesh.ops.delete(bm, geom=weg, context="FACES")
    los = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=los, context="VERTS")

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if sum(f.normal.z for f in bm.faces) < 0:      # bovenvlak moet omhoog wijzen
        bmesh.ops.reverse_faces(bm, faces=bm.faces)

    # afgeronde rand: binnen rand_r van de rand zakt het vlak als een kwartcirkel
    for v in bm.verts:
        s = max(0.0, -sdf(v.co.x, v.co.y))          # diepte binnen de vorm (>= 0)
        if s < rand_r:
            v.co.z = top_z - (rand_r - math.sqrt(max(0.0, rand_r * rand_r - (rand_r - s) ** 2)))
    # zijkant: randranden recht naar beneden extruderen tot top_z - dikte
    rand_edges = [e for e in bm.edges if e.is_boundary]
    ext = bmesh.ops.extrude_edge_only(bm, edges=rand_edges)
    zijkant_verts = [g for g in ext["geom"] if isinstance(g, bmesh.types.BMVert)]
    for v in zijkant_verts:
        v.co.z = top_z - dikte
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if sum(f.normal.z for f in bm.faces) < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces)

    # vertexgroep-gewicht voor de displacement: 0 op de rand en de zijkant, 1 binnenin
    bm.verts.index_update()
    zijkant = set(zijkant_verts)
    gewicht = {}
    for v in bm.verts:
        if v in zijkant:
            gewicht[v.index] = 0.0
            continue
        s = max(0.0, -sdf(v.co.x, v.co.y))
        t = min(1.0, s / (2.5 * rand_r))
        gewicht[v.index] = t * t * (3 - 2 * t)
    uv = bm.loops.layers.uv.new("UVMap")
    for f in bm.faces:
        for lp in f.loops:
            lp[uv].uv = (lp.vert.co.x / uv_maat, lp.vert.co.y / uv_maat)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    # oorsprong in het midden (validate_scene meldt objecten met oorsprong op 0,0,0)
    midden = Vector((sum(v.co.x for v in me.vertices) / len(me.vertices),
                     sum(v.co.y for v in me.vertices) / len(me.vertices), 0.0))
    me.transform(Matrix.Translation(-midden))
    ob = bpy.data.objects.new(name, me)
    ob.location = midden
    bpy.context.scene.collection.objects.link(ob)
    import json
    ob["rtk_route"] = json.dumps({"centerline": centerline, "half_width": half_width,
                                  "schort_rect": schort_rect, "schort_clip": schort_clip,
                                  "start_y": start_y, "eind_y": eind_y})
    vg = ob.vertex_groups.new(name="disp")
    for idx, w in gewicht.items():
        vg.add([idx], w, "REPLACE")
    for p in me.polygons:
        p.use_smooth = True
    ob.data.materials.append(mat)

    tex = bpy.data.textures.new(f"{name}_disp", type="IMAGE")
    tex.image = disp_image
    tex.extension = "REPEAT"
    m = ob.modifiers.new("Displace", "DISPLACE")
    m.texture = tex
    m.texture_coords = "UV"
    m.uv_layer = "UVMap"
    m.direction = "Z"
    m.strength = disp_sterkte
    m.mid_level = 0.5
    m.vertex_group = "disp"
    info = {"vertices": len(me.vertices), "vlakken": len(me.polygons),
            "top_z": top_z, "dikte_m": dikte, "disp_m": disp_sterkte, "sdf": sdf}
    return ob, info


def uv_material(mat):
    """Zet een cl.pbr_from_folder-materiaal (BOX + Object) om op de UVMap, zodat kleur,
    normal en de Displace-modifier precies dezelfde tegel gebruiken."""
    nt = mat.node_tree
    tc = next(n for n in nt.nodes if n.type == "TEX_COORD")
    mp = next(n for n in nt.nodes if n.type == "MAPPING")
    for lk in list(mp.inputs["Vector"].links):
        nt.links.remove(lk)
    nt.links.new(tc.outputs["UV"], mp.inputs["Vector"])
    mp.inputs["Scale"].default_value = (1.0, 1.0, 1.0)
    for n in nt.nodes:
        if n.type == "TEX_IMAGE":
            n.projection = "FLAT"
    return mat


def make_bed(name, rect, mat, z=0.006, hoek_r=0.25, seg=6):
    """Leeg borderbed: plat grondvlak (afgeronde rechthoek) net boven het maaiveld.

    Het gazon blijft er strak buiten (make_lawn), dat geeft de scherpe rand. Beplanting volgt
    in laag 3 van het plan; voor Beike heet dit "nog te beplanten".
    """
    x0, x1, y0, y1 = rect
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    hx, hy = (x1 - x0) / 2 - hoek_r, (y1 - y0) / 2 - hoek_r
    pts = []
    for k, (sx, sy) in enumerate(((1, 1), (-1, 1), (-1, -1), (1, -1))):
        a0 = k * math.pi / 2
        for i in range(seg + 1):
            a = a0 + (math.pi / 2) * i / seg
            pts.append((sx * hx + hoek_r * math.cos(a), sy * hy + hoek_r * math.sin(a), z))
    me = bpy.data.meshes.new(name)
    me.from_pydata(pts, [], [list(range(len(pts)))])
    me.update()
    ob = bpy.data.objects.new(name, me)
    ob.location = (cx, cy, ground_height(cx, cy))
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat)
    return ob


# --------------------------------------------------------------------------- BlenderKit-donors
def fix_image_ext():
    """Beelden waarvan het pad niet bestaat: zelfde naam met .png/.jpg in dezelfde map proberen."""
    gerepareerd = []
    for img in bpy.data.images:
        if img.packed_file or img.source != "FILE" or not img.filepath:
            continue
        ap = Path(bpy.path.abspath(img.filepath))
        if ap.exists():
            continue
        for ext in (".png", ".jpg", ".jpeg", ".exr"):   # .exr: PH-normal maps (rock_moss_set, dressing)
            kand = ap.with_suffix(ext)
            if kand.exists():
                img.filepath = str(kand)
                img.reload()
                gerepareerd.append(img.name)
                break
    return gerepareerd


def aarde_materiaal(mat, kleur=(0.075, 0.048, 0.030), ruw=0.88):
    """Textuur x donkerbruin (vochtige tuinaarde) en een vaste, ruwe roughness."""
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    for lk in list(bsdf.inputs["Base Color"].links):
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.blend_type = "MULTIPLY"
        mix.inputs[0].default_value = 1.0
        mix.inputs[7].default_value = (kleur[0] * 4, kleur[1] * 4, kleur[2] * 4, 1.0)
        nt.links.new(lk.from_socket, mix.inputs[6])
        nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
    for lk in list(bsdf.inputs["Roughness"].links):
        nt.links.remove(lk)
    bsdf.inputs["Roughness"].default_value = ruw
    return mat


def zon_hdri_verhouding(img, hdri_sterkte, zon_vec, zon_sterkte, zon_kleur, rot=0.0):
    """Bestralingssterkte op een horizontaal vlak en op de zuidgevel: zon tegenover HDRI.

    HDRI: som over de bovenste helft van luminantie x cos(invalshoek) x ruimtehoek; voor de
    gevel (normaal -Y) de halve ruimte ervoor. Zon: sterkte x luminantie van de kleur x cos.
    Benadering zonder schaduw of kaatslicht; bedoeld om de verhouding te volgen.
    """
    import numpy as np
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    px = px.reshape(h, w, 4)[:, :, :3]
    lum = (0.2126 * px[:, :, 0] + 0.7152 * px[:, :, 1] + 0.0722 * px[:, :, 2]) * hdri_sterkte
    v = (np.arange(h) + 0.5) / h
    u = (np.arange(w) + 0.5) / w
    elev = (v - 0.5) * np.pi                       # rij 0 = onderkant
    phi = (u - 0.5) * 2 * np.pi                    # u = atan2(y, -x) / 2pi + 0.5
    ce, se = np.cos(elev)[:, None], np.sin(elev)[:, None]
    dy = np.sin(np.pi - phi - rot)[None, :] * ce   # wereldrichting na de mapping-rotatie
    domega = ce * (2 * np.pi / w) * (np.pi / h)
    hor = float((lum * np.clip(se, 0, None) * domega).sum())
    gevel = float((lum * np.clip(-dy, 0, None) * (se > 0) * domega).sum())
    zl = 0.2126 * zon_kleur[0] + 0.7152 * zon_kleur[1] + 0.0722 * zon_kleur[2]
    zon_hor = zon_sterkte * zl * max(0.0, zon_vec.z)
    zon_gevel = zon_sterkte * zl * max(0.0, -zon_vec.y)
    return {"hdri_horizontaal": round(hor, 2), "zon_horizontaal": round(zon_hor, 2),
            "zon_div_hdri_horizontaal": round(zon_hor / max(hor, 1e-6), 2),
            "hdri_zuidgevel": round(gevel, 2), "zon_zuidgevel": round(zon_gevel, 2),
            "zon_div_hdri_zuidgevel": round(zon_gevel / max(gevel, 1e-6), 2)}


def groen_gras(objs, tint=(0.62, 0.85, 0.42)):
    """PH grass_medium_02 mengt een droge (bruine) textuur in; v4-proef las als verdord gras.
    De droge beeldnode krijgt daarom het groene diff-beeld."""
    for m in {sl.material for o in objs for sl in o.material_slots if sl.material}:
        imgs = [n for n in m.node_tree.nodes if n.type == "TEX_IMAGE" and n.image]
        groen = next((n.image for n in imgs if "diff" in n.image.name and "dry" not in n.image.name), None)
        for n in imgs:
            if "dry" in n.image.name and groen is not None:
                n.image = groen
        # v5: ook groen bleef strogeel: diff x frisgroen
        nt = m.node_tree
        for n in [n for n in imgs if "diff" in n.image.name]:
            for lk in list(n.outputs["Color"].links):
                mix = nt.nodes.new("ShaderNodeMix")
                mix.data_type = "RGBA"
                mix.blend_type = "MULTIPLY"
                mix.inputs[0].default_value = 1.0
                mix.inputs[7].default_value = (*tint, 1.0)
                doel = lk.to_socket
                nt.links.remove(lk)
                nt.links.new(n.outputs["Color"], mix.inputs[6])
                nt.links.new(mix.outputs[2], doel)


def groen_struik(objs, kleur=(0.30, 0.48, 0.20)):
    """PH shrub_02 rendert zilverwit (v4-proef); diff vermenigvuldigen met bladgroen."""
    for m in {sl.material for o in objs for sl in o.material_slots if sl.material}:
        nt = m.node_tree
        for n in [n for n in nt.nodes if n.type == "TEX_IMAGE" and n.image and "diff" in n.image.name]:
            for lk in list(n.outputs["Color"].links):
                mix = nt.nodes.new("ShaderNodeMix")
                mix.data_type = "RGBA"
                mix.blend_type = "MULTIPLY"
                mix.inputs[0].default_value = 1.0
                mix.inputs[7].default_value = (*kleur, 1.0)
                doel = lk.to_socket
                nt.links.remove(lk)
                nt.links.new(n.outputs["Color"], mix.inputs[6])
                nt.links.new(mix.outputs[2], doel)


def treeline_groen(mat, tint=(0.45, 0.80, 0.30), s_grens=0.45, v_grens=0.35):
    """Ronde extra (28-10): in Greenleaf Treeline 001 zijn de populierenkruinen bleek grijsblauw (lage
    verzadiging, hoge helderheid; ~10% van de dekkende pixels). In de render lazen ze als zilveren,
    bevroren struiken boven de haag. Die pixels krijgen hun eigen helderheid maal bladgroen; de rest
    van de kaart blijft zoals hij was. Masker = (s_grens - S) x (V - v_grens), beide x4 en geklemd.
    Geeft het aantal aangepaste beeldnodes terug."""
    nt = mat.node_tree
    n_aangepast = 0
    for img in [n for n in nt.nodes if n.type == "TEX_IMAGE" and n.image and "treeline" in n.image.name.lower()]:
        for lk in list(img.outputs["Color"].links):
            doel = lk.to_socket
            hsv = nt.nodes.new("ShaderNodeSeparateColor")
            hsv.mode = "HSV"
            nt.links.new(img.outputs["Color"], hsv.inputs["Color"])
            weinig_s = nt.nodes.new("ShaderNodeMath")
            weinig_s.operation = "MULTIPLY_ADD"          # (S x -4) + 4 x s_grens = 4 x (s_grens - S)
            weinig_s.use_clamp = True
            weinig_s.inputs[1].default_value = -4.0
            weinig_s.inputs[2].default_value = 4.0 * s_grens
            nt.links.new(hsv.outputs[1], weinig_s.inputs[0])
            veel_v = nt.nodes.new("ShaderNodeMath")
            veel_v.operation = "MULTIPLY_ADD"            # 4 x (V - v_grens)
            veel_v.use_clamp = True
            veel_v.inputs[1].default_value = 4.0
            veel_v.inputs[2].default_value = -4.0 * v_grens
            nt.links.new(hsv.outputs[2], veel_v.inputs[0])
            masker = nt.nodes.new("ShaderNodeMath")
            masker.operation = "MULTIPLY"
            nt.links.new(weinig_s.outputs[0], masker.inputs[0])
            nt.links.new(veel_v.outputs[0], masker.inputs[1])
            grijs = nt.nodes.new("ShaderNodeRGBToBW")
            nt.links.new(img.outputs["Color"], grijs.inputs["Color"])
            groen = nt.nodes.new("ShaderNodeMix")
            groen.data_type = "RGBA"
            groen.blend_type = "MULTIPLY"
            groen.inputs[0].default_value = 1.0
            groen.inputs[7].default_value = (*tint, 1.0)
            nt.links.new(grijs.outputs["Val"], groen.inputs[6])
            mix = nt.nodes.new("ShaderNodeMix")
            mix.data_type = "RGBA"
            nt.links.new(masker.outputs[0], mix.inputs[0])
            nt.links.new(img.outputs["Color"], mix.inputs[6])
            nt.links.new(groen.outputs[2], mix.inputs[7])
            nt.links.remove(lk)
            nt.links.new(mix.outputs[2], doel)
            n_aangepast += 1
    return n_aangepast


def treeline_weide_donker(mat, v_grens, kleur=(0.22, 0.27, 0.17)):
    """Ronde extra (28-10): onderaan Greenleaf Treeline 001 zit een lichte, zonnige weidestrook (~5% van
    de beeldhoogte); in Cam_Bekken las die als lichte horizonband. Die strook wordt donker (basiskleur
    x kleur), met een zachte overgang van v_grens/2 tot v_grens x 1,5. Doorzichtig maken (proef 28-10)
    gaf zicht op de zonnige verre grond erachter: weer een lichte band. Zakken van de kaart mag niet
    (validate_scene en audit_extra eisen de boomoorsprong op het maaiveld)."""
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["UV"], sep.inputs["Vector"])
    onder = nt.nodes.new("ShaderNodeMapRange")       # v klein -> 1 (donker), boven de strook -> 0
    onder.interpolation_type = "SMOOTHSTEP"
    onder.inputs["From Min"].default_value = 0.5 * v_grens
    onder.inputs["From Max"].default_value = 1.5 * v_grens
    onder.inputs["To Min"].default_value = 1.0
    onder.inputs["To Max"].default_value = 0.0
    nt.links.new(sep.outputs["Y"], onder.inputs["Value"])
    lk = bsdf.inputs["Base Color"].links[0]
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.blend_type = "MULTIPLY"
    mix.inputs[7].default_value = (*kleur, 1.0)
    nt.links.new(onder.outputs["Result"], mix.inputs[0])
    nt.links.new(lk.from_socket, mix.inputs[6])
    nt.links.remove(lk)
    nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])


def hdri_horizon_camera(world, kleur, e0=6.0, e1=14.0):
    """Bekkenfix (28-10): tussen de kruinen door zag Cam_Bekken op 2-6 graden boven de horizon de
    HDRI zelf (eilenriede_park: bruinrode gebouwen/stammen) als rechthoekige vlakken. Alleen voor
    camerastralen wordt de HDRI onder e0 graden vervangen door een egale, wazige bosgroene achtergrond
    (zachte overgang tot e1). Het licht op de scène (diffuse/glans) blijft de HDRI: luchttoets en
    zon/HDRI-verhouding veranderen niet."""
    nt = world.node_tree
    out = next(n for n in nt.nodes if n.type == "OUTPUT_WORLD")
    lk = out.inputs["Surface"].links[0]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sep.inputs["Vector"])
    hoog = nt.nodes.new("ShaderNodeMapRange")       # 0 onder e0, 1 boven e1 (sin van de elevatie)
    hoog.interpolation_type = "SMOOTHSTEP"
    hoog.inputs["From Min"].default_value = math.sin(math.radians(e0))
    hoog.inputs["From Max"].default_value = math.sin(math.radians(e1))
    nt.links.new(sep.outputs["Z"], hoog.inputs["Value"])
    lp = nt.nodes.new("ShaderNodeLightPath")
    laag = nt.nodes.new("ShaderNodeMath")
    laag.operation = "SUBTRACT"                      # 1 - hoog
    laag.inputs[0].default_value = 1.0
    nt.links.new(hoog.outputs["Result"], laag.inputs[1])
    fac = nt.nodes.new("ShaderNodeMath")
    fac.operation = "MULTIPLY"
    nt.links.new(laag.outputs[0], fac.inputs[0])
    nt.links.new(lp.outputs["Is Camera Ray"], fac.inputs[1])
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs["Color"].default_value = (*kleur, 1.0)
    bg.inputs["Strength"].default_value = 1.0
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(fac.outputs[0], mix.inputs[0])
    nt.links.new(lk.from_socket, mix.inputs[1])
    nt.links.new(bg.outputs["Background"], mix.inputs[2])
    nt.links.remove(lk)
    nt.links.new(mix.outputs[0], out.inputs["Surface"])


def verre_grond_mat(mat, tint=(0.30, 0.42, 0.22), spec=0.15, ruw_min=0.85):
    """Ronde extra (28-10): Ground_Far las in Cam_Bekken als lichte horizonstrook. Van dichtbij scheert
    de blik over de grond (85 m weg), dan spiegelt de lucht in de glans. Glans omlaag (Specular IOR
    Level), ruwheid minstens ruw_min, en de bodem donkerder en groener (diff x tint): proef 28-10 met
    tint (0,55; 0,75; 0,40) liet nog een zonnige weidestrook zien tussen het ruige gras en de kaarten."""
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Specular IOR Level"].default_value = spec
    for lk in list(bsdf.inputs["Roughness"].links):
        mr = nt.nodes.new("ShaderNodeMapRange")
        mr.inputs["To Min"].default_value = ruw_min
        mr.inputs["To Max"].default_value = 1.0
        nt.links.new(lk.from_socket, mr.inputs["Value"])
        nt.links.remove(lk)
        nt.links.new(mr.outputs["Result"], bsdf.inputs["Roughness"])
    if not bsdf.inputs["Roughness"].is_linked:
        bsdf.inputs["Roughness"].default_value = max(bsdf.inputs["Roughness"].default_value, ruw_min)
    for lk in list(bsdf.inputs["Base Color"].links):
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.blend_type = "MULTIPLY"
        mix.inputs[0].default_value = 1.0
        mix.inputs[7].default_value = (*tint, 1.0)
        nt.links.new(lk.from_socket, mix.inputs[6])
        nt.links.remove(lk)
        nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])


def load_ph_collection(blend_path, coll_name, kies):
    """PH-model als donorcollectie voor een GN-scatter. kies(naam) -> bool welke meshes mee."""
    with bpy.data.libraries.load(str(blend_path), link=False) as (src, dst):
        dst.objects = [n for n in src.objects if kies(n)]
    objs = [o for o in dst.objects if o is not None and o.type == "MESH"]
    if not objs:
        raise RtkFout(f"geen meshes gekozen uit {Path(blend_path).name}")
    coll = bpy.data.collections.new(coll_name)
    donor_collection().children.link(coll)
    for o in objs:
        coll.objects.link(o)
        o.parent = None
        o.location = (0.0, 0.0, 0.0)
        o.rotation_euler = (0.0, 0.0, 0.0)
    fix_image_ext()
    return coll, objs


def gn_scatter(ob, coll, n_bron, schaal, seed, dichtheid=None, z_offset=0.0, bodem_mat=None):
    """GN op `ob`: punten (Distribute op vlakken met dichtheid, of de vertices als dichtheid None)
    -> willekeurig exemplaar uit `coll`, willekeurige draaiing en schaal. bodem_mat: de emitter
    zelf blijft zichtbaar met dit materiaal (gazonbodem); anders alleen de instances."""
    ng = bpy.data.node_groups.new(f"RTK_Scatter_{ob.name}", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    nd = ng.nodes
    gi, go = nd.new("NodeGroupInput"), nd.new("NodeGroupOutput")
    iop = nd.new("GeometryNodeInstanceOnPoints")
    if dichtheid is not None:
        dp = nd.new("GeometryNodeDistributePointsOnFaces")
        dp.distribute_method = "RANDOM"
        dp.inputs["Density"].default_value = dichtheid
        dp.inputs["Seed"].default_value = seed
        ng.links.new(gi.outputs[0], dp.inputs["Mesh"])
        ng.links.new(dp.outputs["Points"], iop.inputs["Points"])
    else:
        mp = nd.new("GeometryNodeMeshToPoints")
        ng.links.new(gi.outputs[0], mp.inputs["Mesh"])
        ng.links.new(mp.outputs["Points"], iop.inputs["Points"])
    ci = nd.new("GeometryNodeCollectionInfo")
    ci.inputs["Collection"].default_value = coll
    ci.inputs["Separate Children"].default_value = True
    ci.inputs["Reset Children"].default_value = True
    iop.inputs["Pick Instance"].default_value = True
    ri = nd.new("FunctionNodeRandomValue")
    ri.data_type = "FLOAT"
    ri.inputs[2].default_value, ri.inputs[3].default_value = 0.0, n_bron - 0.001
    ri.inputs["Seed"].default_value = seed + 1
    rs = nd.new("FunctionNodeRandomValue")
    rs.data_type = "FLOAT"
    rs.inputs[2].default_value, rs.inputs[3].default_value = schaal
    rs.inputs["Seed"].default_value = seed + 2
    rz = nd.new("FunctionNodeRandomValue")
    rz.data_type = "FLOAT"
    rz.inputs[2].default_value, rz.inputs[3].default_value = 0.0, 6.283
    rz.inputs["Seed"].default_value = seed + 3
    cz = nd.new("ShaderNodeCombineXYZ")
    rot = nd.new("GeometryNodeRotateInstances")
    tr = nd.new("GeometryNodeTranslateInstances")
    tr.inputs["Translation"].default_value = (0.0, 0.0, z_offset)
    ng.links.new(ci.outputs[0], iop.inputs["Instance"])
    ng.links.new(ri.outputs[1], iop.inputs["Instance Index"])
    ng.links.new(rs.outputs[1], iop.inputs["Scale"])
    ng.links.new(rz.outputs[1], cz.inputs["Z"])
    ng.links.new(iop.outputs["Instances"], rot.inputs["Instances"])
    ng.links.new(cz.outputs["Vector"], rot.inputs["Rotation"])
    ng.links.new(rot.outputs["Instances"], tr.inputs["Instances"])
    if bodem_mat is not None:
        sm = nd.new("GeometryNodeSetMaterial")
        sm.inputs["Material"].default_value = bodem_mat
        jg = nd.new("GeometryNodeJoinGeometry")
        ng.links.new(gi.outputs[0], sm.inputs["Geometry"])
        ng.links.new(sm.outputs[0], jg.inputs[0])
        ng.links.new(tr.outputs["Instances"], jg.inputs[0])
        ng.links.new(jg.outputs[0], go.inputs[0])
    else:
        ng.links.new(tr.outputs["Instances"], go.inputs[0])
    m = ob.modifiers.new("Scatter", "NODES")
    m.node_group = ng
    return m


def grid_emitter(name, gebied, cell, vrij, z_offset=0.0):
    """Maaiveldraster (vlakken waar vrij(x, y) waar is), oorsprong in het midden."""
    x0, x1, y0, y1 = gebied
    nx, ny = int(round((x1 - x0) / cell)), int(round((y1 - y0) / cell))
    midden = Vector(((x0 + x1) / 2, (y0 + y1) / 2, 0.0))
    bm = bmesh.new()
    verts = {}

    def v(i, j):
        if (i, j) not in verts:
            x, y = x0 + i * cell, y0 + j * cell
            verts[(i, j)] = bm.verts.new((x - midden.x, y - midden.y, ground_height(x, y) + z_offset))
        return verts[(i, j)]
    vlakken = 0
    for i in range(nx):
        for j in range(ny):
            if not vrij(x0 + (i + 0.5) * cell, y0 + (j + 0.5) * cell):
                continue
            bm.faces.new((v(i, j), v(i + 1, j), v(i + 1, j + 1), v(i, j + 1)))
            vlakken += 1
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.location = midden
    bpy.context.scene.collection.objects.link(ob)
    return ob, vlakken * cell * cell


def donor_collection():
    """Collectie voor bronmodellen; uitgesloten van de view layer (niet renderen, niet raken)."""
    coll = bpy.data.collections.get("RTK_Donors")
    if coll is None:
        coll = bpy.data.collections.new("RTK_Donors")
        bpy.context.scene.collection.children.link(coll)
    lc = bpy.context.view_layer.layer_collection.children.get("RTK_Donors")
    if lc is not None:
        lc.exclude = True
    return coll


def load_donor(blend_path, label, min_verts=MIN_VERTS_BOOM, alleen=None):
    """Haal de objecten uit een asset-blend binnen als donor.

    Hoofdmeshes = meshes met minstens 25% van de grootste hoogte (bladkaartjes, die een
    GN-modifier gebruikt, tellen niet). alleen: lijst objectnamen om te houden.
    Weigert met RtkFout als de hoofdmeshes samen minder dan min_verts vertices hebben.
    """
    blend_path = Path(blend_path)
    if not blend_path.exists():
        raise RtkFout(f"asset ontbreekt: {blend_path}")
    with bpy.data.libraries.load(str(blend_path), link=False) as (src, dst):
        dst.objects = list(src.objects)
    objs = [o for o in dst.objects if o is not None]
    coll = donor_collection()
    for o in objs:
        coll.objects.link(o)

    # De donorcollectie is uitgesloten van de view layer, dus matrix_world wordt nooit
    # bijgewerkt. Wereldmatrix daarom zelf uitrekenen uit de ouderketen (matrix_basis).
    def wereld(o):
        m = o.matrix_basis.copy()
        while o.parent is not None:
            m = o.parent.matrix_basis @ o.matrix_parent_inverse @ m
            o = o.parent
        return m
    wereldm = {o: wereld(o) for o in objs}
    for o in objs:
        o.parent = None
        o.matrix_basis = wereldm[o]
    meshes = [o for o in objs if o.type == "MESH"]
    if alleen:
        meshes = [o for o in meshes if o.name in alleen]
    if not meshes:
        raise RtkFout(f"geen meshes in {blend_path.name}")

    def bbox(lijst):
        pts = [o.matrix_basis @ Vector(c) for o in lijst for c in o.bound_box]
        return (min(p.x for p in pts), max(p.x for p in pts), min(p.y for p in pts),
                max(p.y for p in pts), min(p.z for p in pts), max(p.z for p in pts))

    def hoogte(o):
        bb = bbox([o])
        return bb[5] - bb[4]
    hmax = max(hoogte(o) for o in meshes)
    hoofd = [o for o in meshes if hoogte(o) >= 0.25 * hmax]
    verts = sum(len(o.data.vertices) for o in hoofd)
    bb = bbox(hoofd)
    for o in hoofd:               # bron zelf nooit renderen of meetellen; kopieën zetten dit terug
        o.hide_render = True
        o.hide_viewport = True
    info = {"label": label, "bestand": str(blend_path), "objs": hoofd,
            "objnamen": [o.name for o in hoofd], "verts": verts,
            "h": bb[5] - bb[4], "breedte": max(bb[1] - bb[0], bb[3] - bb[2]),
            "bbox": [round(v, 3) for v in bb]}
    if verts < min_verts:
        raise RtkFout(f"donor {label} ({blend_path.name}) heeft {verts} vertices < {min_verts}: "
                      f"kale boom, geweigerd (plan §8.2)")
    log(f"donor {label}: {verts} verts, h {info['h']:.2f} m, breedte {info['breedte']:.2f} m")
    return info


def place_bk_tree(donor, name, x, y, schaal, rot_z):
    """Plaats een donor-boom (mesh-data gedeeld) met de stam op het maaiveld."""
    if not (SCHAAL_MIN - 1e-9 <= schaal <= SCHAAL_MAX + 1e-9):
        raise RtkFout(f"{name}: boomschaal {schaal:.2f} buiten {SCHAAL_MIN}-{SCHAAL_MAX}")
    root = cl.place_cluster((donor["h"], donor["objs"]), name, (x, y, 0.0),
                            donor["h"] * schaal, rot_z=rot_z)
    cl.ground_root(root)
    root.location.z += ground_height(x, y)
    root["rtk_schaal"] = schaal
    root["rtk_donor"] = donor["label"]
    return root


# --------------------------------------------------------------------------- haag (BK Cotoneaster-module)
# Plan §4. Module 7,5 x 1,3 x 1,6 m, lengte langs X. Van die 1,6 m zit 0,18 m onder de oorsprong
# (stamvoet); de module staat met zijn oorsprong op het maaiveld (v1/v2 op de bbox-onderkant gaf
# een lichte kier onder de haag). Zichtbare hoogte 1,44 m x schaal: rug 1,25 -> 1,80 m, zij 1,11 -> 1,60 m, voor 0,45 -> 0,65 m (plan: 1,8 m;
# de 1,12 uit het plan rekende met de hele 1,6 m). Per rij: naam, as, begin, eind, midden van
# de andere as, schaal (lengte, diepte, hoogte). Modules schuiven >= 0,4 m in elkaar.
# Oosthaag op X 13,3-14,3 i.p.v. 13,0-14,0: het dak van de kap loopt tot X 13,24 en de schort
# tot 13,1 (Astra-ontwerp: "do not intrude into roof or path bounds").
HAAG_RIJEN = [
    ("Haag_Rug", "x", -0.1, 14.3, 11.9, (1.0, 0.75, 1.25)),
    ("Haag_West", "y", 0.55, 11.45, 0.5, (0.78, 0.75, 1.11)),
    ("Haag_Oost", "y", 0.55, 11.45, 13.8, (0.78, 0.75, 1.11)),
    ("Haag_VoorW", "x", 0.0, 7.3, 0.3, (0.45, 0.45, 0.45)),
    ("Haag_VoorO", "x", 8.7, 14.3, 0.3, (0.45, 0.45, 0.45)),
]
HAAG_VOETEN = [(-0.1, 14.3, 11.4, 12.4), (0.0, 1.0, 0.55, 11.45), (13.3, 14.3, 0.55, 11.45),
               (0.0, 7.3, 0.0, 0.6), (8.7, 14.3, 0.0, 0.6)]
HAAG_OVERLAP_MIN = 0.4


def load_hedge_donor(blend_path):
    """Cotoneaster-module als donor; de rode bessen krijgen het bladmateriaal (plan §4)."""
    d = load_donor(blend_path, "haag", min_verts=MIN_VERTS_BOOM)
    blad = next((m for m in bpy.data.materials if "leaf 1" in m.name.lower()), None)
    vervangen = 0
    for o in d["objs"]:
        for i, m in enumerate(o.data.materials):
            if m is not None and "berr" in m.name.lower() and blad is not None:
                o.data.materials[i] = blad
                vervangen += 1
    d["bessen_vervangen"] = vervangen
    d["bessen_materiaal"] = blad.name if blad else None
    if vervangen == 0:
        log("LET OP: geen bessenmateriaal gevonden om te vervangen")
    bb = d["bbox"]
    d["lokaal_midden"] = ((bb[0] + bb[1]) / 2, (bb[2] + bb[3]) / 2)
    d["lokaal_zmin"] = bb[4]
    d["lengte"], d["diepte"] = bb[1] - bb[0], bb[3] - bb[2]
    return d


def place_hedge_module(donor, name, x, y, rot_z, schaal):
    root = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(root)
    for i, m in enumerate(donor["objs"]):
        c = m.copy()                      # deelt de mesh-data
        c.name = f"{name}_m{i}"
        c.parent = root
        c.location = (-donor["lokaal_midden"][0], -donor["lokaal_midden"][1], 0.0)
        c.rotation_euler = (0.0, 0.0, 0.0)
        c.scale = (1.0, 1.0, 1.0)
        c.hide_render = False
        c.hide_viewport = False
        bpy.context.scene.collection.objects.link(c)
    root.location = (x, y, 0.0)
    root.rotation_euler = (0.0, 0.0, rot_z)
    root.scale = schaal
    bpy.context.view_layer.update()
    # haagvoet op het laagste maaiveld onder de module
    bb = cl.wbbox_meshes([c for c in root.children if c.type == "MESH"])
    gz = min(ground_height(px, py) for px in (bb[0], (bb[0] + bb[1]) / 2, bb[1])
             for py in (bb[2], (bb[2] + bb[3]) / 2, bb[3]))
    root.location.z = gz
    return root


def place_hedges(donor):
    """Alle rijen uit HAAG_RIJEN; om en om 180 graden gedraaid en gespiegeld."""
    L0 = donor["lengte"]
    rijen = {}
    teller = 0
    for naam, as_, a0, a1, mid, (sl, sd, sh) in HAAG_RIJEN:
        L = L0 * sl
        span = a1 - a0
        n = 1 if span <= L else math.ceil((span - L) / (L - HAAG_OVERLAP_MIN)) + 1
        stap = 0.0 if n == 1 else (span - L) / (n - 1)
        overlap = L - stap if n > 1 else 0.0
        for i in range(n):
            c = a0 + L / 2 + i * stap
            basis = 0.0 if as_ == "x" else math.pi / 2
            oneven = i % 2 == 1
            rot = basis + (math.pi if oneven else 0.0)
            schaal = (-sl if oneven else sl, sd, sh)
            x, y = (c, mid) if as_ == "x" else (mid, c)
            place_hedge_module(donor, f"{naam}_{i}", x, y, rot, schaal)
            teller += 1
        rijen[naam] = {"modules": n, "overlap_m": round(overlap, 2), "schaal": [sl, sd, sh],
                       "hoogte_m": round(sh * (donor["h"] + donor["lokaal_zmin"]), 2), "diepte_m": round(sd * donor["diepte"], 2)}
    return {"modules": teller, "rijen": rijen, "donor_verts": donor["verts"],
            "bessen_vervangen": donor["bessen_vervangen"], "bessen_materiaal": donor["bessen_materiaal"]}


# --------------------------------------------------------------------------- gazon
GAZON_GEBIED = (0.0, 14.3, 0.0, 12.4)     # binnen de hagen; buiten de hagen zit de bodemlaag (v4)
# Twee bronnen, gekozen op een gazoncrop voor de hut (v4):
#  "bk": BK Mown Grass-plukken (~5 cm), v1-v3 lazen als klimop/bodembedekker;
#  "ph": PH grass_medium_02 op 8-12 cm (terugval uit plan §3).
GAZON_BRON = {
    # v5: korter (3-4 cm), dichter en lichter, zodat het van afstand egaal gemaaid leest
    "bk": dict(dichtheid=2600.0, schaal=(0.55, 0.75), hsv=(1.0, 2.1), z=0.015),
    # fix_gazon: PH grass_medium_02 kort geschaald (pollen 16-40 cm -> ~4-8 cm)
    "ph": dict(dichtheid=1400.0, schaal=(0.22, 0.32), hsv=None, z=0.0),
    # fix_gazon: BK "Garden Grass Free" (a459e09d, royalty_free): gemodelleerde grassprieten,
    # 8-34 vlakken per pol; pollen 8-9 cm -> ~5 cm, losse sprieten 4-5 cm -> ~3 cm.
    # Ronde 1 (2200 losse pollen/m2) was ijl en strogeel. Ronde 2: pollen samengevoegd tot
    # 'zoden' (bouw_zoden), zodat ~9000 pollen/m2 met maar ~11.000 instances kan; kleur x tint.
    # Ronde 3: korter (schaal 0,45-0,62 -> ~3-5 cm) en overlap 4 (ronde 2 liet gaten zien).
    "tuin": dict(zode=dict(varianten=6, straal=0.08, pollen_per_m2=3000.0, overlap=4.0),
                 schaal=(0.45, 0.62), hsv=None, z=0.0, tint=(0.50, 1.0, 0.42), val=1.15, sat=1.1),
    # fix_gazon: BK "grass lawn cut 1x1 m" (e89bded5, royalty_free): gemaaide pollen 7-13 cm -> ~5 cm
    "kort": dict(dichtheid=1100.0, schaal=(0.42, 0.55), hsv=None, z=0.0),
}
GAZON_KLEUR = dict(baan_m=1.6, baan_val=0.07, vlek_m=2.2, vlek_hue=0.025, vlek_val=0.10)


def gazon_kleurvariatie(mat, cfg=GAZON_KLEUR, tint=None, val_basis=1.0, sat=1.0):
    """Kleurvariatie op wereldpositie, ingevoegd vóór de basiskleur van het grasmateriaal.
    tint: eerst de bronkleur x deze kleur (strogeel -> frisgroen); val_basis/sat: basisniveau.
    Daarna:
    - maaibanen: banen van baan_m breed langs Y (de HeroCam kijkt langs Y), om en om
      +-baan_val helderheid, met zachte overgang;
    - vlekken: ruis op ~vlek_m, hue +-vlek_hue (iets geler / iets blauwer groen) en +-vlek_val.
    Wereldpositie (Geometry.Position) omdat de instances geen eigen UV-vlak over de tuin hebben."""
    nt = mat.node_tree
    doel = None
    for n in nt.nodes:
        if n.type == "BSDF_PRINCIPLED" and n.inputs["Base Color"].is_linked:
            doel = n.inputs["Base Color"]
        elif n.type == "GROUP" and "Diffuse" in n.inputs and n.inputs["Diffuse"].is_linked:
            doel = n.inputs["Diffuse"]
    if doel is None:
        raise RtkFout(f"gazonmateriaal {mat.name}: geen gelinkte basiskleur om variatie op te zetten")
    bron = doel.links[0].from_socket
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    # maaibanen: Wave Bands langs X, sinus; periode = 2 banen
    golf = nt.nodes.new("ShaderNodeTexWave")
    golf.wave_type, golf.bands_direction, golf.wave_profile = "BANDS", "X", "SIN"
    golf.inputs["Scale"].default_value = 2 * math.pi / (20.0 * 2 * cfg["baan_m"])   # Cycles: n = x * 20
    golf.inputs["Distortion"].default_value = 0.0
    nt.links.new(geo.outputs["Position"], golf.inputs["Vector"])
    baan = nt.nodes.new("ShaderNodeMapRange")       # sinus -> bijna-blok met zachte rand
    baan.inputs["From Min"].default_value, baan.inputs["From Max"].default_value = 0.35, 0.65
    baan.inputs["To Min"].default_value = 1.0 - cfg["baan_val"]
    baan.inputs["To Max"].default_value = 1.0 + cfg["baan_val"]
    nt.links.new(golf.outputs["Fac"], baan.inputs["Value"])
    ruis = nt.nodes.new("ShaderNodeTexNoise")
    ruis.inputs["Scale"].default_value = 1.0 / cfg["vlek_m"]
    ruis.inputs["Detail"].default_value = 3.0
    nt.links.new(geo.outputs["Position"], ruis.inputs["Vector"])
    hue = nt.nodes.new("ShaderNodeMapRange")
    hue.inputs["From Min"].default_value, hue.inputs["From Max"].default_value = 0.35, 0.65
    hue.inputs["To Min"].default_value = 0.5 + cfg["vlek_hue"]       # iets geler
    hue.inputs["To Max"].default_value = 0.5 - cfg["vlek_hue"]       # iets blauwer
    nt.links.new(ruis.outputs["Fac"], hue.inputs["Value"])
    ruis2 = nt.nodes.new("ShaderNodeTexNoise")
    ruis2.noise_dimensions = "4D"                 # eerst: de W-ingang bestaat alleen in 4D
    ruis2.inputs["Scale"].default_value = 1.6 / cfg["vlek_m"]
    ruis2.inputs["Detail"].default_value = 2.0
    ruis2.inputs["W"].default_value = 3.7
    nt.links.new(geo.outputs["Position"], ruis2.inputs["Vector"])
    val = nt.nodes.new("ShaderNodeMapRange")
    val.inputs["From Min"].default_value, val.inputs["From Max"].default_value = 0.35, 0.65
    val.inputs["To Min"].default_value = (1.0 - cfg["vlek_val"]) * val_basis
    val.inputs["To Max"].default_value = (1.0 + cfg["vlek_val"]) * val_basis
    nt.links.new(ruis2.outputs["Fac"], val.inputs["Value"])
    keer = nt.nodes.new("ShaderNodeMath")
    keer.operation = "MULTIPLY"
    nt.links.new(baan.outputs["Result"], keer.inputs[0])
    nt.links.new(val.outputs["Result"], keer.inputs[1])
    if tint is not None:
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.blend_type = "MULTIPLY"
        mix.inputs[0].default_value = 1.0
        mix.inputs[7].default_value = (*tint, 1.0)
        nt.links.new(bron, mix.inputs[6])
        bron = mix.outputs[2]
    hsv = nt.nodes.new("ShaderNodeHueSaturation")
    hsv.inputs["Saturation"].default_value = sat
    nt.links.new(bron, hsv.inputs["Color"])
    nt.links.new(hue.outputs["Result"], hsv.inputs["Hue"])
    nt.links.new(keer.outputs["Value"], hsv.inputs["Value"])
    nt.links.new(hsv.outputs["Color"], doel)
    return hsv


GAZON_BODEM_TINT = (0.22, 0.34, 0.12)   # ronde 2/3 (0,42/0,62/0,26 en 0,30/0,45/0,16): gaten lazen bleek grijs


def gazon_bodem(mat, tint=GAZON_BODEM_TINT):
    """Gazonbodem (PH leafy_grass) x groen: in ronde 1 schemerde hij roze-bruin tussen de sprieten
    door. Nu leest een gat als schaduw tussen het gras, niet als aarde."""
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    if not bsdf.inputs["Base Color"].is_linked:
        raise RtkFout(f"gazonbodem {mat.name}: geen textuur op de basiskleur")
    lk = bsdf.inputs["Base Color"].links[0]
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.blend_type = "MULTIPLY"
    mix.inputs[0].default_value = 1.0
    mix.inputs[7].default_value = (*tint, 1.0)
    hs = nt.nodes.new("ShaderNodeHueSaturation")
    hs.inputs["Saturation"].default_value = 0.8            # textuurkleur (bruin/roze) deels weg
    nt.links.new(lk.from_socket, hs.inputs["Color"])
    nt.links.new(hs.outputs["Color"], mix.inputs[6])
    nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
    return mat


def laad_gazon_donor(bron):
    """Donorcollectie + pollen voor een gazonbron uit GAZON_BRON (zie daar)."""
    bk = ROOT / "assets" / "blenderkit" / "renders2"
    if bron == "bk":
        coll, plukken = load_ph_collection(bk / "Mown_Grass_Large_area.blend",
                                           "RTK_GrasPlukken", lambda n: n.startswith("enggrass"))
    elif bron == "tuin":
        # alleen de sprietmeshes; de "GN Make Custer"-objecten (1 vertex) niet
        coll, plukken = load_ph_collection(bk / "Garden_Grass_Free.blend", "RTK_GrasPlukken",
                                           lambda n: n.startswith(("Lawn_Grass_Grown_L", "Garden Grass Loose_S_",
                                                                   "Garden Grass Loose_M_")))
        for o in plukken:
            o.modifiers.clear()          # 'Smooth by Angle'-modifier: alleen shading, niet nodig
    elif bron == "kort":
        # alleen de groene pollen (materiaal 'grass'), niet de dode ('grass dead')
        coll, alle = load_ph_collection(bk / "grass_lawn_cut_1x1_m.blend", "RTK_GrasPlukken",
                                        lambda n: n.startswith("Plane."))
        plukken = []
        for o in alle:
            if all(s.material and s.material.name.startswith("grass") and "dead" not in s.material.name
                   for s in o.material_slots):
                plukken.append(o)
            else:
                bpy.data.objects.remove(o, do_unlink=True)
    else:
        coll, plukken = load_ph_collection(ROOT / "assets" / "polyhaven" / "models" / "grass_medium_02_2k.blend",
                                           "RTK_GrasPlukken", lambda n: n.startswith("grass_medium_02_")
                                           and not n.endswith("_geo") and "geometry" not in n)
        groen_gras(plukken)
    return coll, plukken


def gazon_scatter(ob, bron, bodem_mat, seed=26):
    """Gras-instances op de emitter `ob` (Gazon) volgens GAZON_BRON[bron]; geeft info-dict."""
    cfg = GAZON_BRON[bron]
    coll, plukken = laad_gazon_donor(bron)
    mats = {sl.material for o in plukken for sl in o.material_slots if sl.material}
    if cfg["hsv"]:
        for m in mats:
            for n in m.node_tree.nodes:
                if n.type == "HUE_SAT":
                    n.inputs["Saturation"].default_value, n.inputs["Value"].default_value = cfg["hsv"]
    if bron != "bk":                     # "bk" = de oude stand (v5), ongewijzigd ter vergelijking
        for m in mats:
            gazon_kleurvariatie(m, tint=cfg.get("tint"), val_basis=cfg.get("val", 1.0), sat=cfg.get("sat", 1.0))
    voet = min(min(v[2] for v in o.bound_box) for o in plukken)
    info = {"bron": bron, "plukken": [o.name for o in plukken], "schaal": cfg["schaal"],
            "voet_z_donor": round(voet, 4), "pol_h_m": [round(o.dimensions.z, 3) for o in plukken]}
    if "zode" in cfg:
        z = cfg["zode"]
        coll, zinfo = bouw_zoden(plukken, z["varianten"], z["straal"], z["pollen_per_m2"], cfg["schaal"], seed)
        dichtheid = z["overlap"] / (math.pi * z["straal"] ** 2)
        gn_scatter(ob, coll, z["varianten"], (0.9, 1.1), seed, dichtheid=dichtheid, z_offset=cfg["z"],
                   bodem_mat=bodem_mat)
        info.update(zoden=zinfo, dichtheid=round(dichtheid, 1),
                    pollen_per_m2_effectief=round(z["pollen_per_m2"] * z["overlap"]))
    else:
        gn_scatter(ob, coll, len(plukken), cfg["schaal"], seed, dichtheid=cfg["dichtheid"],
                   z_offset=cfg["z"], bodem_mat=bodem_mat)
        info["dichtheid"] = cfg["dichtheid"]
    return info


def bouw_zoden(pollen, n_var, straal, pollen_per_m2, schaal, seed):
    """Voegt grassprieten samen tot `n_var` ronde 'zoden' (straal m) met pollen_per_m2 erin.

    Waarom: losse sprieten als instances vragen bij gazondichtheid (~9000/m2 op 73 m2) ~660.000
    instances; als zode van ~60 pollen zijn het er ~11.000, met dezelfde sprieten. Grens: binnen
    één zode herhaalt het patroon; 6 varianten + willekeurige draaiing maken dat onzichtbaar
    op meer dan ~0,5 m. Elke zode is één mesh in een eigen donorcollectie."""
    rnd = random.Random(seed + 101)
    coll = bpy.data.collections.new("RTK_GrasZoden")
    donor_collection().children.link(coll)
    k = max(1, int(round(pollen_per_m2 * math.pi * straal ** 2)))
    mat = pollen[0].material_slots[0].material
    vlakken = []
    for vi in range(n_var):
        bm = bmesh.new()
        for _ in range(k):
            bron = rnd.choice(pollen)
            n0 = len(bm.verts)
            bm.from_mesh(bron.data)
            bm.verts.ensure_lookup_table()
            nieuw = bm.verts[n0:]
            r, a = straal * math.sqrt(rnd.random()), rnd.uniform(0, 2 * math.pi)
            s = rnd.uniform(*schaal)
            m = (Matrix.Translation((r * math.cos(a), r * math.sin(a), 0.0))
                 @ Matrix.Rotation(rnd.uniform(0, 2 * math.pi), 4, "Z")
                 @ Matrix.Rotation(rnd.uniform(-0.12, 0.12), 4, "X")       # niet allemaal kaarsrecht
                 @ Matrix.Scale(s, 4))
            bmesh.ops.transform(bm, matrix=m, verts=nieuw)
        me = bpy.data.meshes.new(f"RTK_Zode_{vi}")
        bm.to_mesh(me)
        bm.free()
        for p in me.polygons:
            p.material_index = 0
        me.materials.append(mat)
        ob = bpy.data.objects.new(f"RTK_Zode_{vi}", me)
        coll.objects.link(ob)
        vlakken.append(len(me.polygons))
    return coll, {"varianten": n_var, "straal_m": straal, "pollen_per_zode": k, "vlakken": vlakken}


def make_lawn(bron, route_sdf, bedden, haag_voeten, hut_rect, bodem_mat, cell=0.04, vrij_route=0.10,
              vrij_bed=-0.03, bekken_kern=0.035):
    """Gazon als GN-scatter (plan §7 deel H) op een lichte gazonbodem (bodem_mat).

    Plan §7 noemt "vrij van route + 0,15 m" en "gras loopt 3-5 cm over de rand": met plukken van
    ~10-14 cm breed geeft vrij_route 0,10 m dat overhangen (v1 met 0,15 liet een kale strook).
    Emitter = maaiveldraster binnen GAZON_GEBIED zonder route + vrij_route, bedden, bekkenkern,
    haagvoet en hut.
    """
    cfg = GAZON_BRON[bron]

    def vrij(x, y):
        if route_sdf(x, y) < vrij_route:
            return False
        if any(sdf_rect(x, y, r) < vrij_bed for r in bedden.values()):
            return False
        if basin_depth(x, y) > bekken_kern:
            return False
        if any(sdf_rect(x, y, r) < 0.0 for r in haag_voeten):
            return False
        if sdf_rect(x, y, hut_rect) < 0.0:
            return False
        return True

    ob, opp = grid_emitter("Gazon", GAZON_GEBIED, cell, vrij, z_offset=0.003)
    info = gazon_scatter(ob, bron, bodem_mat)
    info.update(oppervlak_m2=round(opp, 1), verwacht_instances=int(opp * info["dichtheid"]),
                vrij_route_m=vrij_route, bodem=bodem_mat.name)
    return info


# --------------------------------------------------------------------------- onderbegroeiing (v4)
# Opdracht v4: buiten de hagen geen kale bosvloer. Struiklaag 1-6 m buiten de haag (PH shrub_02,
# 1,3-1,6 m, schaal 0,8-1,2, groepjes) en een bodemlaag tot 40 m (PH fern_02 en grass_medium_02 lang).
TUIN_HAAG = (-0.1, 14.4, -0.1, 12.5)
BODEM_GEBIED = (-35.0, 50.0, -35.0, 48.0)


def make_undergrowth(rnd, sun_compass, sun_elev):
    struik_coll, struiken = load_ph_collection(ROOT / "assets" / "polyhaven" / "models" / "shrub_02_2k.blend",
                                               "RTK_Struiken", lambda n: n.endswith("LOD0"))
    # groepsmiddens 1-6 m buiten de haag, 3-6 struiken per groep
    def zone(x, y):
        return 1.0 <= dist_to_rect(x, y, TUIN_HAAG) <= 6.0
    b = (TUIN_HAAG[0] - 6, TUIN_HAAG[1] + 6, TUIN_HAAG[2] - 6, TUIN_HAAG[3] + 6)
    punten, geweigerd_zon = [], 0
    for gx, gy in poisson_groepen(rnd, zone, b, 2.5, 3.5, pogingen=4000):
        for _ in range(rnd.randint(4, 8)):
            a, r = rnd.uniform(0, 2 * math.pi), rnd.uniform(0.0, 1.6)
            x, y = gx + r * math.cos(a), gy + r * math.sin(a)
            if not zone(x, y):
                continue
            if shadow_hits_garden(x, y, 1.9, 0.9, sun_compass, sun_elev, marge=0.3, kroon_begin=0.0):
                geweigerd_zon += 1
                continue
            punten.append((x, y))
    me = bpy.data.meshes.new("Struiklaag")
    me.from_pydata([(x - 7.0, y - 6.0, ground_height(x, y)) for x, y in punten], [], [])
    st = bpy.data.objects.new("Struiklaag", me)
    st.location = (7.0, 6.0, 0.0)
    bpy.context.scene.collection.objects.link(st)
    gn_scatter(st, struik_coll, len(struiken), (0.8, 1.2), 41)

    bodem_coll = bpy.data.collections.new("RTK_Bodemlaag")
    donor_collection().children.link(bodem_coll)
    varen_coll, varens = load_ph_collection(ROOT / "assets" / "polyhaven" / "models" / "fern_02_2k.blend",
                                            "RTK_Varens", lambda n: n.startswith("fern_02_"))
    gras_coll, grassen = load_ph_collection(ROOT / "assets" / "polyhaven" / "models" / "grass_medium_02_2k.blend",
                                            "RTK_RuigGras", lambda n: n.startswith("grass_medium_02_")
                                            and not n.endswith("_geo") and "geometry" not in n)
    groen_gras(grassen)
    groen_struik(struiken)

    def buiten(x, y):
        return dist_to_rect(x, y, TUIN_HAAG) > 0.3
    bl, opp = grid_emitter("Bodemlaag_Gras", BODEM_GEBIED, 0.5, buiten, z_offset=0.0)
    gn_scatter(bl, gras_coll, len(grassen), (1.6, 2.6), 51, dichtheid=16.0)   # v5: was 5/m2, ijl
    bv, _ = grid_emitter("Bodemlaag_Varen", BODEM_GEBIED, 0.5, buiten, z_offset=0.0)
    gn_scatter(bv, varen_coll, len(varens), (0.8, 1.2), 61, dichtheid=2.0)    # v5: was 0,7/m2
    return {"struiken": len(punten), "struik_geweigerd_zon": geweigerd_zon,
            "bodem_oppervlak_m2": round(opp, 0), "ruig_gras_verwacht": int(opp * 16.0),
            "varens_verwacht": int(opp * 2.0), "bronnen": ["shrub_02_2k (LOD0)", "fern_02_2k", "grass_medium_02_2k"]}


# --------------------------------------------------------------------------- boomrand
def shadow_hits_garden(x, y, h, kroon_r, sun_compass_deg, sun_elev_deg, marge=1.0, factor=2.1,
                       kroon_begin=0.3):
    """Zou de schaduw van deze boom (lengte factor x h) de tuin raken?

    Plan §4: in de zonsector geen boom dichter dan 2,1 x zijn hoogte bij de tuin. Hier
    precies uitgerekend: de schaduw van de kroon (vanaf kroon_begin x de lengte; de dunne
    stam telt niet) valt weg van de zon; dat segment, verbreed met de kroonstraal + marge,
    mag de tuin niet raken.
    """
    c = math.radians(sun_compass_deg)
    dx, dy = -math.sin(c), -math.cos(c)
    lengte = factor * h
    stappen = max(2, int(lengte / 0.5))
    for k in range(stappen + 1):
        t = lengte * (kroon_begin + (1 - kroon_begin) * k / stappen)
        if dist_to_rect(x + dx * t, y + dy * t, GARDEN) < kroon_r + marge:
            return True
    return False


def poisson_groepen(rnd, in_zone, bounds, d_min, d_max, pogingen=6000):
    """Groepsmiddens met onderlinge afstand d_min..d_max (dart throwing, per punt eigen straal)."""
    x0, x1, y0, y1 = bounds
    punten = []
    for _ in range(pogingen):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if not in_zone(x, y):
            continue
        r = rnd.uniform(d_min, d_max)
        if all(math.hypot(x - px, y - py) >= max(r, pr) for px, py, pr in punten):
            punten.append((x, y, r))
    return [(x, y) for x, y, _ in punten]


# --------------------------------------------------------------------------- raycasts
IGNORE_PREFIX = ("Mist_Rig",)


def root_of(obj):
    while obj.parent is not None:
        obj = obj.parent
    return obj


def classify(obj):
    if obj is None:
        return "lucht"
    r = root_of(obj)
    n = r.name
    if n == "Cabin_Root":
        return "hut"
    if n.startswith("Haag_"):
        return "haag"
    if n.startswith(("Boom_", "Berk_", "leaves_")):   # leaves_* = bladeren van de berk (GN-instances)
        return "boom"
    if n.startswith(("Struiklaag", "shrub_02")):
        return "struik"
    if n.startswith(("Ground", "Gazon", "Bed_", "Bodemlaag", "fern_", "grass_medium", "enggrass", "shrub_0")):
        return "grond"
    return "ander"


def first_hit(scene, dg, origin, direction, dist=3000.0, ignore=IGNORE_PREFIX):
    o = Vector(origin)
    d = Vector(direction).normalized()
    rest = dist
    for _ in range(32):
        hit, loc, _nor, _idx, obj, _mat = scene.ray_cast(dg, o, d, distance=rest)
        if not hit:
            return None, None
        if obj is not None and obj.name.startswith(ignore):
            stap = (loc - o).length + 1e-3
            o = loc + d * 1e-3
            rest -= stap
            if rest <= 0:
                return None, None
            continue
        return obj, loc
    return None, None


def to_sun_vector(sun_obj):
    return (sun_obj.matrix_world.to_quaternion() @ Vector((0.0, 0.0, 1.0))).normalized()


def shadow_test(scene, sun_obj, hut_rect, haag_rects, step=0.5, z0=0.3, max_boom=0.20,
                hut_west_x=7.3):
    """Plan §5: raster over de tuin, per punt een straal naar de zon. Eis: boomschaduw <= 20%,
    hutschaduw > 0 ten westen van X 7,3."""
    dg = bpy.context.evaluated_depsgraph_get()
    zon = to_sun_vector(sun_obj)
    # "struik": classify() kent die klasse (Struiklaag, shrub_02); sinds fix_gazon staat shrub_02 ook
    # in de oostborder en raakt een straal hem binnen de tuin
    tel = {"hut": 0, "haag": 0, "boom": 0, "struik": 0, "lucht": 0, "grond": 0, "ander": 0}
    boom_punten, ander_namen = [], {}
    hut_west = 0
    n = 0
    x0, x1, y0, y1 = GARDEN
    nx, ny = int(round((x1 - x0) / step)), int(round((y1 - y0) / step))
    for i in range(nx + 1):
        for j in range(ny + 1):
            x, y = x0 + i * step, y0 + j * step
            if sdf_rect(x, y, hut_rect) <= 0.05:
                continue
            if any(sdf_rect(x, y, r) <= 0.0 for r in haag_rects):
                continue
            n += 1
            obj, _loc = first_hit(scene, dg, (x, y, ground_height(x, y) + z0), zon)
            k = classify(obj)
            tel[k] += 1
            if k == "boom":
                boom_punten.append([x, y, root_of(obj).name])
            if k == "ander":
                ander_namen[obj.name] = ander_namen.get(obj.name, 0) + 1
            if k == "hut" and x < hut_west_x:
                hut_west += 1
    boom_frac = tel["boom"] / max(n, 1)
    ok = boom_frac <= max_boom and hut_west > 0
    return {"ok": ok, "punten": n, "telling": tel, "boom_pct": round(100 * boom_frac, 1),
            "hut_pct": round(100 * tel["hut"] / max(n, 1), 1), "hut_west_punten": hut_west,
            "eis": f"boom <= {int(max_boom * 100)}%, hutschaduw ten westen van X {hut_west_x} > 0",
            "boom_punten_eerste_40": boom_punten[:40], "ander": ander_namen,
            "zon_vector": [round(v, 4) for v in zon]}


# Luchttoets op 10 en 15 graden (opdracht v4 van de projectsessie): op 0-6 graden sluiten ring 2,
# ring 3 en de ring 4-kaarten de lucht ook zonder ring 1, waardoor de toets ring 1 niet ving.
# Op 10/15 graden telt ring 1 wel. Eis = midden tussen de meting met en zonder ring 1
# (beide oorsprongen samen). De meting met/zonder ring 1 staat in audit.json -> luchttoets_ring1.
# None = nog niet gemeten: dan geen eis op die elevatie.
# Gemeten in anker v4 (HeroCam + tuinmidden samen): 10 graden 98,6% met en 98,6% zonder ring 1,
# 15 graden 89,7% met en 88,3% zonder ring 1. Eis = het midden. Let op: op 10 graden maakt ring 1
# geen verschil (ring 2 dekt daar al) en op 15 graden is de marge maar 0,7 procentpunt.
LUCHT_EIS_HOOG = {10.0: 0.986, 15.0: 0.890}
LUCHT_DICHT = ("boom", "haag", "hut", "struik")


def sky_closure(scene, origins, az_step=2, elevs=(0.0, 3.0, 6.0), eis=0.95, hoog=(10.0, 15.0),
                eis_hoog=None):
    """Plan §4: stralen rondom per az_step graden op elevs; >= 95% moet boom of haag raken.
    Daarnaast per elevatie in `hoog` een eigen eis (eis_hoog, fractie; standaard LUCHT_EIS_HOOG).

    De hut en de struiklaag tellen ook als dicht; ze worden apart geteld.
    Let op: een straal raakt een bladkaartje ook waar de alpha doorzichtig is; de toets
    overschat de dichtheid dus iets. Lucht tussen stammen vangt hij wel.
    """
    eis_hoog = LUCHT_EIS_HOOG if eis_hoog is None else eis_hoog
    dg = bpy.context.evaluated_depsgraph_get()
    uit = {"ok": True, "eis_pct": eis * 100, "per_origin": {},
           "eis_hoog_pct": {str(k): (None if v is None else round(100 * v, 1)) for k, v in eis_hoog.items()}}
    hoog_tel = {el: [0, 0] for el in hoog}
    for naam, org in origins.items():
        tel = {"boom": 0, "haag": 0, "hut": 0, "struik": 0, "lucht": 0, "grond": 0, "ander": 0}
        gaten = []
        n = 0
        for el in tuple(elevs) + tuple(hoog):
            for az in range(0, 360, az_step):
                a, e = math.radians(az), math.radians(el)
                d = (math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e))
                obj, _ = first_hit(scene, dg, org, d)
                k = classify(obj)
                if el in hoog:
                    hoog_tel[el][1] += 1
                    hoog_tel[el][0] += k in LUCHT_DICHT
                    continue
                tel[k] += 1
                n += 1
                if k not in LUCHT_DICHT:
                    gaten.append([az, el, k if k not in ("ander", "grond") else obj.name])
        dicht = sum(tel[k] for k in LUCHT_DICHT) / n
        ok = dicht >= eis
        uit["per_origin"][naam] = {"ok": ok, "stralen": n, "dicht_pct": round(100 * dicht, 1),
                                   "telling": tel, "gaten": gaten}
        uit["ok"] = uit["ok"] and ok
    uit["dicht_pct_min"] = min(v["dicht_pct"] for v in uit["per_origin"].values())
    uit["hoog_dicht_pct"] = {}
    for el, (raak, tot) in hoog_tel.items():
        frac = raak / max(tot, 1)
        uit["hoog_dicht_pct"][str(el)] = round(100 * frac, 1)
        e = eis_hoog.get(el)
        if e is not None and frac < e:
            uit["ok"] = False
    return uit


# --------------------------------------------------------------------------- eigen audit
def _world_verts_in_box(obj, box, max_n=None):
    """Aantal vertices (wereld) van obj binnen box (x0,x1,y0,y1,z0,z1)."""
    import numpy as np
    me = obj.data
    n = len(me.vertices)
    if n == 0:
        return 0
    co = np.empty(n * 3, dtype=np.float32)
    me.vertices.foreach_get("co", co)
    co = co.reshape(n, 3)
    m = np.array(obj.matrix_world, dtype=np.float32)
    w = co @ m[:3, :3].T + m[:3, 3]
    x0, x1, y0, y1, z0, z1 = box
    binnen = ((w[:, 0] > x0) & (w[:, 0] < x1) & (w[:, 1] > y0) & (w[:, 1] < y1)
              & (w[:, 2] > z0) & (w[:, 2] < z1))
    return int(binnen.sum())


def audit_extra(closed_box, route_obj=None, route_sdf=None, gazon_obj=None, gazon_vrij=0.10):
    """Plan §7 punt 2: eigen audit. closed_box = binnenruimte (x0,x1,y0,y1,z0,z1)."""
    fouten, info = [], {}
    bpy.context.view_layer.update()
    # 1. niets in de gesloten ruimte
    in_hut = []
    for o in bpy.context.scene.objects:
        if o.type != "MESH" or o.hide_render or not o.visible_get():
            continue
        if root_of(o).name == "Cabin_Root":
            continue
        bb = cl.wbbox_meshes([o])
        if bb[1] < closed_box[0] or bb[0] > closed_box[1] or bb[3] < closed_box[2] \
                or bb[2] > closed_box[3] or bb[5] < closed_box[4] or bb[4] > closed_box[5]:
            continue
        k = _world_verts_in_box(o, closed_box)
        if k:
            in_hut.append(f"{o.name} ({k} vertices)")
    if in_hut:
        fouten.append(f"in de gesloten ruimte: {in_hut[:10]}")
    info["in_gesloten_ruimte"] = in_hut

    # 2/3/4. zwevend, boomoorsprong, boomschaal
    zwevend, oorsprong, schaal = [], [], []
    roots = [o for o in bpy.context.scene.objects
             if o.parent is None and o.name.startswith(("Boom_", "Berk_", "Haag_"))]
    for r in roots:
        ms = [c for c in r.children_recursive if c.type == "MESH"]
        if not ms:
            continue
        bb = cl.wbbox_meshes(ms)
        if r.name.startswith("Haag_"):
            # haag: laagste punt over de hele lengte, grond als laagste maaiveld eronder
            gz = min(ground_height(x, y) for x in (bb[0], (bb[0] + bb[1]) / 2, bb[1])
                     for y in (bb[2], (bb[2] + bb[3]) / 2, bb[3]))
        else:
            gz = ground_height(r.location.x, r.location.y)
        if bb[4] - gz > 0.05:
            zwevend.append(f"{r.name} {bb[4] - gz:.3f} m boven maaiveld")
        if not r.name.startswith("Haag_"):
            if abs(r.location.z - gz) > 0.15:
                oorsprong.append(f"{r.name} oorsprong z {r.location.z:.2f}, maaiveld {gz:.2f}")
            s = r.get("rtk_schaal")
            if s is None or not (SCHAAL_MIN - 1e-6 <= s <= SCHAAL_MAX + 1e-6) \
                    or abs(r.scale[0] - s) > 1e-4:
                schaal.append(f"{r.name} schaal {r.scale[0]:.3f} (opgegeven {s})")
    for naam, lijst in (("zwevend", zwevend), ("boomoorsprong", oorsprong), ("boomschaal", schaal)):
        if lijst:
            fouten.append(f"{naam}: {lijst[:8]}")
        info[naam] = lijst
    info["roots_gecontroleerd"] = len(roots)

    # 5. ontbrekende texturen
    mist = []
    import os
    for img in bpy.data.images:
        if img.name in ("Render Result", "Viewer Node") or img.users == 0:
            continue
        if img.packed_file:
            continue
        ap = bpy.path.abspath(img.filepath) if img.filepath else ""
        if img.source == "FILE" and (not ap or not os.path.exists(ap)):
            mist.append(img.name)
    for m in bpy.data.materials:
        if m.users and m.use_nodes:
            for nd in m.node_tree.nodes:
                if nd.type == "TEX_IMAGE" and nd.image is None and nd.outputs["Color"].is_linked:
                    mist.append(f"{m.name}: lege beeldnode")
    if mist:
        fouten.append(f"ontbrekende texturen: {mist[:10]}")
    info["ontbrekende_texturen"] = mist

    # 6. geen gras op Route_Steen
    if gazon_obj is not None and route_sdf is not None:
        dg = bpy.context.evaluated_depsgraph_get()
        op_route, n = 0, 0
        for inst in dg.object_instances:
            if not inst.is_instance or inst.parent is None or inst.parent.original != gazon_obj:
                continue
            n += 1
            p = inst.matrix_world.translation
            if route_sdf(p.x, p.y) < gazon_vrij:
                op_route += 1
        info["gras_instances"] = n
        info["gras_op_route"] = op_route
        if n == 0:
            fouten.append("gazon heeft 0 instances")
        if op_route:
            fouten.append(f"{op_route} grasplukken binnen {gazon_vrij} m van Route_Steen")
    return {"ok": not fouten, "fouten": fouten, **info}


def random_from_seed(seed):
    return random.Random(seed)
