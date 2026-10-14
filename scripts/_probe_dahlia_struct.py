import bpy
from mathutils import Vector

F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Dahlia-250x250-300-zijwand\style-scandi\dahlia_leeshoek.blend"
DIAG = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Dahlia-250x250-300-zijwand\style-scandi\_diag_struct_top.png"
bpy.ops.wm.open_mainfile(filepath=F)
sc = bpy.context.scene

def bb(o):
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs]; ys=[c.y for c in cs]; zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)

CAT = [
    ("ROOF",  ('dak','roof','epdm','overstek','overkap')),
    ("POST",  ('paal','post','staander','pijler','kolom','stijl')),
    ("BEAM",  ('balk','ligger','gording','beam','muurplaat','plate')),
    ("WALL",  ('wand','muur','wall','gevel','board','plank_wall','beschot')),
    ("FLOOR", ('vloer','floor','vlonder','deck','dek')),
    ("DOOR",  ('deur','door','raam','window','kozijn')),
    ("TERRAS",('terras','dlterras','klinker','tegel','stoep','pad')),
]
def cat_of(nm):
    nl = nm.lower()
    for cat, kws in CAT:
        if any(k in nl for k in kws):
            return cat
    return None

groups = {c[0]: [] for c in CAT}
groups["OTHER"] = []
allmesh = []
for o in bpy.data.objects:
    if o.type != 'MESH' or not len(o.data.vertices):
        continue
    nl = o.name.lower()
    if any(k in nl for k in ('tree','pine','den','shrub','grass','gras','weed','hedge','heg','haag',
                             'birch','berk','rooibos','lavendel','flower','bloem','bush','sprig',
                             'ground','sky','cloud','sun','fauteuil','tafel','vacht','boek','mok',
                             'hout','firewood','lantaarn','lantern','rz_','throw','mug','book')):
        continue
    b = bb(o)
    allmesh.append((o.name, b))
    c = cat_of(o.name) or "OTHER"
    groups[c].append((o.name, b))

print("STRUCTPROBE_START")
for cat in ["ROOF","POST","BEAM","WALL","FLOOR","DOOR","TERRAS","OTHER"]:
    items = groups[cat]
    if not items:
        print(f"--- {cat}: (none)"); continue
    xs=[];ys=[];zs=[]
    for nm,b in items:
        xs+= [b[0],b[1]]; ys+=[b[2],b[3]]; zs+=[b[4],b[5]]
    print(f"--- {cat}: {len(items)} objs  COMBINED x[{min(xs):.2f},{max(xs):.2f}] y[{min(ys):.2f},{max(ys):.2f}] z[{min(zs):.2f},{max(zs):.2f}]")
    for nm,b in items[:24]:
        print(f"      {nm:42s} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}]")
print("STRUCTPROBE_END")

# top-down ortho to see floor coverage
cam = bpy.data.cameras.new("TopCam"); cam.type='ORTHO'; cam.ortho_scale=11
camo = bpy.data.objects.new("TopCam", cam); sc.collection.objects.link(camo)
camo.location=(0.0,1.0,30.0); camo.rotation_euler=(0,0,0); sc.camera=camo
sc.render.resolution_x=1100; sc.render.resolution_y=1100; sc.cycles.samples=20
sc.render.filepath=DIAG
bpy.ops.render.render(write_still=True)
print("DIAG_DONE", DIAG)
