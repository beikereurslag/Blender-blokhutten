"""Her-render een R4-preview van een (door Beike bewerkte) _R4.blend.
Gebruik: blender.exe -b <blend> --python render_r4_preview.py -- <out.png>
Respecteert de scene-instellingen (AgX zit in de blend), forceert alleen
diag-formaat + abspath-output (les: relatieve paden zijn onbetrouwbaar)."""
import os
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
out = os.path.abspath(argv[0])
scn = bpy.context.scene
scn.render.resolution_x, scn.render.resolution_y = 1280, 960
scn.render.resolution_percentage = 100
scn.cycles.samples = 64
scn.cycles.texture_limit_render = '2048'
scn.render.filepath = out
bpy.ops.render.render(write_still=True)
print(f"[prev] KLAAR {out}")
