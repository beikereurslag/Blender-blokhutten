import bpy, math
from mathutils import Vector
G = r"C:\Users\beike\Documents\Blender-blokhutten\assets\sketchfab\topiary_hedge\hetz_midget_arborvitae_round_tree_topiary_gltf\scene.gltf"
OUT = r"C:\Users\beike\AppData\Local\Temp\topiary_iso.png"

for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=G)
new = [o for o in bpy.data.objects if o not in before]
bpy.context.view_layer.update()
meshes = [o for o in new if o.type == 'MESH']
cs = []
for o in meshes:
    cs += [o.matrix_world @ Vector(c) for c in o.bound_box]
xs=[c.x for c in cs]; ys=[c.y for c in cs]; zs=[c.z for c in cs]
print("TOPI bbox dx", round(max(xs)-min(xs),3), "dy", round(max(ys)-min(ys),3),
      "dz", round(max(zs)-min(zs),3), "zmin", round(min(zs),3))
print("TOPI nmesh", len(meshes), "names", [o.name for o in meshes][:6])
cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2; cz=(min(zs)+max(zs))/2

sun = bpy.data.lights.new("Sun",'SUN'); sun.energy=4
so=bpy.data.objects.new("Sun",sun); bpy.context.scene.collection.objects.link(so)
so.rotation_euler=(math.radians(50),0,math.radians(30))
w=bpy.data.worlds.new("W"); bpy.context.scene.world=w; w.use_nodes=True
w.node_tree.nodes['Background'].inputs['Color'].default_value=(0.6,0.7,0.9,1)
w.node_tree.nodes['Background'].inputs['Strength'].default_value=1.0
cam=bpy.data.cameras.new("C"); co=bpy.data.objects.new("C",cam)
bpy.context.scene.collection.objects.link(co)
r=max(max(xs)-min(xs),max(zs)-min(zs))*2.2
co.location=(cx+r,cy-r,cz+r*0.4)
dd=(Vector((cx,cy,cz))-co.location).normalized()
co.rotation_euler=dd.to_track_quat('-Z','Y').to_euler()
bpy.context.scene.camera=co
sc=bpy.context.scene; sc.render.engine='CYCLES'
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type='CUDA'; prefs.get_devices()
    for dv in prefs.devices: dv.use=True
    sc.cycles.device='GPU'
except Exception as e: print(e)
sc.cycles.samples=32; sc.render.resolution_x=700; sc.render.resolution_y=700
sc.render.filepath=OUT
bpy.ops.render.render(write_still=True)
print("TOPI_DONE", OUT)
