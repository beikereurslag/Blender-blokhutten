r"""Renders 2.0 - De Regentuinkamer v2, stap 2: BEKKEN + WATER (plan §7, laag 2).

Opbouwen + toetsen + opslaan (geen videokaart):
  blender -b regentuinkamer_v2_anker.blend --python stap2_bekken.py -- --geen-render
Alleen de diag-render (opent regentuinkamer_v2_laag2.blend):
  blender -b regentuinkamer_v2_laag2.blend --python stap2_bekken.py -- --alleen-render

Wat er komt:
- Bekken_Bodem: donkere natte bodem in de kom (PH brown_mud, oever PH forrest_ground), met een
  laag reliëf: twee kommetjes en een drempel, zodat er twee losse plassen ontstaan;
- Water_Plas_A en _B: IOR 1,33, roughness 0,02, elk op een eigen z, nooit overlappend;
- B2_Stenen: natte stenenrand van PH rock_moss_set_02 (CC0; het Sketchfab-mosstenenpack heeft
  geen licentiebestand), half ingegraven; alleen stenen in het lage deel zijn nat;
- B2_Oever_*: oeverplanten (PH grass_medium_02, periwinkle_plant, fern_02), laag aan de oostkant;
- het gazon wijkt in de oeverband (bekkendiepte > 1,2 cm) voor vochtige oevergrond.
Versie via RTK_VERSIE (standaard v1); werkmap previews\_werk\laag2_<versie>\.
Faalt een toets: niet opslaan, exitcode 1.
"""
import argparse
import math
import os
import sys
import time
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix
from mathutils.kdtree import KDTree

SCENE_DIR = Path(r"D:\Blender-blokhutten\scenes\regentuinkamer_v2")
sys.path.insert(0, str(SCENE_DIR))
import rtk_dressing as rd  # noqa: E402

rl, cl = rd.rl, rd.cl
INVOER = SCENE_DIR / "regentuinkamer_v2_anker.blend"
UITVOER = SCENE_DIR / "regentuinkamer_v2_laag2.blend"
VERSIE = os.environ.get("RTK_VERSIE", "v1")
WERK = SCENE_DIR / "previews" / "_werk" / f"laag2_{VERSIE}"
SEED = 2620
OEVER_DIEPTE = 0.012          # gazon weg waar de kom dieper is dan 1,2 cm
# v2: camera blijft waterpas (cl.add_camera), dus shift omlaag om de kom in beeld te krijgen
CAM_CLOSE = dict(loc=(6.9, 2.3, 1.45), doel=(4.6, 5.4, 0.0), lens=28, shift_y=-0.25)


def log(*a):
    print("[stap2]", *a, flush=True)


# =========================================================================== gazon uit de oeverband
def gazon_uit_oever():
    ob = bpy.data.objects["Gazon"]
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    mw = ob.matrix_world
    weg = []
    for f in bm.faces:
        c = mw @ f.calc_center_median()
        if rl.basin_depth(c.x, c.y) > OEVER_DIEPTE:
            weg.append(f)
    bmesh.ops.delete(bm, geom=weg, context="FACES")
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.update()
    log(f"gazon: {len(weg)} cellen weg uit de oeverband")
    return {"cellen_weg": len(weg), "drempel_m": OEVER_DIEPTE}


