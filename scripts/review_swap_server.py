#!/usr/bin/env python3
"""Review-server voor de tekentool-swap: oud naast nieuw, per scene goed- of afkeuren.

Start:  python scripts/review_swap_server.py
Daarna: http://localhost:8771

Het oordeel staat in _tekentool_ab/oordeel.json en overleeft een herstart.
De knop "zet goedgekeurde klaar" kopieert de goedgekeurde previews naar
_tekentool_ab/voor_rene/ en schrijft daar RENDERLIJST.txt met de blends die
nog op finalkwaliteit gerenderd moeten worden.
"""

from __future__ import annotations

import json
import shutil
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
SCENES_TXT = ROOT / "scripts" / "scenes.txt"
BEELDEN = ROOT / "_tekentool_ab" / "scenes"
BEELDEN_V2 = ROOT / "_tekentool_ab" / "scenes_v2"
# zoekvolgorde: de nieuwste ronde wint, de vorige blijft de terugval zolang een
# scene nog niet opnieuw gedraaid is
MAPPEN = [BEELDEN_V2, BEELDEN]
OORDEEL = ROOT / "_tekentool_ab" / "oordeel.json"
EXPORT = ROOT / "_tekentool_ab" / "voor_rene"
POORT = 8771


def zoek_beeld(bestandsnaam: str) -> Path | None:
    """Het pad van een render, uit de nieuwste ronde waarin hij voorkomt."""
    for map_ in MAPPEN:
        pad = map_ / bestandsnaam
        if pad.is_file():
            return pad
    return None

GELDIG = {"goed", "afgekeurd", "twijfel"}


def lees_scenes() -> list[dict]:
    """Elke regel van scenes.txt als dict, met wat er aan beelden bestaat."""
    if not SCENES_TXT.exists():
        sys.exit(f"FOUT: {SCENES_TXT} bestaat niet")

    scenes = []
    for regelnr, regel in enumerate(SCENES_TXT.read_text(encoding="utf-8").splitlines(), 1):
        regel = regel.strip()
        if not regel:
            continue
        delen = regel.split("|")
        if len(delen) != 3:
            sys.exit(f"FOUT: regel {regelnr} in scenes.txt heeft {len(delen)} velden, verwacht 3")
        naam, blend, model = delen
        nieuw = zoek_beeld(f"{naam}_NIEUW.png")
        scenes.append({
            "naam": naam,
            "blend": blend,
            "model": model,
            "oud": zoek_beeld(f"{naam}_OUD.png") is not None,
            "nieuw": nieuw is not None,
            "ronde": "2" if nieuw and nieuw.parent == BEELDEN_V2 else "1",
        })
    return scenes


def lees_oordeel() -> dict:
    if not OORDEEL.exists():
        return {}
    try:
        return json.loads(OORDEEL.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"FOUT: {OORDEEL} is geen geldige JSON ({e}). Verwijder of repareer het bestand.")


def schrijf_oordeel(data: dict) -> None:
    OORDEEL.parent.mkdir(parents=True, exist_ok=True)
    OORDEEL.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def exporteer(scenes: list[dict], oordeel: dict) -> dict:
    """Kopieer de goedgekeurde previews naar voor_rene/ en noteer wat er nog moet renderen."""
    goed = [s for s in scenes if oordeel.get(s["naam"]) == "goed"]
    if not goed:
        return {"aantal": 0, "map": str(EXPORT), "melding": "Nog niets goedgekeurd."}

    EXPORT.mkdir(parents=True, exist_ok=True)
    gekopieerd = []
    for s in goed:
        bron = BEELDEN / f"{s['naam']}_NIEUW.png"
        if not bron.exists():
            continue
        shutil.copy2(bron, EXPORT / f"{s['naam']}.png")
        gekopieerd.append(s)

    regels = [
        "Goedgekeurde scenes die nog op finalkwaliteit gerenderd moeten worden.",
        "De PNG's in deze map zijn reviewrenders: 1280 breed, 128 samples.",
        "",
    ]
    regels += [f"{s['naam']}|{BEELDEN.name}/{s['naam']}_NIEUW.blend|{s['model']}" for s in gekopieerd]
    (EXPORT / "RENDERLIJST.txt").write_text("\n".join(regels) + "\n", encoding="utf-8")

    return {"aantal": len(gekopieerd), "map": str(EXPORT), "melding": ""}


