r"""Renders 2.0 - De Regentuinkamer v2, stap 3: BORDERS (plan §7, laag 3).

Opbouwen + toetsen + opslaan (geen videokaart):
  blender -b regentuinkamer_v2_laag2.blend --python stap3_borders.py -- --geen-render
Alleen de diag-render (opent regentuinkamer_v2_laag3.blend):
  blender -b regentuinkamer_v2_laag3.blend --python stap3_borders.py -- --alleen-render

Wat er komt (ontwerp docs\PLAN_astra_garden.md: wit/lichtviolet, gedempt; drie hoogtes):
- Oostborder (Bed_Oost X 10,0-13,2 / Y 1,2-5,8) in drie in elkaar grijpende drifts:
  laag (0,15-0,35: geranium ingetogen violet, maagdenpalm), midden (0,4-0,7: siergras-pollen,
  maagdenpalm), hoog (0,9-1,2: Abelia, witte 'Moonlight'-lavendel) in het zuidoosten, weg van
  de zichtlijn van de entree naar hut en zitplek;
- westrand van het bekken: drie accenten van 0,9-1,2 m;
- schaduwhoek (Bed_West X 1,0-2,5 / Y 6,5-10,5): varens onder de meerstammige boom, maagdenpalm.
Bronnen: BK Abelia grandiflora (17cff3d0, royalty_free), lokaal BK Geranium_Max_Frei en
SJ-Radiant_Moonlight_Lavender_Petals, PH fern_02, periwinkle_plant, grass_medium_02 (CC0).
Versie via RTK_VERSIE; werkmap previews\_werk\laag3_<versie>\. Toets faalt: niet opslaan, exit 1.
"""
import argparse
import math
import os
import sys
import time
from pathlib import Path

import bpy

SCENE_DIR = Path(r"D:\Blender-blokhutten\scenes\regentuinkamer_v2")
sys.path.insert(0, str(SCENE_DIR))
import rtk_dressing as rd  # noqa: E402

rl, cl = rd.rl, rd.cl
INVOER = SCENE_DIR / "regentuinkamer_v2_laag2.blend"
UITVOER = SCENE_DIR / "regentuinkamer_v2_laag3.blend"
VERSIE = os.environ.get("RTK_VERSIE", "v1")
WERK = SCENE_DIR / "previews" / "_werk" / f"laag3_{VERSIE}"
SEED = 2630
BED_O = rd.BEDDEN["Bed_Oost"]
BED_W = rd.BEDDEN["Bed_West"]
STATEMENT_STAM = (1.7, 8.6)          # stap1_anker.BERK_POS
CAMS = {
    # v4: camera's blijven waterpas (cl.add_camera): shift omlaag, anders alleen haag in beeld (v3)
    "Cam_Close_Oostborder": dict(loc=(9.0, 1.0, 1.50), doel=(11.6, 3.6, 0.0), lens=30, focus=(11.4, 3.4, 0.4),
                                 shift_y=-0.25),
    "Cam_Close_Westhoek": dict(loc=(3.3, 5.0, 1.25), doel=(1.8, 8.4, 0.0), lens=30, focus=(1.9, 8.2, 0.3),
                               shift_y=-0.18),
}
# Geranium Max Frei leest fel roze (handoff G1); ontwerp vraagt ingetogen lichtviolet
GERANIUM_KLEUR = dict(hue=0.53, sat=0.18, val=1.2)     # v5: op Base Color (v3/v4 gingen voor de asset-HueSat langs)


def log(*a):
    print("[stap3]", *a, flush=True)


def logistic(t):
    return 1.0 / (1.0 + math.exp(-t))


def hoogteveld(x, y):
    """0 = laag (west/noord, langs pad en zichtlijn), 1 = hoog (zuidoost). Golvende grenzen
    zodat de drifts in elkaar grijpen."""
    a, b = (x - BED_O[0]) / (BED_O[1] - BED_O[0]), (y - BED_O[2]) / (BED_O[3] - BED_O[2])
    return (0.72 * a + 0.30 * (1 - b) + 0.10 * math.sin(5.5 * b + 1.3)
            + 0.07 * math.sin(6.3 * a + 2.1 * b))


def drift_kans(x, y, drift):
    t = hoogteveld(x, y)
    p_hoog = logistic((t - 0.70) / 0.045)
    p_laag = logistic((0.42 - t) / 0.045)
    return {"hoog": p_hoog, "laag": p_laag, "midden": max(0.0, 1.0 - p_hoog - p_laag)}[drift]


