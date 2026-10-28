"""Read-only state - Magnolia Wintertuin. Geen save."""
import bpy
from mathutils import Vector
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Magnolia-300x200\style-scandi\magnolia_wintertuin.blend"
bpy.ops.wm.open_mainfile(filepath=F)
scn = bpy.context.scene

def bb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
def matkind(o):
    out=[]
    for s in getattr(o,"material_slots",[]):
        m=s.material
        if not m: out.append("<none>"); continue
        imgs=[n.image.name for n in m.node_tree.nodes if m.use_nodes and n.type=='TEX_IMAGE' and n.image]
        out.append(f"{m.name}:{imgs if imgs else 'flat'}")
    return out

print("MW_START")
cam=scn.camera
print("CAMERA:",cam.name if cam else None, (str(tuple(round(v,2) for v in cam.location))+f" lens={cam.data.lens:.0f}") if cam else "")
print("RENDER:",scn.render.engine,scn.view_settings.view_transform,"look=",scn.view_settings.look,"exp=",round(scn.view_settings.exposure,2))
print("COLLECTIONS:",[(c.name,len(c.objects)) for c in bpy.data.collections])
print("--- key props (terras/stap/vacht/hout/bank/bench/berk/lantaarn) + mat ---")
keys=('terras','stap','vacht','hout','bank','bench','berk','lantaarn','throw','fur','sheep','tafel','table')
for o in sorted(bpy.data.objects,key=lambda x:x.name):
    n=o.name.lower()
    if any(k in n for k in keys):
        if o.type=='MESH' and len(o.data.vertices):
            b=bb(o); print(f"  {o.name:26s} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}] v={len(o.data.vertices)} {matkind(o)}")
        else:
            print(f"  {o.name:26s} {o.type} loc{tuple(round(v,2) for v in o.location)}")
print("--- ALL top-level mesh objects ---")
tops=sorted(o.name for o in bpy.data.objects if o.type=='MESH' and not o.parent)
print("  count:",len(tops))
for nm in tops: print("   ",nm)
print("MW_END")
