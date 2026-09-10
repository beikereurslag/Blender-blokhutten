import bpy, re
from mathutils import Vector
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Camelia-250x300-300-zijwand\style-hot-tub-premium\camelia_buitenbad.blend"
bpy.ops.wm.open_mainfile(filepath=F)

pads = [o for o in bpy.data.objects if o.name.startswith("Pad_")]
rows = {}
for o in pads:
    m = re.match(r"Pad_(\d+)_(\d+)", o.name)
    if not m: continue
    r = int(m.group(1))
    cs = [o.matrix_world @ Vector(v) for v in o.bound_box]
    cx = sum(p.x for p in cs)/8; cy = sum(p.y for p in cs)/8; cz = sum(p.z for p in cs)/8
    rows.setdefault(r, []).append((cx, cy, cz))

print("PATHPROBE_START")
print("PAD_COUNT", len(pads), "ROWS", len(rows))
allx = []; ally = []; allz = []
for r in sorted(rows):
    pts = rows[r]
    mx = sum(p[0] for p in pts)/len(pts); my = sum(p[1] for p in pts)/len(pts); mz = sum(p[2] for p in pts)/len(pts)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    allx += xs; ally += ys; allz.append(mz)
    print(f"ROW {r:2d}: center ({mx:.2f},{my:.2f},{mz:.3f}) xspan {max(xs)-min(xs):.2f} yspan {max(ys)-min(ys):.2f}")
if pads:
    print("EXTENT x[%.2f,%.2f] y[%.2f,%.2f] z_top~%.3f" % (min(allx), max(allx), min(ally), max(ally), max(allz)))
    print("PAD_MAT", [s.material.name for s in pads[0].material_slots if s.material])
print("PATHPROBE_END")
