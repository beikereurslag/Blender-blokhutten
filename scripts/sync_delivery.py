#!/usr/bin/env python3
r"""Goedgekeurde finals uit ALLE_FINALS naar de delivery-mappen kopieren.

De mappen D:\Blokhutwinkel-visuals-2026-08-20 en -2026-08 zijn de distributiekopie
(01-blokhutten-stijlen, 02-blokhutten-tuinscenes, ...). Na een fix-ronde lopen die
achter op ALLE_FINALS. Dit script vergelijkt byte-voor-byte en vervangt alleen wat
verschilt; de oude versie gaat eerst naar _pre_plankfix_backup/ in dezelfde map.

    python scripts/sync_delivery.py                 alleen tonen wat er zou gebeuren
    python scripts/sync_delivery.py --doen          uitvoeren
    python scripts/sync_delivery.py --ook-2026-08   ook de oudere snapshot -2026-08 meenemen

Standaard alleen -2026-08-20 (de actuele distributiekopie). De map -2026-08 is de
oudere levering van 14 aug en loopt op alle 23 blokhut-finals achter; die alleen
bijwerken als Beike dat expliciet wil.
"""
import filecmp
import shutil
import sys
from datetime import date
from pathlib import Path

FINALS = Path(r"D:\Blender-blokhutten\ALLE_FINALS")
DELIVERY = [Path(r"D:\Blokhutwinkel-visuals-2026-08-20")]
if "--ook-2026-08" in sys.argv:
    DELIVERY.append(Path(r"D:\Blokhutwinkel-visuals-2026-08"))
# delivery-submap -> bronmap in ALLE_FINALS
PAREN = {
    "01-blokhutten-stijlen": "blokhutten-stijlen",
    "02-blokhutten-tuinscenes": "blokhutten-tuinscenes",
    "03-kapschuren": "kapschuren",
    "04-overkappingen-creatieve-tuinen": "overkappingen-creatieve-tuinen",
    "05-overkappingen-webshop": "overkappingen-webshop",
}
# Niet aanraken: Beikes eigen Zentuin-werk (zie HANDOFF_plankfix.md)
OVERSLAAN = {"roosmarijn_modern.png"}

doen = "--doen" in sys.argv
stempel = date.today().isoformat()
totaal = vervangen = 0

for root in DELIVERY:
    if not root.is_dir():
        print("!! bestaat niet: %s" % root)
        continue
    print("\n== %s" % root)
    backup = root / "_pre_plankfix_backup" / stempel
    for sub, bron_naam in PAREN.items():
        sub_dir = root / sub
        bron_dir = FINALS / bron_naam
        if not sub_dir.is_dir() or not bron_dir.is_dir():
            continue
        for oud in sorted(sub_dir.iterdir()):
            if not oud.is_file():
                continue
            if oud.name in OVERSLAAN:
                continue
            nieuw = bron_dir / oud.name
            if not nieuw.is_file():
                print("   ontbreekt in finals : %s/%s" % (sub, oud.name))
                continue
            totaal += 1
            if filecmp.cmp(oud, nieuw, shallow=False):
                continue
            vervangen += 1
            print("   vervang %s/%s  (%s -> %s)" % (
                sub, oud.name,
                oud.stat().st_mtime.__int__(), nieuw.stat().st_mtime.__int__()))
            if doen:
                doel = backup / sub
                doel.mkdir(parents=True, exist_ok=True)
                shutil.move(str(oud), str(doel / oud.name))
                shutil.copy2(str(nieuw), str(oud))

print("\n%d bestanden vergeleken, %d %s" % (
    totaal, vervangen, "vervangen" if doen else "zouden vervangen worden"))
if not doen and vervangen:
    print("Uitvoeren met: python scripts/sync_delivery.py --doen")
