#!/usr/bin/env python3
"""Hoektest: rendert een scene vanaf hoeken waar hij niet voor ontworpen is.

Beikes afkeuring van 15-09-2026: "je tuinen waren niet af — als je een andere
hoek pakte was het ineens heel lelijk." Een scene die alleen klopt vanuit de
hero-camera is een filmdecor, geen tuin. Deze test maakt dat zichtbaar vóór
Beike ernaar hoeft te kijken: een rondje goedkope probe-renders rondom het
product, zodat kale grond, ontbrekende beplanting en props-van-achteren
meteen opvallen.

Draaien (headless):
    blender -b <scene.blend> --python scripts/hoektest.py -- --out <map>

Opties na `--`:
    --out MAP        waar de probes komen (verplicht)
    --count N        aantal hoeken rondom (standaard 12)
    --radius M       afstand tot het middelpunt in meter (standaard 9.0)
    --height M       camerahoogte in meter (standaard 1.65)
    --target X,Y,Z   waar de camera naar kijkt (standaard 0,0,1.2)
    --samples N      Cycles-samples per probe (standaard 24)
    --res BxH        resolutie (standaard 640x360)
"""
import argparse
import sys
from math import cos, pi, sin
from pathlib import Path

import bpy


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="hoektest")
    parser.add_argument("--out", required=True)
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--radius", type=float, default=9.0)
    parser.add_argument("--height", type=float, default=1.65)
    parser.add_argument("--target", default="0,0,1.2")
    parser.add_argument("--samples", type=int, default=24)
    parser.add_argument("--res", default="640x360")
    return parser.parse_args(argv)


def kies_gpu(scene) -> str:
    """Zet Cycles op de GPU. Valt terug op de CPU met een duidelijke melding."""
    prefs = bpy.context.preferences.addons["cycles"].preferences
    for soort in ("OPTIX", "CUDA"):
        prefs.compute_device_type = soort
        prefs.get_devices()
        kaarten = [d for d in prefs.devices if d.type == soort]
        if kaarten:
            for device in prefs.devices:
                device.use = device in kaarten
            scene.cycles.device = "GPU"
            return f"{soort}: {', '.join(d.name for d in kaarten)}"
    scene.cycles.device = "CPU"
    return "CPU (geen OptiX of CUDA gevonden)"


def main() -> None:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    args = parse_args(argv)
    # Absoluut maken: Blender lost een relatief renderpad anders op dan Python,
    # en dan komen de probes op een heel andere schijf terecht.
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    target = tuple(float(deel) for deel in args.target.split(","))
    breedte, hoogte = (int(deel) for deel in args.res.split("x"))

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import cabin_lib as cl

    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    print(f"HOEKTEST rekent op {kies_gpu(scene)}", flush=True)
    scene.cycles.samples = args.samples
    scene.cycles.use_denoising = True
    scene.render.resolution_x = breedte
    scene.render.resolution_y = hoogte
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.image_settings.color_depth = "8"
    scene.render.use_simplify = True
    scene.render.simplify_subdivision_render = 1
    scene.cycles.texture_limit_render = "1024"

    for index in range(args.count):
        graden = 360.0 * index / args.count
        hoek = 2 * pi * index / args.count
        positie = (
            target[0] + args.radius * sin(hoek),
            target[1] + args.radius * cos(hoek),
            args.height,
        )
        cl.add_camera(positie, target, lens=35, shift_y=-0.03, name=f"Hoektest_{graden:03.0f}")
        scene.render.filepath = str(out / f"hoek_{graden:03.0f}.png")
        bpy.ops.render.render(write_still=True)
        print(f"HOEKTEST {graden:03.0f} graden klaar", flush=True)
    print(f"HOEKTEST KLAAR: {args.count} probes in {out}", flush=True)


if __name__ == "__main__":
    main()
