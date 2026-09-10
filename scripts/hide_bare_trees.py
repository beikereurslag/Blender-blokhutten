"""Herbruikbaar: verberg KALE boom-clusters (takken zonder blad/naald).
Detectie: een tree-cluster (TreeRing_/TreeFillL_/TreeFillR_/RingPine_) met heel weinig
verts (<50k) mist de naaldgeometrie (gezonde pine = miljoenen verts) -> kaal skelet -> verbergen.
Gebruik: blender -b --python hide_bare_trees.py -- <scene.blend> [save?1/0] [png]
"""
import bpy, sys, re, collections
argv = sys.argv[sys.argv.index("--")+1:]
SCENE = argv[0]
SAVE = (len(argv) > 1 and argv[1] == "1")
PNG = argv[2] if len(argv) > 2 else None
bpy.ops.wm.open_mainfile(filepath=SCENE)
scn = bpy.context.scene
clusters = collections.defaultdict(list)
for o in bpy.data.objects:
    if o.type != 'MESH': continue
    m = re.match(r'(TreeRing_\d+|TreeFillL_\d+|TreeFillR_\d+|RingPine_\d+)', o.name)
    if m: clusters[m.group(1)].append(o)
THRESH = 50000
hidden = []
for name, objs in clusters.items():
    verts = sum(len(o.data.vertices) for o in objs)
    if verts < THRESH:
        for o in objs:
            o.hide_render = True; o.hide_viewport = True
        hidden.append((name, verts))
print(f"[bare-trees] {len(clusters)} clusters; {len(hidden)} KAAL verborgen: {[h[0] for h in hidden]}")
if SAVE:
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'CUDA'; prefs.get_devices()
        for dv in prefs.devices: dv.use = True
        scn.cycles.device = 'GPU'
    except Exception as e: print(e)
    scn.cycles.texture_limit_render = '2048'; scn.render.use_persistent_data = False
    cam = scn.camera or bpy.data.objects.get("HeroCam")
    if cam: scn.camera = cam; cam.data.clip_start = 0.02
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=SCENE)
    if PNG:
        scn.render.resolution_x = 1280; scn.render.resolution_y = 720
        scn.cycles.samples = 64; scn.render.filepath = PNG
        bpy.ops.render.render(write_still=True)
        print("[bare-trees] check -> " + PNG)
