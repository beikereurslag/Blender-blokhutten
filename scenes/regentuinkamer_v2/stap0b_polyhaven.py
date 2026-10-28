r"""Renders 2.0 - Regentuinkamer v2, stap 0b: PolyHaven-assets voor de dressing (CC0).

  python stap0b_polyhaven.py

- modellen rock_moss_set_01 en rock_moss_set_02 (2k .blend + textures) naar
  assets\polyhaven\models\ (textures in models\textures\, zoals de PH-blend verwacht)
- textuur brown_mud 2k (diff/rough/nor_gl/disp) naar assets\polyhaven\textures\brown_mud\
Waarom: het mosstenen-pack (Sketchfab/Fab) heeft geen licentiebestand; daarom PH-stenen (CC0).
Bestaat een bestand al, dan wordt het overgeslagen (nooit overschrijven). Log: logs\stap0b_polyhaven.json
"""
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(r"D:\Blender-blokhutten")
MODELS = ROOT / "assets" / "polyhaven" / "models"
TEX = ROOT / "assets" / "polyhaven" / "textures"
LOG = ROOT / "scenes" / "regentuinkamer_v2" / "logs" / "stap0b_polyhaven.json"
API = "https://api.polyhaven.com/files/"
HEADERS = {"User-Agent": "Blender-blokhutten renders2"}   # zonder UA: HTTP 403


def openen(url, timeout):
    return urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=timeout)


def get_json(url):
    with openen(url, 30) as r:
        return json.load(r)


def download(url, doel):
    if doel.exists() and doel.stat().st_size > 1000:
        return "al aanwezig"
    doel.parent.mkdir(parents=True, exist_ok=True)
    tmp = doel.with_suffix(doel.suffix + ".part")
    with openen(url, 120) as r, open(tmp, "wb") as f:
        f.write(r.read())
    tmp.rename(doel)
    return "gedownload"


def main():
    uit = []
    for naam in ("rock_moss_set_01", "rock_moss_set_02"):
        b = get_json(API + naam)["blend"]["2k"]["blend"]
        uit.append([naam, download(b["url"], MODELS / Path(b["url"]).name)])
        for rel, info in b["include"].items():
            uit.append([rel, download(info["url"], MODELS / rel)])
    f = get_json(API + "brown_mud")
    for kaart, fmt in (("Diffuse", "jpg"), ("Rough", "jpg"), ("nor_gl", "jpg"), ("Displacement", "jpg")):
        url = f[kaart]["2k"][fmt]["url"]
        uit.append([url, download(url, TEX / "brown_mud" / Path(url).name)])
    LOG.write_text(json.dumps({"licentie": "CC0 (polyhaven.com)", "bestanden": uit}, indent=1), encoding="utf-8")
    for regel in uit:
        print(*regel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