# =========================================================================== bodem
def bodem_materiaal():
    mat = bpy.data.materials.new("MAT_Bekken_Bodem")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(b.outputs["BSDF"], out.inputs["Surface"])
    uv = nt.nodes.new("ShaderNodeUVMap")
    uv.uv_map = "UVMap"

    def beeld(map_, sleutel, schaal, kleur=True):
        pad = next(p for p in (rd.PH_TEX / map_).iterdir() if sleutel in p.name)
        mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = (schaal, schaal, schaal)
        nt.links.new(uv.outputs["UV"], mp.inputs["Vector"])
        tx = nt.nodes.new("ShaderNodeTexImage")
        tx.image = bpy.data.images.load(str(pad), check_existing=True)
        if not kleur:
            tx.image.colorspace_settings.name = "Non-Color"
        nt.links.new(mp.outputs["Vector"], tx.inputs["Vector"])
        return tx.outputs["Color"]

    def attr(naam):
        a = nt.nodes.new("ShaderNodeAttribute")
        a.attribute_type = "GEOMETRY"
        a.attribute_name = naam
        return a.outputs["Fac"]

    modder = beeld("brown_mud", "diff", 1.6)
    oever = beeld("forrest_ground_01", "diff", 1.4)
    # oevergrond donkerder dan het gazon (vochtig), modder diep donkerbruin
    mix_o = nt.nodes.new("ShaderNodeMix")
    mix_o.data_type = "RGBA"
    nt.links.new(attr("oever"), mix_o.inputs[0])
    nt.links.new(modder, mix_o.inputs[6])
    nt.links.new(oever, mix_o.inputs[7])
    donker = nt.nodes.new("ShaderNodeMix")
    donker.data_type = "RGBA"
    donker.blend_type = "MULTIPLY"
    donker.inputs[0].default_value = 1.0
    donker.inputs[7].default_value = (0.30, 0.27, 0.22, 1.0)     # v2: v1 las als rode zandbak
    nt.links.new(mix_o.outputs[2], donker.inputs[6])
    nat_kleur = nt.nodes.new("ShaderNodeMix")      # nat = nog donkerder
    nat_kleur.data_type = "RGBA"
    nat_kleur.blend_type = "MULTIPLY"
    nt.links.new(attr("nat"), nat_kleur.inputs[0])
    nat_kleur.inputs[7].default_value = (0.66, 0.64, 0.60, 1.0)     # fix_gazon: was 0,55 (rand te zwart)
    nt.links.new(donker.outputs[2], nat_kleur.inputs[6])
    nt.links.new(nat_kleur.outputs[2], b.inputs["Base Color"])
    # ruwheid: droog 0,85 (v4-les: vochtig-glad spiegelde als betonplaat), nat bij het water 0,32;
    # fix_gazon: alleen het natste deel (nat > 0,8, smalle rand langs de waterlijn) naar 0,14, zodat
    # daar een lichte glans van de lucht ligt; de brede band blijft mat (geen betonplaat)
    ruw = nt.nodes.new("ShaderNodeMapRange")
    nt.links.new(attr("nat"), ruw.inputs["Value"])
    ruw.inputs["To Min"].default_value = 0.85
    ruw.inputs["To Max"].default_value = 0.32
    rand = nt.nodes.new("ShaderNodeMapRange")
    nt.links.new(attr("nat"), rand.inputs["Value"])
    rand.inputs["From Min"].default_value = 0.8
    rand.inputs["From Max"].default_value = 1.0
    rand.inputs["To Min"].default_value = 1.0
    rand.inputs["To Max"].default_value = 0.14 / 0.32
    ruw_tot = nt.nodes.new("ShaderNodeMath")
    ruw_tot.operation = "MULTIPLY"
    nt.links.new(ruw.outputs["Result"], ruw_tot.inputs[0])
    nt.links.new(rand.outputs["Result"], ruw_tot.inputs[1])
    nt.links.new(ruw_tot.outputs["Value"], b.inputs["Roughness"])
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nm.inputs["Strength"].default_value = 0.7
    nt.links.new(beeld("brown_mud", "nor_gl", 1.6, kleur=False), nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], b.inputs["Normal"])
    return mat


def maak_bodem(cel=0.03):
    """Bodemmesh over de kom (bekkendiepte > rd.BODEM_MIN_DIEPTE) op rd.bodem_z, met attributen
    'oever' (1 in de ondiepe rand) en 'nat' (wordt na de waterstand gezet)."""
    x0, x1, y0, y1 = 2.5, 7.0, 2.4, 8.2
    nx, ny = int(round((x1 - x0) / cel)), int(round((y1 - y0) / cel))
    bm = bmesh.new()
    verts = {}
    mid = (4.75, 5.30)

    def v(i, j):
        if (i, j) not in verts:
            x, y = x0 + i * cel, y0 + j * cel
            z = rd.bodem_z(x, y)
            if z is None:
                z = max(rl.ground_height(x, y), rd.grond_mesh_z(x, y)) + rd.BODEM_LIFT
            verts[(i, j)] = bm.verts.new((x - mid[0], y - mid[1], z))
        return verts[(i, j)]
    for i in range(nx):
        for j in range(ny):
            cx, cy = x0 + (i + 0.5) * cel, y0 + (j + 0.5) * cel
            if rl.basin_depth(cx, cy) <= rd.BODEM_MIN_DIEPTE:
                continue
            bm.faces.new((v(i, j), v(i + 1, j), v(i + 1, j + 1), v(i, j + 1)))
    uvl = bm.loops.layers.uv.new("UVMap")
    for f in bm.faces:
        for lp in f.loops:
            lp[uvl].uv = ((lp.vert.co.x + mid[0]) / 1.6, (lp.vert.co.y + mid[1]) / 1.6)
    me = bpy.data.meshes.new("Bekken_Bodem")
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new("Bekken_Bodem", me)
    ob.location = (mid[0], mid[1], 0.0)
    bpy.context.scene.collection.objects.link(ob)
    oever = [rd.smoothstep(0.035, 0.015, rl.basin_depth(vv.co.x + mid[0], vv.co.y + mid[1])) for vv in me.vertices]
    me.attributes.new("oever", "FLOAT", "POINT").data.foreach_set("value", oever)
    me.attributes.new("nat", "FLOAT", "POINT")
    ob.data.materials.append(bodem_materiaal())
    return ob


