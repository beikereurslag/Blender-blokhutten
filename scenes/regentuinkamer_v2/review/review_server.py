"""Lokale review-server voor Renders 2.0, pilot De Regentuinkamer.
Kopie van overkappingen-website/review_server.py (die blijft ongewijzigd); alleen
de beeldbron, de titel en de poort zijn anders.
Beike vinkt per beeld aan: HOUDEN (mee door) of WEG (mag weg), optioneel met notitie.
Keuzes worden live opgeslagen in review_keuzes.json (naast dit script).

Beelden komen uit ../previews/<fase>/*.png; een nieuwe fase = een nieuwe map in FASES.

Run:  python review_server.py   ->  http://localhost:8767
"""
import io
import json
import os
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PREVIEWS = os.path.join(os.path.dirname(HERE), "previews")
THUMBS = os.path.join(HERE, "_review_thumbs")
KEUZES = os.path.join(HERE, "review_keuzes.json")
os.makedirs(THUMBS, exist_ok=True)

_lock = threading.Lock()


def veilige_naam(fn):
    return re.match(r"^[A-Za-z0-9._-]+\.png$", fn) is not None


# (map onder previews/, sectiekop) — bovenaan staat wat nu beoordeeld moet worden.
FASES = [("dressing", "② Dressing (tuin aankleden)"),
         ("anker", "① Anker: hut, grond, pad, haag, bomen, licht")]


def beelden():
    """(sectie, naam, pad) per preview. De naam krijgt de fase als voorvoegsel
    ("anker--x.png"), zodat dezelfde bestandsnaam in twee fases niet botst."""
    out = []
    for map_naam, sectie in FASES:
        map_pad = os.path.join(PREVIEWS, map_naam)
        if not os.path.isdir(map_pad):
            continue
        for fn in sorted(os.listdir(map_pad)):
            if fn.lower().endswith(".png") and veilige_naam(fn):
                out.append((sectie, f"{map_naam}--{fn}", os.path.join(map_pad, fn)))
    return out


def pad_van(naam):
    for _, fn, pad in beelden():
        if fn == naam:
            return pad
    return None


def laad_keuzes():
    with _lock:
        if os.path.exists(KEUZES):
            with open(KEUZES, "r", encoding="utf-8") as f:
                return json.load(f)
    return {}


def bewaar_keuze(naam, keuze, notitie):
    with _lock:
        data = {}
        if os.path.exists(KEUZES):
            with open(KEUZES, "r", encoding="utf-8") as f:
                data = json.load(f)
        data[naam] = {"keuze": keuze, "notitie": notitie}
        with open(KEUZES, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=1, ensure_ascii=False)


def thumb(pad, naam, maxw=1200):
    cache = os.path.join(THUMBS, naam + ".jpg")
    if os.path.exists(cache) and os.path.getmtime(cache) >= os.path.getmtime(pad):
        with open(cache, "rb") as f:
            return f.read()
    im = Image.open(pad)
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)))
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "JPEG", quality=84)
    data = buf.getvalue()
    with open(cache, "wb") as f:
        f.write(data)
    return data


