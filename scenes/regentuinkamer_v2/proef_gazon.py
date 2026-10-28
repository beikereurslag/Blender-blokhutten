r"""Renders 2.0 - Regentuinkamer v2: gazonproef (fixronde gazon). Slaat NIETS op.

Opent het eindbestand, vervangt alleen de gras-instances op 'Gazon' door een bron uit
rtk_lib.GAZON_BRON en rendert een crop van ~1 m breed dicht bij de grond plus de HeroCam:
  blender -b regentuinkamer_v2.blend --python proef_gazon.py -- <bron|oud> <werkmap> [bodem_val]
bron "oud" = het huidige gazon ongewijzigd (ter vergelijking).
"""
import sys
from pathlib import Path

import bpy
from mathutils import Vector

SCENE_DIR = Path(r"D:\Blender-blokhutten\scenes\regentuinkamer_v2")
sys.path.insert(0, str(SCENE_DIR))
import rtk_dressing as rd  # noqa: E402

rl = rd.rl
CROP = dict(loc=(6.0, 0.95, 0.50), doel=(6.0, 1.95, 0.0), lens=40)


def crop_camera():
    """Camera ~1 m van het gras, schuin omlaag; beeld ~1 m breed op het doelpunt."""
    cam = bpy.data.cameras.new("Cam_GazonCrop")
    cam.lens = CROP["lens"]
    cam.clip_start = 0.02
    ob = bpy.data.objects.new("Cam_GazonCrop", cam)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = CROP["loc"]
    ob.rotation_euler = (Vector(CROP["doel"]) - Vector(CROP["loc"])).to_track_quat("-Z", "Y").to_euler()
    cam.dof.use_dof = False
    return ob


def bodem_lichter(val):
    """Gazonbodem (PH leafy_grass) lichter en groener, zodat gaten niet donker doorschijnen."""
    mat = bpy.data.materials["MAT_Gazonbodem"]
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    lk = bsdf.inputs["Base Color"].links[0]
    hs = nt.nodes.new("ShaderNodeHueSaturation")
    hs.inputs["Hue"].default_value = 0.52
    hs.inputs["Saturation"].default_value = 1.1
    hs.inputs["Value"].default_value = val
    nt.links.new(lk.from_socket, hs.inputs["Color"])
    nt.links.new(hs.outputs["Color"], bsdf.inputs["Base Color"])


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    bron, werk = argv[0], Path(argv[1])
    bodem_val = float(argv[2]) if len(argv) > 2 else None
    rd.open_invoer(SCENE_DIR / "regentuinkamer_v2.blend")
    gazon = bpy.data.objects["Gazon"]
    info = {"bron": bron}
    if bron != "oud":
        gazon.modifiers.clear()
        info.update(rl.gazon_scatter(gazon, bron, bpy.data.materials["MAT_Gazonbodem"]))
    if bodem_val:
        bodem_lichter(bodem_val)
        info["bodem_val"] = bodem_val
    elif bron == "tuin":
        rl.gazon_bodem(bpy.data.materials["MAT_Gazonbodem"])
        info["bodem"] = f"gazon_bodem tint {rl.GAZON_BODEM_TINT}"
    dg = bpy.context.evaluated_depsgraph_get()
    n = sum(1 for inst in dg.object_instances if inst.is_instance and inst.parent
            and inst.parent.original.name == "Gazon")
    info["instances"] = n
    crop_camera()
    rd.log(f"proef gazon: {info}")
    rd.schrijf_json(werk / "gazon.json", info)
    rd.render_diag(["Cam_GazonCrop", "HeroCam"], werk, verwacht_min=4)
    return 0


if __name__ == "__main__":
    rd.main_wrapper(main, "proef_gazon")