def grond_onder_kom_weg(drempel=0.011):   # v5: grotere kommen, dus alles onder de bodemmesh weg
    """Ground_Tuin-vlakken diep in de kom weg (alle hoeken dieper dan `drempel`): de kommetjes van
    de nieuwe bodem liggen tot ~1,4 cm onder de ankergrond, die er anders doorheen steekt (v3: rode
    vlekken op de plek van de plassen). Bekken_Bodem dekt alles vanaf 1,0 cm diepte."""
    g = bpy.data.objects["Ground_Tuin"]
    bm = bmesh.new()
    bm.from_mesh(g.data)
    mw = g.matrix_world
    weg = [f for f in bm.faces if all(rl.basin_depth(*(mw @ v.co).xy) > drempel for v in f.verts)]
    bmesh.ops.delete(bm, geom=weg, context="FACES")
    bm.to_mesh(g.data)
    bm.free()
    g.data.update()
    log(f"Ground_Tuin: {len(weg)} vlakken onder de kom weg")
    return len(weg)


# =========================================================================== water
def flood(start, niveau, cel, rand=0.006):
    """Cellen (i, j) op raster `cel` rond start waar de bodem onder niveau + rand ligt (4-buren)."""
    def ok(i, j):
        z = rd.bodem_z((i + 0.5) * cel, (j + 0.5) * cel)
        return z is not None and z < niveau + rand
    s = (int(start[0] / cel), int(start[1] / cel))
    if not ok(*s):
        raise rd.RtkFout(f"plas-start {start} ligt niet onder het waterniveau {niveau:.3f}")
    gezien, rij = {s}, [s]
    while rij:
        i, j = rij.pop()
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (i + d[0], j + d[1])
            if n not in gezien and ok(*n):
                gezien.add(n)
                rij.append(n)
        if len(gezien) > 40000:
            raise rd.RtkFout(f"plas rond {start} loopt over (> 40000 cellen): drempel te laag")
    return gezien


def min_bodem(kom, cel=0.01):
    x, y, r, _ = kom
    best = 1.0
    for i in range(-int(r / cel), int(r / cel) + 1):
        for j in range(-int(r / cel), int(r / cel) + 1):
            z = rd.bodem_z(x + i * cel, y + j * cel)
            if z is not None:
                best = min(best, z)
    return best


