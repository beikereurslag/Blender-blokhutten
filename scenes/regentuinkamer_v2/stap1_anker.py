r"""Renders 2.0 - De Regentuinkamer v2, stap 1: ANKER (plan: docs\PLAN_renders2_2026-10.md §7).

Bouwen + toetsen + opslaan (geen render; videokaart niet nodig):
  blender -b _hut_tekentool.blend --python stap1_anker.py -- --geen-render
Alleen renderen (HeroCam, Cam_Bekken, Cam_Westhoek, Cam_Haagproef), opent het anker:
  blender -b regentuinkamer_v2_anker.blend --python stap1_anker.py -- --alleen-render
Negatieve tests (slaan nooit op; exitcode 1 = de toets ving de fout, zoals bedoeld):
  blender -b _hut_tekentool.blend --python stap1_anker.py -- --negatief hut_verschoven
  blender -b regentuinkamer_v2_anker.blend --python stap1_anker.py -- --negatief boom_in_zonsector
  blender -b regentuinkamer_v2_anker.blend --python stap1_anker.py -- --negatief boom_weg_ring1

Versie via omgevingsvariabele RTK_VERSIE (standaard v1). Werkbestanden in
previews\_werk\anker_<versie>\ (audit.json, renders). Faalt een toets: niet opslaan, exitcode 1.
Herhaalbaar: vaste seeds, opent altijd zijn eigen invoer, eigen uitvoernaam.
"""
import argparse
import json
import math
import os
import re
import sys
import time
from pathlib import Path

import bpy
from mathutils import Vector

SCENE_DIR = Path(r"D:\Blender-blokhutten\scenes\regentuinkamer_v2")
sys.path.insert(0, str(SCENE_DIR))
import rtk_lib as rl  # noqa: E402

cl = rl.cl
import validate_scene as vs  # noqa: E402  (pad gezet door rtk_lib)

ROOT = rl.ROOT
INVOER = SCENE_DIR / "_hut_tekentool.blend"
UITVOER = SCENE_DIR / "regentuinkamer_v2_anker.blend"
VERSIE = os.environ.get("RTK_VERSIE", "v1")
WERK = SCENE_DIR / "previews" / "_werk" / f"anker_{VERSIE}"
ASSETS = ROOT / "assets"
BK = ASSETS / "blenderkit" / "renders2"
PHTEX = ASSETS / "polyhaven" / "textures"
GPU_BEZET = Path(r"D:\Beeldherkenning\GPU_BEZET.txt")
SEED = 2610

# Hut (plan §7 + §8.1)
HUT_ROOT_LOC = (10.263, 9.25, 0.0)
DEUR_MID_X, DEUR_MID_TOL = 9.028, 0.05
DEUR_VOOR_Y, DEUR_VOOR_TOL = 8.0, 0.08
PALEN_X_MIN = 11.0

# Licht (plan §5)
# v5: kompas 125 en 130 geprobeerd: dan weert de zonregel andere bomen en zakt de luchttoets naar
# 94,4% (HeroCam). Daarom terug naar kompas 115 uit het plan; de zon domineert via de sterkte. (opdracht projectsessie: 125-135, >= 53 graden naast de camera-as) zodat de
# zuidgevel meer zon vangt. cl-conventie: azimut = 180 - kompas.
SUN_AZ = 180.0 - float(os.environ.get("RTK_ZONKOMPAS", "115"))
# v4: HDRI eilenriede_park (gemeten zon 36,8 graden, frisse daglucht) i.p.v. kloppenheim_06
# (zon 4,7 graden: avondlucht, alles somber). Zonhoogte richting de HDRI, binnen 26-35 graden
# (opdracht projectsessie v4), mits de schaduwtoets groen blijft.
SUN_ELEV = float(os.environ.get("RTK_ZONHOOGTE", "35"))
SUN_KOMPAS = 180.0 - SUN_AZ
# v5: de zon moet domineren (v4 oogde bewolkt: HDRI gaf meer licht dan de zon, zie audit licht.verhouding)
SUN_K, SUN_HOEK = 4500, 1.2
SUN_E = float(os.environ.get("RTK_ZONSTERKTE", "9.0"))
HDRI = "eilenriede_park_2k.hdr"
HDRI_STERKTE = float(os.environ.get("RTK_HDRISTERKTE", "0.35"))
HDRI_STERKTE_HOOG = HDRI_STERKTE * 0.75
HORIZON_KLEUR = (0.030, 0.042, 0.026)   # wazig bosgroen achter de kaarten (proef6/fix2, Cam_Bekken)
EXPOSURE = float(os.environ.get("RTK_EXPOSURE", "0.0"))
# v4-proef op een gazoncrop (previews\_werk\gras_vergelijk_v4.png): BK-plukken lezen groener en
# meer als gazon dan PH grass_medium_02 (bleek, ruig). Keuze: bk, op de lichte gazonbodem.
# fix_gazon (26-10): v5-gras (bk) las als donkere klaver; nu BK Garden Grass Free als zoden met
# maaibanen en kleurvlekken (vergelijking: previews\_werk\fix_gazon_v1..v3).
GRAS_BRON = os.environ.get("RTK_GRAS", "tuin")
MIST = dict(xmin=-40, xmax=55, ymin=-40, ymax=55, zmin=0, zmax=25, density=0.0012)

