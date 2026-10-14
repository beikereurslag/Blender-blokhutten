"""Read-only state diagnose - Zonnebloem Ochtendhoek (na realism prop-swap).
Geen save. Dumpt: collections, RealismSwap-inhoud, deck/pad-objecten + hun
materiaal (flat color vs PBR image), camera, lavendel. Schrijft clean report
naar scripts/_diag_zo_state.txt EN print naar stdout (markers).
"""
import bpy, os
from mathutils import Vector

F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Zonnebloem-300x300-300-zijwand\style-scandi\zonnebloem_ochtendhoek.blend"
OUT = r"C:\Users\beike\Documents\Blender-blokhutten\scripts\_diag_zo_state.txt"
bpy.ops.wm.open_mainfile(filepath=F)
scn = bpy.context.scene

L = []
def p(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s)

def bb(o):
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs]; ys=[c.y for c in cs]; zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)

def mat_kind(o):
    """Beschrijf materiaal-realisme: heeft het image-textures (PBR) of vlakke kleur?"""
    out = []
    for slot in getattr(o, "material_slots", []):
        m = slot.material
        if not m:
            out.append("<none>"); continue
        if not m.use_nodes:
            out.append(f"{m.name}:nonodes"); continue
        imgs = [n.image.name for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]
        bsdf = [n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED']
        base = None
        if bsdf:
            bc = bsdf[0].inputs['Base Color']
            if not bc.is_linked:
                base = tuple(round(v,2) for v in bc.default_value)
        tag = f"{m.name}: imgs={imgs if imgs else 'NONE(flat)'}"
        if base is not None: tag += f" baseRGBA={base}"
        out.append(tag)
    return out

p("DIAG_START Zonnebloem Ochtendhoek")
cam = scn.camera
p("ACTIVE CAMERA:", cam.name if cam else None,
  ("loc"+str(tuple(round(v,2) for v in cam.location)) + f" lens={cam.data.lens:.0f}") if cam else "")
p("RENDER:", scn.render.engine, scn.view_settings.view_transform, "look=", scn.view_settings.look,
  "res", scn.render.resolution_x, "x", scn.render.resolution_y)
p("")
p("COLLECTIONS:", [(c.name, len(c.objects)) for c in bpy.data.collections])
p("")

rz = bpy.data.collections.get("RealismSwap")
p("=== RealismSwap collection ===")
if rz:
    for o in sorted(rz.objects, key=lambda x:x.name):
        if o.type=='MESH' and len(o.data.vertices):
            b=bb(o); p(f"  {o.name:30s} {o.type:7s} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}] v={len(o.data.vertices)}")
        else:
            p(f"  {o.name:30s} {o.type:7s} loc{tuple(round(v,2) for v in o.location)}")
else:
    p("  <geen RealismSwap collection!>")
p("")

# deck / pad / lavender / table objecten
p("=== Hardscape + key props (deck/pad/terras/lavendel/tafel) + materiaal ===")
keys=('deck','vlonder','terras','pad','path','tegel','plank','klink','step','steen',
      'lavend','tafel','table','stoel','chair','ground','gras','grass','lawn')
for o in sorted(bpy.data.objects, key=lambda x:x.name):
    n=o.name.lower()
    if any(k in n for k in keys) and o.type=='MESH' and len(o.data.vertices):
        b=bb(o)
        p(f"  {o.name:30s} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}] v={len(o.data.vertices)}")
        for mk in mat_kind(o):
            p(f"        mat: {mk}")
p("")
p("=== ALL top-level (parentless) mesh objects ===")
tops=[o.name for o in bpy.data.objects if o.type=='MESH' and not o.parent]
p("  count:", len(tops))
for nm in sorted(tops):
    p("   ", nm)
p("DIAG_END")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L))
