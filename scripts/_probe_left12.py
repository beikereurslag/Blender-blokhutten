"""Scene 12 - wat is het GRIJZE links van de hut? Lijst alle objecten met zwaartepunt
in de scherm-linker voorgrond (wereld +x, y>-1) + materiaal/kleur, plus alle grote
platte vlakken (2e grond?). Render daarna een linker-crop."""
import sys, bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
sys.path.insert(0, r"C:\Users\beike\Documents\Blender-blokhutten\scripts")
import swap_lib as sl
D = sl.ROOT + r"\pilots\Magnolia-300x200\style-scandi"
scn = sl.open_scene(D + r"\magnolia_wintertuin_v4.blend")
cam = scn.camera
def wbb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]
    return (min(c.x for c in cs),max(c.x for c in cs),min(c.y for c in cs),max(c.y for c in cs),min(c.z for c in cs),max(c.z for c in cs))
def col(o):
    if o.material_slots and o.material_slots[0].material and o.material_slots[0].material.use_nodes:
        b=next((n for n in o.material_slots[0].material.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if b: return [round(v,2) for v in b.inputs['Base Color'].default_value[:3]], b.inputs['Base Color'].is_linked
    return None,None
SKIP=("wall-","roof","fascia","trim-","parentboard","flatroof",".scharnier",".doorhandle",".deurbasic","hedge_","mist","sun")
print("\n==== SCHERM-LINKER VOORGROND objecten (screen x<0.45) ====")
for o in bpy.data.objects:
    if o.type!='MESH' or not len(o.data.vertices) or o.hide_render: continue
    if any(k in o.name.lower() for k in SKIP): continue
    b=wbb(o); c=Vector(((b[0]+b[1])/2,(b[2]+b[3])/2,(b[4]+b[5])/2))
    sc=world_to_camera_view(scn,cam,c)
    if not (-0.05<sc.x<0.48 and -0.05<sc.y<1.05 and sc.z>0): continue
    cc,linked=col(o)
    print(f"  scrX={sc.x:.2f} {o.name:<26} world x[{b[0]:.1f},{b[1]:.1f}] y[{b[2]:.1f},{b[3]:.1f}] z[{b[4]:.2f},{b[5]:.2f}] "
          f"col={cc} {'LINK' if linked else ''} mat={o.material_slots[0].material.name if o.material_slots and o.material_slots[0].material else '-'}")
print("==== end\n")
# linker-crop
scn.render.use_border=True; scn.render.use_crop_to_border=True
scn.render.border_min_x=0.0; scn.render.border_max_x=0.45; scn.render.border_min_y=0.0; scn.render.border_max_y=0.55
scn.render.resolution_x=1280; scn.render.resolution_y=720; scn.cycles.samples=100
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences; prefs.compute_device_type='CUDA'; prefs.get_devices()
    for dv in prefs.devices: dv.use=True
    scn.cycles.device='GPU'
except Exception as e: print(e)
scn.cycles.texture_limit_render='2048'
scn.render.filepath=D+r"\_mw_LINKS_crop.png"
bpy.ops.render.render(write_still=True)
print("crop -> "+scn.render.filepath)