# Camera's (plan §6) + haagproef (§4): rughaag op ~6 m
CAMS = {
    "HeroCam": dict(loc=(8.0, 0.7, 1.55), doel=(9.028, 8.0, 1.2), lens=33),
    "Cam_Bekken": dict(loc=(12.8, 6.2, 1.6), doel=(3.5, 2.5, 0.8), lens=28),
    "Cam_Westhoek": dict(loc=(1.5, 1.2, 1.6), doel=(10.0, 9.2, 1.4), lens=30),
    "Cam_Haagproef": dict(loc=(4.2, 5.4, 1.5), doel=(4.2, 11.4, 1.0), lens=35),
}
PREVIEW_RES, PREVIEW_SAMPLES = (960, 540), 24

ROUTE_CTRL = [(8.0, 0.0), (8.0, 1.5), (7.7, 3.5), (9.028, 5.8)]
SCHORT = (7.5, 13.1, 6.6, 8.1)
BEDDEN = {"Bed_Oost": (10.0, 13.2, 1.2, 5.8), "Bed_West": (1.0, 2.5, 6.5, 10.5)}


def log(*a):
    print("[stap1]", *a, flush=True)


# =========================================================================== A. hut
def deel_a_hut(negatief):
    cl.delete_glb_cameras()
    cl.warm_wood_walls()
    cl.fix_glass_chrome()
    mat_wand = bpy.data.materials.get("basetexture-firstLayer-wall")
    if mat_wand is None:
        raise rl.RtkFout("wandmateriaal basetexture-firstLayer-wall ontbreekt in _hut_tekentool.blend")
    n_deur = 0
    for o in bpy.data.objects:
        if o.type == "MESH" and o.name.lower().startswith(".deurbasic"):
            for s in o.material_slots:
                if s.material and not any(k in s.material.name.lower() for k in ("glas", "glass")):
                    s.material = mat_wand
                    n_deur += 1
    log(f"deurpanelen -> {mat_wand.name}: {n_deur} slots")

    roots = [o for o in bpy.data.objects if o.parent is None]
    croot = bpy.data.objects.new("Cabin_Root", None)
    bpy.context.scene.collection.objects.link(croot)
    for o in roots:
        o.parent = croot
        o.matrix_parent_inverse.identity()
    croot.rotation_euler = (0.0, 0.0, math.pi)
    croot.location = HUT_ROOT_LOC
    if negatief == "hut_verschoven":
        croot.location.x += 0.3
        log("NEGATIEVE TEST: hut 0,3 m naar oost verschoven")
    bpy.context.view_layer.update()

    meshes = [o for o in croot.children_recursive if o.type == "MESH"]
    bb = cl.wbbox_meshes(meshes)
    deur = [o for o in meshes if o.name.lower().startswith(".deurbasic")]
    if not deur:
        raise rl.RtkFout("geen deur (.DEURBASIC) in de hut: swap_verslag nalopen")
    db = cl.wbbox_meshes(deur)
    palen = [o for o in meshes if o.name.lower().startswith("pole")
             and "foundation" not in o.name.lower() and "scaffold" not in o.name.lower()]
    pb = cl.wbbox_meshes(palen) if palen else None
    # gesloten kamer = wandplanken wall-N zonder het kap-materiaal (wall-7 is de achterwand van de kap)
    muren = [o for o in meshes if re.match(r"^wall-\d", o.name)
             and not any(s.material and "canopy" in s.material.name.lower() for s in o.material_slots)]
    mb = cl.wbbox_meshes(muren)
    meting = {
        "envelop": [round(v, 3) for v in bb],
        "deur_bbox": [round(v, 3) for v in db],
        "deur_mid_x": round((db[0] + db[1]) / 2, 4),
        "deur_voorkant_y": round(db[2], 4),
        "deur_dorpel_z": round(db[4], 4),
        "palen_x": [round(pb[0], 3), round(pb[1], 3)] if pb else None,
        "gesloten_ruimte_bbox": [round(v, 3) for v in mb],
    }
    fouten = []
    if abs(meting["deur_mid_x"] - DEUR_MID_X) > DEUR_MID_TOL:
        fouten.append(f"deurmidden X {meting['deur_mid_x']:.3f} wijkt meer dan {DEUR_MID_TOL} af van {DEUR_MID_X}")
    if abs(meting["deur_voorkant_y"] - DEUR_VOOR_Y) > DEUR_VOOR_TOL:
        fouten.append(f"deurvoorkant Y {meting['deur_voorkant_y']:.3f} wijkt meer dan {DEUR_VOOR_TOL} af van {DEUR_VOOR_Y}")
    if not pb or pb[0] <= PALEN_X_MIN:
        fouten.append(f"palen niet ten oosten van X {PALEN_X_MIN}: {meting['palen_x']}")
    meting["ok"] = not fouten
    meting["fouten"] = fouten
    log(f"hut: envelop {meting['envelop']}, deur mid X {meting['deur_mid_x']}, "
        f"voorkant Y {meting['deur_voorkant_y']}, palen X {meting['palen_x']}")
    if fouten:
        raise rl.RtkFout("hut niet op de ontwerpplek: " + "; ".join(fouten))
    # binnenruimte van de gesloten kamer (muurdikte eraf) voor de audit
    meting["binnenruimte"] = [mb[0] + 0.08, mb[1] - 0.08, mb[2] + 0.08, mb[3] - 0.08,
                              meting["deur_dorpel_z"] + 0.01, mb[5] - 0.10]
    return meting


