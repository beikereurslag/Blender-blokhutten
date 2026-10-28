"""Controle na de tekentool-swap: beslist of een scene als omgezet telt.

Draait headless op de NIEUWE blend, met het verslag dat swap_cabin_tekentool.py
schreef (--verslag). Doet drie dingen:

1. Toetst het verslag: geen nieuwe validate_scene-flags (CRITICAL/HIGH) door de
   swap, palen op dezelfde plek, maat binnen het bekende verschil tussen oud en
   nieuw tekentool-formaat, wand op de oude fundering, deur bewaard en de
   deuropening echt gesneden.
2. Proefrender 1920x1080 / 256 samples met de hero-camera van de scene.
3. Hoektest: goedkope probes rondom de CABIN (niet rond 0,0,0), zodat een
   verkeerd gedraaide luifel, een dichte deur of een gat in een achterwand
   zichtbaar wordt vanaf kanten die de hero-camera niet ziet.

Gebruik:
  blender -b <nieuw.blend> --python scripts/tekentool_controle.py -- \\
      --verslag <swap.json> --out <map> [--hoeken 8]

Schrijft <map>/controle.json met "omgezet": true/false en de redenen.
"""
import argparse
import json
import sys
from math import cos, pi, sin
from pathlib import Path

import bpy

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

# Bekend verschil tussen het oude (apr) en nieuwe (sep) tekentool-formaat, zie
# TEKENTOOL_HEREXPORT.md: breedte +3 cm, diepte gelijk, hoogte +0,5 tot +12 cm.
# Ruimer dan dat betekent een ander model of een andere oriëntatie.
MAX_BREEDTE_DIEPTE_VERSCHIL = 0.10   # m
MIN_HOOGTE_VERSCHIL = -0.02          # m
MAX_HOOGTE_VERSCHIL = 0.20           # m
MAX_PAAL_VERSCHUIVING = 0.08         # m: +3 cm luifel, de helft door het centreren
MAX_BODEM_VERSCHIL = 0.01            # m: nieuwe wand moet op de oude fundering staan
ZWARE_FLAGS = ("CRITICAL", "ERROR", "HIGH")