def laad_donors():
    d = {}
    d["abelia"] = rd.soort_donor(rd.BK / "renders2" / "Abelia_grandiflora.blend", "abelia",
                                 lambda n: True, geheel=True, verwacht_h=(0.9, 1.5))
    # v4: SJ-Radiant_Moonlight_Lavender_Petals eruit: kostte 630 MB videogeheugen (Cycles-piek 6,7 GB >
    # grens 6,5) en rendert als felpaarse aren, niet wit/gedempt. Hoge drift = alleen Abelia.
    d["geranium"] = rd.soort_donor(rd.BK / "border-planten" / "Geranium_Max_Frei.blend", "geranium",
                                   lambda n: True, geheel=True, verwacht_h=(0.2, 0.5))
    n_kleur = 0
    for m in {sl.material for o in d["geranium"]["coll"].objects for sl in o.material_slots if sl.material}:
        for beeld in ("fake bush geranium", "max frei ref"):   # v9: de knoppen/bloemen tonen de referentiefoto (roze)
            n_kleur += rd.bloemen_herkleuren(m, beeld, hue=0.53, sat=0.18, val=1.2, drempel=(0.02, 0.10))
        if not any(k in m.name.lower() for k in ("leaf", "stem", "fake")):   # v10: bloemen = Material.006 (100k vlakken), knoppen, flower
            n_kleur += rd.basiskleur_bijstellen(m, **GERANIUM_KLEUR)
    if n_kleur == 0:
        raise rd.RtkFout("geranium: bloembeeld 'geranium max frei flower' niet gevonden, kleur niet aangepast")
    d["geranium"]["kleur_aangepast_nodes"] = n_kleur
    d["gras"] = rd.soort_donor(rd.PH_MODELS / "grass_medium_02_2k.blend", "siergras",
                               lambda n: n.startswith("grass_medium_02_") and not n.endswith("_geo")
                               and "geometry" not in n, verwacht_h=(0.1, 0.5))
    rl.groen_gras(list(d["gras"]["coll"].objects))
    d["maagd"] = rd.soort_donor(rd.PH_MODELS / "periwinkle_plant_2k.blend", "maagdenpalm",
                                lambda n: n.startswith("periwinkle_plant_") and n.endswith("_LOD0"),
                                verwacht_h=(0.12, 0.6))
    for m in {sl.material for o in d["maagd"]["coll"].objects for sl in o.material_slots if sl.material}:
        if not rd.bloemen_herkleuren(m, "periwinkle_plant_diff", hue=0.53, sat=0.15, val=1.25,
                                     drempel=(0.02, 0.10)):   # v8: roze bloemen -> bleek lila (v7 nog paars)
            raise rd.RtkFout(f"maagdenpalm: diff-beeld niet gevonden in {m.name}")
    d["varen"] = rd.soort_donor(rd.PH_MODELS / "fern_02_2k.blend", "varen",
                                lambda n: n.startswith("fern_02_"), verwacht_h=(0.1, 0.6))
    # fix_gazon (Beike: "Oostborder: lossere struiken met één of twee bollen als accent"):
    # PH shrub_02 (CC0, open natuurlijke groeivorm, 1,3-1,6 m) op 0,85-1,15 m. Staat al in de scène
    # als Struiklaag buiten de haag, dus nauwelijks extra videogeheugen (Hydrangea: 2,2 mln vlakken).
    d["struik"] = rd.soort_donor(rd.PH_MODELS / "shrub_02_2k.blend", "struik_los",
                                 lambda n: n.endswith("LOD0"), verwacht_h=(0.9, 1.9))   # variant d = 1,00 m
    rl.groen_struik(list(d["struik"]["coll"].objects))
    return d


class Planter:
    """Houdt per instancer de punten bij en weigert te dichte plekken (ook tegen laag 2)."""

    def __init__(self, rnd, donors, route_sdf, bezet):
        self.rnd, self.d, self.route_sdf, self.bezet = rnd, donors, route_sdf, bezet
        self.lijsten = {}

    def zet(self, inst, soort, x, y, doel_h, factor=0.72, sink=0.012):
        donor = self.d[soort]
        vi = self.rnd.randrange(len(donor["varianten"]))
        var = donor["varianten"][vi]
        s = doel_h / var["h"]
        r = var["w"] * s / 2
        if self.route_sdf(x, y) < 0.25 + 0.5 * r:
            return False
        if rd.dicht_genoeg(x, y, r, self.bezet, factor=factor):
            return False
        rot = self.rnd.uniform(0, 2 * math.pi)
        lijst = self.lijsten.setdefault(inst, (soort, []))[1]
        for q in lijst:          # v2: geen kloon (zelfde variant, schaal en draaiing) binnen 1,2 m
            if q["v"] == vi and math.hypot(q["x"] - x, q["y"] - y) < 1.2 and abs(q["s"] - s) / s < 0.04:
                if abs((q["rot"] - rot + math.pi) % (2 * math.pi) - math.pi) < 0.3:
                    rot = (rot + self.rnd.uniform(1.0, 2.5)) % (2 * math.pi)
        lijst.append({"x": x, "y": y, "z": rd.oppervlak_z(x, y) - sink, "rot": rot, "s": s, "v": vi})
        self.bezet.append((x, y, r))
        return True