# =========================================================================== B. grond + bedden
def deel_b_grond():
    mat = cl.pbr_from_folder("MAT_Grond_Bos", str(PHTEX / "forrest_ground_01"), scale=0.4, val=0.6)
    # v5: bedden en bekkenkern als donkerbruine, licht ruwe tuinaarde. v4 dempte de ruwheid
    # ("vochtig"): dat spiegelde de lucht en las als grijze betonplaat.
    mat_bed = rl.aarde_materiaal(cl.pbr_from_folder("MAT_Aarde_Vers", str(PHTEX / "forrest_ground_01"),
                                                    scale=0.55))
    ground, info = rl.make_ground("Ground_Tuin", mat, mat_kern=mat_bed)
    bpy.ops.mesh.primitive_plane_add(size=900, location=(7.0, 6.0, rl.FAR_Z))
    far = bpy.context.active_object
    far.name = "Ground_Far"
    # v5: verre grond donkerder, anders leest hij onder ring 4 als lichte horizonstrook
    far.data.materials.append(cl.pbr_from_folder("MAT_Grond_Ver", str(PHTEX / "forrest_ground_01"),
                                                 scale=0.4, sat=1.1, val=0.22))
    # ronde extra (28-10): in Cam_Bekken bleef een lichte strook (glans + zonnige kale grond op ~85 m)
    rl.verre_grond_mat(far.data.materials[0])
    for naam, rect in BEDDEN.items():
        rl.make_bed(naam, rect, mat_bed)
    info["bedden"] = BEDDEN
    log(f"grond: {info}")
    return info


# =========================================================================== C. route
def deel_c_route(meting):
    map_ = PHTEX / "grey_stone_path"
    terugval = None
    if not (map_ / "grey_stone_path_disp_2k.jpg").exists():
        terugval = "slate_floor_02 (grey_stone_path ontbreekt)"
        map_ = PHTEX / "slate_floor_02"
    disp_pad = next(map_.glob("*disp*"))
    mat = rl.uv_material(cl.pbr_from_folder("MAT_Route_Steen", str(map_), scale=1.0,
                                            rough_fallback=0.7))
    disp = bpy.data.images.load(str(disp_pad), check_existing=True)
    disp.colorspace_settings.name = "Non-Color"
    disp_m = 0.012
    dorpel = meting["deur_dorpel_z"]
    top = dorpel - 0.005 - disp_m / 2          # hoogste steen 5 mm onder de dorpel
    lijn = rl.route_centerline(ROUTE_CTRL, (DEUR_MID_X, meting["deur_voorkant_y"]))
    gb = meting["gesloten_ruimte_bbox"]
    ob, info = rl.make_route("Route_Steen", lijn, 0.6, SCHORT, top, mat, disp,
                             disp_sterkte=disp_m, start_y=0.0, eind_y=meting["deur_voorkant_y"],
                             schort_clip=(gb[0] - 0.05, gb[1] + 0.05, meting["deur_voorkant_y"] + 0.04))
    info["materiaal"] = map_.name
    info["terugval"] = terugval
    info["pad_eind"] = [DEUR_MID_X, meting["deur_voorkant_y"]]
    info["recht_laatste_m"] = round(meting["deur_voorkant_y"] - ROUTE_CTRL[-1][1], 3)
    log(f"route: {({k: v for k, v in info.items() if k != 'sdf'})}")
    return ob, info


# =========================================================================== D. hagen
def deel_d_hagen():
    donor = rl.load_hedge_donor(BK / "Cotoneáster.blend")
    info = rl.place_hedges(donor)
    log(f"hagen: {info}")
    return info


# =========================================================================== E. bomen
TREE_FILES = {
    "fagus09": "Tree_Fagus_Sylvatica09.blend",
    "acer_campestre": "European_Maple_Acer_Campreste.blend",
    "fagus05": "Tree_Fagus_Sylvatica05.blend",
    "fagus_grandifolia05": "Tree_Fagus_Grandifolia05.blend",
}
# Afgekeurd na anker v1: European Maple Acer Platanoide heeft een herfstblad-textuur
# (gemiddelde bladkleur oranje 0,64/0,44/0,06); past niet bij "ochtend na de bui".
AFGEKEURD = {"acer_platanoides": "European_Maple_Acer_Platanoide.blend: herfstkleurig blad (anker v1)"}
BERK = ASSETS / "blenderkit" / "berk" / "Silver_Birch_Tree.blend"
# Terugval uit plan §3: in anker v1 had de berk (18 m, x0,8) kale lange takken in Cam_Bekken
# en een ijle kruin in de HeroCam. Daarom de BK Multi-stem Deciduous Tree (9 m).
STATEMENT = BK / "Multi_stem_Deciduous_Tree.blend"
BERK_POS = (1.7, 8.6)
# Ronde extra (28-10): Boom_1_022 (fagus09, 23 m achter de rughaag) toonde in de HeroCam een kale
# onderkroon met dode takken, van elke kant (proef: 0/90/180/270 graden, previews/_werk/ronde_extra/proef1).
# Vervangen door een veldesdoorn met dezelfde stand als Boom_1_019 (proef h_acer). De seed-volgorde
# blijft gelijk; pos = verwachte plek, zodat een andere seed of ringindeling hier hard stopt.
BOOM_VERVANG = {"Boom_1_022": {"donor": "acer_campestre", "schaal": 0.986, "rot_graden": 20.03,
                               "pos": (3.1, 23.0)}}
# ronde extra: onderste strook van de treeline-kaart (lichte weide, ~5% van de beeldhoogte) donker maken.
# Kaarten 0,35 m laten zakken mocht niet: validate_scene en audit_extra eisen de boomoorsprong op het maaiveld.
KAART_WEIDE_V = 0.06


