"""Poster per clip: 2x2 contactvel (A begin, A eind, B midden, C midden) op 1920x1080.

Waarom 2x2 en niet een strip: de poster hangt in het `<video>`-element op de Werkbank-reviewtab,
dus hij moet 16:9 zijn. Vier frames dekken de hele clip, zodat Beike per scene kan beoordelen
zonder 30 filmpjes af te spelen - hij speelt alleen wat hem opvalt.

    python scripts/clips_v2/build_posters.py [scene ...]

Zonder argumenten: alle scenes met frames. Bestaande posters worden alleen vervangen als de
frames nieuwer zijn.
"""
import sys
from pathlib import Path

from PIL import Image

WORTEL = Path(__file__).resolve().parents[2]
FRAMES = WORTEL / "scripts" / "clips_v2" / "_frames"
CLIPS = WORTEL / "ALLE_FINALS" / "filmpjes-v2"
POSTERS = CLIPS / "_posters"
TEGEL = (960, 540)


def _uit_runlog():
    """scene -> clipnaam uit de runlog-regels `START <scene> -> <clip>`.

    Dat is de enige plek waar de echte koppeling staat: bij een paar scenes wijkt de clipnaam af
    van de mapnaam (overkapping_keuken -> overkapping-buitenkeuken), en die is niet te raden."""
    log = FRAMES / "_run_full.log"
    uit = {}
    if log.exists():
        for regel in log.read_text(errors="replace").split("\n"):
            if " START " in regel and " -> " in regel:
                links, rechts = regel.split(" START ", 1)[1].split(" -> ", 1)
                uit[links.strip()] = rechts.strip()
    return uit


_RUNLOG = None


def clipnaam(scene):
    """Scene-map -> mp4. Eerst de runlog-koppeling, dan de naam zelf (streepjes i.p.v. underscores)."""
    global _RUNLOG
    if _RUNLOG is None:
        _RUNLOG = _uit_runlog()
    if scene in _RUNLOG:
        mp4 = CLIPS / (_RUNLOG[scene] + ".mp4")
        if mp4.exists():
            return mp4
    for mp4 in CLIPS.glob("*.mp4"):
        if mp4.stem.replace("-", "_").lower() == scene.replace("-", "_").lower():
            return mp4
    return None


def kies_frames(map_):
    """Vier frames die de clip dekken: A begin, A eind, B midden, C midden."""
    per_shot = {}
    for png in sorted(map_.glob("*.png")):
        shot = png.stem.rsplit("_", 1)[0]
        per_shot.setdefault(shot, []).append(png)
    a = next((v for k, v in per_shot.items() if k.startswith("A_")), None)
    b = next((v for k, v in per_shot.items() if k.startswith("B_")), None)
    c = next((v for k, v in per_shot.items() if k.startswith("C_")), None)
    uit = []
    if a:
        uit += [a[min(8, len(a) - 1)], a[-1]]
    if b:
        uit.append(b[len(b) // 2])
    if c:
        uit.append(c[len(c) // 2])
    return uit


def bouw(scene):
    map_ = FRAMES / scene
    frames = kies_frames(map_)
    if len(frames) < 2:
        return f"{scene}: te weinig frames ({len(frames)})"
    mp4 = clipnaam(scene)
    if mp4 is None:
        return f"{scene}: geen mp4 gevonden, poster overgeslagen"
    doel = POSTERS / (mp4.stem + ".jpg")
    nieuwste = max(f.stat().st_mtime for f in frames)
    if doel.exists() and doel.stat().st_mtime >= nieuwste:
        return f"{scene}: poster al actueel"
    vel = Image.new("RGB", (TEGEL[0] * 2, TEGEL[1] * 2), (18, 18, 20))
    for i, f in enumerate(frames[:4]):
        im = Image.open(f).convert("RGB").resize(TEGEL, Image.LANCZOS)
        vel.paste(im, ((i % 2) * TEGEL[0], (i // 2) * TEGEL[1]))
    POSTERS.mkdir(parents=True, exist_ok=True)
    vel.save(doel, quality=85, optimize=True)
    return f"{scene}: {doel.name} ({doel.stat().st_size // 1024} KB, {len(frames[:4])} frames)"


if __name__ == "__main__":
    scenes = sys.argv[1:] or sorted(p.name for p in FRAMES.iterdir() if p.is_dir())
    for s in scenes:
        print(bouw(s))