def water_materiaal():
    mat = bpy.data.materials.new("MAT_Water_Plas")
    mat.use_nodes = True
    b = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    # transmissie neemt de basiskleur over: v2 had 0,03 en gaf zwarte gaten; v7 (0,86) liet de
    # modderbodem zo helder door dat de plas las als natte modder. fix_gazon: gedempt groenbruin,
    # zodat de spiegeling (lucht, haag) de plas bepaalt en de bodem alleen nog vaag doorschemert.
    b.inputs["Base Color"].default_value = WATER_TINT
    b.inputs["Roughness"].default_value = 0.02
    b.inputs["IOR"].default_value = 1.33
    b.inputs["Transmission Weight"].default_value = 1.0
    # fix_gazon_v4: heel lichte rimpeling (fijne ruis als bump) voor een levendiger spiegeling
    nt = mat.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    ruis = nt.nodes.new("ShaderNodeTexNoise")
    ruis.inputs["Scale"].default_value = 9.0
    ruis.inputs["Detail"].default_value = 4.0
    nt.links.new(tc.outputs["Object"], ruis.inputs["Vector"])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.06
    bump.inputs["Distance"].default_value = 0.002
    nt.links.new(ruis.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return mat


PLAS_DOEL_M2 = {"A": 2.0, "B": 2.0}       # opdracht: elk 1,0-2,5 m2; fix_gazon_v4: ~2 m2 (ruimere kommen)
# (fix_gazon: B naar 1,8 geprobeerd -> zelfde 1,28 + 1,11 m2: de kommen zijn vol, groter kan alleen
#  met diepere/ruimere KOM_A/KOM_B in rtk_dressing; niet gedaan)
WATER_TINT = (0.42, 0.48, 0.42, 1.0)
# fix_gazon: vanuit Cam_Bekken (stap1_anker.CAMS) zag je de plassen niet: oeverplanten van 0,2-0,4 m
# tussen camera en plas verbergen bij een kijkhoek van ~13 graden 0,6-1,2 m water erachter.
# In de zichtstrook plas -> camera (breedte plas + marge) komen daarom geen zegge, bloeiers of
# bodembedekker; daar blijft natte oevergrond.
ZICHT_CAM = (12.8, 6.2)
ZICHT_MARGE = 0.15
NATTE_BAND_M = 0.12                        # fix_gazon_v4: vaste natte rand 10-15 cm (v8: ~30% van de kom
                                           # was kale modder en las als kuil); de rest bodembedekker
DEK_DICHTHEID = 70.0                       # v5: 18/m2 las als losse sprieten op kale modder


def maak_plassen(cel=0.02):
    """Per kom de waterstand zoeken (bisectie) waarbij de zichtbare plas het doeloppervlak heeft;
    daarna: nooit overlappen of raken, en elk een eigen z (v1-les: zwarte schijf)."""
    cache = {}

    def bz(i, j):
        if (i, j) not in cache:
            cache[(i, j)] = rd.bodem_z((i + 0.5) * cel, (j + 0.5) * cel)
        return cache[(i, j)]

    def vul(kom, niveau, rand=0.006):
        s = (int(kom[0] / cel), int(kom[1] / cel))
        if bz(*s) is None or bz(*s) >= niveau + rand:
            return set(), set()
        gezien, rij = {s}, [s]
        while rij:
            i, j = rij.pop()
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (i + d[0], j + d[1])
                if n not in gezien and bz(*n) is not None and bz(*n) < niveau + rand:
                    gezien.add(n)
                    rij.append(n)
            if len(gezien) > 60000:
                raise rd.RtkFout(f"plas rond {kom[:2]} loopt over: drempel te laag")
        return gezien, {c for c in gezien if bz(*c) < niveau}

    niveaus, cellen, zichtbaar = {}, {}, {}
    for naam, kom in (("A", rd.KOM_A), ("B", rd.KOM_B)):
        lo = min_bodem(kom) + 0.001
        hi = lo + 0.10                     # v5: 0,06 was het plafond (plassen bleven < 1,2 m2)
        for _ in range(16):
            mid = (lo + hi) / 2
            _, zicht = vul(kom, mid)
            if len(zicht) * cel * cel < PLAS_DOEL_M2[naam]:
                lo = mid
            else:
                hi = mid
        if naam == "B" and abs(lo - niveaus["A"]) < 0.004:
            lo = min(lo, niveaus["A"]) - 0.004      # eigen waterlijn: >= 4 mm onder plas A
        niveaus[naam] = lo
        cellen[naam], zichtbaar[naam] = vul(kom, lo)
    raak = [c for c in cellen["A"] if any((c[0] + d[0], c[1] + d[1]) in cellen["B"]
                                         for d in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)))]
    if raak:
        raise rd.RtkFout(f"plassen A en B raken elkaar in {len(raak)} cellen: drempel te laag")
    if abs(niveaus["A"] - niveaus["B"]) < 0.003:
        raise rd.RtkFout(f"plassen op bijna dezelfde z ({niveaus})")
    mat = water_materiaal()
    info = {}
    for naam in ("A", "B"):
        bm = bmesh.new()
        vs = {}

        def v(i, j):
            if (i, j) not in vs:
                vs[(i, j)] = bm.verts.new((i * cel, j * cel, 0.0))
            return vs[(i, j)]
        for i, j in cellen[naam]:
            bm.faces.new((v(i, j), v(i + 1, j), v(i + 1, j + 1), v(i, j + 1)))
        me = bpy.data.meshes.new(f"Water_Plas_{naam}")
        bm.to_mesh(me)
        bm.free()
        cx = sum(vv.co.x for vv in me.vertices) / len(me.vertices)
        cy = sum(vv.co.y for vv in me.vertices) / len(me.vertices)
        me.transform(Matrix.Translation((-cx, -cy, 0.0)))
        ob = bpy.data.objects.new(f"Water_Plas_{naam}", me)
        ob.location = (cx, cy, niveaus[naam])
        bpy.context.scene.collection.objects.link(ob)
        ob.data.materials.append(mat)
        info[naam] = {"z": round(niveaus[naam], 4), "zichtbaar_water_m2": round(len(zichtbaar[naam]) * cel * cel, 2),
                      "mesh_m2": round(len(cellen[naam]) * cel * cel, 2), "midden": [round(cx, 2), round(cy, 2)]}
    info["z_verschil_mm"] = round(abs(niveaus["A"] - niveaus["B"]) * 1000, 1)
    log(f"plassen: {info}")
    pts = [((i + 0.5) * cel, (j + 0.5) * cel) for k in ("A", "B") for i, j in zichtbaar[k]]
    kd = KDTree(len(pts))
    for n, (x, y) in enumerate(pts):
        kd.insert((x, y, 0.0), n)
    kd.balance()
    return info, kd


def water_afstand(kd, x, y):
    return kd.find((x, y, 0.0))[2]


def in_zichtstrook(x, y, plassen):
    """Ligt (x, y) tussen een plas en ZICHT_CAM, binnen de plasbreedte + ZICHT_MARGE?"""
    for k in ("A", "B"):
        cx, cy = plassen[k]["midden"]
        r = math.sqrt(plassen[k]["zichtbaar_water_m2"] / math.pi) + ZICHT_MARGE
        ux, uy = ZICHT_CAM[0] - cx, ZICHT_CAM[1] - cy
        lengte = math.hypot(ux, uy)
        ux, uy = ux / lengte, uy / lengte
        langs = (x - cx) * ux + (y - cy) * uy
        dwars = abs(-(x - cx) * uy + (y - cy) * ux)
        if langs > 0.0 and dwars < r:
            return True
    return False


