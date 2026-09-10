import bpy, math
from mathutils import Vector

F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Dahlia-250x250-300-zijwand\style-scandi\dahlia_leeshoek.blend"
bpy.ops.wm.open_mainfile(filepath=F)
sc = bpy.context.scene

VEG = ('tree', 'pine', 'den', 'shrub', 'grass', 'gras', 'weed', 'hedge', 'heg', 'haag',
       'birch', 'berk', 'rooibos', 'lavendel', 'flower', 'bloem', 'bush', 'sprig', 'asset',
       'ground', 'sky', 'cloud', 'sun', 'light')
struct = []
allc = []
for o in bpy.data.objects:
    if o.type != 'MESH' or not len(o.data.vertices):
        continue
    nl = o.name.lower()
    if any(k in nl for k in VEG):
        continue
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    allc += cs
    struct.append((o.name, cs))

xs = [c.x for c in allc]; ys = [c.y for c in allc]; zs = [c.z for c in allc]
print("CABINPROBE_START")
print("STRUCT_OBJS:", len(struct))
print(f"NONVEG_BBOX x[{min(xs):.2f},{max(xs):.2f}] y[{min(ys):.2f},{max(ys):.2f}] z[{min(zs):.2f},{max(zs):.2f}]")
print(f"CABIN_CENTER ({(min(xs)+max(xs))/2:.2f}, {(min(ys)+max(ys))/2:.2f}, {(min(zs)+max(zs))/2:.2f})")
# wall/roof only (exclude deck/pad/stoep) for a tighter cabin box
WALL = ('wall', 'board', 'muur', 'dak', 'roof', 'deur', 'raam', 'paal', 'post', 'plate', 'epdm')
wc = []
for nm, cs in struct:
    if any(k in nm.lower() for k in WALL):
        wc += cs
if wc:
    wx = [c.x for c in wc]; wy = [c.y for c in wc]; wz = [c.z for c in wc]
    print(f"WALL_BBOX x[{min(wx):.2f},{max(wx):.2f}] y[{min(wy):.2f},{max(wy):.2f}] z[{min(wz):.2f},{max(wz):.2f}]")
    print(f"WALL_CENTER ({(min(wx)+max(wx))/2:.2f}, {(min(wy)+max(wy))/2:.2f}, {(min(wz)+max(wz))/2:.2f})")
print("CABINPROBE_END")
