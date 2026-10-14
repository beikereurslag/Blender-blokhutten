# Probe alle 8 base-blends (playbook Fase 0b) — geometrie-feiten voor de scene-plannen.
# Run: & "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" -b --python scripts\probe_all_bases.py
import bpy
import os
from mathutils import Vector

BASE = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\base"
BLENDS = [
    "Camelia-250x300-300-zijwand.blend",
    "Dahlia-250x250-300-zijwand.blend",
    "Jasmijn-300x250-300-zijwand.blend",
    "Lavendel-400x300-400-zijwand.blend",
    "Lelie-400x250-300-zijwand.blend",
    "Magnolia-300x200.blend",
    "Roosmarijn-200x300-400-zijwand.blend",
    "Zonnebloem-300x300-300-zijwand.blend",
]

def wbbox(o):
    pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
    xs = [p.x for p in pts]; ys = [p.y for p in pts]; zs = [p.z for p in pts]
    return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))

def fmt(b):
    return "X %.2f..%.2f  Y %.2f..%.2f  Z %.2f..%.2f" % b

lines = []
for fname in BLENDS:
    path = os.path.join(BASE, fname)
    bpy.ops.wm.open_mainfile(filepath=path)
    lines.append("=" * 70)
    lines.append("CABIN: %s" % fname)

    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    if meshes:
        allb = [wbbox(o) for o in meshes]
        tot = (min(b[0] for b in allb), max(b[1] for b in allb),
               min(b[2] for b in allb), max(b[3] for b in allb),
               min(b[4] for b in allb), max(b[5] for b in allb))
        lines.append("TOTAL BBOX: %s" % fmt(tot))
        lines.append("FOOTPRINT: %.2f x %.2f m, hoogte %.2f m" %
                     (tot[1]-tot[0], tot[3]-tot[2], tot[5]-tot[4]))

    # deuren
    for o in meshes:
        n = o.name.lower()
        if 'deur' in n or 'door' in n:
            lines.append("  DOOR: %-28s %s" % (o.name, fmt(wbbox(o))))
    # palen (open zijde)
    for o in meshes:
        if o.name.lower().startswith('pole'):
            lines.append("  POLE: %-28s %s" % (o.name, fmt(wbbox(o))))
    # canopy-wanden
    canopy = [o.name for o in meshes if 'canopy' in o.name.lower()]
    if canopy:
        lines.append("  CANOPY OBJS: %s" % ", ".join(canopy[:12]))
    # glas / chroom / verborgen elementen
    hidden = [o.name for o in bpy.data.objects if o.hide_render or o.hide_viewport]
    if hidden:
        lines.append("  HIDDEN (%d): %s" % (len(hidden), ", ".join(hidden[:15])))
    # camera's (GLB-resten)
    cams = [o.name for o in bpy.data.objects if o.type == 'CAMERA']
    lines.append("  CAMERAS: %s" % (", ".join(cams) if cams else "geen"))
    # materialen
    mats = sorted(set(m.name for m in bpy.data.materials if m.users > 0))
    lines.append("  MATERIALS (%d): %s" % (len(mats), ", ".join(mats[:20])))
    # dak-indicatie: hoogste object + naam
    if meshes:
        top = max(meshes, key=lambda o: wbbox(o)[5])
        lines.append("  HIGHEST OBJ: %s (top Z %.2f)" % (top.name, wbbox(top)[5]))
    roofish = sorted(set(o.name.split('.')[0] for o in meshes if 'roof' in o.name.lower() or 'flat' in o.name.lower()))
    lines.append("  ROOF NAMES: %s" % ", ".join(roofish[:12]))

out = r"C:\Users\beike\Documents\Blender-blokhutten\scripts\probe_all_bases_OUTPUT.txt"
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("\n".join(lines))
print("WROTE:", out)
