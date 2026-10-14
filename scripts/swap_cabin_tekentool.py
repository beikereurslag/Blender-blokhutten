"""Vervang de cabin in een bestaande scene door een nieuwe tekentool-export.

De scene houdt alles: camera, licht, tuin, props en de goedgekeurde
cabin-materialen. Alleen de geometrie wisselt.

De nieuwe GLB heeft nog maar drie materialen (luxehouse-onbehandeld, epdm,
chrome) terwijl de scene er negen kent, per onderdeel ingesteld. De koppeling
gaat daarom op OBJECTNAAM, niet op materiaalnaam.

Gebruik:
  blender -b <scene.blend> --python scripts/swap_cabin_tekentool.py -- \
      --glb "<pad naar nieuwe .glb>" --uit "<render.png>" [--blend "<opslaan.blend>"]
      [--alleen-render] [--geen-render] [--verslag "<verslag.json>"]

--verslag schrijft de meetgegevens van de swap weg (maten, palen, deuropening,
materialen) plus de uitkomst van validate_scene.py voor en na de swap. Daarop
beslist scripts/tekentool_controle.py of een scene als omgezet telt.
"""
import json
import argparse
import os
import re
import sys

import bpy
from mathutils import Vector

ROOT = r"D:\Blender-blokhutten"
sys.path.insert(0, os.path.join(ROOT, "scripts"))

# Rol van een onderdeel, afgeleid uit de objectnaam. Welk MATERIAAL bij een rol
# hoort verschilt per scene (de ene gebruikt 'basetexture-firstLayer-wall', de
# andere 'DG_wand'), dus dat leren we uit de scene zelf -- zie leer_materialen().
ROLLEN = [
    (re.compile(r"^wall-openEnded", re.I),                "canopywand"),
    (re.compile(r"^wall-\d", re.I),                       "wand"),
    (re.compile(r"^parentBoard.*roofWall", re.I),         "roofboard"),
    (re.compile(r"^parentBoard", re.I),                   "wand"),
    (re.compile(r"^pole", re.I),                          "paal"),
    (re.compile(r"^(roofbeam|wallBeam|muurplaat)", re.I), "balk"),
    (re.compile(r"^(roofPlate|roofboard|dakbeschot)", re.I), "dakplaat"),
    (re.compile(r"^(foundationBeam|log-)", re.I),         "fundering"),
    (re.compile(r"^(fasciaboard|boei)", re.I),            "boei"),
    (re.compile(r"^(trim|wallcorner|scaffold|schoor)", re.I), "trim"),
    (re.compile(r"^flatroof", re.I),                      "dakbedekking"),
]
CABIN = re.compile(
    r"^(shed|blokhut|wall-|pole|roofbeam|log-|parentBoard|fasciaboard|trim|wallcorner|"
    r"flatroof|roofPlate|scaffold|foundationBeam|walls|boards|roof|poles|muurplaat)", re.I)

# De tekentool kan voor BHW-select geen deuren plaatsen (product_options is leeg),
# dus de deur uit de bestaande scene blijft staan. Hij hangt toch los voor de
# wand -- ook in de oude export zit geen uitsparing.
BEWAAR = re.compile(r"(DEURBASIC|doorhandle|scharnier|deurblad|beslag)", re.I)

# De tekentool exporteert geen funderingsbalken; de scenes hebben ze wel, als
# een plint van een paar centimeter waar de wand op rust. Werden ze meeverwijderd,
# dan zakte de nieuwe wand tot op het maaiveld: gras kwam over de muurvoet en het
# terras sloot niet meer aan op de deur. Ze blijven dus staan, net als de deur.
# Let op 'pole-0-foundation': dat is de voet onder een luifelpaal, geen paal.
# Viel hij buiten deze regex, dan telde hij als cabin mee, kwam de onderkant van
# de oude cabin op maaiveld uit en zakte de nieuwe wand er alsnog naartoe.
FUNDERING = re.compile(r"^(foundationBeam|log-|pole-\d+-foundation)", re.I)


def wereld_bbox(objs):
    lo = Vector((1e9,) * 3)
    hi = Vector((-1e9,) * 3)
    for o in objs:
        if o.type != "MESH":
            continue
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            lo = Vector((min(lo[i], w[i]) for i in range(3)))
            hi = Vector((max(hi[i], w[i]) for i in range(3)))
    return lo, hi


