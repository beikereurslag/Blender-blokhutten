import bpy, json
from mathutils import Vector

floats = []
for o in bpy.data.objects:
    if o.type == 'MESH' and o.visible_get():
        zs = [(o.matrix_world @ Vector(c)).z for c in o.bound_box]
        if min(zs) > 3.0:
            loc = o.matrix_world.translation
            floats.append([o.name, round(min(zs), 1), round(max(zs), 1),
                           round(loc.x, 1), round(loc.y, 1)])

paving = []
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    for s in o.material_slots:
        m = s.material
        if not m:
            continue
        hit = any(k in m.name.lower() for k in ('pav', 'path', 'pad', 'terras', 'tile', 'stone'))
        bc = None
        if m.use_nodes:
            for n in m.node_tree.nodes:
                if n.type == 'TEX_IMAGE' and n.image:
                    ref = (n.image.name + (n.image.filepath or '')).lower()
                    if 'paving_stones_64' in ref:
                        hit = True
                if n.type == 'BSDF_PRINCIPLED':
                    bc = [round(x, 2) for x in n.inputs['Base Color'].default_value]
        if hit:
            paving.append([o.name, m.name, bc])
            break

print("INSPECT_START")
print(json.dumps({"floating": floats, "paving_mats": paving[:12]}, indent=2))
print("INSPECT_END")
