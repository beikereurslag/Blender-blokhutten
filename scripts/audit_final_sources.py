r"""Map every cabin final in ALLE_FINALS back to the render it came from and the
blend that produced it, and flag the ones that can no longer be reproduced.

A final is only safe to re-render if the blend still holds the state that was
approved. Where the blend was saved again after the final was made (a later
review round), re-rendering gives a different picture -- different light, fog or
dressing -- not just repaired planks.

  python scripts/audit_final_sources.py
"""
import hashlib
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FINAL_DIRS = [
    os.path.join(ROOT, "ALLE_FINALS", "blokhutten-tuinscenes"),
    os.path.join(ROOT, "ALLE_FINALS", "blokhutten-stijlen"),
]
PILOTS = os.path.join(ROOT, "pilots")


def md5(path, chunk=1 << 20):
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def ts(path):
    return datetime.fromtimestamp(os.path.getmtime(path))


print("indexing pilot renders...", flush=True)
by_size = {}
for dirpath, _dirs, files in os.walk(PILOTS):
    for fn in files:
        if fn.lower().endswith(".png"):
            p = os.path.join(dirpath, fn)
            by_size.setdefault(os.path.getsize(p), []).append(p)

rows = []
for d in FINAL_DIRS:
    if not os.path.isdir(d):
        continue
    for fn in sorted(os.listdir(d)):
        if not fn.lower().endswith(".png"):
            continue
        final = os.path.join(d, fn)
        fsize = os.path.getsize(final)
        source = None
        for cand in by_size.get(fsize, []):
            if md5(cand) == md5(final):
                source = cand
                break
        if not source:
            rows.append((fn, None, None, "NO SOURCE RENDER FOUND"))
            continue

        folder = os.path.dirname(source)
        blends = [os.path.join(folder, b) for b in os.listdir(folder)
                  if b.endswith(".blend") and "_PLANKFIX" not in b]
        if not blends:
            rows.append((fn, os.path.relpath(source, ROOT), None, "NO BLEND IN FOLDER"))
            continue
        blend = max(blends, key=os.path.getmtime)
        drift = ts(blend) - ts(source)
        if drift.total_seconds() > 3600:
            status = f"BLEND MOVED ON (+{drift.days}d {drift.seconds // 3600}h)"
        else:
            status = "ok"
        rows.append((fn, os.path.relpath(source, ROOT), os.path.relpath(blend, ROOT), status))

print(f"\n{'final':32s} {'status':28s} blend")
print("-" * 110)
bad = 0
for fn, source, blend, status in rows:
    if status != "ok":
        bad += 1
    print(f"{fn:32s} {status:28s} {os.path.basename(blend) if blend else '-'}")
print("-" * 110)
print(f"{len(rows)} finals, {bad} need attention before re-rendering")