def zoek_cabin():
    """De objecten die de nieuwe export vervangt.

    Deur en fundering horen er niet bij: die levert de export niet, dus
    weggooien betekent kwijt zijn. Doordat de fundering blijft staan, is de
    onderkant van deze selectie de onderkant van de oude WAND -- en daar komt
    de nieuwe wand straks precies op terug.
    """
    return [o for o in bpy.data.objects
            if CABIN.match(o.name)
            and not BEWAAR.search(o.name)
            and not FUNDERING.match(o.name)]


def rol_van(naam):
    for pat, rol in ROLLEN:
        if pat.match(naam):
            return rol
    return None


def leer_materialen(oud):
    """Kijk af welk materiaal de scene per rol gebruikt.

    Scenes verschillen hierin: de ene heeft 'basetexture-firstLayer-wall', de
    andere 'DG_wand'. Per rol wint het materiaal dat op de meeste objecten zit.
    """
    from collections import Counter
    per_rol = {}
    for o in oud:
        if o.type != "MESH":
            continue
        rol = rol_van(o.name)
        if not rol:
            continue
        for slot in o.material_slots:
            if slot.material:
                per_rol.setdefault(rol, Counter())[slot.material.name] += 1
    geleerd = {r: c.most_common(1)[0][0] for r, c in per_rol.items()}
    # terugval voor rollen die in deze scene niet voorkwamen
    val = geleerd.get("wand") or geleerd.get("canopywand")
    if val:
        for r in ("wand", "canopywand", "roofboard", "paal", "balk",
                  "dakplaat", "fundering", "boei", "trim"):
            geleerd.setdefault(r, val)
    return geleerd


# Materiaal op PLEK. Op rol alleen gaat het mis zodra een scene twee materialen
# voor dezelfde rol gebruikt: de Dahlia Leeshoek heeft een natuurhouten
# luifelwand naast een grijze hut. In de oude export heette die luifelwand
# anders dan in de nieuwe, dus op rol werd hij grijs. Daarom krijgt elk nieuw
# onderdeel het materiaal van het oude onderdeel op dezelfde plek, met dezelfde
# dunste as (een wandplank pakt geen dakplaat). Ligt er binnen MAX_PLEK_AFSTAND
# niets, dan valt hij terug op de rol.
MAX_PLEK_AFSTAND = 0.6   # m tussen de middens; planken schuiven hooguit ~7 cm
# Alleen binnen dezelfde familie zoeken: anders pakt een balk vlak onder de
# dakrand het materiaal van de aluminium daktrim (gezien bij de Dahlia).
# Wand, luifelwand en gevelplank zijn één familie: precies daar verschillen de
# namen tussen oude en nieuwe export.
FAMILIE = {"wand": "bekleding", "canopywand": "bekleding", "roofboard": "bekleding"}


def familie_van(naam):
    rol = rol_van(naam)
    return FAMILIE.get(rol, rol)


def plek_van(o):
    lo, hi = wereld_bbox([o])
    maat = hi - lo
    return (lo + hi) / 2, min(range(3), key=lambda i: maat[i])


def onthoud_oude_plekken(oud):
    """(midden, dunste as, materiaal) van elk oud cabin-onderdeel met materiaal."""
    plekken = []
    for o in oud:
        if o.type != "MESH" or not o.material_slots or not o.material_slots[0].material:
            continue
        midden, as_ = plek_van(o)
        plekken.append((midden, as_, familie_van(o.name), o.material_slots[0].material))
    return plekken


def materiaal_op_plek(o, plekken):
    midden, as_ = plek_van(o)
    fam = familie_van(o.name)
    beste, afstand = None, MAX_PLEK_AFSTAND
    for m, a, f, mat in plekken:
        if a != as_ or (fam is not None and f != fam):
            continue
        d = (m - midden).length
        if d < afstand:
            beste, afstand = mat, d
    return beste


