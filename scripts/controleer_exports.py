"""Controleer de nieuwe tekentool-exports tegen de verwachte productmaten.

Leest elke GLB in source-glbs-new/<datum>/, meet de bounding box en de
aanwezige wanden, en vergelijkt dat met wat de bestandsnaam belooft.

    python scripts/controleer_exports.py
    python scripts/controleer_exports.py source-glbs-new/2026-09-11
"""
import glob
import json
import os
import re
import struct
import sys

import numpy as np

# dakoverstek van de tekentool, gemeten aan de exports (cm)
OVERSTEK_BREEDTE = 45.6
OVERSTEK_DIEPTE = 40.7


def gltf(path):
    with open(path, "rb") as f:
        if f.read(4) != b"glTF":
            return None, None
        struct.unpack("<II", f.read(8))
        clen, _ = struct.unpack("<II", f.read(8))
        js = json.loads(f.read(clen))
        struct.unpack("<II", f.read(8))
        return js, f.read()


CT = {5120: "b", 5121: "B", 5122: "h", 5123: "H", 5125: "I", 5126: "f"}
NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}


def accessor(js, bin_, idx):
    a = js["accessors"][idx]
    bv = js["bufferViews"][a["bufferView"]]
    fmt, n = CT[a["componentType"]], NC[a["type"]]
    stride = bv.get("byteStride") or struct.calcsize(fmt) * n
    start = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
    out = np.empty((a["count"], n), dtype=np.dtype(fmt))
    for i in range(a["count"]):
        out[i] = struct.unpack_from("<" + fmt * n, bin_, start + i * stride)
    return out.astype(np.float64)


def matrix(node):
    if "matrix" in node:
        return np.array(node["matrix"]).reshape(4, 4).T
    t = node.get("translation", [0, 0, 0])
    x, y, z, w = node.get("rotation", [0, 0, 0, 1])
    s = node.get("scale", [1, 1, 1])
    R = np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
                  [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)],
                  [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
    M = np.eye(4)
    M[:3, :3] = R @ np.diag(s)
    M[:3, 3] = t
    return M


def meet(path):
    js, bin_ = gltf(path)
    if js is None:
        return None
    lo = np.array([1e9] * 3)
    hi = np.array([-1e9] * 3)
    wanden, palen = set(), 0

    def loop(i, parent):
        nonlocal lo, hi, palen
        node = js["nodes"][i]
        M = parent @ matrix(node)
        naam = node.get("name", "")
        if "mesh" in node:
            for prim in js["meshes"][node["mesh"]]["primitives"]:
                p = accessor(js, bin_, prim["attributes"]["POSITION"])
                ph = np.hstack([p, np.ones((len(p), 1))])
                w = (M @ ph.T).T[:, :3]
                lo = np.minimum(lo, w.min(0))
                hi = np.maximum(hi, w.max(0))
            m = re.match(r"^(wall-[\w]+)-board", naam)
            if m:
                wanden.add(m.group(1).replace("wall-", ""))
            if naam.startswith("pole"):
                palen += 1
        for c in node.get("children", []):
            loop(c, M)

    for i in js["scenes"][js.get("scene", 0)]["nodes"]:
        loop(i, np.eye(4))

    roots = [js["nodes"][i].get("name") for i in js["scenes"][js.get("scene", 0)]["nodes"]]
    return {"bbox": (hi - lo) * 100, "wanden": sorted(wanden), "palen": palen,
            "roots": roots, "materialen": len(js.get("materials", []))}


def verwacht(naam):
    """Lees B, D, L en zijwand uit een bestandsnaam als 'Camelia 250x300 + 300 + zijwand'."""
    m = re.match(r"^[A-Za-z]+ (\d+)x(\d+)(?:\s*\+\s*(\d+))?(\s*\+\s*z?ijwand)?$", naam)
    if not m:
        return None
    B, D = int(m.group(1)), int(m.group(2))
    L = int(m.group(3)) if m.group(3) else 0
    return {"B": B, "D": D, "L": L, "zijwand": bool(m.group(4))}


def main():
    map_ = sys.argv[1] if len(sys.argv) > 1 else None
    if not map_:
        mappen = sorted(glob.glob(os.path.join("source-glbs-new", "20*")))
        map_ = mappen[-1] if mappen else None
    if not map_ or not os.path.isdir(map_):
        print("Geen exportmap gevonden.")
        return 1

    print(f"Controle van {map_}\n")
    kop = f"{'model':<38} {'breedte':>16} {'diepte':>15} {'wanden':<14} {'palen':>5}"
    print(kop)
    print("-" * len(kop))

    goed = fout = 0
    for pad in sorted(glob.glob(os.path.join(map_, "*.glb"))):
        naam = os.path.splitext(os.path.basename(pad))[0]
        g = meet(pad)
        v = verwacht(naam)
        if g is None:
            print(f"{naam:<38} ONLEESBAAR")
            fout += 1
            continue
        if v is None:
            print(f"{naam:<38} (geen productnaam, overgeslagen)")
            continue

        wb = v["B"] + v["L"] + OVERSTEK_BREEDTE
        wd = v["D"] + OVERSTEK_DIEPTE
        db, dd = g["bbox"][0] - wb, g["bbox"][2] - wd
        ok_b, ok_d = abs(db) < 1.0, abs(dd) < 1.0
        heeft7 = "7" in g["wanden"]
        heeft8 = "8" in g["wanden"]
        ok_w = heeft7 == bool(v["L"]) and heeft8 == v["zijwand"]
        if ok_b and ok_d and ok_w:
            goed += 1
        else:
            fout += 1
        vlag = "" if (ok_b and ok_d and ok_w) else "  <-- LET OP"
        print(f"{naam:<38} {g['bbox'][0]:8.1f}/{wb:<7.1f} {g['bbox'][2]:7.1f}/{wd:<7.1f} "
              f"{','.join(g['wanden']):<14} {g['palen']:>5}{vlag}")

    print(f"\n{goed} in orde, {fout} met afwijking")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