def in_bed(x, y, rect, inset):
    return rl.sdf_rect(x, y, rect) < -inset


def oostborder(p, rnd):
    """Dart throwing per soort, van groot naar klein; acceptatie = kans van zijn drift."""
    x0, x1, y0, y1 = BED_O
    plan = [  # instancer, soort, drift, doel-hoogte, aantal, zijdelingse inset
        # fix_gazon: 5 Abelia-bollen -> 2 als accent + 4 losse struiken (Beike, 26-10)
        ("D3_Oost_Abelia", "abelia", "hoog", (0.92, 1.18), 2, 0.62),
        ("D3_Oost_Struik", "struik", "hoog", (0.85, 1.15), 4, 0.55),
        ("D3_Oost_Geranium", "geranium", "laag", (0.25, 0.36), 11, 0.30),   # v2: voor het gras (v1: maar 3)
        ("D3_Oost_Gras", "gras", "midden", (0.40, 0.62), 16, 0.18),
        ("D3_Oost_Maagdenpalm", "maagd", "midden", (0.38, 0.52), 5, 0.18),
        ("D3_Oost_Maagdenpalm", "maagd", "laag", (0.18, 0.28), 6, 0.18),
        ("D3_Oost_Gras", "gras", "laag", (0.15, 0.24), 6, 0.18),
    ]
    geplaatst = {}
    for inst, soort, drift, hoog, aantal, inset in plan:
        n = 0
        for _ in range(6000):
            x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
            if not in_bed(x, y, BED_O, inset):
                continue
            if rnd.random() > drift_kans(x, y, drift):
                continue
            if p.zet(inst, soort, x, y, rnd.uniform(*hoog), factor=0.70):
                n += 1
                if n >= aantal:
                    break
        geplaatst[f"{inst}/{drift}"] = n
    return geplaatst


WESTHOEK_CAM = ((1.5, 1.2), (10.0, 9.2))   # stap1_anker.CAMS["Cam_Westhoek"]: loc, doel
WESTHOEK_VRIJ_M = 1.5


def afstand_tot_zichtlijn(x, y, lijn):
    (ax, ay), (bx, by) = lijn
    ux, uy = bx - ax, by - ay
    return abs(ux * (y - ay) - uy * (x - ax)) / math.hypot(ux, uy)


def westrand(p, rnd):
    """fix_gazon_v4 (Beike: lossere struiken, hooguit twee bollen in de hele tuin): drie losse
    struiken (shrub_02) i.p.v. Abelia-bollen, niet binnen 1,5 m van de zichtlijn van Cam_Westhoek
    (v11 had een bol op (2,90; 3,68) voor het bekken)."""
    n, uit = 0, []
    for _ in range(400):
        th = rnd.uniform(0.80 * math.pi, 1.22 * math.pi)
        x, y = rd.bekken_punt(th, rnd.uniform(1.05, 1.45))
        soort, inst = "struik", "D3_West_Struik"
        if in_bed(x, y, BED_W, -0.3):
            continue
        if afstand_tot_zichtlijn(x, y, WESTHOEK_CAM) < WESTHOEK_VRIJ_M:
            continue
        if p.zet(inst, soort, x, y, rnd.uniform(0.92, 1.18), factor=0.6):   # v5: 0,85 gaf maar 1 accent
            n += 1
            uit.append([round(x, 2), round(y, 2), soort])
            if n >= 3:
                break
    return uit


