r"""Welke final-camera's zien de fauteuils? Raycast vanaf elke camera naar punten op de stoelen.

  blender -b regentuinkamer_v2.blend --python stoel_in_beeld.py

Per camera: hoeveel stoelpunten binnen het beeld (frustum) vallen en daarvan hoeveel echt zichtbaar
zijn (eerste raakobject is de stoel zelf, niet een muur/plant ervoor). Schrijft logs\stoel_in_beeld.json.
"""
import json
import sys
from pathlib import Path

import bpy
from bpy_extras.object_utils import world_to_camera_view

SCENE_DIR = Path(r"D:\Blender-blokhutten\scenes\regentuinkamer_v2")
CAMS = ["HeroCam", "Cam_Bekken", "Cam_Westhoek", "Cam_Close_Bekken", "Cam_Close_Oostborder", "Cam_Close_Zitplek"]


def main():
    scn = bpy.context.scene
    scn.render.resolution_x, scn.render.resolution_y = 2560, 1440
    dg = bpy.context.evaluated_depsgraph_get()
    stoel_obs = [o for o in bpy.data.objects if o.name.startswith("Zit_Fauteuil_") and o.type == "MESH"]
    if not stoel_obs:
        raise SystemExit("FOUT: geen Zit_Fauteuil_*-meshes in de scène")
    punten = []
    for o in stoel_obs:
        me = o.data
        stap = max(1, len(me.vertices) // 150)
        punten += [o.matrix_world @ me.vertices[i].co for i in range(0, len(me.vertices), stap)]
    namen = {o.name for o in stoel_obs}
    uit = {}
    for cn in CAMS:
        cam = bpy.data.objects[cn]
        oog = cam.matrix_world.translation
        in_frustum = zichtbaar = 0
        for p in punten:
            c = world_to_camera_view(scn, cam, p)
            if not (0 <= c.x <= 1 and 0 <= c.y <= 1 and c.z > 0):
                continue
            in_frustum += 1
            r = p - oog
            hit, loc, _n, _i, ob, _m = scn.ray_cast(dg, oog, r.normalized(), distance=r.length + 0.01)
            if hit and ob is not None and (ob.original.name in namen or (loc - p).length < 0.02):
                zichtbaar += 1
        uit[cn] = {"punten": len(punten), "in_beeld": in_frustum, "zichtbaar": zichtbaar,
                   "afstand_m": round((oog - punten[0]).length, 1)}
        print(f"[inbeeld] {cn}: {uit[cn]}", flush=True)
    (SCENE_DIR / "logs" / "stoel_in_beeld.json").write_text(json.dumps(uit, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
