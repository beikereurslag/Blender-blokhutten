r"""Renders 2.0 - Regentuinkamer v2: één final renderen (wordt per camera aangeroepen door finals_run.ps1).

  blender -b regentuinkamer_v2.blend --python finals_render.py -- <camera> <uitbestand.png> [texture_limit]

2560x1440, AgX Medium High Contrast, 512 samples adaptief (drempel 0,008), OIDN, texture_limit 2048
(of het meegegeven getal), persistent data uit, 16-bit PNG, OPTIX expliciet. Slaat de blend niet op.
Schrijft <uitbestand>.json met rendertijd en de Cycles-geheugenpiek. Exitcode 0 = gelukt.
GPU_BEZET.txt regelt finals_run.ps1, niet dit script.
"""
import json
import re
import sys
import time
from pathlib import Path

import bpy

GRENS_MB = 6.5 * 1024


def zet_optix(scn):
    # losse 'blender -b' heeft compute_device_type NONE en rendert dan stil op de processor (gemeten 26-10)
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "OPTIX"
    prefs.get_devices()
    for dv in prefs.devices:
        dv.use = dv.type == "OPTIX"
    if not any(dv.use for dv in prefs.devices):
        raise SystemExit("FOUT: geen OPTIX-videokaart gevonden; niet stil op de processor renderen")
    scn.cycles.device = "GPU"
    return [dv.name for dv in prefs.devices if dv.use]


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    cam, uit = argv[0], Path(argv[1])
    tex = argv[2] if len(argv) > 2 else "2048"
    scn = bpy.context.scene
    if cam not in bpy.data.objects:
        raise SystemExit(f"FOUT: camera {cam} bestaat niet in {bpy.data.filepath}")
    apparaat = zet_optix(scn)
    scn.camera = bpy.data.objects[cam]
    r, c = scn.render, scn.cycles
    r.engine = "CYCLES"
    r.resolution_x, r.resolution_y, r.resolution_percentage = 2560, 1440, 100
    r.use_persistent_data = False
    c.samples = 512
    c.use_adaptive_sampling = True
    c.adaptive_threshold = 0.008
    c.use_denoising = True
    c.denoiser = "OPENIMAGEDENOISE"
    c.texture_limit_render = tex
    scn.view_settings.view_transform = "AgX"
    scn.view_settings.look = "AgX - Medium High Contrast"
    r.image_settings.file_format = "PNG"
    r.image_settings.color_mode = "RGB"
    r.image_settings.color_depth = "16"
    r.filepath = str(uit)
    uit.parent.mkdir(parents=True, exist_ok=True)
    piek = {"mb": 0.0}

    def stats(tekst, *_):
        for m in re.finditer(r"Mem:\s*([\d.]+)([MG])", str(tekst)):
            piek["mb"] = max(piek["mb"], float(m.group(1)) * (1024 if m.group(2) == "G" else 1))
    bpy.app.handlers.render_stats.append(stats)
    t = time.time()
    bpy.ops.render.render(write_still=True)
    sec = round(time.time() - t, 1)
    info = {"camera": cam, "uit": str(uit), "rendertijd_s": sec, "cycles_mem_max_mb": round(piek["mb"]),
            "grens_mb": GRENS_MB, "geheugen_ok": 0 < piek["mb"] <= GRENS_MB, "texture_limit": tex,
            "apparaat": apparaat, "look": scn.view_settings.look, "samples": c.samples,
            "adaptief": c.adaptive_threshold, "denoiser": c.denoiser, "kleurdiepte": r.image_settings.color_depth}
    Path(str(uit) + ".json").write_text(json.dumps(info, indent=1), encoding="utf-8")
    print(f"[final] {info}", flush=True)
    if not uit.exists():
        raise SystemExit(f"FOUT: {uit} niet geschreven")


if __name__ == "__main__":
    main()