def deel_e_bomen():
    rnd = rl.random_from_seed(SEED)
    donors, terugval = {}, []
    for label, fn in TREE_FILES.items():
        try:
            donors[label] = rl.load_donor(BK / fn, label)
        except rl.RtkFout as e:
            terugval.append(str(e))
            log("BOOM-DONOR MIST:", e)
    berk = rl.load_donor(STATEMENT, "multistem", alleen=["TREE"])
    terugval.append("statement-boom: Multi-stem Deciduous Tree i.p.v. Silver_Birch_Tree (kale takken in v1)")
    terugval.extend(AFGEKEURD.values())
    ring1 = [donors[k] for k in ("fagus09", "acer_campestre") if k in donors] or [berk]
    ring2 = [donors[k] for k in ("fagus05", "fagus_grandifolia05") if k in donors] or ring1
    ring3 = list(donors.values()) or ring1
    if not donors:
        terugval.append("geen enkele BK-boom: alle ringen met de lokale berk")

    hero = Vector(CAMS["HeroCam"]["loc"])
    tuin_haag = (-0.1, 14.4, -0.1, 12.5)         # tuin inclusief hagen
    geplaatst = {"ring1": 0, "ring2": 0, "ring3": 0}
    geweigerd = {"zon": 0, "zone": 0, "afstand": 0, "boven_hut": 0}
    eb = cl.wbbox_meshes([o for o in bpy.data.objects["Cabin_Root"].children_recursive if o.type == "MESH"])
    hut_rect = (eb[0], eb[1], eb[2], eb[3])
    alle = []
    vervangen = []

    def zone_ring(d_min, d_max, sectoren):
        def f(x, y):
            d = rl.dist_to_rect(x, y, tuin_haag)
            if not (d_min <= d <= d_max):
                return False
            if sectoren == "NWNOZ" and x > tuin_haag[1] and y < tuin_haag[3]:
                return False                    # oostflank (zonzijde) niet in ring 1
            if sectoren == "NW" and not (y > tuin_haag[3] or x < tuin_haag[0]):
                return False                    # v4: extra ring-1-bomen alleen noord en west
            return True
        return f

    ringen = [("ring1", 2.0, 8.0, "NWNOZ", ring1, 6.0, 9.0),
              ("ring1", 8.0, 13.0, "NW", ring1, 6.0, 9.0),
              ("ring2", 15.0, 30.0, "rondom", ring2, 6.0, 9.0),
              ("ring3", 35.0, 70.0, "rondom", ring3, 6.0, 9.0)]
    for ring, d0, d1, sect, pool, gmin, gmax in ringen:
        zone = zone_ring(d0, d1, sect)
        b = (tuin_haag[0] - d1, tuin_haag[1] + d1, tuin_haag[2] - d1, tuin_haag[3] + d1)
        groepen = rl.poisson_groepen(rnd, zone, b, gmin, gmax, pogingen=4000 if ring != "ring3" else 9000)
        for gi, (gx, gy) in enumerate(groepen):
            n = rnd.choice((2, 3))
            for k in range(n):
                if k == 0:
                    x, y = gx + rnd.uniform(-0.8, 0.8), gy + rnd.uniform(-0.8, 0.8)
                else:
                    a = rnd.uniform(0, 2 * math.pi)
                    r = rnd.uniform(2.0, 3.5)
                    x, y = gx + r * math.cos(a), gy + r * math.sin(a)
                donor = rnd.choice(pool)
                s = rnd.uniform(rl.SCHAAL_MIN, rl.SCHAAL_MAX)
                h = donor["h"] * s
                if not zone(x, y):
                    geweigerd["zone"] += 1
                    continue
                if rl.shadow_hits_garden(x, y, h, donor["breedte"] * s / 2, SUN_KOMPAS, SUN_ELEV):
                    geweigerd["zon"] += 1
                    continue
                if rl.dist_to_rect(x, y, hut_rect) < 0.71 * donor["breedte"] * s + 0.2:
                    geweigerd["boven_hut"] += 1          # kroon (ook gedraaid) niet boven de hut
                    continue
                if any(math.hypot(x - ox, y - oy) < 1.8 for ox, oy, _ in alle):
                    geweigerd["afstand"] += 1
                    continue
                naam = f"Boom_{ring[-1]}_{geplaatst[ring]:03d}"
                rot = rnd.uniform(0, 2 * math.pi)
                if naam in BOOM_VERVANG:
                    v = BOOM_VERVANG[naam]
                    if math.hypot(x - v["pos"][0], y - v["pos"][1]) > 0.5:
                        raise rl.RtkFout(f"{naam} staat op ({x:.2f}, {y:.2f}), verwacht {v['pos']}: "
                                         f"BOOM_VERVANG klopt niet meer bij de seed")
                    donor, s, rot = donors[v["donor"]], v["schaal"], math.radians(v["rot_graden"])
                    if rl.shadow_hits_garden(x, y, donor["h"] * s, donor["breedte"] * s / 2, SUN_KOMPAS, SUN_ELEV):
                        raise rl.RtkFout(f"{naam}: vervangende boom {v['donor']} werpt schaduw in de tuin")
                    vervangen.append(f"{naam}: {v['donor']} (schaal {s}, rot {v['rot_graden']} gr)")
                rl.place_bk_tree(donor, naam, x, y, s, rot)
                alle.append((x, y, naam))
                geplaatst[ring] += 1
    # statement-berk westhoek (plan §3: lokaal, schaal 0,8-1,1)
    s_berk = 1.0
    rl.place_bk_tree(berk, "Boom_Statement_W", BERK_POS[0], BERK_POS[1], s_berk, 0.0)

    # ring 4 (plan §3/§4): alleen als de luchttoets met ring 1-3 faalt
    voor = rl.sky_closure(bpy.context.scene, {"HeroCam": CAMS["HeroCam"]["loc"],
                                              "tuinmidden": (7.0, 6.0, 1.6)})
    ring4 = {"luchttoets_zonder_ring4_pct": voor["dicht_pct_min"], "geplaatst": 0}
    if not voor["ok"]:
        kaart = rl.load_donor(BK / "Greenleaf_Treeline_Backdrop_001.blend", "treeline", min_verts=0)
        # v4: in de zon (35 graden) lichtte de kaart op als witte boompjes boven de haag; kleur dempen
        for m in {sl.material for o in kaart["objs"] for sl in o.material_slots if sl.material}:
            # ronde extra (28-10): bleke populierenkruinen lazen als zilveren struiken boven de haag
            if not rl.treeline_groen(m):
                raise rl.RtkFout(f"treeline: geen treeline-beeld gevonden in materiaal {m.name}")
            nt = m.node_tree
            bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
            for lk in list(bsdf.inputs["Base Color"].links):
                hs = nt.nodes.new("ShaderNodeHueSaturation")
                # bekkenfix (28-10): 1,15/0,45 las in Cam_Bekken (kaart in de waas op 96 m) nog zilvergrijs
                hs.inputs["Saturation"].default_value = 1.7
                hs.inputs["Value"].default_value = 0.22
                nt.links.new(lk.from_socket, hs.inputs["Color"])
                nt.links.new(hs.outputs["Color"], bsdf.inputs["Base Color"])
            rl.treeline_weide_donker(m, KAART_WEIDE_V)
        straal, n = 90.0, 22
        for i in range(n):
            a = 2 * math.pi * i / n
            x, y = 7.0 + straal * math.cos(a), 6.0 + straal * math.sin(a)
            rl.place_bk_tree(kaart, f"Boom_4_{i:03d}", x, y, 1.1, a)
        ring4.update(geplaatst=n, straal_m=straal, kaart_breedte_m=round(kaart["breedte"], 1), weide_donker_onder_v=KAART_WEIDE_V)
        log(f"ring 4: luchttoets zonder ring 4 {voor['dicht_pct_min']}% < 95 -> {n} kaarten op {straal} m")

    # daklijn-regel achter de hut (plan §4): kruin niet op de daklijn in de HeroCam
    dak_z = cl.wbbox_meshes([o for o in bpy.data.objects["Cabin_Root"].children_recursive
                             if o.type == "MESH"])[5]
    dak_hoek = math.degrees(math.atan2(dak_z - hero.z, 10.7 - hero.y))
    daklijn = []
    for x, y, naam in alle:
        if 7.0 <= x <= 13.0 and y > 12.4 and y < 10.7 + 9.0:
            r = bpy.data.objects[naam]
            top = cl.wbbox_meshes([c for c in r.children_recursive if c.type == "MESH"])[5]
            top_hoek = math.degrees(math.atan2(top - hero.z, y - hero.y))
            if top_hoek - dak_hoek < 3.0:
                daklijn.append(f"{naam}: kruintop {top_hoek:.1f} gr vs dak {dak_hoek:.1f} gr")
    info = {"geplaatst": geplaatst, "geweigerd": geweigerd, "totaal": len(alle) + 1, "ring4": ring4,
            "donors": {k: {kk: vv for kk, vv in v.items() if kk not in ("objs",)} for k, v in donors.items()},
            "berk": {"donor": {kk: vv for kk, vv in berk.items() if kk not in ("objs",)},
                     "schaal": s_berk, "pos": BERK_POS},
            "terugval": terugval, "vervangen": vervangen,
            "daklijn_conflicten": daklijn, "dak_hoek_hero": round(dak_hoek, 2)}
    log(f"bomen: {geplaatst}, geweigerd {geweigerd}, daklijn-conflicten {len(daklijn)}")
    return info


