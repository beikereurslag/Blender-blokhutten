r"""Apply the wall-board repair to a scene blend and render it at final quality.

The original blend is never touched: the repaired scene is saved next to it as
<name>_PLANKFIX.blend, and the render goes to the review folder.

  blender.exe -b <scene.blend> --python scripts/apply_plankfix.py -- <out.png> [width] [samples] [height]

Give the height explicitly to match an existing final: the S-series was rendered
at 2560x1920 by _s1_final.py, which overrides whatever the blend has stored.
"""
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fix_cabin_boards as fcb  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
PNG = os.path.abspath(argv[0])
WIDTH = int(argv[1]) if len(argv) > 1 else 2560
SAMPLES = int(argv[2]) if len(argv) > 2 else 512
HEIGHT = int(argv[3]) if len(argv) > 3 else 0

src = bpy.data.filepath


def log(m):
    print(f"[plankfix] {m}", flush=True)


log(f"scene: {src}")
log("--- layout before ---")
fcb.report()

fcb.align_courses()
fcb.plank_groove()

log("--- layout after ---")
fcb.report()

# save the repaired scene beside the original, same folder so relative paths hold
out_blend = os.path.splitext(src)[0] + "_PLANKFIX.blend"
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=out_blend, copy=True)
log(f"saved {out_blend}")

scn = bpy.context.scene
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'
    prefs.get_devices()
    for dv in prefs.devices:
        dv.use = dv.type in ('OPTIX', 'CPU')
    scn.cycles.device = 'GPU'
except Exception as e:
    log(f"gpu: {e}")

scn.render.engine = 'CYCLES'
ratio = scn.render.resolution_y / scn.render.resolution_x   # keep the scene's framing
scn.render.resolution_x = WIDTH
scn.render.resolution_y = HEIGHT if HEIGHT else int(round(WIDTH * ratio))
scn.render.resolution_percentage = 100
scn.cycles.samples = SAMPLES
scn.cycles.use_adaptive_sampling = True
scn.cycles.adaptive_threshold = 0.008
scn.cycles.use_denoising = True
scn.cycles.texture_limit_render = '4096'
scn.render.use_persistent_data = False
scn.render.filepath = PNG
log(f"render {scn.render.resolution_x}x{scn.render.resolution_y} @ {SAMPLES}")
bpy.ops.render.render(write_still=True)
log(f"FINAL -> {PNG}")
log("KLAAR")
