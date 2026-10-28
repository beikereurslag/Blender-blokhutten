"""Import van tekentool-GLB's (formaat vanaf sep 2026) in Blender.

Het exportformaat is veranderd ten opzichte van de GLB's uit april:

    | onderdeel   | oud (source-glbs)              | nieuw (source-glbs-new)      |
    |-------------|--------------------------------|------------------------------|
    | eenheid     | centimeters                    | meters                       |
    | scene-roots | 'shed' + 'camera' (+ losse)    | 'blokhut'                    |
    | materialen  | 9x basetexture-firstLayer-*    | epdm, luxehouse-onbehandeld, |
    |             |                                | chrome                       |
    | plankhoogte | 150 mm, gang 135 mm            | 130 mm, gang 109,2 mm        |

Deze module leest beide formaten en levert altijd een cabin op meters, met de
onderkant op Z=0 en gecentreerd op de oorsprong.

Let op: de halve-laag verschuiving tussen naastgelegen wanden zit ook in de
nieuwe export. Draai `scripts/fix_cabin_boards.py::align_courses()` er nog
overheen -- zie [[project_plank_defect]].
"""
import os

import bpy
from mathutils import Vector

# materiaalnamen in de nieuwe export -> rol in de scene
NIEUWE_MATERIALEN = {
    "luxehouse-onbehandeld": "hout",
    "epdm": "dakbedekking",
    "chrome": "aluminium",
}


def _wereld_bbox(objecten):
    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    for ob in objecten:
        if ob.type != "MESH":
            continue
        for hoek in ob.bound_box:
            w = ob.matrix_world @ Vector(hoek)
            lo = Vector((min(lo[i], w[i]) for i in range(3)))
            hi = Vector((max(hi[i], w[i]) for i in range(3)))
    return lo, hi


def detecteer_formaat(objecten):
    """'nieuw' (meters, root blokhut) of 'oud' (centimeters, root shed)."""
    namen = {ob.name.split(".")[0] for ob in objecten}
    if "blokhut" in namen:
        return "nieuw"
    if "shed" in namen:
        # dubbelcheck op grootte: een cabin van >50 eenheden staat in cm
        lo, hi = _wereld_bbox(objecten)
        return "oud" if max(hi - lo) > 50 else "nieuw"
    lo, hi = _wereld_bbox(objecten)
    return "oud" if max(hi - lo) > 50 else "nieuw"


def importeer(pad, naam=None, centreren=True):
    """Importeer een tekentool-GLB en geef (root_empty, objecten) terug.

    De cabin staat daarna in meters, met de onderkant op Z=0.
    """
    if not os.path.exists(pad):
        raise FileNotFoundError(pad)

    naam = naam or os.path.splitext(os.path.basename(pad))[0]
    voor = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=pad)
    nieuw = [ob for ob in bpy.data.objects if ob not in voor]

    # de export kan een camera meesturen die op een rare plek staat
    for ob in list(nieuw):
        if ob.type == "CAMERA":
            bpy.data.objects.remove(ob, do_unlink=True)
            nieuw.remove(ob)

    formaat = detecteer_formaat(nieuw)

    # alle top-level objecten onder een eigen root hangen: nieuwere exports
    # zetten wand-skeletons als losse scene-roots naast de hoofdnode
    root = bpy.data.objects.new(naam, None)
    bpy.context.collection.objects.link(root)
    for ob in nieuw:
        if ob.parent is None:
            ob.parent = root
            ob.matrix_parent_inverse = root.matrix_world.inverted()

    if formaat == "oud":
        root.scale = (0.01, 0.01, 0.01)   # cm -> m
    bpy.context.view_layer.update()

    if centreren:
        lo, hi = _wereld_bbox(nieuw)
        midden = (lo + hi) / 2
        root.location = (root.location.x - midden.x,
                         root.location.y - midden.y,
                         root.location.z - lo.z)
        bpy.context.view_layer.update()

    return root, nieuw, formaat


def materiaal_rollen(objecten):
    """Groepeer materialen op rol, zodat een swap niet op naam hoeft te gokken."""
    rollen = {}
    for ob in objecten:
        if ob.type != "MESH":
            continue
        for slot in ob.material_slots:
            if not slot.material:
                continue
            stam = slot.material.name.split(".")[0]
            rol = NIEUWE_MATERIALEN.get(stam)
            if rol is None:
                # oud formaat: basetexture-firstLayer-<onderdeel>
                if stam.startswith("basetexture"):
                    rol = "hout"
                elif "chrome" in stam:
                    rol = "aluminium"
                elif "flatroof" in stam or "epdm" in stam:
                    rol = "dakbedekking"
                else:
                    rol = "overig"
            rollen.setdefault(rol, set()).add(slot.material.name)
    return {k: sorted(v) for k, v in rollen.items()}


if __name__ == "__main__":
    import sys
    pad = sys.argv[-1]
    root, objs, formaat = importeer(pad)
    lo, hi = _wereld_bbox(objs)
    print(f"formaat   : {formaat}")
    print(f"objecten  : {len(objs)}")
    print(f"afmeting  : {[round(v, 3) for v in (hi - lo)]} m")
    print(f"materialen: {materiaal_rollen(objs)}")
