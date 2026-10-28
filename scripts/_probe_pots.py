import bpy
from mathutils import Vector
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Camelia-250x300-300-zijwand\style-mediterraan\camelia_wijnterras.blend"
bpy.ops.wm.open_mainfile(filepath=F)
def bb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
print("POTS_START")
KW=('pot','terracotta','terra','pottery','vase','vaas','urn','clay','olij','olive','plant','kruik')
for o in bpy.data.objects:
    nl=o.name.lower()
    if any(k in nl for k in KW):
        if o.type=='MESH' and len(o.data.vertices):
            b=bb(o)
            par=o.parent.name if o.parent else None
            print(f"  {o.name:34s} parent={par} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}]")
        else:
            print(f"  {o.name:34s} type={o.type} (empty/non-mesh) loc={tuple(round(v,2) for v in o.location)}")
# also: anything in the foreground bottom-left of frame (x<-2.5, y<1.0) that's small
print("--- small foreground objects (x<-2.5, y<1.5, not grass/cabin):")
SKIP=('grass','gras','sky','hedge','heg','pine','den','birch','shrub','bush','leaf','leaves','corn','mais','wand','muur','wall','vloer','floor','dak','roof','cwfloor','cwterras','pad','terras')
for o in bpy.data.objects:
    if o.type!='MESH' or not len(o.data.vertices): continue
    nl=o.name.lower()
    if any(k in nl for k in SKIP): continue
    b=bb(o)
    if b[1]<-2.0 and b[3]<2.0 and (b[5]-b[4])<1.2:
        par=o.parent.name if o.parent else None
        print(f"  {o.name:34s} parent={par} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}]")
print("POTS_END")
