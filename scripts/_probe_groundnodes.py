"""Dump M_PBR_GrassRock node-waarden (HUE_SAT/MIX/BSDF) om de washout-oorzaak te zien."""
import bpy
from mathutils import Vector
g = None; best = 0
for o in bpy.data.objects:
    if o.type == 'MESH' and any(k in o.name.lower() for k in ('ground', 'grass', 'grond')) and len(o.data.vertices):
        cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
        a = (max(c.x for c in cs)-min(c.x for c in cs))*(max(c.y for c in cs)-min(c.y for c in cs))
        if a > best: best = a; g = o
print("ground:", g.name if g else None)
m = g.material_slots[0].material
nt = m.node_tree
print("mat:", m.name)
for n in nt.nodes:
    if n.type == 'HUE_SAT':
        print("  HUE_SAT  hue=%.3f sat=%.3f val=%.3f fac=%.3f" % (
            n.inputs['Hue'].default_value, n.inputs['Saturation'].default_value,
            n.inputs['Value'].default_value, n.inputs['Fac'].default_value))
    if n.type == 'MIX_RGB':
        c1 = [round(v,2) for v in n.inputs['Color1'].default_value[:3]] if not n.inputs['Color1'].is_linked else 'LINK'
        c2 = [round(v,2) for v in n.inputs['Color2'].default_value[:3]] if not n.inputs['Color2'].is_linked else 'LINK'
        print("  MIX_RGB  blend=%s fac=%.2f c1=%s c2=%s" % (n.blend_type, n.inputs['Fac'].default_value, c1, c2))
    if n.type == 'BSDF_PRINCIPLED':
        print("  BSDF  rough=%.2f (linked=%s)" % (n.inputs['Roughness'].default_value, n.inputs['Roughness'].is_linked))
    if n.type == 'TEX_IMAGE' and n.image:
        print("  TEX_IMAGE", n.image.name, "colorspace", n.image.colorspace_settings.name)
