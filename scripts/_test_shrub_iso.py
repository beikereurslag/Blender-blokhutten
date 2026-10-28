import bpy, math
from mathutils import Vector
F = r"C:\Users\beike\Documents\Blender-blokhutten\assets\polyhaven\models\shrub_02_2k.blend"
OUT = r"C:\Users\beike\AppData\Local\Temp\shrub_iso.png"

# clean default scene
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

with bpy.data.libraries.load(F, link=False) as (s, d):
    d.objects = list(s.objects)
objs = [o for o in d.objects if o]
for o in objs:
    bpy.context.scene.collection.objects.link(o)
# keep only variant a LOD0
keep = []
for o in objs:
    if o.type == 'MESH' and "_a_LOD0" in o.name:
        keep.append(o)
    else:
        bpy.data.objects.remove(o, do_unlink=True)
bpy.context.view_layer.update()
cs = []
for o in keep:
    cs += [o.matrix_world @ Vector(c) for c in o.bound_box]
xs=[c.x for c in cs]; ys=[c.y for c in cs]; zs=[c.z for c in cs]
cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2; cz=(min(zs)+max(zs))/2
print("ISO bush bbox dx", round(max(xs)-min(xs),2), "dz", round(max(zs)-min(zs),2))

# sun
sun = bpy.data.lights.new("Sun", 'SUN'); sun.energy = 4
so = bpy.data.objects.new("Sun", sun); bpy.context.scene.collection.objects.link(so)
so.rotation_euler = (math.radians(50), 0, math.radians(30))
# world bg light
w = bpy.data.worlds.new("W"); bpy.context.scene.world = w
w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.6,0.7,0.9,1)
w.node_tree.nodes['Background'].inputs['Strength'].default_value = 1.0

# camera
cam = bpy.data.cameras.new("C"); co = bpy.data.objects.new("C", cam)
bpy.context.scene.collection.objects.link(co)
r = max(max(xs)-min(xs), max(zs)-min(zs)) * 2.2
co.location = (cx + r, cy - r, cz + r*0.4)
d = (Vector((cx,cy,cz)) - co.location).normalized()
co.rotation_euler = d.to_track_quat('-Z','Y').to_euler()
bpy.context.scene.camera = co

sc = bpy.context.scene
sc.render.engine = 'CYCLES'
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type='CUDA'; prefs.get_devices()
    for dv in prefs.devices: dv.use=True
    sc.cycles.device='GPU'
except Exception as e: print(e)
sc.cycles.samples = 32
sc.render.resolution_x = 700; sc.render.resolution_y = 700
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("ISO_DONE", OUT)
