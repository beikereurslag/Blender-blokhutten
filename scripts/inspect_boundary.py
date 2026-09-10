import bpy, json, re
from mathutils import Vector

def add(o, acc):
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        acc['x'][0] = min(acc['x'][0], w.x); acc['x'][1] = max(acc['x'][1], w.x)
        acc['y'][0] = min(acc['y'][0], w.y); acc['y'][1] = max(acc['y'][1], w.y)
        acc['z'][0] = min(acc['z'][0], w.z); acc['z'][1] = max(acc['z'][1], w.z)
    for s in o.material_slots:
        if s.material:
            acc['mats'].add(s.material.name)
    acc['n'] += 1

groups = {}
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    n = o.name
    if n.startswith("SM_vgztealha"):
        key = "SM_vgztealha"
    elif n.startswith("Object"):
        key = re.sub(r'\.\d+$', '', n)   # strip .001 etc
    else:
        continue
    g = groups.setdefault(key, {'x': [1e9, -1e9], 'y': [1e9, -1e9], 'z': [1e9, -1e9], 'mats': set(), 'n': 0})
    add(o, g)

out = {}
for k, g in groups.items():
    out[k] = {'n': g['n'],
              'x': [round(g['x'][0], 1), round(g['x'][1], 1)],
              'y': [round(g['y'][0], 1), round(g['y'][1], 1)],
              'z': [round(g['z'][0], 1), round(g['z'][1], 1)],
              'mats': sorted(g['mats'])}
print("BND_START")
print(json.dumps(out, indent=0))
print("BND_END")