def snij_deuropening(nieuw, verbose=True):
    """Snij een deuropening in de wandboards voor de bewaarde deur.

    De tekentool maakt zo'n uitsparing zelf zodra er een deur-inset op de wand
    staat. BHW select heeft geen productcatalogus, dus die inset is er niet en
    komt de wand dicht binnen -- je kijkt dan tegen hout aan in plaats van door
    de ruit. Hier snijden we het gat alsnog.
    """
    deur = [o for o in bpy.data.objects
            if o.type == "MESH" and BEWAAR.search(o.name)]
    if not deur:
        return 0
    lo, hi = wereld_bbox(deur)

    # snijblok: exact de deurbreedte en -hoogte, ruim door de wand heen
    # size=2 -> de kubus loopt van -1 tot +1, dus scale = halve afmeting
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    blok = bpy.context.active_object
    blok.name = "_deuropening"
    marge = 0.004                       # kozijn net vrijhouden
    blok.scale = ((hi.x - lo.x) / 2 - marge,
                  0.60,                 # dwars door de wand
                  (hi.z - lo.z) / 2 - marge)
    blok.location = ((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, (lo.z + hi.z) / 2)
    bpy.context.view_layer.update()

    blo, bhi = wereld_bbox([blok])
    gesneden = kandidaat = 0
    for o in list(nieuw):
        if o.type != "MESH" or not o.name.startswith("wall-"):
            continue
        olo, ohi = wereld_bbox([o])
        # overlap met een kleine tolerantie: een board dat de rand van de
        # opening net raakt moet ook mee
        t = 0.001
        raakt = (ohi.x > blo.x + t and olo.x < bhi.x - t and
                 ohi.y > blo.y + t and olo.y < bhi.y - t and
                 ohi.z > blo.z + t and olo.z < bhi.z - t)
        if not raakt:
            continue
        kandidaat += 1
        mod = o.modifiers.new("deuropening", "BOOLEAN")
        mod.operation = "DIFFERENCE"
        mod.object = blok
        mod.solver = "EXACT"   # FLOAT struikelt over coplanaire plankvlakken
        try:
            with bpy.context.temp_override(object=o):
                bpy.ops.object.modifier_apply(modifier=mod.name)
            gesneden += 1
        except Exception as e:
            print(f"[swap]   boolean mislukt op {o.name}: {e}")

    bpy.data.objects.remove(blok, do_unlink=True)
    if verbose:
        print(f"[swap] deuropening {(hi.x-lo.x)*100:.0f} x {(hi.z-lo.z)*100:.0f} cm: "
              f"{gesneden}/{kandidaat} boards gesneden")
    return gesneden, kandidaat


def paalmiddens(objs):
    """XY-midden van elke luifelpaal. Een paalvoet (pole-N-foundation) telt niet."""
    uit = []
    for o in objs:
        if o.type != "MESH" or not re.match(r"^pole", o.name, re.I):
            continue
        if re.search(r"foundation", o.name, re.I):
            continue
        lo, hi = wereld_bbox([o])
        uit.append([round((lo.x + hi.x) / 2, 3), round((lo.y + hi.y) / 2, 3)])
    return uit


def beperk_texturen(scn):
    """Texturen bij het renderen hooguit 2K, zoals het render-recept zegt.

    De zware scenes (S-reeks, 1,7 GB) vullen anders de 8 GB van de RTX 3070 tot
    de rand en een 1080p-proef duurt dan ruim 10 minuten. Op 1080p is het
    verschil tussen 8K en 2K hout niet te zien. Staat de scene al lager, dan
    blijft die waarde staan.
    """
    huidig = scn.cycles.texture_limit_render
    if huidig in ("OFF", "4096", "8192"):
        scn.cycles.texture_limit_render = "2048"
    print(f"[swap] texturen bij renderen: {scn.cycles.texture_limit_render} (was {huidig})")


def valideer():
    """validate_scene.run(), of de fout als tekst: de swap mag er niet op stuklopen."""
    try:
        import validate_scene
        return validate_scene.run()
    except Exception as e:  # noqa: BLE001 -- melding gaat het verslag in
        return {"fout": f"validate_scene faalde: {e!r}"}


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb")
    ap.add_argument("--uit", required=True)
    ap.add_argument("--blend")
    ap.add_argument("--alleen-render", action="store_true")
    ap.add_argument("--draai180", action="store_true",
                    help="draai een halve slag om Z. De export zet de luifel "
                         "rechts met de luifelwand aan de voorkant; de scenes "
                         "hebben de luifel links met die wand achter.")
    ap.add_argument("--geen-render", action="store_true",
                    help="alleen swappen en opslaan; renderen doet tekentool_controle.py")
    ap.add_argument("--verslag", help="schrijf meetgegevens + validatie als JSON")
    ap.add_argument("--samples", type=int)
    ap.add_argument("--breedte", type=int)
    args = ap.parse_args(argv)

    scn = bpy.context.scene
    verslag = {}

    if not args.alleen_render:
        if args.verslag:
            verslag["validatie_oud"] = valideer()
        oud = zoek_cabin()
        lo_o, hi_o = wereld_bbox(oud)
        verslag["oud_maat"] = [round(v, 3) for v in (hi_o - lo_o)]
        verslag["oud_lo"] = [round(v, 3) for v in lo_o]
        verslag["palen_oud"] = paalmiddens(oud)
        print(f"[swap] oude cabin: {len(oud)} objecten, maat "
              f"{[round(v,3) for v in (hi_o-lo_o)]}")

        # collecties onthouden zodat de nieuwe cabin op dezelfde plek in de
        # scene-opbouw komt
        colls = set()
        for o in oud:
            for c in o.users_collection:
                colls.add(c)
        geleerd = leer_materialen(oud)
        print("[swap] materialen uit de scene geleerd:", geleerd)
        oude_plekken = onthoud_oude_plekken(oud)

        # de deur hangt aan de cabin-hierarchie; die valt zo weg. Eerst de
        # wereldtransform vastzetten en de parent losknippen, anders vliegt de
        # deur bij het verwijderen honderden meters weg.
        weg = set(oud)
        losgemaakt = 0
        for o in bpy.data.objects:
            if o in weg:
                continue
            ouder = o.parent
            if ouder is not None and ouder in weg:
                mw = o.matrix_world.copy()
                o.parent = None
                o.matrix_world = mw
                losgemaakt += 1
        if losgemaakt:
            print(f"[swap] {losgemaakt} object(en) losgemaakt van de oude cabin")

        for o in oud:
            bpy.data.objects.remove(o, do_unlink=True)

        voor = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=args.glb)
        nieuw = [o for o in bpy.data.objects if o not in voor]
        for o in list(nieuw):
            if o.type == "CAMERA":
                bpy.data.objects.remove(o, do_unlink=True)
                nieuw.remove(o)

        if args.draai180:
            import math
            from mathutils import Matrix
            R = Matrix.Rotation(math.pi, 4, "Z")
            for o in nieuw:
                if o.parent is None:
                    o.matrix_world = R @ o.matrix_world
            bpy.context.view_layer.update()
            print("[swap] halve slag gedraaid om Z")

        bpy.context.view_layer.update()
        lo_n, hi_n = wereld_bbox(nieuw)
        print(f"[swap] nieuwe cabin: {len(nieuw)} objecten, maat "
              f"{[round(v,3) for v in (hi_n-lo_n)]}")

        # zelfde plek: gecentreerd in x/y op het oude midden, en in de hoogte de
        # onderkant van de nieuwe wand op de onderkant van de oude wand -- dus
        # bovenop de fundering die is blijven staan.
        fundering = [o for o in bpy.data.objects
                     if o.type == "MESH" and FUNDERING.match(o.name)]
        if fundering:
            print(f"[swap] {len(fundering)} funderingsbalken bewaard, "
                  f"wand komt op {lo_o.z * 100:.1f} cm")
        else:
            print("[swap] deze scene heeft geen fundering; wand op de oude bodem")
        mid_o = (lo_o + hi_o) / 2
        mid_n = (lo_n + hi_n) / 2
        delta = Vector((mid_o.x - mid_n.x, mid_o.y - mid_n.y, lo_o.z - lo_n.z))
        for o in nieuw:
            if o.parent is None:
                o.location += delta
        bpy.context.view_layer.update()

        # in dezelfde collecties hangen als de oude cabin
        doel = [c for c in colls if c.name != "Master Collection"]
        if doel:
            for o in nieuw:
                for c in list(o.users_collection):
                    c.objects.unlink(o)
                doel[0].objects.link(o)

        # de scene-materialen terugzetten: eerst op plek, anders op rol
        gezet, gemist, op_plek, op_rol, zonder, anders = {}, 0, 0, 0, [], []
        for o in nieuw:
            if o.type != "MESH":
                continue
            mat = materiaal_op_plek(o, oude_plekken)
            if mat:
                op_plek += 1
                rolmat = geleerd.get(rol_van(o.name) or "", "")
                if rolmat and rolmat != mat.name:
                    anders.append(f"{o.name}: {mat.name} (rol zei {rolmat})")
            else:
                rol = rol_van(o.name)
                mat = bpy.data.materials.get(geleerd.get(rol, "")) if rol else None
                if mat:
                    op_rol += 1
            if not mat:
                gemist += 1
                zonder.append(o.name)
                continue
            o.data.materials.clear()
            o.data.materials.append(mat)
            gezet[mat.name] = gezet.get(mat.name, 0) + 1
        print("[swap] materialen:", gezet,
              f"(op plek: {op_plek}, op rol: {op_rol}, geen: {gemist})")
        verslag["materiaal_op_plek"] = op_plek
        verslag["materiaal_op_rol"] = op_rol
        verslag["plek_anders_dan_rol"] = anders
        if anders:
            print(f"[swap] {len(anders)} onderdelen kregen op plek een ander materiaal dan op rol, "
                  f"bv. {anders[:3]}")
        verslag["materialen"] = gezet
        verslag["zonder_rol"] = sorted(zonder)   # houden hun GLB-materiaal

        lo_c, hi_c = wereld_bbox(nieuw)
        verslag["nieuw_maat"] = [round(v, 3) for v in (hi_c - lo_c)]
        verslag["nieuw_lo"] = [round(v, 3) for v in lo_c]
        verslag["palen_nieuw"] = paalmiddens(nieuw)
        verslag["nieuw_objecten"] = sorted(o.name for o in nieuw)
        print(f"[swap] geplaatst: lo {[round(v,3) for v in lo_c]} "
              f"hi {[round(v,3) for v in hi_c]}")

        # eerst de plankfix (die rekent met hele planken), daarna pas de
        # deuropening erin snijden
        try:
            import fix_cabin_boards as fcb
            if hasattr(fcb, "align_courses"):
                fcb.align_courses()
                print("[swap] plankfix toegepast")
            if hasattr(fcb, "separate_overlapping_walls"):
                fcb.separate_overlapping_walls(offset=0.006)
                print("[swap] veranda-hoekfix toegepast")
        except Exception as e:
            print("[swap] plankfix overgeslagen:", e)

        gesneden, kandidaat = snij_deuropening(nieuw)
        verslag["deur_boards_gesneden"] = gesneden
        verslag["deur_boards_kandidaat"] = kandidaat
        verslag["deur_aanwezig"] = any(o.type == "MESH" and BEWAAR.search(o.name)
                                       for o in bpy.data.objects)

        if args.verslag:
            verslag["validatie_nieuw"] = valideer()
            verslag["glb"] = args.glb
            with open(args.verslag, "w", encoding="utf-8") as f:
                json.dump(verslag, f, indent=1, ensure_ascii=False)
            print("[swap] verslag:", args.verslag)

        if args.blend:
            bpy.ops.wm.save_as_mainfile(filepath=args.blend)
            print("[swap] opgeslagen:", args.blend)

    if args.geen_render:
        return
    # Headless pakt Blender de CPU als de voorkeuren niets zeggen: een 1080p-render
    # duurde zo ruim 10 minuten in plaats van één. Daarom expliciet de GPU.
    # Ook de render-engine expliciet: een deel van de scenes is opgeslagen met
    # EEVEE (de viewport-preview). Zo gerenderd duurt het langer en oogt het
    # anders (platte heg, groene ruiten), en dan vergelijk je oud en nieuw niet
    # eerlijk. Finals en proefrenders zijn Cycles.
    scn.render.engine = "CYCLES"
    import hoektest
    print(f"[swap] rekent op {hoektest.kies_gpu(scn)}")
    beperk_texturen(scn)
    if args.samples:
        scn.cycles.samples = args.samples
    if args.breedte:
        h = round(args.breedte * scn.render.resolution_y / scn.render.resolution_x)
        scn.render.resolution_x = args.breedte
        scn.render.resolution_y = h
    scn.render.filepath = args.uit
    scn.render.image_settings.file_format = "PNG"
    print(f"[swap] render {scn.render.resolution_x}x{scn.render.resolution_y} "
          f"@ {scn.cycles.samples} samples -> {args.uit}")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":   # tekentool_controle.py importeert beperk_texturen
    main()
