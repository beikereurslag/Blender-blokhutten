"""Pak de laatste tekentool-GLB uit Downloads en zet hem goed weg.

De tekentool downloadt als naamloze .tmp. Dit script pakt de nieuwste .tmp
(of .glb) die echt een glTF is, controleert de magic bytes en verplaatst hem
naar source-glbs-new/<datum>/<naam>.glb.

Gebruik:
    python scripts/pak_export.py "Camelia 250x300"
    python scripts/pak_export.py "Camelia 250x300 + 300 + zijwand"

Zonder argument toont hij alleen wat er klaarstaat.
"""
import json
import os
import re
import shutil
import struct
import sys
from datetime import date

DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")
OUTDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "source-glbs-new", date.today().isoformat())


def is_gltf(path):
    try:
        with open(path, "rb") as f:
            return f.read(4) == b"glTF"
    except OSError:
        return False


def gltf_json(path):
    """Lees de JSON-chunk van een GLB."""
    with open(path, "rb") as f:
        if f.read(4) != b"glTF":
            return None
        struct.unpack("<II", f.read(8))
        clen, _ = struct.unpack("<II", f.read(8))
        return json.loads(f.read(clen))


def keur(path):
    """Controleer of dit de verwachte tekentool-export is.

    De goede export heeft scene-root 'blokhut', staat in meters en heeft een
    handvol materialen. De tool levert soms een heel andere dump (root 'shed',
    honderden materialen, tientallen megabytes) -- die willen we niet.
    """
    js = gltf_json(path)
    if js is None:
        return ["geen geldig GLB (magic bytes kloppen niet)"]
    klachten = []
    roots = [js["nodes"][i].get("name") for i in js["scenes"][js.get("scene", 0)]["nodes"]]
    if "blokhut" not in roots:
        klachten.append(f"scene-root is {roots} in plaats van ['blokhut']")
    n_mat = len(js.get("materials", []))
    if n_mat > 12:
        klachten.append(f"{n_mat} materialen (verwacht een handvol)")
    mb = os.path.getsize(path) / 1e6
    if mb > 8:
        klachten.append(f"{mb:.1f} MB (verwacht ~1,5 MB)")
    return klachten


def nieuwste_export():
    kandidaten = []
    for naam in os.listdir(DOWNLOADS):
        if not naam.lower().endswith((".tmp", ".glb")):
            continue
        pad = os.path.join(DOWNLOADS, naam)
        if os.path.isfile(pad) and is_gltf(pad):
            kandidaten.append((os.path.getmtime(pad), pad))
    if not kandidaten:
        return None
    return max(kandidaten)[1]


def pak_alles():
    """Verplaats alle correct benoemde .glb-exports uit Downloads."""
    os.makedirs(OUTDIR, exist_ok=True)
    gevonden = 0
    for naam in sorted(os.listdir(DOWNLOADS)):
        if not naam.lower().endswith(".glb"):
            continue
        bron = os.path.join(DOWNLOADS, naam)
        if not os.path.isfile(bron) or not is_gltf(bron):
            continue
        gevonden += 1
        klachten = keur(bron)
        # Chrome hangt er " (2)" achter als de naam al bestond -- dat hoort niet
        # bij de modelnaam
        schoon = re.sub(r" \(\d+\)(?=\.glb$)", "", naam)
        doel = os.path.join(OUTDIR, schoon)
        if klachten:
            print(f"AFGEKEURD  {naam}")
            for k in klachten:
                print(f"           - {k}")
            continue
        if os.path.exists(doel):
            print(f"BESTAAT AL {schoon} -- overgeslagen")
            continue
        shutil.move(bron, doel)
        print(f"OK         {schoon}  ({os.path.getsize(doel):,} bytes)")
    if not gevonden:
        print("Geen .glb-exports in", DOWNLOADS)
    return 0


def main():
    if "--alles" in sys.argv:
        return pak_alles()
    bron = nieuwste_export()
    if not bron:
        print("Geen GLB-export gevonden in", DOWNLOADS)
        print("Exporteer eerst in de tekentool (Meer informatie -> Exporteer GLB).")
        return 1

    grootte = os.path.getsize(bron)
    if len(sys.argv) < 2:
        print(f"Klaar om op te pakken: {os.path.basename(bron)} ({grootte:,} bytes)")
        print('Geef een naam mee, bijvoorbeeld:')
        print('  python scripts/pak_export.py "Camelia 250x300"')
        return 0

    naam = sys.argv[1].strip()
    if not naam.lower().endswith(".glb"):
        naam += ".glb"

    os.makedirs(OUTDIR, exist_ok=True)
    doel = os.path.join(OUTDIR, naam)
    if os.path.exists(doel):
        print(f"LET OP: {naam} bestaat al -- niets gedaan.")
        print(f"        Verwijder of hernoem eerst: {doel}")
        return 1

    klachten = keur(bron)
    if klachten and "--forceer" not in sys.argv:
        print(f"AFGEKEURD: {naam}")
        for k in klachten:
            print(f"  - {k}")
        print("  Export opnieuw doen vanuit een verse pagina (F5).")
        print("  Toch bewaren? Voeg --forceer toe.")
        return 1

    shutil.move(bron, doel)
    print(f"OK  {naam}  ({grootte:,} bytes)")
    print(f"    {doel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
