r"""Probe voor clips-v2: hero-camera, cabin-bbox, grond en prop-vignetten IN het hero-beeld -> JSON.
Geen render, geen save.

  blender -b <blend> --python probe_scene.py -- <scene_naam> <uit.json>

Kernidee (Beike 3 sep: "vanuit een bepaalde hoek ziet het er goed uit, op de filmpjes zag je
hoeken waardoor de tuin lelijk leek"): het hero-beeld is het bewezen-goede beeld; elke clip-shot
moet daar binnen blijven. geo.Ctx.frame_score() meet dat.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geo  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
SCENE, UIT = argv[0], argv[1]

ctx = geo.Ctx()
d = ctx.to_json(SCENE)
os.makedirs(os.path.dirname(os.path.abspath(UIT)), exist_ok=True)
with open(UIT, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=1, ensure_ascii=False)
hs = d['hero_score']
print(f"[probe] {SCENE}: cam {d['cam']['loc']} lens {d['cam']['lens']} doel {d['cam']['doel']} cabin {d['cabin']['center']} "
      f"hero ground={hs['ground']} sky={hs['sky']} void={hs['void']} vign={len(d['vignetten'])} deuren={len(d['deuren'])}")
print("[probe] KLAAR")