def natte_band(kd, cel=0.05):
    """Aandeel kale natte grond in de kom bij de vaste rand NATTE_BAND_M rond de plassen."""
    afst = []
    for i in range(int(2.5 / cel), int(7.0 / cel)):
        for j in range(int(2.4 / cel), int(8.2 / cel)):
            x, y = (i + 0.5) * cel, (j + 0.5) * cel
            if rl.basin_depth(x, y) > OEVER_DIEPTE:
                afst.append(water_afstand(kd, x, y))
    droog = [d for d in afst if d > cel * 0.7]          # niet onder water
    frac = sum(1 for d in droog if d <= NATTE_BAND_M) / len(droog)
    return {"band_m": NATTE_BAND_M, "natte_grond_aandeel": round(frac, 3),
            "kom_m2_zonder_water": round(len(droog) * cel * cel, 2), "eis": "vaste rand 10-15 cm"}


def zet_nat(bodem, kd, band):
    """Bodem nat in de band rond de plassen, daarbuiten vochtig-droog (natte voegen alleen laag)."""
    me = bodem.data
    mw = bodem.matrix_world
    nat = [1.0 - rd.smoothstep(band * 0.7, band * 1.3, water_afstand(kd, *(mw @ v.co).xy)) for v in me.vertices]
    me.attributes["nat"].data.foreach_set("value", nat)
    return round(sum(1 for n in nat if n > 0.5) / len(nat), 3)


# =========================================================================== stenen en beplanting
def sector(th):
    """'oost' = kant van het pad/zichtlijn naar de hut: daar alleen laag."""
    a = math.degrees(th) % 360
    if a < 60 or a > 320:
        return "oost"
    if a < 150:
        return "noord"
    if a < 220:
        return "west"
    return "zuid"


def plaats_stenen(rnd, kd, plassen):
    """2-3 groepjes van 3-5 stenen aan de natte kant en bij de plassen, 30-40% ingegraven, plus
    per plas twee platte stenen als natte rand. Geen losse steentjes in het gras."""
    donor = rd.soort_donor(rd.PH_MODELS / "rock_moss_set_02_2k.blend", "stenen",
                           lambda n: n.startswith("rock_moss_set_02_rock"), verwacht_h=(0.4, 1.5))
    for m in {sl.material for o in donor["coll"].objects for sl in o.material_slots if sl.material}:
        rd.instancer_nat(m, donker=0.48, ruw_min=0.35)
    vars_ = donor["varianten"]
    plat = sorted(range(len(vars_)), key=lambda i: vars_[i]["h"] / vars_[i]["w"])[:2]
    punten, nat, bezet, groepen = [], [], [], []

    def rand_van(plas, hoek):
        """Punt net buiten de waterlijn, in richting `hoek` vanaf het plasmidden."""
        cx, cy = plassen[plas]["midden"]
        for k in range(4, 200):
            r = 0.05 * k
            x, y = cx + r * math.cos(hoek), cy + r * math.sin(hoek)
            if water_afstand(kd, x, y) > 0.15:          # fix_gazon_v4: was 0,06 (steen in plas B)
                return x, y
        return None

    def steen(x, y, doel, vi, zink_frac):
        var = vars_[vi]
        s = doel / var["w"]
        if rd.dicht_genoeg(x, y, doel / 2, bezet, factor=0.85) or rd.bodem_z(x, y) is None:
            return False
        if water_afstand(kd, x, y) < 0.35 * doel:    # fix_gazon_v4: geen steen midden in een plas
            return False
        h = var["h"] * s
        punten.append({"x": x, "y": y, "z": rd.oppervlak_z(x, y) - zink_frac * h,
                       "rot": rnd.uniform(0, 2 * math.pi), "s": s, "v": vi})
        nat.append(1.0 - rd.smoothstep(0.15, 0.6, water_afstand(kd, x, y)))
        bezet.append((x, y, doel / 2))
        return True

    # groep 1 westkant plas A, groep 2 zuidoostkant plas B, groep 3 lage zuidwesthelling van de kom
    middens = [rand_van("A", math.radians(rnd.uniform(160, 200))),
               rand_van("B", math.radians(rnd.uniform(-60, -20))),
               rd.bekken_punt(math.radians(rnd.uniform(215, 245)), 0.62)]
    for m in (m for m in middens if m is not None):
        n_doel, n = rnd.randint(3, 5), 0
        for _ in range(80):
            a, r = rnd.uniform(0, 2 * math.pi), rnd.uniform(0.0, 0.42)
            if steen(m[0] + r * math.cos(a), m[1] + r * math.sin(a), rnd.uniform(0.16, 0.40),
                     rnd.randrange(len(vars_)), rnd.uniform(0.30, 0.40)):
                n += 1
                if n >= n_doel:
                    break
        groepen.append({"midden": [round(m[0], 2), round(m[1], 2)], "stenen": n})
    for plas in ("A", "B"):                      # platte stenen als natte rand, twee per plas
        geplaatst = 0
        for _ in range(40):
            p = rand_van(plas, rnd.uniform(0, 2 * math.pi))
            if p and steen(p[0], p[1], rnd.uniform(0.32, 0.48), rnd.choice(plat), rnd.uniform(0.30, 0.38)):
                geplaatst += 1
                if geplaatst >= 2:
                    break
    ob = rd.plaats_soort("B2_Stenen", donor, punten, attrs={"nat": nat})
    return ob, donor, punten, bezet, groepen


