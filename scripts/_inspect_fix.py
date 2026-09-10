"""Gerichte read-only inspectie voor de Lelie-fixes. Geen save.
Gebruik: blender -b --python scripts/_inspect_fix.py -- <scene.blend>
"""
import bpy, sys, re
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

argv = sys.argv
F = argv[argv.index("--") + 1]
bpy.ops.wm.open_mainfile(filepath=F)
scn = bpy.context.scene
cam = scn.camera

def bb(o):
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    xs = [c.x for c in cs]; ys = [c.y for c in cs]; zs = [c.z for c in cs]
    return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))

def ndc(co):
    c = world_to_camera_view(scn, cam, Vector(co))
    return (round(c.x, 2), round(c.y, 2), round(c.z, 1))  # x,y in 0..1 (0,0)=lo-left, z=depth(m)

def base_val(m):
    if not m or not m.use_nodes: return None
    for n in m.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            c = n.inputs['Base Color'].default_value
            return (round(c[0], 2), round(c[1], 2), round(c[2], 2))
    return None

def imgs(m):
    if not m or not m.use_nodes: return []
    return [n.image.name for n in m.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image]

print("INSPECT_START", F)
print("CAMERA", cam.name, tuple(round(v,2) for v in cam.location), "lens", round(cam.data.lens))

print("=MATERIALS=")
for m in sorted(bpy.data.materials, key=lambda x: x.name):
    print(f"  {m.name:30s} base={base_val(m)} imgs={imgs(m)}")

COLLAPSE = ['LaDeck_p', 'LaDeck_f', 'OnDeck_p', 'OnDeck_f', 'Plank_', 'LaPaver_',
            'MosPlek_', 'LaCorten_', 'LaBoll', 'KlaproosX', 'KlaproosFG', 'Klaproos_']
SKIP = re.compile(r'(pine_tree|shrub_[014]|weed_plant_02_[a-e]_LOD|jacaranda_tree_leaves|'
                  r'_LOD[0-9]|needle|branch|twig|dead_branch)')
PLANT = re.compile(r'(weed_plant|BakGras|jacaranda|Hedge|fern|Varen|shrub)')

print("=STRUCTURE / OTHER OBJECTS (non-veg)=")
gseen = set()
for o in sorted(bpy.data.objects, key=lambda x: x.name):
    g = next((g for g in COLLAPSE if o.name.startswith(g)), None)
    if g:
        if g in gseen: continue
        gseen.add(g)
        members = [x for x in bpy.data.objects if x.name.startswith(g)]
        cs = []
        for x in members:
            if x.type == 'MESH' and len(x.data.vertices):
                b = bb(x); cs += [b]
        if cs:
            xs0=min(c[0] for c in cs); xs1=max(c[1] for c in cs)
            ys0=min(c[2] for c in cs); ys1=max(c[3] for c in cs)
            zs0=min(c[4] for c in cs); zs1=max(c[5] for c in cs)
            mat = next((s.material.name for m2 in members for s in m2.material_slots if s.material), '?')
            print(f"  [{g}* x{len(members)}] x[{xs0:.2f},{xs1:.2f}] y[{ys0:.2f},{ys1:.2f}] z[{zs0:.2f},{zs1:.2f}] mat~{mat}")
        continue
    if SKIP.search(o.name) or PLANT.search(o.name): continue
    if o.type == 'MESH' and len(o.data.vertices):
        b = bb(o)
        mats = [s.material.name if s.material else '<none>' for s in o.material_slots]
        cx = ((b[0]+b[1])/2, (b[2]+b[3])/2, (b[4]+b[5])/2)
        print(f"  {o.name:32s} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}] ndc{ndc(cx)} {mats}")
    elif o.type == 'EMPTY':
        print(f"  {o.name:32s} EMPTY loc{tuple(round(v,2) for v in o.location)}")

print("=PLANTS / HEDGE (bbox + ndc center; foreground = ndc x,y small & in 0..1)=")
rows = []
for o in bpy.data.objects:
    if o.type != 'MESH' or not len(o.data.vertices): continue
    if not PLANT.search(o.name): continue
    if re.search(r'_LOD[1-9]|needle|branch|twig', o.name): continue  # keep LOD0 + named clumps
    b = bb(o)
    cx = ((b[0]+b[1])/2, (b[2]+b[3])/2, (b[4]+b[5])/2)
    n = ndc(cx)
    rows.append((n[1], o.name, b, n))   # sort by ndc.y (low = bottom of frame)
rows.sort()
for ndcy, name, b, n in rows:
    inframe = (0 <= n[0] <= 1 and 0 <= n[1] <= 1 and n[2] > 0)
    flag = "  <<FG" if (inframe and n[1] < 0.45 and n[0] < 0.6) else ""
    print(f"  {name:30s} zmin={b[4]:.2f} z[{b[4]:.2f},{b[5]:.2f}] x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] ndc{n} inframe={inframe}{flag}")
print("INSPECT_END", F)