def toets(verslag: dict) -> tuple[list[str], list[str]]:
    """Geeft (fouten, opmerkingen). Eén fout = niet omgezet."""
    fouten, opm = [], []

    oud, nieuw = verslag["oud_maat"], verslag["nieuw_maat"]
    for as_, i in (("breedte", 0), ("diepte", 1)):
        d = nieuw[i] - oud[i]
        if abs(d) > MAX_BREEDTE_DIEPTE_VERSCHIL:
            fouten.append(f"{as_} wijkt {d * 100:+.1f} cm af (oud {oud[i]:.3f} m, nieuw {nieuw[i]:.3f} m)")
    dz = nieuw[2] - oud[2]
    if not MIN_HOOGTE_VERSCHIL <= dz <= MAX_HOOGTE_VERSCHIL:
        fouten.append(f"hoogte wijkt {dz * 100:+.1f} cm af (verwacht +0,5 tot +12 cm)")

    bodem = verslag["nieuw_lo"][2] - verslag["oud_lo"][2]
    if abs(bodem) > MAX_BODEM_VERSCHIL:
        fouten.append(f"onderkant cabin {bodem * 100:+.1f} cm verschoven t.o.v. de fundering")

    # Alleen oud -> nieuw toetsen: de oude scenes hebben soms een paal onder een
    # andere naam (Lelie Ochtendnevel: 1 'pole'-object, de export heeft er 2).
    # Een oude paal zonder nieuwe ernaast betekent een gedraaide of andere luifel.
    p_oud, p_nieuw = verslag["palen_oud"], verslag["palen_nieuw"]
    if len(p_oud) != len(p_nieuw):
        opm.append(f"aantal paal-objecten {len(p_oud)} -> {len(p_nieuw)}")
    for p in p_oud:
        if not p_nieuw:
            break
        afstand = min(((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 0.5 for q in p_nieuw)
        if afstand > MAX_PAAL_VERSCHUIVING:
            fouten.append(f"paal bij {p} staat nu {afstand * 100:.0f} cm verderop (luifel gedraaid of andere maat?)")

    if not verslag.get("deur_aanwezig"):
        fouten.append("deur niet meer in de scene")
    elif verslag.get("deur_boards_gesneden", 0) < 1:
        fouten.append("deuropening niet gesneden: er loopt een plank voor de ruit")
    elif verslag["deur_boards_gesneden"] < verslag.get("deur_boards_kandidaat", 0):
        fouten.append(f"deuropening half gesneden ({verslag['deur_boards_gesneden']}/"
                      f"{verslag['deur_boards_kandidaat']} planken)")

    if verslag.get("materiaal_op_rol"):
        opm.append(f"{verslag['materiaal_op_rol']} onderdelen kregen hun materiaal op rol "
                   "(geen oud onderdeel op die plek): nakijken in de vergelijking oud/nieuw")
    if verslag.get("zonder_rol"):
        opm.append(f"{len(verslag['zonder_rol'])} onderdelen houden hun GLB-materiaal: "
                   + ", ".join(verslag["zonder_rol"][:6]))

    v_oud, v_nieuw = verslag.get("validatie_oud", {}), verslag.get("validatie_nieuw", {})
    for v, wanneer in ((v_oud, "voor"), (v_nieuw, "na")):
        if "fout" in v:
            fouten.append(f"validatie {wanneer} de swap: {v['fout']}")
    if "flags" in v_oud and "flags" in v_nieuw:
        bekend = {(f.get("category"), f.get("object")) for f in v_oud["flags"]}
        # validate_scene kent de objectnamen van het nieuwe formaat niet allemaal
        # (de aluminium daktrim heet 'chrome'); onderdelen van de geïmporteerde
        # cabin bewegen als geheel mee en tellen hier niet als los object.
        cabin = set(verslag.get("nieuw_objecten", []))
        nieuwe = [f for f in v_nieuw["flags"]
                  if (f.get("category"), f.get("object")) not in bekend
                  and f.get("object") not in cabin]
        for f in nieuwe:
            regel = f"nieuwe validatieflag {f['severity']}: {f['message']}"
            (fouten if f["severity"] in ZWARE_FLAGS else opm).append(regel)
        oude_zware = sum(1 for f in v_oud["flags"] if f["severity"] in ZWARE_FLAGS)
        if oude_zware:
            opm.append(f"{oude_zware} zware flag(s) zaten al in de oude scene (niet door de swap)")
    return fouten, opm


def main() -> None:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(prog="tekentool_controle")
    ap.add_argument("--verslag", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--hoeken", type=int, default=8)
    args = ap.parse_args(argv)

    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    verslag = json.loads(Path(args.verslag).read_text(encoding="utf-8"))
    fouten, opm = toets(verslag)

    import hoektest
    import validate_scene

    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    apparaat = hoektest.kies_gpu(scene)
    print(f"[controle] rekent op {apparaat}", flush=True)
    scene.render.use_persistent_data = False
    scene.render.image_settings.file_format = "PNG"

    # --- proefrender met de hero-camera van de scene
    if scene.camera is None:
        fouten.append("scene heeft geen actieve camera")
    else:
        from swap_cabin_tekentool import beperk_texturen  # zelfde instelling als de oude render
        beperk_texturen(scene)
        scene.cycles.samples = 256
        scene.render.resolution_x = 1920
        scene.render.resolution_y = 1080
        scene.render.resolution_percentage = 100
        scene.render.filepath = str(out / "hero_1080.png")
        bpy.ops.render.render(write_still=True)
        print(f"[controle] hero klaar ({scene.camera.name})", flush=True)

    # --- hoektest rond de cabin
    bbox = validate_scene.compute_cabin_bbox()
    if bbox is None:
        fouten.append("geen cabin gevonden voor de hoektest")
    else:
        lo, hi, _ = bbox
        mid = (lo + hi) / 2
        half_diag = ((hi.x - lo.x) ** 2 + (hi.y - lo.y) ** 2) ** 0.5 / 2
        straal = half_diag + 5.0
        import cabin_lib as cl
        scene.cycles.samples = 24
        scene.render.resolution_x, scene.render.resolution_y = 640, 360
        scene.render.use_simplify = True
        scene.render.simplify_subdivision_render = 1
        scene.cycles.texture_limit_render = "1024"
        doel = (mid.x, mid.y, 1.2)
        for i in range(args.hoeken):
            graden = 360.0 * i / args.hoeken
            hoek = 2 * pi * i / args.hoeken
            pos = (mid.x + straal * sin(hoek), mid.y + straal * cos(hoek), 1.65)
            cl.add_camera(pos, doel, lens=28, shift_y=-0.03, name=f"Hoektest_{graden:03.0f}")
            scene.render.filepath = str(out / f"hoek_{graden:03.0f}.png")
            bpy.ops.render.render(write_still=True)
        print(f"[controle] {args.hoeken} hoeken klaar, straal {straal:.1f} m", flush=True)

    uitkomst = {"omgezet": not fouten, "fouten": fouten, "opmerkingen": opm,
                "apparaat": apparaat, "verslag": str(Path(args.verslag).resolve())}
    (out / "controle.json").write_text(json.dumps(uitkomst, indent=1, ensure_ascii=False),
                                       encoding="utf-8")
    print(f"[controle] OMGEZET={uitkomst['omgezet']} fouten={len(fouten)}", flush=True)
    for f in fouten:
        print(f"[controle]   FOUT {f}", flush=True)


if __name__ == "__main__":
    main()