def plaats_beplanting(rnd, route_sdf, bezet, kd, band, plassen):
    """Kom grotendeels beplant: dichte bodembedekker (GN-scatter) buiten de natte band, zegge-
    pollen in groepen, witte bloeiers in groepjes; oeverrand met graspollen, varens in het NW."""
    gras = rd.soort_donor(rd.PH_MODELS / "grass_medium_02_2k.blend", "zegge",
                          lambda n: n.startswith("grass_medium_02_") and not n.endswith("_geo")
                          and "geometry" not in n, verwacht_h=(0.1, 0.5))
    rl.groen_gras(list(gras["coll"].objects))
    bloei = rd.soort_donor(rd.PH_MODELS / "periwinkle_plant_2k.blend", "maagdenpalm_bloei",
                           lambda n: n.startswith("periwinkle_plant_") and n.endswith("_LOD0"), verwacht_h=(0.12, 0.6))
    for m in {sl.material for o in bloei["coll"].objects for sl in o.material_slots if sl.material}:
        if not rd.bloemen_herkleuren(m, "periwinkle_plant_diff"):
            raise rd.RtkFout(f"maagdenpalm: diff-beeld niet gevonden in {m.name}; roze bloemen blijven roze")
    dek = rd.soort_donor(rd.PH_MODELS / "periwinkle_plant_2k.blend", "bodembedekker",
                         lambda n: n.startswith("periwinkle_plant_") and n.endswith("_LOD0"), verwacht_h=(0.12, 0.6))
    for m in {sl.material for o in dek["coll"].objects for sl in o.material_slots if sl.material}:
        if not rd.bloemen_herkleuren(m, "periwinkle_plant_diff", vaste_kleur=(0.05, 0.09, 0.03)):
            raise rd.RtkFout(f"bodembedekker: diff-beeld niet gevonden in {m.name}")
    varen = rd.soort_donor(rd.PH_MODELS / "fern_02_2k.blend", "varen_oever",
                           lambda n: n.startswith("fern_02_"), verwacht_h=(0.1, 0.6))
    soorten = {"B2_Zegge": (gras, []), "B2_Bloei_Maagdenpalm": (bloei, []), "B2_Oever_Varen": (varen, [])}

    def beplantbaar(x, y):
        return (rd.bodem_z(x, y) is not None and water_afstand(kd, x, y) > band
                and not in_zichtstrook(x, y, plassen))

    def zet(naam, x, y, doel_h, varianten=None, sink=0.012, factor=0.7):
        if in_zichtstrook(x, y, plassen):
            return False
        donor, lijst = soorten[naam]
        vi = rnd.choice(varianten or list(range(len(donor["varianten"]))))
        var = donor["varianten"][vi]
        s = doel_h / var["h"]
        r = var["w"] * s / 2
        if route_sdf(x, y) < 0.25 + r * 0.5 or rd.dicht_genoeg(x, y, r, bezet, factor=factor):
            return False
        if rl.sdf_rect(x, y, rd.BEDDEN["Bed_West"]) < 0.15:
            return False
        lijst.append({"x": x, "y": y, "z": rd.oppervlak_z(x, y) - sink, "rot": rnd.uniform(0, 2 * math.pi),
                      "s": s, "v": vi})
        bezet.append((x, y, r))
        return True

    hoge_gras = [i for i, v in enumerate(gras["varianten"]) if v["h"] >= 0.22]     # geen dunne sprieten
    for _ in range(200):                       # varens eerst: vochtige noordwestrand, schaduwkant
        th = rnd.uniform(0.55 * math.pi, 0.85 * math.pi)
        x, y = rd.bekken_punt(th, rnd.uniform(0.92, 1.30))
        zet("B2_Oever_Varen", x, y, rnd.uniform(0.32, 0.48))
        if len(soorten["B2_Oever_Varen"][1]) >= 4:
            break
    for _ in range(13):                        # zegge-pollen in groepen; oostkant lager (zicht op de hut)
        th, gx, gy = 0.0, None, None
        for _ in range(50):
            th, n0 = rnd.uniform(0, 2 * math.pi), rnd.uniform(0.35, 0.85)
            gx, gy = rd.bekken_punt(th, n0)
            if beplantbaar(gx, gy):
                break
        hoog = (0.30, 0.42) if sector(th) == "oost" else (0.38, 0.70)
        for _ in range(rnd.randint(4, 7)):
            x, y = gx + rnd.uniform(-0.35, 0.35), gy + rnd.uniform(-0.35, 0.35)
            if beplantbaar(x, y):
                zet("B2_Zegge", x, y, rnd.uniform(*hoog), varianten=hoge_gras, factor=0.6)
    for _ in range(5):                         # graspollen op de oeverrand, in drifts (niet rondom)
        th = rnd.uniform(0.3 * math.pi, 1.6 * math.pi)
        for _ in range(rnd.randint(3, 5)):
            x, y = rd.bekken_punt(th + rnd.uniform(-0.2, 0.2), rnd.uniform(0.88, 1.06))
            zet("B2_Zegge", x, y, rnd.uniform(0.28, 0.48), varianten=hoge_gras, factor=0.6)
    for _ in range(3):                         # witte bloeiers: 3 groepjes van 5-8
        gx, gy = None, None
        for _ in range(50):
            gx, gy = rd.bekken_punt(rnd.uniform(0, 2 * math.pi), rnd.uniform(0.45, 0.95))
            if beplantbaar(gx, gy):
                break
        for _ in range(rnd.randint(5, 8)):
            x, y = gx + rnd.uniform(-0.28, 0.28), gy + rnd.uniform(-0.28, 0.28)
            if beplantbaar(x, y):
                zet("B2_Bloei_Maagdenpalm", x, y, rnd.uniform(0.22, 0.32), factor=0.55)
    obs, info = [], {}
    for naam, (donor, lijst) in soorten.items():
        if not lijst:
            raise rd.RtkFout(f"{naam}: niets geplaatst")
        obs.append(rd.plaats_soort(naam, donor, lijst))
        info[naam] = {"aantal": len(lijst), "donor": rd.donor_info_json(donor)}
    # dichte bodembedekker: GN-scatter (rl.gn_scatter) op een raster over het beplantbare deel van de kom.
    # fix_gazon_v4: in de zichtstrook naar Cam_Bekken een tweede, heel lage laag (zelfde maagdenpalm op
    # 25-35%, ~5-8 cm: leest als mos) i.p.v. kale modder; zo geen kuil en toch zicht op het water.
    cel = 0.05
    mid = (4.75, 5.30)

    def bodem_emitter(naam, kies, schaal, seed):
        bm = bmesh.new()
        vs = {}

        def v(i, j):
            if (i, j) not in vs:
                x, y = i * cel, j * cel
                z = rd.bodem_z(x, y)
                if z is None:
                    z = rl.ground_height(x, y)
                vs[(i, j)] = bm.verts.new((x - mid[0], y - mid[1], z - 0.01))
            return vs[(i, j)]
        n_cel = 0
        for i in range(int(2.5 / cel), int(7.0 / cel)):
            for j in range(int(2.4 / cel), int(8.2 / cel)):
                x, y = (i + 0.5) * cel, (j + 0.5) * cel
                if rl.basin_depth(x, y) > OEVER_DIEPTE and kies(x, y) and route_sdf(x, y) > 0.3:
                    bm.faces.new((v(i, j), v(i + 1, j), v(i + 1, j + 1), v(i, j + 1)))
                    n_cel += 1
        me = bpy.data.meshes.new(naam)
        bm.to_mesh(me)
        bm.free()
        em = bpy.data.objects.new(naam, me)
        em.location = (mid[0], mid[1], 0.0)
        bpy.context.scene.collection.objects.link(em)
        rl.gn_scatter(em, dek["coll"], len(dek["varianten"]), schaal, seed, dichtheid=DEK_DICHTHEID)
        info[naam] = {"oppervlak_m2": round(n_cel * cel * cel, 2), "dichtheid_per_m2": DEK_DICHTHEID,
                      "schaal": schaal, "verwacht": int(n_cel * cel * cel * DEK_DICHTHEID),
                      "donor": rd.donor_info_json(dek), "bloemen": "groen gemaakt (geen losse witte sprieten)"}

    bodem_emitter("B2_Bodembedekker", beplantbaar, (0.8, 1.15), 2627)
    bodem_emitter("B2_Bodembedekker_Laag",
                  lambda x, y: (rd.bodem_z(x, y) is not None and water_afstand(kd, x, y) > band
                                and in_zichtstrook(x, y, plassen)), (0.25, 0.35), 2628)
    return obs, info


