"""Read-only geometry probe: source GLB transforms, bounds, doors and poles.

Reads no textures, changes no Blender scene, and writes only the requested JSON.
"""
import json
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, r"C:\Users\beike\blokhut-print")
from glb_extract import read_glb, acc_array, node_matrix

source = Path(r"D:\Blender-blokhutten\source-glbs\Jasmijn 300x250 + 250.glb")
g, binary = read_glb(source)
stack = [(i, np.eye(4)) for i in g['scenes'][g.get('scene', 0)]['nodes']]
rows = []
cameras = []
while stack:
    idx, parent = stack.pop()
    node = g['nodes'][idx]
    world = parent @ node_matrix(node)
    name = node.get('name', str(idx))
    if 'camera' in node:
        cameras.append(name)
    if 'mesh' in node:
        points = []
        for prim in g['meshes'][node['mesh']].get('primitives', []):
            if 'POSITION' not in prim.get('attributes', {}):
                continue
            p = acc_array(g, binary, prim['attributes']['POSITION'])
            p = (world @ np.c_[p, np.ones(len(p))].T).T[:, :3]
            # glTF Y-up cm to Blender Z-up metres: X, -Z, Y.
            points.append(p[:, [0, 2, 1]] * np.array([0.01, -0.01, 0.01]))
        if points:
            p = np.vstack(points)
            rows.append(dict(name=name, min=p.min(0).round(5).tolist(),
                             max=p.max(0).round(5).tolist(), vertices=len(p)))
    stack.extend((i, world) for i in node.get('children', []))

def bounds(items):
    if not items:
        return None
    low = np.array([r['min'] for r in items]).min(0)
    high = np.array([r['max'] for r in items]).max(0)
    return dict(min=low.round(5).tolist(), max=high.round(5).tolist(),
                dimensions=(high-low).round(5).tolist())

structure = [r for r in rows if re.search(r'^(wall-|parentBoard|roof|pole-|foundationBeam|trim-|fasciaboard)', r['name'])]
doors = [r for r in rows if re.search(r'deur|double.door|door.inset', r['name'], re.I)]
report = dict(source=str(source), source_bytes=source.stat().st_size,
              coordinates='metres, X/-Z/Y from source glTF world cm; before garden placement',
              mesh_nodes=len(rows), cameras=cameras, structure=bounds(structure),
              doors=doors, poles=[r for r in rows if re.match(r'^pole-\d+$', r['name'])],
              wall_bounds=bounds([r for r in rows if r['name'].startswith(('wall-', 'parentBoard'))]),
              materials=[m.get('name') for m in g.get('materials', [])],
              nodes=rows)
output = Path(r'D:\Blender-blokhutten\docs\astra_source_probe.json')
output.write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('nodes','materials')}, indent=2))
