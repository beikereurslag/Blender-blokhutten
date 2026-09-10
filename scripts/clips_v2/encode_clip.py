r"""PNG-reeksen van een scene-map -> één mp4 met crossfades (Blender 5.1 heeft geen video-uitvoer meer).

  python encode_clip.py <framemap> <uit.mp4> [--fps 24] [--fade 12] [--order A_reveal,B_push,C_detail] [--crf 18]

Shots worden herkend aan <naam>_0001.png; volgorde = alfabetisch op shotnaam (A_, B_, C_) tenzij --order.
Codec: H.264 via PyAV (libx264, yuv420p, crf 18 = visueel verliesvrij, speelt overal incl. Drive/WhatsApp);
valt terug op cv2 mp4v als PyAV ontbreekt.
"""
import argparse
import glob
import os
import re

import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("framemap")
ap.add_argument("uit")
ap.add_argument("--fps", type=int, default=24)
ap.add_argument("--fade", type=int, default=12)
ap.add_argument("--order", default=None)
ap.add_argument("--crf", type=int, default=18)
a = ap.parse_args()

reeksen = {}
for f in glob.glob(os.path.join(a.framemap, "*_[0-9][0-9][0-9][0-9].png")):
    m = re.match(r"^(.*)_(\d{4})\.png$", os.path.basename(f))
    reeksen.setdefault(m.group(1), []).append((int(m.group(2)), f))
if not reeksen:
    raise SystemExit(f"geen frames in {a.framemap}")
volgorde = a.order.split(",") if a.order else sorted(reeksen)
volgorde = [v for v in volgorde if v in reeksen]
for k in volgorde:
    reeksen[k].sort()

eerste = cv2.imread(reeksen[volgorde[0]][0][1])
h, w = eerste.shape[:2]
h -= h % 2
w -= w % 2
os.makedirs(os.path.dirname(os.path.abspath(a.uit)), exist_ok=True)


class AvWriter:
    def __init__(self):
        import av
        self.c = av.open(a.uit, mode="w")
        self.s = self.c.add_stream("libx264", rate=a.fps)
        self.s.width, self.s.height = w, h
        self.s.pix_fmt = "yuv420p"
        self.s.options = {"crf": str(a.crf), "preset": "slow", "movflags": "+faststart"}
        self.av = av

    def write(self, bgr):
        fr = self.av.VideoFrame.from_ndarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB), format="rgb24")
        for pkt in self.s.encode(fr):
            self.c.mux(pkt)

    def release(self):
        for pkt in self.s.encode():
            self.c.mux(pkt)
        self.c.close()


class CvWriter:
    def __init__(self):
        self.w = cv2.VideoWriter(a.uit, cv2.VideoWriter_fourcc(*"mp4v"), a.fps, (w, h))
        if not self.w.isOpened():
            raise SystemExit("geen werkende codec")

    def write(self, bgr):
        self.w.write(bgr)

    def release(self):
        self.w.release()


try:
    writer = AvWriter()
    print("[encode] codec libx264 (PyAV)")
except Exception as e:   # noqa: BLE001
    print(f"[encode] PyAV niet beschikbaar ({e}) -> cv2 mp4v")
    writer = CvWriter()


def lees(pad):
    img = cv2.imread(pad, cv2.IMREAD_COLOR)
    if img.shape[:2] != (h, w):
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
    return img


totaal = 0
vorige_staart = None    # laatste `fade` frames van de vorige shot
for idx, naam in enumerate(volgorde):
    frames = [f for _, f in reeksen[naam]]
    n = len(frames)
    print(f"[encode] {naam}: {n} frames")
    kop = min(len(vorige_staart), n // 2) if vorige_staart else 0
    staart = min(a.fade, n // 2) if idx < len(volgorde) - 1 else 0
    for i, f in enumerate(frames):
        img = lees(f)
        if i < kop:
            t = (i + 1) / (kop + 1)
            img = cv2.addWeighted(vorige_staart[i], 1 - t, img, t, 0)
        if i >= n - staart:
            continue    # staart wordt in de volgende shot gemengd
        writer.write(img)
        totaal += 1
    vorige_staart = [lees(f) for f in frames[n - staart:]] if staart else None
writer.release()
print(f"[encode] {totaal} frames -> {a.uit} ({totaal / a.fps:.1f} s)")
