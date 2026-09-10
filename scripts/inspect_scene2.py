import bpy, json
from mathutils import Vector

def wbb(o):
    xs = []; ys = []; zs = []
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c); xs.append(w.x); ys.append(w.y); zs.append(w.z)
    return [round(min(xs), 1), round(max(xs), 1), round(min(ys), 1), round(max(ys), 1), round(min(zs), 1), round(max(zs), 1)]

keys = ['hedge', 'heg', 'fence', 'hek', 'schutting', 'lawn', 'grass', 'gras', 'ground', 'grond',
        'lantern', 'lamp', 'hydrang', 'hortensia', 'lavend', 'birch', 'tree', 'boom', 'shrub', 'bush', 'path', 'paver']
groups = {}
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    nl = o.name.lower()
    for k in keys:
        if k in nl:
            groups.setdefault(k, []).append(o.name)
            break

out = {}
for k, names in groups.items():
    objs = [bpy.data.objects[n] for n in names]
    xs = []; ys = []; zmax = -1e9
    for o in objs:
        bb = wbb(o); xs += [bb[0], bb[1]]; ys += [bb[2], bb[3]]; zmax = max(zmax, bb[5])
    out[k] = {'n': len(names), 'x': [min(xs), max(xs)], 'y': [min(ys), max(ys)], 'zmax': round(zmax, 1), 'ex': names[:3]}

# grootste grond/lawn object + materiaal
ground = None; gmax = 0
for o in bpy.data.objects:
    if o.type == 'MESH':
        bb = wbb(o); area = (bb[1] - bb[0]) * (bb[3] - bb[2])
        if area > gmax and (bb[5] - bb[4]) < 0.6:  # plat + groot
            gmax = area; ground = o
gmat = None
if ground:
    m = ground.active_material
    nodes = [n.type for n in m.node_tree.nodes] if (m and m.use_nodes) else []
    has_tex = any(t == 'TEX_IMAGE' for t in nodes)
    gmat = {'obj': ground.name, 'bb': wbb(ground), 'mat': m.name if m else None, 'has_texture': has_tex, 'node_types': nodes}

# camera
cam = bpy.context.scene.camera
caminfo = None
if cam:
    d = cam.data
    caminfo = {'name': cam.name, 'loc': [round(v, 1) for v in cam.location],
               'lens': round(d.lens, 1), 'rot_deg': [round(__import__('math').degrees(a), 0) for a in cam.rotation_euler]}

print("INSPECT2_START")
print(json.dumps({'groups': out, 'ground': gmat, 'camera': caminfo}, indent=1))
print("INSPECT2_END")
