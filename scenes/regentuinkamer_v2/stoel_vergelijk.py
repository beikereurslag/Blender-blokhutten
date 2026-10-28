r"""Vergelijking zitplek: Meshy-fauteuil (huidig) vs eigen teakstoel (stoel_teak.py) vs BK Delhi.

  blender -b regentuinkamer_v2.blend --python stoel_vergelijk.py -- [--alleen eigen,delhi,meshy] [--detail]

Rendert Cam_Close_Zitplek en een detailcamera (960x540, previewinstellingen van rtk_dressing)
per variant naar previews\_werk\stoel_vergelijk\<variant>\. Slaat de blend NIET op.
"""
import math
import sys
from pathlib import Path

import bpy

SCENE_DIR = Path(r"D:\Blender-blokhutten\scenes\regentuinkamer_v2")
sys.path.insert(0, str(SCENE_DIR))
import rtk_dressing as rd  # noqa: E402
import stoel_teak  # noqa: E402

UIT = SCENE_DIR / "previews" / "_werk" / "stoel_vergelijk"
DELHI = rd.BK / "renders2" / "Delhi_Wooden_Slat_Lounge_Chair.blend"
STOELEN = {"A": (11.30, 9.30, math.radians(15)), "B": (12.62, 9.30, math.radians(-15))}


def meshy_objecten():
    return [o for o in bpy.data.objects if o.name.startswith("Zit_Fauteuil_")]


def zet_zichtbaar(obs, aan):
    for o in obs:
        o.hide_render = not aan
        o.hide_viewport = not aan


def delhi(naam, x, y, rot):
    with bpy.data.libraries.load(str(DELHI), link=False) as (src, dst):
        dst.objects = list(src.objects)
    obs = [o for o in dst.objects if o is not None]
    for o in obs:
        bpy.context.scene.collection.objects.link(o)
    root = next(o for o in obs if o.parent is None)
    root.name = naam
    # Delhi-front is al -Y (zie DELHI_ROT)
    root.location = (x, y, rd.KAPVLOER_TOP)
    root.rotation_euler = (0, 0, rot + DELHI_ROT)
    return [root, *root.children_recursive]


DELHI_ROT = 0.0         # render 1: met pi stond de rug naar de camera, dus het front is al -Y


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    varianten = ["meshy", "eigen", "delhi"]
    if "--alleen" in argv:
        varianten = argv[argv.index("--alleen") + 1].split(",")
    # waterpasse camera (cl.add_camera): hoogte via shift_y
    detail = rd.zet_camera("Cam_Stoel_Detail", (10.95, 8.0, 0.62), (11.30, 9.30, 0.62), 28, shift_y=-0.15,
                           dof_focus=(11.3, 9.1, 0.45), fstop=8.0)
    cams = ["Cam_Close_Zitplek", detail.name]
    meshy = meshy_objecten()
    for var in varianten:
        zet_zichtbaar(meshy, var == "meshy")
        nieuw = []
        if var == "eigen":
            for k, (x, y, r) in STOELEN.items():
                root = stoel_teak.bouw_stoel(f"Test_Eigen_{k}", (x, y, rd.KAPVLOER_TOP), r, seed=3 if k == "A" else 17)
                nieuw += [root, *root.children_recursive]
            print("[vergelijk] eigen info", stoel_teak.info(nieuw[0]), flush=True)
        elif var == "delhi":
            for k, (x, y, r) in STOELEN.items():
                nieuw += delhi(f"Test_Delhi_{k}", x, y, r)
        bpy.context.view_layer.update()
        uit = rd.render_diag(cams, UIT / var, verwacht_min=3)
        print(f"[vergelijk] {var}: {uit}", flush=True)
        for o in nieuw:
            bpy.data.objects.remove(o, do_unlink=True)
    return 0


if __name__ == "__main__":
    rd.main_wrapper(main, "vergelijk")
