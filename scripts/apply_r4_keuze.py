r"""Voer Beikes review van de R4-plankfix-renders door.

Leest de '## Review'-regels van de Werkbank-job 'R4-stijlen' (goed | fix | weg | open) en:
  goed  -> nieuwe render vervangt ALLE_FINALS/blokhutten-stijlen/<scene>.png; de oude gaat naar
           ALLE_FINALS/_pre_plankfix_backup/<scene>.png (bestaat die al, dan <scene>_<datum>.png)
  weg   -> oude blijft staan, niets gebeurt
  fix   -> gemeld met notitie, niets gebeurt
Een regel mag naar het PNG, de CMP_-jpg of de CROP_-jpg verwijzen; '<scene>_ALT-<x>' telt als <scene>.
Standaard dry-run; met --doen wordt er echt gekopieerd/verplaatst. Nooit committen: dat is Beikes stap.

  python scripts/apply_r4_keuze.py [--doen]
"""
import os
import re
import shutil
import sys
from datetime import date

ROOT = r"D:\Blender-blokhutten"
JOB = r"C:\Users\beike\Desktop\Icloud\iCloudDrive\Vault\Claude\Werkbank\jobs\r4-keuze-oud-of-plankfix-per-scene.md"
NIEUW = os.path.join(ROOT, "ALLE_FINALS", "r4-plankfix-2sep")
FINALS = os.path.join(ROOT, "ALLE_FINALS", "blokhutten-stijlen")
BACKUP = os.path.join(ROOT, "ALLE_FINALS", "_pre_plankfix_backup")
R4 = {"camelia_buitenbad", "camelia_wijnterras", "dahlia_leeshoek", "dahlia_tuinkantoor",
      "lavendel_lavendelveld", "lavendel_pluktuin", "lelie_avondkubus", "lelie_ochtendnevel"}
DOEN = "--doen" in sys.argv


def scene_van(naam):
    stem = os.path.splitext(os.path.basename(naam.strip()))[0]
    stem = re.sub(r"^(CMP|CROP)_", "", stem)
    return stem.split("_ALT-")[0], stem


tekst = open(JOB, encoding="utf-8").read()
m = re.search(r"^## Review\s*\n(.*?)(?=^## |\Z)", tekst, flags=re.M | re.S)
regels = [r for r in (m.group(1).splitlines() if m else []) if r.strip().startswith("- ")]
keuzes = {}
for r in regels:
    delen = [d.strip() for d in r.strip()[2:].split("|")]
    if len(delen) < 2:
        continue
    status, naam = delen[0], delen[1]
    notitie = delen[3] if len(delen) > 3 else ""
    scene, stem = scene_van(naam)
    if scene not in R4 or "_PREVIEW" in stem:   # previews van de fixronde zijn geen finals
        continue
    keuzes.setdefault(scene, []).append((status, stem, notitie))

if not keuzes and "--markeer" not in sys.argv:
    print("Geen reviewregels voor de 8 R4-stijlen gevonden in de job; niets te doen.")
    sys.exit(0)

print(("DOEN" if DOEN else "DRY-RUN") + f" - {len(keuzes)} scenes met een keuze\n")
os.makedirs(BACKUP, exist_ok=True)
for scene in sorted(R4):
    lijst = keuzes.get(scene)
    if not lijst:
        print(f"{scene:24s} nog niet beoordeeld")
        continue
    goed = [k for k in lijst if k[0] == "goed"]
    # het reviewblad zet de gekozen kandidaat op goed en de andere kandidaten op weg: dat is één besluit, geen conflict.
    # Alleen goed én weg/fix op DEZELFDE kandidaat is tegenstrijdig.
    goed_stems = {k[1] for k in goed}
    tegenstrijdig = [k for k in lijst if k[0] in ("weg", "fix") and k[1] in goed_stems]
    if goed and tegenstrijdig:
        print(f"{scene:24s} LET OP: tegenstrijdig oordeel op {', '.join(sorted({k[1] for k in tegenstrijdig}))} (goed én {tegenstrijdig[0][0]}) - eerst gelijktrekken, niets gedaan")
        continue
    if len(goed) > 1 and len({k[1] for k in goed}) > 1:
        print(f"{scene:24s} LET OP: {len(goed)} x goed ({', '.join(k[1] for k in goed)}) - kies er een, niets gedaan")
        continue
    if goed:
        stem = goed[0][1]
        bron = os.path.join(NIEUW, stem + ".png")
        doel = os.path.join(FINALS, scene + ".png")
        if not os.path.exists(bron):
            print(f"{scene:24s} goed, maar {bron} ontbreekt")
            continue
        backup = os.path.join(BACKUP, scene + ".png")
        if os.path.exists(backup):
            backup = os.path.join(BACKUP, f"{scene}_{date.today().isoformat()}.png")
        print(f"{scene:24s} goed  <- {stem}.png   (oude -> {os.path.relpath(backup, ROOT)})")
        if DOEN:
            if os.path.exists(doel):
                shutil.move(doel, backup)
            shutil.copy2(bron, doel)
    else:
        for status, stem, notitie in lijst:
            print(f"{scene:24s} {status:5s} {stem}" + (f"   notitie: {notitie}" if notitie else ""))
print("\nKlaar." + ("" if DOEN else " Niets gewijzigd (dry-run); met --doen wordt het uitgevoerd."))

# --- afhandeling: tegels van scènes waarvan de final al vervangen is, op 'klaar' zetten -------------------
import filecmp
import json
import urllib.request

def _markeer(naam, status, notitie):
    d = {"slug": os.path.splitext(os.path.basename(JOB))[0], "naam": naam, "status": status, "notitie": notitie}
    req = urllib.request.Request("http://localhost:8780/api/review", data=json.dumps(d).encode("utf-8"), headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=10).read()

def markeer_klaar(doen):
    """Voor elke scène: staat een kandidaat-PNG nu als final (identiek bestand), dan zijn alle tegels van die scène
    afgehandeld: de gekozen op 'klaar · vervangen', de rest op 'klaar · niet gekozen'. Bestaande notities blijven staan."""
    try:
        items = json.load(urllib.request.urlopen("http://localhost:8780/api/resultaten?job=" + os.path.splitext(os.path.basename(JOB))[0], timeout=10))["items"]
    except Exception as e:
        print("Werkbank niet bereikbaar, tegels niet gemarkeerd:", e); return
    huidig = {i["naam"]: i for i in items}
    for scene in sorted(R4):
        final = os.path.join(FINALS, scene + ".png")
        if not os.path.exists(final):
            continue
        gekozen = None
        for f in os.listdir(NIEUW):
            if f.lower().endswith(".png") and scene_van(f)[0] == scene and "_PREVIEW" not in f and filecmp.cmp(os.path.join(NIEUW, f), final, shallow=False):
                gekozen = os.path.splitext(f)[0]; break
        if not gekozen:
            continue
        for naam, it in huidig.items():
            sc, stem = scene_van(naam)
            if sc != scene or it["status"] == "klaar":
                continue
            basis = (it.get("notitie") or "").split(" · klaar:")[0]
            tekst = f"klaar: vervangen als final ({date.today().isoformat()})" if stem == gekozen else f"klaar: niet gekozen, {gekozen} is de final"
            notitie = (basis + " · " + tekst) if basis else tekst
            print(f"{scene:24s} {naam:44s} -> klaar" + ("" if doen else "  (dry-run)"))
            if doen:
                _markeer(naam, "klaar", notitie)

if __name__ == "__main__":
    markeer_klaar(DOEN or "--markeer" in sys.argv)