def schaduwhoek(p, rnd):
    n_v = n_m = 0
    # varens in twee losse groepen onder de kroon, stam vrij (0,5 m)
    for _ in range(4000):
        x, y = rnd.uniform(BED_W[0], BED_W[1]), rnd.uniform(BED_W[2], BED_W[3])
        if not in_bed(x, y, BED_W, 0.22) or math.hypot(x - STATEMENT_STAM[0], y - STATEMENT_STAM[1]) < 0.5:
            continue
        groep = min(math.hypot(x - 1.65, y - 7.4), math.hypot(x - 1.85, y - 9.7))
        if rnd.random() > math.exp(-(groep / 0.9) ** 2) + 0.15:
            continue
        if p.zet("D3_Schaduw_Varen", "varen", x, y, rnd.uniform(0.36, 0.68), factor=0.62):
            n_v += 1
            if n_v >= 13:
                break
    for _ in range(3000):
        x, y = rnd.uniform(BED_W[0], BED_W[1]), rnd.uniform(BED_W[2], BED_W[3])
        if not in_bed(x, y, BED_W, 0.18) or math.hypot(x - STATEMENT_STAM[0], y - STATEMENT_STAM[1]) < 0.4:
            continue
        if p.zet("D3_Schaduw_Maagdenpalm", "maagd", x, y, rnd.uniform(0.17, 0.27), factor=0.6):
            n_m += 1
            if n_m >= 18:          # fix_gazon: was 9, liet kale aarde tussen de varens
                break
    return {"varens": n_v, "maagdenpalm": n_m}


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(prog="stap3_borders")
    ap.add_argument("--geen-render", action="store_true")
    ap.add_argument("--alleen-render", action="store_true")
    args = ap.parse_args(argv)
    log(f"versie {VERSIE}, args {vars(args)}")
    if args.alleen_render:
        rd.open_invoer(UITVOER)
        rd.render_diag(list(CAMS) + ["HeroCam"], WERK)
        return 0

    rd.open_invoer(INVOER)
    t0 = time.time()
    rnd = rl.random_from_seed(SEED)
    meting = rd.meting_anker()
    route_sdf = rl.route_sdf_from_meta(bpy.data.objects["Route_Steen"])
    audit = {"versie": VERSIE, "invoer": str(INVOER), "seed": SEED}
    donors = laad_donors()
    audit["donors"] = {k: rd.donor_info_json(v) for k, v in donors.items()}
    # bezet: alles uit laag 2 (stenen en oeverplanten), zodat niets erdoorheen groeit
    bezet = []
    for o in bpy.data.objects:
        if o.get("rtk_dressing") and o.name.startswith("B2_"):
            for q in rd.punten_van(o):
                bezet.append((q["x"], q["y"], 0.12))
    p = Planter(rnd, donors, route_sdf, bezet)
    audit["oostborder"] = oostborder(p, rnd)
    audit["westrand"] = westrand(p, rnd)
    audit["schaduwhoek"] = schaduwhoek(p, rnd)
    instancers = []
    for inst, (soort, lijst) in sorted(p.lijsten.items()):
        instancers.append(rd.plaats_soort(inst, donors[soort], lijst))
    audit["instancers"] = {o.name: len(o.data.vertices) for o in instancers}
    for naam, c in CAMS.items():
        rd.zet_camera(naam, c["loc"], c["doel"], c["lens"], shift_y=c["shift_y"], dof_focus=c["focus"], fstop=8.0)
    audit["opbouw_s"] = round(time.time() - t0, 1)

    uit = {"standaard": rd.standaard_toetsen(meting)}
    regels = {o.name: {"pad_marge": 0.25, "kap_vrij": True, "zinken": 0.06} for o in instancers}
    uit["dressing"] = rd.audit_dressing(instancers, route_sdf, meting, regels)
    uit["kloon"] = rd.kloon_check({o.name: rd.punten_van(o) for o in instancers})
    hoog_bij_zichtlijn = [q for o in instancers if o.name.startswith(("D3_Oost_Abelia", "D3_Oost_Struik"))
                          for q in rd.punten_van(o) if q["x"] < 11.3 and q["y"] > 3.8]
    uit["zichtlijn"] = {"ok": not hoog_bij_zichtlijn, "hoge_planten_in_zichtlijn": len(hoog_bij_zichtlijn),
                        "eis": "geen planten > 0,9 m in X < 11,3 en Y > 3,8 (zicht entree -> zitplek)"}
    uit["ok"] = all(uit[k]["ok"] for k in ("standaard", "dressing", "kloon", "zichtlijn"))
    uit["samenvatting"] = (f"{uit['standaard']['samenvatting']}; dressing "
                           f"{'OK' if uit['dressing']['ok'] else 'FOUT'} ({sum(uit['dressing']['instances'].values())}"
                           f" instances), kloon {uit['kloon']['klonen']} / rijen {uit['kloon']['rijen']}, "
                           f"zichtlijn {'OK' if uit['zichtlijn']['ok'] else 'FOUT'}")
    log("TOETSEN:", uit["samenvatting"], "->", "OK" if uit["ok"] else "FOUT")
    audit["toetsen"] = uit
    rd.schrijf_json(WERK / "audit.json", audit)
    if not uit["ok"]:
        log("TOETSEN FAALDEN: niet opgeslagen. Zie", WERK / "audit.json")
        return 1
    bpy.ops.wm.save_as_mainfile(filepath=str(UITVOER))
    log("opgeslagen:", UITVOER)
    if not args.geen_render:
        rd.render_diag(list(CAMS) + ["HeroCam"], WERK)
    log(f"KLAAR stap 3 {VERSIE} in {time.time() - t0:.0f} s")
    return 0


if __name__ == "__main__":
    rd.main_wrapper(main, "stap3")