# =========================================================================== main
def toetsen_laag2(meting, instancers, plassen):
    route_sdf = rl.route_sdf_from_meta(bpy.data.objects["Route_Steen"])
    uit = {"standaard": rd.standaard_toetsen(meting)}
    regels = {o.name: {"pad_marge": 0.2, "kap_vrij": True, "zinken": 0.06} for o in instancers}
    regels["B2_Stenen"] = {"pad_marge": 0.3, "kap_vrij": True, "zinken": 0.25}
    uit["dressing"] = rd.audit_dressing(instancers, route_sdf, meting, regels)
    uit["kloon"] = rd.kloon_check({o.name: rd.punten_van(o) for o in instancers})
    uit["plassen"] = {"ok": plassen["z_verschil_mm"] >= 3.0 and all(1.0 <= plassen[k]["zichtbaar_water_m2"] <= 2.5
                                                                     for k in ("A", "B")),
                      "eis": "elk 1,0-2,5 m2 zichtbaar water, z-verschil >= 3 mm", **plassen}
    uit["ok"] = all(uit[k]["ok"] for k in ("standaard", "dressing", "kloon", "plassen"))
    s = uit["standaard"]
    uit["samenvatting"] = (f"{s['samenvatting']}; dressing {'OK' if uit['dressing']['ok'] else 'FOUT'} "
                           f"({sum(uit['dressing']['instances'].values())} instances), kloon {uit['kloon']['klonen']} "
                           f"/ rijen {uit['kloon']['rijen']}, plassen {plassen['A']['zichtbaar_water_m2']} + "
                           f"{plassen['B']['zichtbaar_water_m2']} m2, dz {plassen['z_verschil_mm']} mm")
    log("TOETSEN:", uit["samenvatting"], "->", "OK" if uit["ok"] else "FOUT")
    return uit


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(prog="stap2_bekken")
    ap.add_argument("--geen-render", action="store_true")
    ap.add_argument("--alleen-render", action="store_true")
    args = ap.parse_args(argv)
    log(f"versie {VERSIE}, args {vars(args)}")
    if args.alleen_render:
        rd.open_invoer(UITVOER)
        rd.render_diag(["Cam_Close_Bekken", "Cam_Bekken"], WERK)
        return 0

    rd.open_invoer(INVOER)
    t0 = time.time()
    rnd = rl.random_from_seed(SEED)
    meting = rd.meting_anker()
    route_sdf = rl.route_sdf_from_meta(bpy.data.objects["Route_Steen"])
    audit = {"versie": VERSIE, "invoer": str(INVOER), "seed": SEED}
    audit["gazon"] = gazon_uit_oever()
    bodem = maak_bodem()
    audit["plassen"], kd = maak_plassen()
    audit["natte_grond"] = natte_band(kd)
    band = audit["natte_grond"]["band_m"]
    audit["bodem"] = {"nat_aandeel_vertices": zet_nat(bodem, kd, band), "vertices": len(bodem.data.vertices),
                      "kommen": {"A": rd.KOM_A, "B": rd.KOM_B, "drempel_h": rd.DREMPEL_H}}
    audit["bodem"]["ground_tuin_vlakken_weg"] = grond_onder_kom_weg()
    stenen, sdonor, spunten, bezet, groepen = plaats_stenen(rnd, kd, audit["plassen"])
    audit["stenen"] = {"aantal": len(spunten), "groepen": groepen,
                       "nat_gt_0_5": sum(1 for p in range(len(spunten))
                                         if stenen.data.attributes["nat"].data[p].value > 0.5),
                       "donor": rd.donor_info_json(sdonor), "licentie": "CC0 (polyhaven.com)"}
    oever_obs, audit["beplanting"] = plaats_beplanting(rnd, route_sdf, bezet, kd, band, audit["plassen"])
    audit["beplanting"]["zichtstrook"] = {"camera": ZICHT_CAM, "marge_m": ZICHT_MARGE,
                                          "doel": "geen oeverplanten tussen de plassen en Cam_Bekken"}
    c = CAM_CLOSE
    rd.zet_camera("Cam_Close_Bekken", c["loc"], c["doel"], c["lens"], shift_y=c["shift_y"],
                  dof_focus=(4.9, 5.0, 0.0), fstop=8.0)
    audit["opbouw_s"] = round(time.time() - t0, 1)
    audit["toetsen"] = toetsen_laag2(meting, [stenen] + oever_obs, audit["plassen"])
    rd.schrijf_json(WERK / "audit.json", audit)
    if not audit["toetsen"]["ok"]:
        log("TOETSEN FAALDEN: niet opgeslagen. Zie", WERK / "audit.json")
        return 1
    bpy.ops.wm.save_as_mainfile(filepath=str(UITVOER))
    log("opgeslagen:", UITVOER)
    if not args.geen_render:
        rd.render_diag(["Cam_Close_Bekken", "Cam_Bekken"], WERK)
    log(f"KLAAR stap 2 {VERSIE} in {time.time() - t0:.0f} s")
    return 0


if __name__ == "__main__":
    rd.main_wrapper(main, "stap2")
