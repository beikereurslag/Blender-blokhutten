"""Contactvel van de omgezette tekentool-scenes, plus een hoektest-vel per scene.

Leest _tekentool_2026-10/<naam>/controle.json. Alleen scenes met "omgezet": true
komen op het contactvel, in de volgorde van scripts/scenes.txt. Het beeld zelf
bevat geen tekst (Beikes regel); welke scene waar staat, staat in de legenda
ernaast.

    python scripts/maak_contactvel.py            # contactvel + legenda
    python scripts/maak_contactvel.py --hoeken   # ook per scene een hoektest-vel

Uitvoer: docs/verslagen/tekentool_2026-10/contactvel.png en legenda.md.
"""
import argparse
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
WERK = ROOT / "_tekentool_2026-10"
DOEL = ROOT / "docs" / "verslagen" / "tekentool_2026-10"
BREEDTE = 1800          # Beike: voorbeelden in het gesprek hooguit 1800 px breed
KOLOMMEN = 3
MARGE = 6
ACHTERGROND = (24, 24, 24)


def scenes_in_volgorde() -> list[str]:
    regels = (ROOT / "scripts" / "scenes.txt").read_text(encoding="utf-8").splitlines()
    return [r.split("|")[0] for r in regels if r.strip()]


def lees_controle(naam: str) -> dict | None:
    pad = WERK / naam / "controle.json"
    if not pad.is_file():
        return None
    return json.loads(pad.read_text(encoding="utf-8"))


def raster(beelden: list[Path], kolommen: int, breedte: int) -> Image.Image:
    tegel_b = (breedte - MARGE * (kolommen + 1)) // kolommen
    tegel_h = round(tegel_b * 9 / 16)
    rijen = -(-len(beelden) // kolommen)
    vel = Image.new("RGB", (breedte, rijen * tegel_h + (rijen + 1) * MARGE), ACHTERGROND)
    for i, pad in enumerate(beelden):
        with Image.open(pad) as im:
            tegel = im.convert("RGB").resize((tegel_b, tegel_h), Image.LANCZOS)
        r, k = divmod(i, kolommen)
        vel.paste(tegel, (MARGE + k * (tegel_b + MARGE), MARGE + r * (tegel_h + MARGE)))
    return vel


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hoeken", action="store_true", help="ook per scene een hoektest-vel")
    args = ap.parse_args()
    DOEL.mkdir(parents=True, exist_ok=True)

    omgezet, niet, ontbreekt = [], [], []
    for naam in scenes_in_volgorde():
        c = lees_controle(naam)
        if c is None:
            ontbreekt.append(naam)
        elif c["omgezet"] and (WERK / naam / "hero_1080.png").is_file():
            omgezet.append(naam)
        else:
            niet.append((naam, c.get("fouten", [])))

        if args.hoeken and c is not None:
            probes = sorted((WERK / naam).glob("hoek_*.png"))
            if probes:
                raster(probes, 4, 1600).save(WERK / naam / "hoeken_vel.png")

    if omgezet:
        vel = raster([WERK / n / "hero_1080.png" for n in omgezet], KOLOMMEN, BREEDTE)
        vel.save(DOEL / "contactvel.png", optimize=True)

    regels = ["# Contactvel tekentool-swap (okt 2026)", "",
              f"Proefrenders 1920x1080 / 256 samples met de hero-camera, {KOLOMMEN} per rij, "
              "van links naar rechts gelezen.", ""]
    for i, naam in enumerate(omgezet):
        r, k = divmod(i, KOLOMMEN)
        regels.append(f"{i + 1}. rij {r + 1}, plek {k + 1}: `{naam}`")
    if niet:
        regels += ["", "## Niet omgezet", ""]
        for naam, fouten in niet:
            regels.append(f"- `{naam}`: " + "; ".join(fouten))
    if ontbreekt:
        regels += ["", "## Nog niet gedraaid", ""] + [f"- `{n}`" for n in ontbreekt]
    (DOEL / "legenda.md").write_text("\n".join(regels) + "\n", encoding="utf-8")

    print(f"omgezet {len(omgezet)}, niet omgezet {len(niet)}, nog niet gedraaid {len(ontbreekt)}")
    print(f"contactvel: {DOEL / 'contactvel.png'}" if omgezet else "geen contactvel: nog niets omgezet")


if __name__ == "__main__":
    sys.exit(main())
