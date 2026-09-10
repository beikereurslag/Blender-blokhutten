import bpy
from mathutils import Vector

F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Camelia-250x300-300-zijwand\style-mediterraan\camelia_wijnterras.blend"
DIAG = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Camelia-250x300-300-zijwand\style-mediterraan\_diag_wijn_top.png"
bpy.ops.wm.open_mainfile(filepath=F)
sc = bpy.context.scene

def bb(o):
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs]; ys=[c.y for c in cs]; zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)

CAT = [
    ("ROOF",  ('dak','roof','epdm','overstek','overkap','trim','fascia')),
    ("POST",  ('paal','post','staander','pijler','kolom','stijl','pole','pilaar')),
    ("BEAM",  ('balk','ligger','gording','beam','muurplaat','roofbeam','roofwall')),
    ("WALL",  ('wand','muur','wall','gevel','board','beschot')),
    ("FLOOR", ('vloer','floor','vlonder','deck','dek')),
    ("TERRAS",('terras','klinker','tegel','stoep','pad','path','flagstone','paver','grind','gravel')),
    ("DOOR",  ('deur','door','raam','window','kozijn','scharnier','handle','handvat')),
    ("PROP",  ('wijn','fles','glas','glass','bottle','slinger','festoen','festoon','pot','plant','stoel','chair','tafel','table','boom','tree','maple','esdoorn')),
]
def cat_of(nm):
    nl = nm.lower()
    for cat, kws in CAT:
        if any(k in nl for k in kws):
            return cat
    return None

groups = {c[0]: [] for c in CAT}; groups["OTHER"]=[]
SKIP = ('grass','gras','sky','cloud','sun','ground','hedge','heg','haag','pine','den','birch','berk','shrub','bush','twig','leaf','leaves','corn','mais','field')
for o in bpy.data.objects:
    if o.type!='MESH' or not len(o.data.vertices): continue
    nl=o.name.lower()
    if any(k in nl for k in SKIP):
        # still record trees/big veg combined extent? skip for clarity
        continue
    b=bb(o); c=cat_of(o.name) or "OTHER"; groups[c].append((o.name,b))

print("WPROBE_START")
for cat in ["ROOF","POST","BEAM","WALL","FLOOR","TERRAS","DOOR","PROP","OTHER"]:
    items=groups[cat]
    if not items: print(f"--- {cat}: (none)"); continue
    xs=[];ys=[];zs=[]
    for nm,b in items: xs+=[b[0],b[1]];ys+=[b[2],b[3]];zs+=[b[4],b[5]]
    print(f"--- {cat}: {len(items)} objs COMBINED x[{min(xs):.2f},{max(xs):.2f}] y[{min(ys):.2f},{max(ys):.2f}] z[{min(zs):.2f},{max(zs):.2f}]")
    for nm,b in items[:30]:
        print(f"      {nm:40s} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}]")

print("--- CAMERAS:")
for o in bpy.data.objects:
    if o.type=='CAMERA':
        t = " (ACTIVE)" if sc.camera==o else ""
        print(f"      {o.name}{t}: loc({o.location.x:.2f},{o.location.y:.2f},{o.location.z:.2f}) lens={o.data.lens:.0f}")
print("WPROBE_END")

# top-down ortho
cam=bpy.data.cameras.new("TopCam"); cam.type='ORTHO'; cam.ortho_scale=13
camo=bpy.data.objects.new("TopCam",cam); sc.collection.objects.link(camo)
camo.location=(0.0,1.0,30.0); camo.rotation_euler=(0,0,0); sc.camera=camo
sc.render.resolution_x=1100; sc.render.resolution_y=1100; sc.cycles.samples=24
sc.render.filepath=DIAG
bpy.ops.render.render(write_still=True)
print("DIAG_DONE")
