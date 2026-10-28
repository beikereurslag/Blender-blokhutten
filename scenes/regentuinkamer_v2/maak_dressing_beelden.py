"""Renders 2.0 - Regentuinkamer v2: dressing-beelden voor de review-site samenstellen (PIL, geen Blender).

  python maak_dressing_beelden.py v1 [laag4-werkversie, bv. v3]

Leest previews\\_werk\\laag4_<v>\\bundel\\ (HeroCam, Cam_Bekken, Cam_Westhoek, Cam_Close_*.png) en
previews\\_werk\\laag4_<v>\\hoektest\\hoek_*.png, en schrijft previews\\dressing\\01..07_*_<v>.png.
Oudere 0[1-7]_*.png in previews\\dressing worden eerst naar previews\\_werk\\dressing_oud\\ verplaatst.
"""
import shutil
import sys
from pathlib import Path

from maak_beelden import contactvel

SCENE_DIR = Path(r"D:\Blender-blokhutten\scenes\regentuinkamer_v2")
NAMEN = {
    "01_heldenbeeld": "HeroCam",
    "02_over_het_bekken": "Cam_Bekken",
    "03_vanuit_westhoek": "Cam_Westhoek",
    "04_bekken_dichtbij": "Cam_Close_Bekken",
    "05_oostborder_dichtbij": "Cam_Close_Oostborder",
    "06_zitplek_onder_kap": "Cam_Close_Zitplek",
}


def main(versie, werkversie=None):
    werk = SCENE_DIR / "previews" / "_werk" / f"laag4_{werkversie or versie}"
    doelmap = SCENE_DIR / "previews" / "dressing"
    bronnen = {naam: werk / "bundel" / f"{cam}.png" for naam, cam in NAMEN.items()}
    bronnen["07_rondom_12_hoeken"] = contactvel(werk)
    ontbreekt = [str(p) for p in bronnen.values() if not p.exists()]
    if ontbreekt:
        raise SystemExit(f"FOUT: ontbreekt: {ontbreekt}")
    doelmap.mkdir(parents=True, exist_ok=True)
    oud = SCENE_DIR / "previews" / "_werk" / "dressing_oud"
    for p in doelmap.glob("0[1-7]_*.png"):
        oud.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p), str(oud / p.name))
    for naam, bron in bronnen.items():
        doel = doelmap / f"{naam}_{versie}.png"
        shutil.copyfile(bron, doel)
        print(f"{doel}  <- {bron.name}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "v1", sys.argv[2] if len(sys.argv) > 2 else None)
