import bpy, sys

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
hdri = argv[0]
strength = float(argv[1]) if len(argv) > 1 else 1.0

world = bpy.context.scene.world
world.use_nodes = True
nt = world.node_tree

env = next((n for n in nt.nodes if n.type == 'TEX_ENVIRONMENT'), None)
bg = next((n for n in nt.nodes if n.type == 'BACKGROUND'), None)
print("CUR env:", (env.image.name if env and env.image else None),
      "| bg strength:", (round(bg.inputs['Strength'].default_value, 2) if bg else None))
for o in bpy.data.objects:
    if o.type == 'LIGHT' and o.data.type == 'SUN':
        print(f"SUN: {o.name} energy={o.data.energy} rot={[round(a,2) for a in o.rotation_euler]}")

img = bpy.data.images.load(hdri, check_existing=True)

out = next((n for n in nt.nodes if n.type == 'OUTPUT_WORLD'), None)
if env is None:
    env = nt.nodes.new('ShaderNodeTexEnvironment')
if bg is None:
    bg = nt.nodes.new('ShaderNodeBackground')
if out is None:
    out = nt.nodes.new('ShaderNodeOutputWorld')
nt.links.new(env.outputs['Color'], bg.inputs['Color'])
nt.links.new(bg.outputs['Background'], out.inputs['Surface'])
env.image = img
bg.inputs['Strength'].default_value = strength

print("NEW env:", env.image.name, "| strength:", strength)
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print("HDRI_DONE")
