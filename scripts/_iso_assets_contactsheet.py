"""Batch ISO-render every downloaded asset to a contact sheet, to catch broken
materials (magenta / invisible alpha / wrong scale) BEFORE per-scene swaps.
Run headless:
  blender --background --python scripts/_iso_assets_contactsheet.py
Writes one small thumb per asset to %TEMP%\iso_assets\ then montages them.
"""
import bpy, math, os
from mathutils import Vector

ROOT = r"C:\Users\beike\Documents\Blender-blokhutten"
A = ROOT + r"\assets\sketchfab"
PH = ROOT + r"\assets\polyhaven\models"
OUTDIR = os.path.join(os.environ.get("TEMP", ROOT), "iso_assets")
os.makedirs(OUTDIR, exist_ok=True)

ASSETS = [
    ("tea_set",        A + r"\tableware\tea_set.blend", "blend"),
    ("mug",            A + r"\tableware\mug.blend", "blend"),
    ("french_press",   A + r"\tableware\french_press.blend", "blend"),
    ("plate",          A + r"\tableware\plate.blend", "blend"),
    ("wine_set",       A + r"\tableware\wine_set.blend", "blend"),
    ("throw_sheepskin",A + r"\textiles\throw_sheepskin.blend", "blend"),
    ("firewood_stack", A + r"\decor\firewood_stack.blend", "blend"),
    ("book",           A + r"\decor\book.blend", "blend"),
    ("rain_barrel",    A + r"\decor\rain_barrel.blend", "blend"),
    ("solar_panel",    A + r"\energy\solar_panel.blend", "blend"),
    ("office_desk",    A + r"\furniture\office_desk.blend", "blend"),
    ("hot_tub_scandi", A + r"\spa\hot_tub_scandi.blend", "blend"),
    ("towel_stack",    A + r"\spa\towel_stack.blend", "blend"),
    ("towel_folded",   A + r"\spa\towel_folded.blend", "blend"),
    ("spa_step",       A + r"\spa\spa_step.blend", "blend"),
    ("lamp_2",         A + r"\lighting\lamp_2.blend", "blend"),
    ("lamp_3",         A + r"\lighting\lamp_3.blend", "blend"),
    ("garden_lamp",    A + r"\lighting\garden_lamp.blend", "blend"),
    ("watering_can",   A + r"\uncategorized\blender\Blender\Watering_Can.blend", "blend"),
    ("tachka",         A + r"\tools\tachka.blend", "blend"),
    ("axe",            A + r"\tools\axe_fab_blend\axe.blend", "blend"),
    ("moss_01",        PH + r"\moss_01_2k.blend", "blend"),
    ("topiary",        A + r"\topiary_hedge\hetz_midget_arborvitae_round_tree_topiary_gltf\scene.gltf", "gltf"),
    ("goldmound",      A + r"\flowering_bushes\goldmound_spiraea_red_flowering_gltf\scene.gltf", "gltf"),
]

def fresh():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)

def setup_env():
    sun = bpy.data.lights.new("Sun", 'SUN'); sun.energy = 3.5
    so = bpy.data.objects.new("Sun", sun); bpy.context.scene.collection.objects.link(so)
    so.rotation_euler = (math.radians(52), 0, math.radians(35))
    w = bpy.data.worlds.new("W"); bpy.context.scene.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (0.62, 0.70, 0.85, 1)
    bg.inputs['Strength'].default_value = 1.0

def frame_and_render(meshes, out):
    bpy.context.view_layer.update()
    cs = []
    for o in meshes:
        if o.type == 'MESH' and len(o.data.vertices):
            cs += [o.matrix_world @ Vector(c) for c in o.bound_box]
    if not cs:
        print("NOGEO", out); return None
    xs=[c.x for c in cs]; ys=[c.y for c in cs]; zs=[c.z for c in cs]
    cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2; cz=(min(zs)+max(zs))/2
    span = max(max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs))
    cam = bpy.data.cameras.new("C"); co = bpy.data.objects.new("C", cam)
    bpy.context.scene.collection.objects.link(co)
    r = span * 1.9 + 0.5
    co.location = (cx + r, cy - r, cz + r*0.45)
    d = (Vector((cx,cy,cz)) - co.location).normalized()
    co.rotation_euler = d.to_track_quat('-Z','Y').to_euler()
    bpy.context.scene.camera = co
    sc = bpy.context.scene; sc.render.engine = 'CYCLES'
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type='CUDA'; prefs.get_devices()
        for dv in prefs.devices: dv.use=True
        sc.cycles.device='GPU'
    except Exception as e: print("dev", e)
    sc.cycles.samples = 24
    sc.cycles.texture_limit_render = '1024'
    sc.render.resolution_x = 360; sc.render.resolution_y = 360
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    return (round(max(xs)-min(xs),2), round(max(ys)-min(ys),2), round(max(zs)-min(zs),2))

thumbs = []
for label, path, kind in ASSETS:
    fresh(); setup_env()
    if not os.path.exists(path):
        print("MISSING", label, path); continue
    before = set(bpy.data.objects)
    try:
        if kind == "blend":
            with bpy.data.libraries.load(path, link=False) as (s, d):
                d.objects = list(s.objects)
            new = [o for o in d.objects if o]
            for o in new: bpy.context.scene.collection.objects.link(o)
        else:
            bpy.ops.import_scene.gltf(filepath=path)
            new = [o for o in bpy.data.objects if o not in before]
        out = os.path.join(OUTDIR, label + ".png")
        dims = frame_and_render([o for o in new], out)
        print("ASSET", label, "dims", dims, "nobj", len(new))
        if dims: thumbs.append((label, out))
    except Exception as e:
        print("FAIL", label, e)

try:
    from PIL import Image, ImageDraw
    cols = 5
    cell = 360; pad = 6; labelh = 18
    rows = (len(thumbs) + cols - 1) // cols
    W = cols*(cell+pad)+pad; H = rows*(cell+labelh+pad)+pad
    sheet = Image.new("RGB", (W, H), (40,40,46))
    dr = ImageDraw.Draw(sheet)
    for i,(label,p) in enumerate(thumbs):
        r=i//cols; c=i%cols
        x=pad+c*(cell+pad); y=pad+r*(cell+labelh+pad)
        try:
            im=Image.open(p).convert("RGB"); sheet.paste(im,(x,y+labelh))
        except Exception as e: print("paste",label,e)
        dr.text((x+2,y+3), label, fill=(235,235,235))
    sheetpath = os.path.join(OUTDIR, "_CONTACT_SHEET.png")
    sheet.save(sheetpath)
    print("CONTACT_SHEET", sheetpath)
except Exception as e:
    print("montage failed", e)
print("ISO_BATCH_DONE")
