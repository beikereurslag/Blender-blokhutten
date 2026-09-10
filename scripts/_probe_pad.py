import bpy
from mathutils import Vector
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Camelia-250x300-300-zijwand\style-mediterraan\camelia_wijnterras.blend"
bpy.ops.wm.open_mainfile(filepath=F)
def bb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
print("PAD_START")
for o in bpy.data.objects:
    nl=o.name.lower()
    if ('pad' in nl or 'path' in nl or 'grind' in nl or 'gravel' in nl or 'stoep' in nl or 'step' in nl) and o.type=='MESH':
        b=bb(o)
        mats=[s.material.name if s.material else None for s in o.material_slots]
        print(f"{o.name:24s} verts{len(o.data.vertices)} polys{len(o.data.polygons)} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}] mats={mats}")
        # material detail
        for s in o.material_slots:
            m=s.material
            if m and m.use_nodes:
                imgs=[n.image.name for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]
                bsdf=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
                bc=bsdf.inputs['Base Color'].default_value[:] if bsdf else None
                bclink=[l.from_node.type for l in bsdf.inputs['Base Color'].links] if bsdf else None
                print(f"    mat {m.name}: imgs={imgs} baseColorLink={bclink} baseRGBA={tuple(round(x,2) for x in bc) if bc else None}")
print("PAD_END")
