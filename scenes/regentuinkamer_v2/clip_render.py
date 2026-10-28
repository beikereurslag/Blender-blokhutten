r"""Renders 2.0 - Regentuinkamer v2: proefclip HeroCam, langzame dolly-in naar de deur (slaat de blend niet op).

  blender -b regentuinkamer_v2.blend --python clip_render.py -- <framesmap> [--frames 1,72,144] [--samples 64]

Zonder --frames: alle 144 frames (6 s x 24 fps) als animatie. Met --frames: alleen die frames (testframes).
Beweging: 0,8 m in de richting van het deurmidden, met een zijwaartse boog van max 0,12 m (sinus), tijd
via smootherstep (ease in/out, snelheid 0 aan begin en eind: geen schok). De camera blijft waterpas
(zoals cl.add_camera) en kijkt elk frame naar de deur; de scherpte volgt de afstand tot de deur.
1280x720, Cycles OPTIX (expliciet), adaptief, OIDN, persistent data aan, texture_limit 2048, PNG 8-bit.
Schrijft <framesmap>\clip.json met tijd per frame en Cycles-piek.
"""
import argparse
import json
import math
import sys
import time
from pathlib import Path

import bpy
from mathutils import Vector

DEUR = Vector((9.028, 8.0, 1.2))      # stap1_anker: DEUR_MID_X, DEUR_VOOR_Y, doelhoogte HeroCam
DOLLY_M = 0.8
BOOG_M = 0.12
FPS, N_FRAMES = 24, 144
RES = (1280, 720)


def smootherstep(t):
    return t * t * t * (t * (6 * t - 15) + 10)


def camera_stand(start, t):
    """Positie op tijd t (0..1) en de waterpas kijkrichting naar de deur."""
    vlak = Vector((DEUR.x - start.x, DEUR.y - start.y, 0.0)).normalized()
    zij = Vector((-vlak.y, vlak.x, 0.0))
    s = smootherstep(t)
    pos = start + vlak * (DOLLY_M * s) + zij * (BOOG_M * math.sin(math.pi * s))
    d = Vector((DEUR.x, DEUR.y, pos.z)) - pos
    return pos, d.to_track_quat("-Z", "Y").to_euler()


def zet_optix(scn):
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "OPTIX"
    prefs.get_devices()
    for dv in prefs.devices:
        dv.use = dv.type == "OPTIX"
    if not any(dv.use for dv in prefs.devices):
        raise SystemExit("FOUT: geen OPTIX-videokaart gevonden; niet stil op de processor renderen")
    scn.cycles.device = "GPU"


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    ap = argparse.ArgumentParser(prog="clip_render")
    ap.add_argument("map")
    ap.add_argument("--frames", default="")
    ap.add_argument("--samples", type=int, default=64)
    args = ap.parse_args(argv)
    uit = Path(args.map)
    uit.mkdir(parents=True, exist_ok=True)
    scn = bpy.context.scene
    cam = bpy.data.objects["HeroCam"]
    start = cam.location.copy()
    if (Vector((start.x, start.y)) - Vector((8.0, 0.7))).length > 0.01:
        raise SystemExit(f"FOUT: HeroCam staat op {tuple(start)}, verwacht (8,0; 0,7): andere scène?")
    # keyframes per frame (lineair tussen de frames: de ease zit in de berekende standen)
    cam.animation_data_clear()
    cam.data.animation_data_clear()
    for f in range(1, N_FRAMES + 1):
        pos, rot = camera_stand(start, (f - 1) / (N_FRAMES - 1))
        cam.location = pos
        cam.rotation_euler = rot
        cam.data.dof.focus_distance = (Vector((DEUR.x, DEUR.y, DEUR.z)) - pos).length
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
    for ad in (cam.animation_data, cam.data.animation_data):
        for fc in ad.action.fcurves if hasattr(ad.action, "fcurves") else []:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"
    zet_optix(scn)
    scn.camera = cam
    r, c = scn.render, scn.cycles
    r.engine = "CYCLES"
    r.resolution_x, r.resolution_y, r.resolution_percentage = *RES, 100
    r.fps = FPS
    r.use_border = False
    r.use_persistent_data = True
    c.samples = args.samples
    c.use_adaptive_sampling = True
    c.adaptive_threshold = 0.02
    c.use_denoising = True
    c.denoiser = "OPENIMAGEDENOISE"
    c.texture_limit_render = "2048"
    c.seed = 0
    c.use_animated_seed = False        # zelfde ruispatroon per frame: minder flikkering na denoise
    scn.view_settings.view_transform = "AgX"
    scn.view_settings.look = "AgX - Medium High Contrast"
    r.image_settings.file_format = "PNG"
    r.image_settings.color_mode = "RGB"
    r.image_settings.color_depth = "8"
    piek = {"mb": 0.0}

    def stats(tekst, *_):
        import re
        for m in re.finditer(r"Mem:\s*([\d.]+)([MG])", str(tekst)):
            piek["mb"] = max(piek["mb"], float(m.group(1)) * (1024 if m.group(2) == "G" else 1))
    bpy.app.handlers.render_stats.append(stats)
    frames = [int(f) for f in args.frames.split(",") if f] or list(range(1, N_FRAMES + 1))
    tijden = {}
    t_alles = time.time()
    for f in frames:
        scn.frame_set(f)
        r.filepath = str(uit / f"frame_{f:04d}.png")
        t = time.time()
        bpy.ops.render.render(write_still=True)
        tijden[f] = round(time.time() - t, 1)
        print(f"[clip] frame {f}: {tijden[f]} s, piek {piek['mb']:.0f} MB, cam {tuple(round(v, 3) for v in cam.location)}",
              flush=True)
    info = {"frames": len(frames), "tijden_s": tijden, "totaal_s": round(time.time() - t_alles, 1),
            "cycles_mem_max_mb": round(piek["mb"]), "samples": c.samples, "res": list(RES),
            "dolly_m": DOLLY_M, "boog_m": BOOG_M}
    (uit / "clip.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
    print(f"[clip] KLAAR {info['totaal_s']} s", flush=True)


if __name__ == "__main__":
    main()
