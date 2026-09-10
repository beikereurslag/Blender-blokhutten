r"""Bouwt het reviewblad voor de clips-v2 probe-stills: per scène een contactvel (begin->eind per shot,
met de hero-toets erbij) + een index.html met de oude clip ernaast ter vergelijking.

  python build_review.py            -> _clips_v2_review/index.html + <scene>_sheet.jpg
Draait buiten Blender (cv2 + numpy).
"""
import glob
import html
import json
import os
import sys

import cv2
import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import scenes  # noqa: E402

ROOT = scenes.ROOT
STILLS = os.path.join(HIER, "_probe", "stills")
UIT = os.path.join(ROOT, "_clips_v2_review")
CLIPS_OUD = os.path.join(ROOT, "ALLE_FINALS", "filmpjes")
os.makedirs(UIT, exist_ok=True)

W, H = 640, 360
PAD = 14
FONT = cv2.FONT_HERSHEY_SIMPLEX


def lees(pad):
    img = cv2.imread(pad)
    if img is None:
        return np.full((H, W, 3), 40, np.uint8)
    return cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA)


def tekst(img, t, x, y, schaal=0.55, kleur=(235, 235, 235), dik=1):
    cv2.putText(img, t, (x, y), FONT, schaal, (0, 0, 0), dik + 2, cv2.LINE_AA)
    cv2.putText(img, t, (x, y), FONT, schaal, kleur, dik, cv2.LINE_AA)


def sheet(scene):
    map_ = os.path.join(STILLS, scene)
    scores = sorted(glob.glob(os.path.join(map_, "*_score.json")))
    if not scores:
        return None, []
    rijen = []
    info = []
    for sj in scores:
        d = json.load(open(sj, encoding="utf-8"))
        naam = d["shot"]
        b = lees(os.path.join(map_, f"{naam}_begin.png"))
        e = lees(os.path.join(map_, f"{naam}_eind.png"))
        rij = np.full((H + 2 * PAD + 22, 2 * W + 3 * PAD, 3), 24, np.uint8)
        rij[PAD + 22:PAD + 22 + H, PAD:PAD + W] = b
        rij[PAD + 22:PAD + 22 + H, 2 * PAD + W:2 * PAD + 2 * W] = e
        k0, k1 = d["keys"]
        ok = d["ok"]
        kleur = (120, 220, 120) if ok else (90, 160, 255)
        tekst(rij, f"{naam}  {d['frames']} fr ({d['frames'] / 24:.0f} s)   "
                   f"lens {d['cam'][0]['lens']}->{d['cam'][1]['lens']}   "
                   f"hero-toets: {'OK' if ok else 'LET OP ' + '; '.join(k0['problemen'] + k1['problemen'])}",
              PAD, PAD + 14, 0.5, kleur)
        tekst(rij, f"begin  inside {k0['inside']:.2f} grond {k0['ground']:.2f} lucht {k0['sky']:.2f}", PAD + 6, PAD + 22 + H - 8, 0.45)
        tekst(rij, f"eind   inside {k1['inside']:.2f} grond {k1['ground']:.2f} lucht {k1['sky']:.2f}", 2 * PAD + W + 6, PAD + 22 + H - 8, 0.45)
        rijen.append(rij)
        info.append(dict(naam=naam, ok=ok, frames=d["frames"], problemen=k0["problemen"] + k1["problemen"]))
    kop = np.full((40, rijen[0].shape[1], 3), 24, np.uint8)
    tekst(kop, f"{scene}   -   begin (links) -> eind (rechts) per shot", PAD, 28, 0.7, (255, 255, 255), 2)
    vel = np.vstack([kop] + rijen)
    pad = os.path.join(UITMAP := UIT, f"{scene}_sheet.jpg")
    cv2.imwrite(pad, vel, [cv2.IMWRITE_JPEG_QUALITY, 82])
    return os.path.basename(pad), info


alle = scenes.alle()
kaarten = []
for scene, reg in alle.items():
    vel, info = sheet(scene)
    if not vel:
        continue
    oud = os.path.join(CLIPS_OUD, reg["clip"] + ".mp4")
    oud_rel = os.path.relpath(oud, UIT).replace("\\", "/") if os.path.exists(oud) else None
    status = "alle shots OK" if all(i["ok"] for i in info) else "let op: " + ", ".join(i["naam"] for i in info if not i["ok"])
    kaarten.append(f"""
<section class="scene" id="{scene}">
  <h2>{html.escape(scene)} <span class="{'ok' if all(i['ok'] for i in info) else 'warn'}">{html.escape(status)}</span></h2>
  <div class="row">
    <div class="oud">{('<video src="' + oud_rel + '" controls muted loop preload="metadata"></video><span>oude clip (aug)</span>') if oud_rel else '<span>geen oude clip</span>'}</div>
    <a class="vel" href="{vel}" target="_blank"><img src="{vel}" loading="lazy"></a>
  </div>
</section>""")

pagina = f"""<!doctype html>
<meta charset="utf-8">
<title>Clips v2 — shotreview (hero-kegel)</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ background:#14161a; color:#e8e6e3; font:15px/1.5 system-ui,sans-serif; margin:0; padding:28px 32px 80px; }}
  h1 {{ font-size:21px; margin:0 0 6px; }}
  p.sub {{ color:#9aa0a6; margin:0 0 22px; max-width:1100px; }}
  nav a {{ color:#9cc4ff; margin-right:12px; font-size:13px; }}
  .scene {{ border:1px solid #2c3037; border-radius:10px; padding:16px 20px; margin:22px 0; background:#191c21; }}
  .scene h2 {{ font-size:16px; margin:0 0 12px; }}
  .ok {{ color:#7ad67a; font-weight:normal; font-size:13px; margin-left:10px; }}
  .warn {{ color:#ffb060; font-weight:normal; font-size:13px; margin-left:10px; }}
  .row {{ display:flex; gap:18px; align-items:flex-start; flex-wrap:wrap; }}
  .oud {{ flex:0 0 420px; }}
  .oud video {{ width:420px; border-radius:6px; background:#000; display:block; }}
  .oud span {{ font-size:12px; color:#9aa0a6; }}
  .vel img {{ max-width:min(1000px, 100%); border-radius:6px; display:block; }}
</style>
<h1>Clips v2 — shotreview</h1>
<p class="sub">Elke shot blijft binnen het hero-beeld (de goedgekeurde final). Per shot: begin-still links, eind-still
rechts (960×540, 24 samples — previewkwaliteit). "inside" = deel van het beeld dat ook in het hero-beeld ligt
(1.00 = volledig). Links de oude clip van augustus ter vergelijking. Klik op een contactvel voor groot.</p>
<nav>{' '.join(f'<a href="#{s}">{s}</a>' for s in alle if os.path.exists(os.path.join(UIT, s + "_sheet.jpg")))}</nav>
{''.join(kaarten)}
"""
open(os.path.join(UIT, "index.html"), "w", encoding="utf-8").write(pagina)
print(f"[review] {len(kaarten)} scenes -> {os.path.join(UIT, 'index.html')}")
