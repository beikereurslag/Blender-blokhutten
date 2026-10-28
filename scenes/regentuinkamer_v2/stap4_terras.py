r"""Renders 2.0 - De Regentuinkamer v2, stap 4: KAPVLOER + ZITGROEP (plan §7, laag 4).

Opbouwen + toetsen + opslaan als eindbestand regentuinkamer_v2.blend (geen videokaart):
  blender -b regentuinkamer_v2_laag3.blend --python stap4_terras.py -- --geen-render
Alleen renderen (opent regentuinkamer_v2.blend): diag = alleen de zitplek, bundel = 3 camera's + 3 close-ups:
  blender -b regentuinkamer_v2.blend --python stap4_terras.py -- --alleen-render
  blender -b regentuinkamer_v2.blend --python stap4_terras.py -- --bundel

Wat er komt:
- Kapvloer_Steen: zelfde steen en tegelpatroon als de schort (rl.make_route, UV in wereldmaat),
  sluit aan op de schort, bovenkant 0,033 (schort 0,039, dorpel 0,050);
- twee teak-fauteuils, zelf gebouwd in stoel_teak.py (front = -Y, ~0,74 m hoog, roughness >= 0,52;
  28-10: vervangt de GLB Creator/Meshy-fauteuil, die was betaald), licht naar elkaar gedraaid met het
  front naar de tuin; PH side_table_01 (h 0,50) ertussen
  (Tambora-tafel is onbruikbaar: 223 losse delen, handoff G1);
- gebruikssporen met echte assets: PH watering_can_metal_01 op het gras bij de oostborder,
  PH wicker_basket_01 op de kapvloer.
Versie via RTK_VERSIE; werkmap previews\_werk\laag4_<versie>\. Toets faalt: niet opslaan, exit 1.
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
import stoel_teak  # noqa: E402

rl, cl = rd.rl, rd.cl
INVOER = SCENE_DIR / "regentuinkamer_v2_laag3.blend"
UITVOER = SCENE_DIR / "regentuinkamer_v2.blend"
VERSIE = os.environ.get("RTK_VERSIE", "v1")
WERK = SCENE_DIR / "previews" / "_werk" / f"laag4_{VERSIE}"
# zitgroep (ontwerp: X 11,4-12,6 / Y 8,6-9,5): front -Y = naar de tuin, 15 graden naar elkaar toe
# 28-10 (eigen stoel, iets dieper dan de Meshy-stoel): 2 cm naar de tafel, B stak anders buiten de kapvloer
# ronde extra (28-10): B 5 cm naar binnen; stond 1,7 cm van de rand van de kapvloer (vrij van tafel en paal: toets_meubels)
STOELEN = {"Zit_Fauteuil_A": (11.32, 9.30, math.radians(15)), "Zit_Fauteuil_B": (12.55, 9.30, math.radians(-15))}
TAFEL = (11.96, 8.68, 0.0)     # v2: op 8,98 raakten beide armleuningen de tafel (115 vertices)
GIETER = (9.55, 2.45, 2.2)
MAND = (12.62, 10.08, 0.45)
CAM_ZIT = dict(loc=(11.7, 5.4, 1.35), doel=(11.95, 9.2, 0.45), lens=32, focus=(11.95, 9.1, 0.5),
               shift_y=-0.28)   # v3: waterpas camera; zonder shift vielen de stoelen onderuit beeld
BUNDEL = ["HeroCam", "Cam_Bekken", "Cam_Westhoek", "Cam_Close_Bekken", "Cam_Close_Oostborder", "Cam_Close_Zitplek"]


def log(*a):
    print("[stap4]", *a, flush=True)


def kapvloer():
    route = bpy.data.objects["Route_Steen"]
    mat = bpy.data.materials["MAT_Route_Steen"]
    disp = route.modifiers["Displace"].texture.image
    rect = rd.KAPVLOER_RECT
    mid = ((rect[0] + rect[1]) / 2, (rect[2] + rect[3]) / 2)
    # make_route met een piepklein padje midden in de rechthoek: de vorm is dan precies de rechthoek
    ob, info = rl.make_route("Kapvloer_Steen", [mid, (mid[0], mid[1] + 0.05)], 0.01, rect,
                             rd.KAPVLOER_TOP, mat, disp, disp_sterkte=0.012)
    info.pop("sdf")
    info["rect"] = rect
    log(f"kapvloer: {info}")
    return ob, info


def fauteuils():
    # eigen model (stoel_teak.py); per stoel een andere seed, zodat de nerf per lat verschilt
    roots = {}
    for seed, (naam, (x, y, r)) in zip((3, 17), STOELEN.items()):
        roots[naam] = stoel_teak.bouw_stoel(naam, (x, y, rd.KAPVLOER_TOP), r, seed=seed)
    bpy.context.view_layer.update()
    info = {"bron": "stoel_teak.py (eigen model, PH teak_veneer CC0)"}
    for naam, r in roots.items():
        bb = cl.wbbox_meshes([c for c in r.children_recursive if c.type == "MESH"])
        info[naam] = {"bbox": [round(v, 3) for v in bb], "rot_graden": round(math.degrees(r.rotation_euler.z), 1),
                      **stoel_teak.info(r)}
    return roots, info


def props():
    tafel = rd.soort_donor(rd.PH_MODELS / "side_table_01_2k.blend", "bijzettafel",
                           lambda n: n == "side_table_01", geheel=True, verwacht_h=(0.45, 0.65))
    # fix_gazon: gieter (GIETER) weggelaten; las in het heldenbeeld als witte vlek op het gras
    mand = rd.soort_donor(rd.PH_MODELS / "wicker_basket_01_2k.blend", "mand",
                          lambda n: n == "wicker_basket_01", geheel=True, verwacht_h=(0.06, 0.25))
    obs = []
    for naam, donor, (x, y, r), s in (("D4_Bijzettafel", tafel, TAFEL, 0.50 / tafel["varianten"][0]["h"]),
                                      ("D4_Mand", mand, MAND, 1.0)):
        obs.append(rd.plaats_soort(naam, donor, [{"x": x, "y": y, "z": rd.oppervlak_z(x, y), "rot": r, "s": s, "v": 0}]))
    return obs, {"bijzettafel": rd.donor_info_json(tafel), "gieter": "weggelaten (fix_gazon: witte vlek)",
                 "mand": rd.donor_info_json(mand)}


def toets_meubels(meting, roots, tafel_ob):
    """Fauteuils: op de kapvloer (onderkant +-2 cm), binnen de kapvloer, geen vertex in muur,
    paal, tafel of de andere stoel; front (-Y lokaal) wijst naar de tuin (wereld-Y < 0)."""
    fouten, info = [], {}
    bpy.context.view_layer.update()
    k = rd.KAPVLOER_RECT
    blokken = {"muur_gesloten": (10.50, 10.56, 7.9, 10.65, 0.0, 2.2), "achterwand": (10.4, 13.12, 10.50, 10.56, 0.0, 2.2),
               "paal_0": (12.92, 13.02, 8.02, 8.12, 0.0, 2.4), "paal_1": (12.92, 13.02, 10.42, 10.53, 0.0, 2.2)}
    dg = bpy.context.evaluated_depsgraph_get()
    for inst in dg.object_instances:
        if inst.is_instance and inst.parent is not None and inst.parent.original.name == tafel_ob.name:
            tb = rd._wbbox_inst(inst)
            blokken["bijzettafel"] = tb
            info["tafel_bbox"] = [round(v, 3) for v in tb]
    for naam, r in roots.items():
        ms = [c for c in r.children_recursive if c.type == "MESH"]
        bb = cl.wbbox_meshes(ms)
        rec = {"bbox": [round(v, 3) for v in bb]}
        if abs(bb[4] - rd.KAPVLOER_TOP) > 0.02:
            fouten.append(f"{naam}: onderkant z {bb[4]:.3f}, kapvloer {rd.KAPVLOER_TOP}")
        if bb[0] < k[0] + 0.03 or bb[1] > k[1] - 0.03 or bb[2] < k[2] + 0.03 or bb[3] > k[3] - 0.03:
            fouten.append(f"{naam}: steekt buiten de kapvloer {k}: {rec['bbox']}")
        andere = {f"stoel_{n}": cl.wbbox_meshes([c for c in rr.children_recursive if c.type == "MESH"])
                  for n, rr in roots.items() if n != naam}
        for bnaam, box in {**blokken, **andere}.items():
            n_in = sum(rl._world_verts_in_box(m, box) for m in ms)
            if n_in:
                fouten.append(f"{naam}: {n_in} vertices in {bnaam}")
        voor = (r.matrix_world.to_3x3() @ __import__("mathutils").Vector((0.0, -1.0, 0.0))).normalized()
        rec["front_wereld"] = [round(voor.x, 3), round(voor.y, 3)]
        if voor.y > -0.85:
            fouten.append(f"{naam}: front wijst niet naar de tuin ({rec['front_wereld']})")
        info[naam] = rec
    a, b = (roots[n].matrix_world.translation for n in STOELEN)
    fa = info["Zit_Fauteuil_A"]["front_wereld"]
    fb = info["Zit_Fauteuil_B"]["front_wereld"]
    info["naar_elkaar"] = fa[0] > 0 and fb[0] < 0 and a.x < b.x
    if not info["naar_elkaar"]:
        fouten.append(f"fauteuils niet naar elkaar gedraaid: A {fa}, B {fb}")
    return {"ok": not fouten, "fouten": fouten, **info}


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(prog="stap4_terras")
    ap.add_argument("--geen-render", action="store_true")
    ap.add_argument("--alleen-render", action="store_true")
    ap.add_argument("--bundel", action="store_true")
    args = ap.parse_args(argv)
    log(f"versie {VERSIE}, args {vars(args)}")
    if args.alleen_render or args.bundel:
        rd.open_invoer(UITVOER)
        rd.render_diag(BUNDEL if args.bundel else ["Cam_Close_Zitplek"], WERK / ("bundel" if args.bundel else ""),
                       verwacht_min=10 if args.bundel else 3)
        return 0

    rd.open_invoer(INVOER)
    t0 = time.time()
    meting = rd.meting_anker()
    route_sdf = rl.route_sdf_from_meta(bpy.data.objects["Route_Steen"])
    audit = {"versie": VERSIE, "invoer": str(INVOER)}
    _, audit["kapvloer"] = kapvloer()
    roots, audit["fauteuils"] = fauteuils()
    prop_obs, audit["props"] = props()
    c = CAM_ZIT
    rd.zet_camera("Cam_Close_Zitplek", c["loc"], c["doel"], c["lens"], shift_y=c["shift_y"], dof_focus=c["focus"],
                  fstop=8.0)
    audit["opbouw_s"] = round(time.time() - t0, 1)

    uit = {"standaard": rd.standaard_toetsen(meting)}
    regels = {"D4_Bijzettafel": {"pad_marge": None, "kap_vrij": False, "zinken": 0.02},
              "D4_Mand": {"pad_marge": None, "kap_vrij": False, "zinken": 0.02}}
    uit["dressing"] = rd.audit_dressing(prop_obs, route_sdf, meting, regels)
    uit["meubels"] = toets_meubels(meting, roots, bpy.data.objects["D4_Bijzettafel"])
    # alle dressing-lagen samen nog eens: niets onder/op de nieuwe kapvloer
    eerder = [o for o in bpy.data.objects if o.get("rtk_dressing") and o.name.startswith(("B2_", "D3_"))]
    uit["eerdere_lagen"] = rd.audit_dressing(eerder, route_sdf, meting,
                                             {o.name: {"pad_marge": 0.2, "kap_vrij": True,
                                                       "zinken": 0.25 if o.name == "B2_Stenen" else 0.06}
                                              for o in eerder})
    uit["ok"] = all(uit[k]["ok"] for k in ("standaard", "dressing", "meubels", "eerdere_lagen"))
    uit["samenvatting"] = (f"{uit['standaard']['samenvatting']}; props {'OK' if uit['dressing']['ok'] else 'FOUT'}, "
                           f"meubels {'OK' if uit['meubels']['ok'] else 'FOUT'}, lagen 2+3 "
                           f"{'OK' if uit['eerdere_lagen']['ok'] else 'FOUT'}")
    log("TOETSEN:", uit["samenvatting"], "->", "OK" if uit["ok"] else "FOUT")
    audit["toetsen"] = uit
    rd.schrijf_json(WERK / "audit.json", audit)
    if not uit["ok"]:
        log("TOETSEN FAALDEN: niet opgeslagen. Zie", WERK / "audit.json")
        return 1
    bpy.ops.wm.save_as_mainfile(filepath=str(UITVOER))
    log("opgeslagen:", UITVOER)
    if not args.geen_render:
        rd.render_diag(["Cam_Close_Zitplek"], WERK, verwacht_min=3)
    log(f"KLAAR stap 4 {VERSIE} in {time.time() - t0:.0f} s")
    return 0


if __name__ == "__main__":
    rd.main_wrapper(main, "stap4")
