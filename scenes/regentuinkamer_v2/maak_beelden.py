"""Renders 2.0 - Regentuinkamer v2: beelden voor de review-site samenstellen (PIL, geen Blender).

  python maak_beelden.py v1

Leest previews\\_werk\\anker_<v>\\ (HeroCam.png, Cam_Bekken.png, Cam_Westhoek.png,
Cam_Haagproef.png, hoektest\\hoek_*.png) en schrijft:
  _werk\\anker_<v>\\haagproef_naast_referentie.png en hoektest_contactvel.png
  previews\\anker\\01..05_*_<v>.png  (oudere versies daar worden verwijderd; die staan in _werk)
"""
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw

SCENE_DIR = Path(r"D:\Blender-blokhutten\scenes\regentuinkamer_v2")
REFERENTIE = Path(r"D:\Blender-blokhutten\pilots\ai_omgeving_2026-10\contactvel.png")


def label(img, tekst):
    d = ImageDraw.Draw(img)
    w = 8 + 7 * len(tekst)
    d.rectangle([0, 0, w, 22], fill=(0, 0, 0))
    d.text((5, 4), tekst, fill=(255, 255, 255))
    return img


def haagproef(werk):
    ref = Image.open(REFERENTIE).convert("RGB")
    kolom = ref.width // 3
    rij = round(kolom * 9 / 16)                      # bovenrij = 16:9-beelden
    ref = ref.crop((2 * kolom, 0, 3 * kolom, rij)).resize((960, 540), Image.LANCZOS)
    eigen = Image.open(werk / "Cam_Haagproef.png").convert("RGB").resize((960, 540), Image.LANCZOS)
    uit = Image.new("RGB", (1920 + 8, 540), (20, 20, 20))
    uit.paste(label(ref, "referentie: AI-beeld nieuw (A_2611)"), (0, 0))
    uit.paste(label(eigen, "Blender: rughaag op ~6 m (Cotoneaster-module)"), (968, 0))
    pad = werk / "haagproef_naast_referentie.png"
    uit.save(pad)
    return pad


def contactvel(werk):
    beelden = sorted((werk / "hoektest").glob("hoek_*.png"))
    if len(beelden) != 12:
        raise SystemExit(f"FOUT: verwacht 12 hoektest-beelden in {werk / 'hoektest'}, gevonden {len(beelden)}")
    tw, th = 480, 270
    uit = Image.new("RGB", (4 * tw + 3 * 6, 3 * th + 2 * 6), (20, 20, 20))
    for i, p in enumerate(beelden):
        im = Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS)
        label(im, p.stem.replace("hoek_", "hoek ") + " gr")
        uit.paste(im, ((i % 4) * (tw + 6), (i // 4) * (th + 6)))
    pad = werk / "hoektest_contactvel.png"
    uit.save(pad)
    return pad


def main(versie, alleen_werk=False):
    werk = SCENE_DIR / "previews" / "_werk" / f"anker_{versie}"
    anker = SCENE_DIR / "previews" / "anker"
    anker.mkdir(parents=True, exist_ok=True)
    bronnen = {
        "01_heldenbeeld": werk / "HeroCam.png",
        "02_over_het_bekken": werk / "Cam_Bekken.png",
        "03_vanuit_westhoek": werk / "Cam_Westhoek.png",
        "04_haagproef_naast_referentie": haagproef(werk),
        "05_rondom_12_hoeken": contactvel(werk),
    }
    for p in bronnen.values():
        if not p.exists():
            raise SystemExit(f"FOUT: {p} ontbreekt")
    if alleen_werk:          # versie nog niet voor de review-site
        for naam, bron in bronnen.items():
            print(f"{bron}  ({naam}, alleen in _werk)")
        return
    for oud in anker.glob("0[1-5]_*.png"):
        oud.unlink()                                 # alleen de laatste versie op de review-site
    for naam, bron in bronnen.items():
        doel = anker / f"{naam}_{versie}.png"
        shutil.copyfile(bron, doel)
        print(f"{doel}  <- {bron.name}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "v1", alleen_werk="--alleen-werk" in sys.argv)