# =========================================================================== F. licht
def deel_f_licht():
    import numpy as np
    scn = bpy.context.scene
    for o in list(bpy.data.objects):
        if o.type == "LIGHT":
            bpy.data.objects.remove(o, do_unlink=True)
    sun = cl.add_sun(energy=SUN_E, color=cl._kelvin_rgb(SUN_K), elev_deg=SUN_ELEV,
                     azim_deg=SUN_AZ, angle_deg=SUN_HOEK)
    env = cl.setup_hdri(HDRI, strength=HDRI_STERKTE, rot_z_deg=0.0)
    wn = scn.world.node_tree
    mp = next(n for n in wn.nodes if n.type == "MAPPING")
    bg = next(n for n in wn.nodes if n.type == "BACKGROUND")
    img = env.image
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    px = px.reshape(h, w, 4)[:, :, :3].sum(axis=2)
    px[: h // 2, :] = 0                       # alleen de bovenste helft (lucht)
    rij, kol = np.unravel_index(int(px.argmax()), px.shape)
    u, v = (kol + 0.5) / w, (rij + 0.5) / h
    hdri_elev = (v - 0.5) * 180.0
    phi = (u - 0.5) * 2 * math.pi             # Blender: u = atan2(y, -x) / 2pi + 0.5
    theta_b = math.pi - phi
    theta_sun = math.atan2(-math.cos(math.radians(SUN_AZ)), math.sin(math.radians(SUN_AZ)))
    rot = theta_b - theta_sun
    mp.inputs["Rotation"].default_value = (0.0, 0.0, rot)
    sterkte = HDRI_STERKTE_HOOG if hdri_elev > 40.0 else HDRI_STERKTE
    bg.inputs["Strength"].default_value = sterkte
    # bekkenfix (28-10): bruinrode HDRI-gebouwen tussen de kruinen door; alleen voor de camera weg
    rl.hdri_horizon_camera(scn.world, HORIZON_KLEUR)
    bpy.context.view_layer.update()          # anders is matrix_world van de nieuwe zon nog leeg
    verhouding = rl.zon_hdri_verhouding(img, sterkte, rl.to_sun_vector(sun), SUN_E, cl._kelvin_rgb(SUN_K), rot)
    log(f"zon/HDRI: {verhouding}")
    cl.volumetric_fog("Mist_Rig", MIST["xmin"], MIST["xmax"], MIST["ymin"], MIST["ymax"],
                      MIST["zmin"], MIST["zmax"], density=MIST["density"])
    # v4: zwak licht binnen en onder de kap (recept oude G1: _patch_v5/_v6_astra.py), niet zichtbaar
    # voor de camera; zo zie je door het glas de lichte binnenwand in plaats van zwart.
    fills = {}
    gb = None
    for naam, loc, w, kleur, maat in (("Interieur_Fill", (8.90, 9.20, 2.00), 40.0, (1.0, 0.90, 0.80), 1.2),
                                      ("Kap_Fill", (11.90, 9.20, 2.10), 55.0, (1.0, 0.88, 0.76), 1.6)):
        li = cl.area_light(naam, loc, w, color=kleur, size=maat)
        li.visible_camera = False
        fills[naam] = {"loc": loc, "watt": w, "maat": maat}
    glas = bpy.data.materials.get("glass")
    glas_info = None
    if glas is not None:
        bsdf = next((n for n in glas.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if bsdf is not None:
            glas_info = {k: round(float(bsdf.inputs[k].default_value), 3)
                         for k in ("Roughness", "Transmission Weight", "IOR") if k in bsdf.inputs}
    cl.render_setup(samples=PREVIEW_SAMPLES, res=PREVIEW_RES)
    cl.set_agx("AgX - Medium High Contrast", exposure=EXPOSURE)
    scn.cycles.texture_limit_render = "1024"
    scn.use_nodes = False                      # geen compositor uit de base
    zon = rl.to_sun_vector(sun)
    info = {"zon": {"az_cl": SUN_AZ, "kompas": SUN_KOMPAS, "elev": SUN_ELEV, "kelvin": SUN_K,
                    "sterkte": SUN_E, "hoek": SUN_HOEK, "vector": [round(c, 4) for c in zon]},
            "hdri": {"bestand": HDRI, "helderste_pixel_uv": [round(float(u), 4), round(float(v), 4)],
                     "zon_hoogte_gemeten": round(float(hdri_elev), 1), "sterkte": sterkte,
                     "mapping_rot_graden": round(math.degrees(rot) % 360, 1)},
            "mist": MIST, "fills": fills, "glas": glas_info, "verhouding": verhouding,
            "kleur": {"view_transform": scn.view_settings.view_transform,
                      "look": scn.view_settings.look, "exposure": scn.view_settings.exposure},
            "render": {"engine": scn.render.engine, "device": scn.cycles.device,
                       "samples": scn.cycles.samples, "denoise": scn.cycles.use_denoising,
                       "texture_limit": scn.cycles.texture_limit_render,
                       "res": [scn.render.resolution_x, scn.render.resolution_y]}}
    log(f"licht: {info}")
    return info


# =========================================================================== G. camera's
def deel_g_cameras():
    for naam, c in CAMS.items():
        cl.add_camera(c["loc"], c["doel"], lens=c["lens"], shift_y=-0.03, name=naam)
    cl.set_camera_dof("HeroCam", fstop=5.6, focus_xyz=(DEUR_MID_X, DEUR_VOOR_Y, 1.2))
    bpy.context.scene.camera = bpy.data.objects["HeroCam"]
    return {k: {"loc": v["loc"], "doel": v["doel"], "lens": v["lens"]} for k, v in CAMS.items()}


# =========================================================================== H. gazon
def deel_h_gazon(route_sdf, hagen_rects, meting):
    eb = meting["envelop"]
    bodem = cl.pbr_from_folder("MAT_Gazonbodem", str(PHTEX / "leafy_grass"), scale=0.8)
    if GRAS_BRON == "tuin":
        rl.gazon_bodem(bodem)
    info = rl.make_lawn(GRAS_BRON, route_sdf, BEDDEN, hagen_rects, (eb[0], eb[1], eb[2], eb[3]), bodem)
    info["onderbegroeiing"] = rl.make_undergrowth(rl.random_from_seed(SEED + 7), SUN_KOMPAS, SUN_ELEV)
    log(f"gazon: {info}")
    return info


# =========================================================================== toetsen
KNOWN_VALIDATE = {("floating", "chrome")}   # daktrim van de hut heet 'chrome'; valt buiten de hut-trefwoorden


def root_naam(o):
    while o.parent is not None:
        o = o.parent
    return o.name


def toetsen(meting, route_sdf, meet_ring1=False):
    uit = {}
    scn = bpy.context.scene
    # 1. validate_scene + cl.audit
    res = vs.run()
    vs.print_report(res)
    ernstig = [f for f in res["flags"] if f["severity"] in ("CRITICAL", "ERROR", "HIGH")
               and (f.get("category"), f.get("object")) not in KNOWN_VALIDATE]
    uit["validate_scene"] = {"ok": not ernstig, "flag_counts": res.get("flag_counts"),
                             "flags": res["flags"][:30],
                             "bekend_vals_alarm": sorted(f"{a}:{b}" for a, b in KNOWN_VALIDATE)}
    gb = meting["gesloten_ruimte_bbox"]
    issues = cl.audit(cabin_x=(gb[0], gb[1]), cabin_y=(gb[2], gb[3]),
                      extra_safe=("boom_", "mist_rig", "gazon", "rtk_", "chrome", "wallcorner",
                                  "struiklaag", "bodemlaag"))
    uit["cl_audit"] = {"ok": not issues, "issues": issues}

    # raycasts zonder gras (miljoenen instances maken elke straal traag) en zonder mist
    gazon = bpy.data.objects.get("Gazon")
    mods = [m for o in scn.objects if o.name.startswith(("Gazon", "Bodemlaag"))
            for m in o.modifiers if m.type == "NODES"]
    for m in mods:
        m.show_viewport = False
    mist = bpy.data.objects.get("Mist_Rig")
    if mist:
        mist.hide_viewport = True
    bpy.context.view_layer.update()
    sun = next(o for o in scn.objects if o.type == "LIGHT" and o.data.type == "SUN")
    eb = meting["envelop"]
    hut_rect = (eb[0], eb[1], eb[2], eb[3])
    haag_rects = rl.HAAG_VOETEN
    t = time.time()
    uit["schaduwtoets"] = rl.shadow_test(scn, sun, hut_rect, haag_rects)
    uit["schaduwtoets"]["sec"] = round(time.time() - t, 1)
    t = time.time()
    uit["luchttoets"] = rl.sky_closure(scn, {"HeroCam": CAMS["HeroCam"]["loc"],
                                             "tuinmidden": (7.0, 6.0, 1.6)})
    uit["luchttoets"]["sec"] = round(time.time() - t, 1)
    if meet_ring1:
        # meting met en zonder ring 1 op 10/15 graden (basis voor rl.LUCHT_EIS_HOOG)
        r1 = [o for o in scn.objects if root_naam(o).startswith("Boom_1_")]
        for o in r1:
            o.hide_viewport = True
        bpy.context.view_layer.update()
        zonder = rl.sky_closure(scn, {"HeroCam": CAMS["HeroCam"]["loc"], "tuinmidden": (7.0, 6.0, 1.6)})
        for o in r1:
            o.hide_viewport = False
        bpy.context.view_layer.update()
        uit["luchttoets_ring1"] = {"met_ring1": uit["luchttoets"]["hoog_dicht_pct"],
                                   "zonder_ring1": zonder["hoog_dicht_pct"],
                                   "zonder_ring1_0_6_graden": zonder["dicht_pct_min"],
                                   "eis_in_rtk_lib": uit["luchttoets"]["eis_hoog_pct"]}
        log("luchttoets ring 1:", uit["luchttoets_ring1"])
    for m in mods:
        m.show_viewport = True
    if mist:
        mist.hide_viewport = False
    bpy.context.view_layer.update()

    # 3. eigen audit (met gras: geen sprieten op de route)
    uit["audit_extra"] = rl.audit_extra(meting["binnenruimte"], route_sdf=route_sdf, gazon_obj=gazon,
                                         gazon_vrij=0.05)
    uit["hut"] = {k: v for k, v in meting.items()}
    uit["ok"] = all(uit[k]["ok"] for k in ("validate_scene", "cl_audit", "schaduwtoets",
                                           "luchttoets", "audit_extra", "hut"))
    s, lu = uit["schaduwtoets"], uit["luchttoets"]
    uit["samenvatting"] = (f"hut deur X {meting['deur_mid_x']} / Y {meting['deur_voorkant_y']}; "
                           f"boomschaduw {s['boom_pct']}% (eis <= 20), hutschaduw west {s['hut_west_punten']} pt; "
                           f"luchtsluiting HeroCam {lu['per_origin']['HeroCam']['dicht_pct']}% / "
                           f"tuinmidden {lu['per_origin']['tuinmidden']['dicht_pct']}% (eis >= 95); "
                           f"validate {'OK' if uit['validate_scene']['ok'] else 'FOUT'}, "
                           f"cl.audit {len(issues)} issues, eigen audit {'OK' if uit['audit_extra']['ok'] else 'FOUT'}")
    log("TOETSEN:", uit["samenvatting"], "->", "OK" if uit["ok"] else "FOUT")
    return uit


def schrijf_json(pad, data):
    pad.parent.mkdir(parents=True, exist_ok=True)
    pad.write_text(json.dumps(data, indent=1, ensure_ascii=False, default=str), encoding="utf-8")


# =========================================================================== renderen
def gpu_vrij_of_stop():
    if GPU_BEZET.exists():
        tekst = GPU_BEZET.read_text(encoding="utf-8", errors="replace")
        if not tekst.startswith("Renders 2.0"):
            raise rl.RtkFout(f"videokaart bezet volgens {GPU_BEZET}: {tekst.strip()[:120]}")


def render_previews():
    gpu_vrij_of_stop()
    scn = bpy.context.scene
    WERK.mkdir(parents=True, exist_ok=True)
    piek = {"max_mb": 0.0}

    def stats(tekst, *_):
        import re
        for m in re.finditer(r"Peak[: ]+([\d.]+)([MG])", str(tekst)):
            mb = float(m.group(1)) * (1024 if m.group(2) == "G" else 1)
            piek["max_mb"] = max(piek["max_mb"], mb)
    bpy.app.handlers.render_stats.append(stats)
    tijden = {}
    scn.render.resolution_x, scn.render.resolution_y = PREVIEW_RES
    scn.render.resolution_percentage = 100
    scn.cycles.samples = PREVIEW_SAMPLES
    scn.cycles.use_denoising = True
    scn.cycles.texture_limit_render = "1024"
    scn.render.image_settings.file_format = "PNG"
    alleen = [c for c in os.environ.get("RTK_CAMS", "").split(",") if c]   # proefrender: bv. HeroCam
    for naam in (alleen or CAMS):
        scn.camera = bpy.data.objects[naam]
        scn.render.filepath = str(WERK / f"{naam}.png")
        t = time.time()
        bpy.ops.render.render(write_still=True)
        tijden[naam] = round(time.time() - t, 1)
        log(f"render {naam}: {tijden[naam]} s")
    scn.camera = bpy.data.objects["HeroCam"]
    uit = {"rendertijden_s": tijden, "geheugenpiek_mb": round(piek["max_mb"], 1),
           "geheugen_grens_mb": 6.5 * 1024, "geheugen_ok": piek["max_mb"] <= 6.5 * 1024}
    schrijf_json(WERK / "render.json", uit)
    log(f"renders klaar: {uit}")
    return uit


# =========================================================================== main
def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(prog="stap1_anker")
    ap.add_argument("--geen-render", action="store_true")
    ap.add_argument("--alleen-render", action="store_true")
    ap.add_argument("--negatief", choices=("hut_verschoven", "boom_in_zonsector", "boom_weg_ring1"))
    args = ap.parse_args(argv)
    log(f"versie {VERSIE}, bestand {bpy.data.filepath}, args {vars(args)}")

    if args.alleen_render:
        if Path(bpy.data.filepath) != UITVOER:
            bpy.ops.wm.open_mainfile(filepath=str(UITVOER))
        render_previews()
        return 0

    if args.negatief in ("boom_in_zonsector", "boom_weg_ring1"):
        # op het opgeslagen anker: één fout aanbrengen, toetsen draaien, NIET opslaan
        if Path(bpy.data.filepath) != UITVOER:
            bpy.ops.wm.open_mainfile(filepath=str(UITVOER))
        meting = json.loads((WERK / "audit.json").read_text(encoding="utf-8"))["hut"]
        if args.negatief == "boom_in_zonsector":
            c = math.radians(SUN_KOMPAS)
            donor_root = next(o for o in bpy.data.objects if o.name.startswith("Boom_2_"))
            dup = cl.dup_hierarchy(donor_root, "Boom_NEG_zonsector", (13.0 + 6.0 * math.sin(c),
                                                                       4.0 + 6.0 * math.cos(c), 0.0))
            dup["rtk_schaal"] = donor_root["rtk_schaal"]
            log(f"NEGATIEVE TEST: kopie van {donor_root.name} in de zonsector op {tuple(dup.location)}")
        else:
            weg = [o for o in bpy.data.objects if o.parent is None and o.name.startswith("Boom_1_")]
            for r in weg:
                for c in list(r.children_recursive) + [r]:
                    bpy.data.objects.remove(c, do_unlink=True)
            log(f"NEGATIEVE TEST: alle {len(weg)} bomen van ring 1 weg")
        bpy.context.view_layer.update()
        route = bpy.data.objects["Route_Steen"]
        route_sdf = rl.route_sdf_from_meta(route)
        uit = toetsen(meting, route_sdf)
        schrijf_json(WERK / f"negatief_{args.negatief}.json", {
            "test": args.negatief, "toetsen_ok": uit["ok"],
            "schaduwtoets": {k: uit["schaduwtoets"][k] for k in ("ok", "boom_pct", "hut_west_punten")},
            "luchttoets": {k: uit["luchttoets"]["per_origin"][k]["dicht_pct"] for k in uit["luchttoets"]["per_origin"]},
            "samenvatting": uit["samenvatting"]})
        log(f"NEGATIEVE TEST {args.negatief}: toetsen {'OK (FOUT: niet gevangen!)' if uit['ok'] else 'faalden (goed)'}")
        return 1 if not uit["ok"] else 0

    if Path(bpy.data.filepath) != INVOER:
        bpy.ops.wm.open_mainfile(filepath=str(INVOER))
    t0 = time.time()
    audit = {"versie": VERSIE, "invoer": str(INVOER)}
    meting = deel_a_hut(args.negatief)
    audit["grond"] = deel_b_grond()
    route, route_info = deel_c_route(meting)
    route_sdf = route_info.pop("sdf")
    audit["route"] = route_info
    audit["hagen"] = deel_d_hagen()
    audit["bomen"] = deel_e_bomen()
    audit["licht"] = deel_f_licht()
    audit["cameras"] = deel_g_cameras()
    audit["gazon"] = deel_h_gazon(route_sdf, rl.HAAG_VOETEN, meting)
    cl.fix_broken_image_materials()
    audit["opbouw_s"] = round(time.time() - t0, 1)
    audit["toetsen"] = toetsen(meting, route_sdf, meet_ring1=not args.negatief)
    audit["hut"] = audit["toetsen"]["hut"]
    audit["objecten"] = len(bpy.data.objects)
    audit["meshes"] = len(bpy.data.meshes)
    audit["vertices_uniek"] = sum(len(m.vertices) for m in bpy.data.meshes if m.users)
    if args.negatief:
        log("negatieve test: niet opslaan")
        schrijf_json(WERK / f"negatief_{args.negatief}.json", audit)
        return 1 if not audit["toetsen"]["ok"] else 0
    schrijf_json(WERK / "audit.json", audit)
    if not audit["toetsen"]["ok"]:
        log("TOETSEN FAALDEN: niet opgeslagen. Zie", WERK / "audit.json")
        return 1
    bpy.ops.wm.save_as_mainfile(filepath=str(UITVOER))
    log("opgeslagen:", UITVOER)
    if not args.geen_render:
        render_previews()
    log(f"KLAAR stap 1 {VERSIE} in {time.time() - t0:.0f} s")
    return 0


if __name__ == "__main__":
    try:
        code = main()
    except rl.RtkFout as e:
        print(f"[stap1] STOP: {e}", flush=True)
        code = 1
    except Exception:   # noqa: BLE001 - volledige traceback naar de log, en exitcode 2
        import traceback
        traceback.print_exc()
        print("[stap1] STOP: onverwachte fout (traceback hierboven)", flush=True)
        code = 2
    sys.stdout.flush()
    os._exit(code)