def bouw_html(scenes: list[dict], oordeel: dict) -> str:
    beoordeeld = sum(1 for s in scenes if s["naam"] in oordeel)
    goed = sum(1 for s in scenes if oordeel.get(s["naam"]) == "goed")

    secties = []
    for s in scenes:
        naam = s["naam"]
        keuze = oordeel.get(naam, "")
        label = naam.replace("_", " ")

        if s["oud"]:
            oud_fig = f'<figure><img src="/img/{naam}_OUD.png" loading="lazy"><figcaption>oud &mdash; plank 150 mm</figcaption></figure>'
        else:
            oud_fig = '<figure class="mist">oude render ontbreekt</figure>'

        if s["nieuw"]:
            bij = ("nieuw &mdash; ronde 2, fundering behouden" if s["ronde"] == "2"
                   else "nieuw &mdash; <b>ronde 1, nog zonder fundering</b>")
            nieuw_fig = f'<figure><img src="/img/{naam}_NIEUW.png" loading="lazy"><figcaption>{bij}</figcaption></figure>'
        else:
            nieuw_fig = '<figure class="mist">nieuwe render ontbreekt</figure>'

        knoppen = "".join(
            f'<button class="k {w}{" aan" if keuze == w else ""}" '
            f'data-scene="{naam}" data-waarde="{w}">{t}</button>'
            for w, t in (("goed", "Goed als final"), ("twijfel", "Twijfel"), ("afgekeurd", "Afgekeurd"))
        )

        secties.append(f"""
  <section id="{naam}" data-scene="{naam}" class="scene {keuze}">
    <div class="kop"><h2>{label}</h2><span class="model">{s["model"]}</span></div>
    <div class="paar">{oud_fig}{nieuw_fig}</div>
    <div class="knoppen">{knoppen}<span class="stand">{keuze or "nog niet beoordeeld"}</span></div>
  </section>""")

    nav = "".join(
        f'<a href="#{s["naam"]}" class="{oordeel.get(s["naam"], "")}">{s["naam"].replace("_", " ")}</a>'
        for s in scenes
    )

    return f"""<!doctype html>
<meta charset="utf-8">
<title>Tekentool-swap &mdash; beoordelen</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ margin:0; background:#141414; color:#e8e8e8;
         font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif; }}
  header {{ position:sticky; top:0; background:#1c1c1c; padding:14px 20px;
           border-bottom:1px solid #2e2e2e; z-index:3;
           display:flex; align-items:center; gap:20px; flex-wrap:wrap; }}
  h1 {{ margin:0; font-size:17px; font-weight:600; }}
  .meta {{ color:#9a9a9a; font-size:13px; }}
  .teller {{ color:#b9d98a; font-size:13px; font-variant-numeric:tabular-nums; }}
  #export {{ margin-left:auto; background:#2f4f22; color:#dff0c8; border:1px solid #4a7136;
            border-radius:6px; padding:7px 14px; font-size:13px; cursor:pointer; }}
  #export:hover {{ background:#3a6029; }}
  #melding {{ padding:8px 20px; background:#20281a; color:#cfe6b4; font-size:13px; display:none; }}
  nav {{ display:flex; flex-wrap:wrap; gap:6px; padding:12px 20px; background:#181818; }}
  nav a {{ color:#9a9a9a; text-decoration:none; font-size:12px;
          border:1px solid #333; border-radius:11px; padding:2px 9px; }}
  nav a.goed {{ color:#b9d98a; border-color:#4a7136; }}
  nav a.afgekeurd {{ color:#e09a9a; border-color:#7a3d3d; }}
  nav a.twijfel {{ color:#e0c88a; border-color:#7a6a3d; }}
  section {{ padding:20px; border-bottom:1px solid #262626; border-left:4px solid transparent; }}
  section.goed {{ border-left-color:#4a7136; }}
  section.afgekeurd {{ border-left-color:#7a3d3d; }}
  section.twijfel {{ border-left-color:#7a6a3d; }}
  .kop {{ display:flex; align-items:baseline; gap:12px; margin-bottom:12px; }}
  h2 {{ margin:0; font-size:15px; font-weight:600; text-transform:capitalize; }}
  .model {{ color:#8f8f8f; font-size:12px; }}
  .paar {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; }}
  figure {{ margin:0; }}
  figure.mist {{ background:#1e1e1e; border:1px dashed #3a3a3a; border-radius:5px;
                color:#8f8f8f; font-size:13px; display:grid; place-items:center; min-height:200px; }}
  img {{ width:100%; display:block; border-radius:5px; background:#000; cursor:zoom-in; }}
  figcaption {{ color:#8f8f8f; font-size:12px; padding-top:5px; }}
  .knoppen {{ display:flex; gap:8px; align-items:center; padding-top:12px; }}
  .k {{ background:#232323; color:#c8c8c8; border:1px solid #383838; border-radius:6px;
       padding:6px 13px; font-size:13px; cursor:pointer; }}
  .k:hover {{ background:#2c2c2c; }}
  .k.goed.aan {{ background:#2f4f22; color:#dff0c8; border-color:#4a7136; }}
  .k.afgekeurd.aan {{ background:#4f2222; color:#f0c8c8; border-color:#713636; }}
  .k.twijfel.aan {{ background:#4f4322; color:#f0e3c8; border-color:#716136; }}
  .stand {{ color:#8f8f8f; font-size:12px; }}
  #groot {{ position:fixed; inset:0; background:#000d; z-index:9; display:none;
           place-items:center; cursor:zoom-out; }}
  #groot img {{ max-width:96vw; max-height:96vh; width:auto; border-radius:4px; }}
  @media (max-width:900px) {{ .paar {{ grid-template-columns:1fr; }} }}
</style>
<header>
  <div>
    <h1>Tekentool-swap &mdash; oud vs nieuw</h1>
    <div class="meta">{len(scenes)} scenes &middot; reviewrenders 1280 breed, 128 samples, identiek voor beide</div>
  </div>
  <div class="teller"><span id="beoordeeld">{beoordeeld}</span>/{len(scenes)} beoordeeld &middot;
       <span id="goed">{goed}</span> goedgekeurd</div>
  <button id="export">Zet goedgekeurde klaar</button>
</header>
<div id="melding"></div>
<nav>{nav}</nav>
{"".join(secties)}
<div id="groot"><img></div>
<script>
const totaal = {len(scenes)};

document.querySelectorAll(".k").forEach(knop => {{
  knop.addEventListener("click", async () => {{
    const scene = knop.dataset.scene;
    const sectie = document.getElementById(scene);
    const huidig = sectie.classList.contains(knop.dataset.waarde);
    const waarde = huidig ? "" : knop.dataset.waarde;

    const res = await fetch("/oordeel", {{
      method: "POST",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify({{ scene, waarde }})
    }});
    if (!res.ok) {{ toon("Opslaan mislukt: " + await res.text()); return; }}
    const data = await res.json();

    sectie.classList.remove("goed", "afgekeurd", "twijfel");
    if (waarde) sectie.classList.add(waarde);
    sectie.querySelectorAll(".k").forEach(k => k.classList.toggle("aan", k.dataset.waarde === waarde));
    sectie.querySelector(".stand").textContent = waarde || "nog niet beoordeeld";

    const link = document.querySelector(`nav a[href="#${{scene}}"]`);
    link.className = waarde;
    document.getElementById("beoordeeld").textContent = data.beoordeeld;
    document.getElementById("goed").textContent = data.goed;
  }});
}});

document.querySelectorAll("section img").forEach(img => {{
  img.addEventListener("click", () => {{
    const laag = document.getElementById("groot");
    laag.querySelector("img").src = img.src;
    laag.style.display = "grid";
  }});
}});
document.getElementById("groot").addEventListener("click", e => e.currentTarget.style.display = "none");
document.addEventListener("keydown", e => {{
  if (e.key === "Escape") document.getElementById("groot").style.display = "none";
}});

document.getElementById("export").addEventListener("click", async () => {{
  const res = await fetch("/export", {{ method: "POST" }});
  if (!res.ok) {{ toon("Export mislukt: " + await res.text()); return; }}
  const data = await res.json();
  toon(data.melding || `${{data.aantal}} beelden staan in ${{data.map}} (met RENDERLIJST.txt).`);
}});

function toon(tekst) {{
  const el = document.getElementById("melding");
  el.textContent = tekst;
  el.style.display = "block";
}}
</script>
"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # stil, behalve fouten
        pass

    def _stuur(self, code: int, inhoud: bytes, type_: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", type_)
        self.send_header("Content-Length", str(len(inhoud)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(inhoud)

    def _json(self, data: dict) -> None:
        self._stuur(200, json.dumps(data).encode("utf-8"), "application/json")

    def _fout(self, code: int, tekst: str) -> None:
        self._stuur(code, tekst.encode("utf-8"), "text/plain; charset=utf-8")

    def do_GET(self):
        pad = unquote(urlparse(self.path).path)

        if pad in ("/", "/index.html"):
            html = bouw_html(lees_scenes(), lees_oordeel())
            self._stuur(200, html.encode("utf-8"), "text/html; charset=utf-8")
            return

        if pad.startswith("/img/"):
            naam = Path(pad[len("/img/"):]).name  # geen mapstappen omhoog
            bestand = zoek_beeld(naam) if naam.lower().endswith(".png") else None
            if bestand is None:
                self._fout(404, f"niet gevonden: {naam}")
                return
            self._stuur(200, bestand.read_bytes(), "image/png")
            return

        self._fout(404, f"onbekend pad: {pad}")

    def do_POST(self):
        pad = urlparse(self.path).path

        if pad == "/export":
            scenes = lees_scenes()
            self._json(exporteer(scenes, lees_oordeel()))
            return

        if pad != "/oordeel":
            self._fout(404, f"onbekend pad: {pad}")
            return

        lengte = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(lengte).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            self._fout(400, f"onleesbare aanvraag: {e}")
            return

        scene = data.get("scene")
        waarde = data.get("waarde", "")
        namen = {s["naam"] for s in lees_scenes()}
        if scene not in namen:
            self._fout(400, f"onbekende scene: {scene}")
            return
        if waarde and waarde not in GELDIG:
            self._fout(400, f"ongeldig oordeel: {waarde}")
            return

        oordeel = lees_oordeel()
        if waarde:
            oordeel[scene] = waarde
        else:
            oordeel.pop(scene, None)
        schrijf_oordeel(oordeel)

        self._json({
            "beoordeeld": len(oordeel),
            "goed": sum(1 for v in oordeel.values() if v == "goed"),
        })


def main() -> None:
    scenes = lees_scenes()
    zonder_nieuw = [s["naam"] for s in scenes if not s["nieuw"]]

    print(f"{len(scenes)} scenes uit {SCENES_TXT.name}")
    if zonder_nieuw:
        print(f"LET OP: {len(zonder_nieuw)} zonder nieuwe render: {', '.join(zonder_nieuw)}")
    print(f"Oordeel wordt bewaard in {OORDEEL}")
    print(f"\n  http://localhost:{POORT}\n")

    try:
        ThreadingHTTPServer(("127.0.0.1", POORT), Handler).serve_forever()
    except OSError as e:
        sys.exit(f"FOUT: kan niet luisteren op poort {POORT} ({e}). Draait er al een server?")
    except KeyboardInterrupt:
        print("gestopt")


if __name__ == "__main__":
    main()