PAGINA = """<!doctype html><html><head><meta charset="utf-8">
<title>Regentuinkamer 2.0 — review</title>
<style>
body{background:#16181c;color:#ddd;font-family:system-ui;margin:0;padding:1.2rem 2rem 4rem}
h1{font-size:1.25rem} h2{font-size:1.05rem;color:#aac;margin-top:2.2rem;
border-bottom:1px solid #333;padding-bottom:.3rem}
#balk{position:sticky;top:0;background:#16181cee;padding:.6rem 0;z-index:5;
display:flex;gap:1rem;align-items:center;flex-wrap:wrap}
#balk .f{background:#242830;border:1px solid #444;color:#ccc;border-radius:6px;
padding:.35rem .8rem;cursor:pointer}
#balk .f.aan{background:#3a4560;border-color:#7af;color:#fff}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(430px,1fr));gap:1.1rem}
.kaart{background:#1d2026;border:3px solid #333;border-radius:10px;padding:.6rem;
transition:border-color .15s}
.kaart.houden{border-color:#39b54a}.kaart.weg{border-color:#d33}
.kaart h3{font-size:.82rem;font-weight:600;margin:.1rem 0 .45rem;word-break:break-all}
.kaart img{width:100%;border-radius:6px;display:block;cursor:zoom-in;background:#111;
min-height:180px}
.knoppen{display:flex;gap:.5rem;margin-top:.55rem}
.knoppen button{flex:1;padding:.45rem;border-radius:6px;border:1px solid #444;
background:#242830;color:#ccc;cursor:pointer;font-size:.85rem}
.knoppen button.h.actief{background:#1f7a2d;border-color:#39b54a;color:#fff}
.knoppen button.w.actief{background:#8a1f1f;border-color:#d33;color:#fff}
.kaart input{width:100%;box-sizing:border-box;margin-top:.45rem;background:#14161a;
border:1px solid #333;border-radius:6px;color:#ddd;padding:.4rem .5rem;font-size:.8rem}
#tel{color:#8fa;font-size:.9rem}
#groot{position:fixed;inset:0;background:#000d;display:none;z-index:20;cursor:zoom-out;
align-items:center;justify-content:center}
#groot img{max-width:97vw;max-height:97vh}
</style></head><body>
<h1>De Regentuinkamer 2.0 — scène opnieuw gebouwd (Renders 2.0)</h1>
<div id="balk">
 <span id="tel"></span>
 <button class="f aan" data-f="alles">Alles</button>
 <button class="f" data-f="open">Nog te beoordelen</button>
 <button class="f" data-f="houden">Houden</button>
 <button class="f" data-f="weg">Weg</button>
 <span style="color:#888;font-size:.8rem">Klik op een beeld voor groot; keuzes worden direct opgeslagen.</span>
</div>
<div id="inhoud"></div>
<div id="groot" onclick="this.style.display='none'"><img id="grootimg"></div>
<script>
let STATE = {}, ITEMS = [], FILTER = 'alles';
async function init(){
  const r = await fetch('/data'); const d = await r.json();
  STATE = d.keuzes; ITEMS = d.items; render();
}
function telling(){
  const tot = ITEMS.length;
  let h=0,w=0; for(const it of ITEMS){ const k=(STATE[it.naam]||{}).keuze;
    if(k==='houden')h++; else if(k==='weg')w++; }
  document.getElementById('tel').textContent =
    `${tot} beelden — ${h} houden · ${w} weg · ${tot-h-w} open`;
}
function render(){
  const c = document.getElementById('inhoud'); c.innerHTML='';
  telling();
  const secties = [...new Set(ITEMS.map(i=>i.sectie))];
  for(const s of secties){
    const its = ITEMS.filter(i=>i.sectie===s).filter(i=>{
      const k=(STATE[i.naam]||{}).keuze;
      if(FILTER==='alles') return true;
      if(FILTER==='open') return !k;
      return k===FILTER;
    });
    if(!its.length) continue;
    const h2 = document.createElement('h2'); h2.textContent = s; c.appendChild(h2);
    const g = document.createElement('div'); g.className='grid'; c.appendChild(g);
    for(const it of its){
      const st = STATE[it.naam]||{};
      const k = document.createElement('div');
      k.className = 'kaart ' + (st.keuze||'');
      k.innerHTML = `<h3>${it.naam.replace('--',' · ').replace('.png','')}</h3>
        <img loading="lazy" src="/thumb/${it.naam}?v=${it.v||0}" onclick="groot('${it.naam}',${it.v||0})">
        <div class="knoppen">
          <button class="h ${st.keuze==='houden'?'actief':''}" onclick="kies('${it.naam}','houden',this)">✔ Houden / mee door</button>
          <button class="w ${st.keuze==='weg'?'actief':''}" onclick="kies('${it.naam}','weg',this)">✘ Mag weg</button>
        </div>
        <input placeholder="notitie (optioneel)" value="${(st.notitie||'').replace(/"/g,'&quot;')}"
          onchange="notitie('${it.naam}',this.value)">`;
      g.appendChild(k);
    }
  }
}
function groot(n, v){
  document.getElementById('grootimg').src = '/full/'+n+'?v='+(v||0);
  document.getElementById('groot').style.display='flex';
}
async function kies(n, keuze, el){
  const st = STATE[n]||{};
  st.keuze = (st.keuze===keuze) ? null : keuze;   // nogmaals klikken = ongedaan
  STATE[n]=st;
  await fetch('/save', {method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({naam:n, keuze:st.keuze, notitie:st.notitie||''})});
  render();
}
async function notitie(n, v){
  const st = STATE[n]||{}; st.notitie=v; STATE[n]=st;
  await fetch('/save', {method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({naam:n, keuze:st.keuze||null, notitie:v})});
  telling();
}
document.querySelectorAll('#balk .f').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('#balk .f').forEach(x=>x.classList.remove('aan'));
  b.classList.add('aan'); FILTER=b.dataset.f; render();
});
init();
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="text/html; charset=utf-8", nocache=False):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        if nocache:
            # verse renders overschrijven dezelfde bestandsnaam — browser mag
            # beelden nooit uit cache tonen (Beike zag oude thumbnails, 8 jul)
            self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self._send(200, PAGINA.encode("utf-8"))
        elif self.path == "/data":
            items = [{"sectie": s, "naam": n, "v": int(os.path.getmtime(p))}
                     for s, n, p in beelden()]
            body = json.dumps({"items": items, "keuzes": laad_keuzes()}).encode("utf-8")
            self._send(200, body, "application/json", nocache=True)
        elif self.path.startswith("/thumb/") or self.path.startswith("/full/"):
            naam = self.path.split("/", 2)[2].split("?", 1)[0]
            pad = pad_van(naam)
            if not pad:
                self._send(404, b"niet gevonden", "text/plain")
                return
            if self.path.startswith("/thumb/"):
                try:
                    self._send(200, thumb(pad, naam), "image/jpeg", nocache=True)
                except Exception as e:
                    self._send(500, str(e).encode(), "text/plain")
            else:
                with open(pad, "rb") as f:
                    self._send(200, f.read(), "image/png", nocache=True)
        else:
            self._send(404, b"?", "text/plain")

    def do_POST(self):
        if self.path != "/save":
            self._send(404, b"?", "text/plain")
            return
        # alleen de eigen reviewpagina mag keuzes opslaan, geen andere website in dezelfde browser
        origin = self.headers.get("Origin")
        if origin and origin not in ("http://localhost:8767", "http://127.0.0.1:8767"):
            self._send(403, b"verkeerde herkomst", "text/plain")
            return
        ln = int(self.headers.get("Content-Length", 0))
        d = json.loads(self.rfile.read(ln))
        naam = d.get("naam", "")
        if pad_van(naam) is None:
            self._send(400, b"naam?", "text/plain")
            return
        bewaar_keuze(naam, d.get("keuze"), d.get("notitie", ""))
        self._send(200, b"ok", "text/plain")


if __name__ == "__main__":
    srv = ThreadingHTTPServer(("127.0.0.1", 8767), Handler)
    print("[review] http://localhost:8767  (keuzes -> review_keuzes.json)")
    srv.serve_forever()
