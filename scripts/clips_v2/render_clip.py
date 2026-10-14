r"""Clips-v2 render-engine. Laadt een scene-blend, past de registry-tweaks toe (fixronde-instellingen
die niet in de blend staan), bouwt de shots (uit shots/<scene>.py of het standaardrecept), toetst elke
shot aan het hero-beeld (frame_score) en rendert.

  blender -b <blend> --python render_clip.py -- <scene> probe <uitmap>      begin/eind-still per shot, 960x540/24
  blender -b <blend> --python render_clip.py -- <scene> full  <uitmap>      PNG-reeksen 1920x1080/48, hervatbaar
  blender -b <blend> --python render_clip.py -- <scene> toets <uitmap>      alleen de hero-toets, geen render
  ... [--shots A_reveal,B_push] [--force]

Blend wordt NOOIT opgeslagen. Elke shot krijgt een <uitmap>/<shot>_score.json met de toets.
"""
import glob
import json
import math
import os
import re
import sys

import bpy
from mathutils import Vector

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import geo  # noqa: E402
import scenes  # noqa: E402
import shotlib  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
SCENE, MODE, UITMAP = argv[0], argv[1], os.path.abspath(argv[2])
ALLEEN = None
FORCE = "--force" in argv
if "--shots" in argv:
    ALLEEN = set(argv[argv.index("--shots") + 1].split(","))
FPS = 24
os.makedirs(UITMAP, exist_ok=True)

scn = bpy.context.scene
reg = scenes.alle()[SCENE]


def log(m):
    print(f"[clip] {m}", flush=True)


# ------------------------------------------------------------------ tweaks (uit _fixronde/fixround.py)
def apply_tweaks(tw):
    if not tw:
        return
    zonnen = [o for o in bpy.data.objects if o.type == 'LIGHT' and o.data.type == 'SUN']
    if "exposure" in tw:
        scn.view_settings.exposure = tw["exposure"]
    if "look" in tw:
        scn.view_settings.look = tw["look"]
    for z in zonnen:
        if "sun_energy" in tw:
            z.data.energy = tw["sun_energy"]
        if "sun_angle" in tw:
            z.data.angle = math.radians(tw["sun_angle"])
        if "sun_rot" in tw:
            z.rotation_euler = tuple(math.radians(v) for v in tw["sun_rot"])
    if "world_strength" in tw and scn.world and scn.world.use_nodes:
        for n in scn.world.node_tree.nodes:
            if n.type == 'BACKGROUND' and not n.inputs['Strength'].is_linked:
                n.inputs['Strength'].default_value = tw["world_strength"]
    for sub, waarden in (tw.get("mats") or {}).items():
        for m in bpy.data.materials:
            if sub.lower() in m.name.lower() and m.use_nodes:
                for n in m.node_tree.nodes:
                    if n.type == 'BSDF_PRINCIPLED':
                        for k, v in waarden.items():
                            i = n.inputs.get(k)
                            if i is not None and not i.is_linked:
                                i.default_value = v
    if "fill_canopy" in tw:
        fc = tw["fill_canopy"]
        pts = [o.matrix_world @ Vector(c) for o in bpy.data.objects if o.type == 'MESH'
               and re.match(r"^wall-(openEnded-)?\d+-board", o.name)
               and any(m and 'canopy' in m.name.lower() for m in o.data.materials) for c in o.bound_box]
        if pts:
            xs, ys, zs = [p.x for p in pts], [p.y for p in pts], [p.z for p in pts]
            cam = scn.camera.matrix_world.translation
            cx, cy, ztop = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, max(zs)
            richting = Vector((cam.x - cx, cam.y - cy, 0)).normalized()
            pos = Vector((cx, cy, 0)) + richting * fc.get("diepte", 1.2)
            ld = bpy.data.lights.new("L_FixFill", 'AREA')
            ld.energy, ld.size, ld.shape = fc.get("energy", 60), fc.get("size", 2.5), 'SQUARE'
            ld.color = tuple(fc.get("color", (1.0, 0.95, 0.9)))
            lo = bpy.data.objects.new("L_FixFill", ld)
            scn.collection.objects.link(lo)
            lo.location = (pos.x, pos.y, ztop - fc.get("onder_dak", 0.12))
            log(f"fill_canopy op {tuple(round(v, 2) for v in lo.location)}")
    log(f"tweaks toegepast: {tw}")


apply_tweaks(reg.get("tweaks"))


# ------------------------------------------------------------------ ontbrekende textures
# Een image-texture die naar een niet-bestaand bestand wijst rendert zwart, en dat haalt het hele
# materiaal onderuit: bij jasmijn_vinylmiddag wijzen de metalen delen van de platenspeler naar de
# schijf van de oorspronkelijke maker (...BlenderProgects/винил/...) en lossen hier nooit op. De
# blend wordt nooit opgeslagen, dus dit is een runtime-reparatie: de kapotte tak eruit, en de
# Principled terug op zijn eigen waarde zodat het vlak metaal wordt i.p.v. zwart plastic.
HERSTEL = {'Roughness': 0.25, 'Metallic': 1.0, 'Specular IOR Level': 0.5, 'Alpha': 1.0,
           'Base Color': (0.55, 0.55, 0.57, 1.0), 'Emission Strength': 0.0}


def fix_missing_textures():
    kapot = set()
    paden = []
    for im in bpy.data.images:
        if im.source not in ('FILE', 'SEQUENCE') or im.packed_file:
            continue
        p = bpy.path.abspath(im.filepath, library=im.library)
        if p and not os.path.exists(p):
            kapot.add(im.name)
            paden.append(os.path.normpath(p))
    if not kapot:
        return
    for p in sorted(paden):
        log(f"  ONTBREEKT: {p}")
    los = []
    for m in bpy.data.materials:
        if not m.use_nodes or not m.node_tree:
            continue
        nt = m.node_tree
        for n in [x for x in nt.nodes if x.type == 'TEX_IMAGE' and x.image and x.image.name in kapot]:
            for out in n.outputs:
                for lk in list(out.links):
                    doel, sok = lk.to_node, lk.to_socket
                    nt.links.remove(lk)
                    if doel.type == 'BSDF_PRINCIPLED' and sok.name in HERSTEL:
                        sok.default_value = HERSTEL[sok.name]
                    los.append(f"{m.name}:{sok.name}")
    log(f"ontbrekende textures: {len(kapot)} image(s) {sorted(kapot)[:8]} -> {len(los)} link(s) losgemaakt {los[:8]}")


fix_missing_textures()

# clips zijn 16:9; de S/B-finals zijn 4:3 (2560x1920) -> de 16:9-uitsnede van dezelfde camera is een deelverzameling
# van het goedgekeurde beeld. Eerst zetten, dan pas de Ctx (frame_score en w2cv gebruiken deze verhouding).
if MODE in ("probe", "toets"):
    scn.render.resolution_x, scn.render.resolution_y = 960, 540
else:
    scn.render.resolution_x, scn.render.resolution_y = 1920, 1080
scn.render.resolution_percentage = 100

# camera zonder parent: keys zijn wereldcoördinaten
if scn.camera.parent:
    _mw = scn.camera.matrix_world.copy()
    scn.camera.parent = None
    scn.camera.matrix_world = _mw

# ------------------------------------------------------------------ context + shots
ctx = geo.Ctx()
hs = ctx.hero_score
log(f"hero: cam {geo.r3(ctx.loc)} lens {ctx.lens:.0f} doel {geo.r3(ctx.doel)} ground={hs['ground']} sky={hs['sky']}")

shots_mod = None
try:
    import importlib
    shots_mod = importlib.import_module(f"shots.{SCENE}")
except ModuleNotFoundError:
    pass
if shots_mod and hasattr(shots_mod, "shots"):
    SHOTS = shots_mod.shots(ctx, shotlib)
    log(f"shots uit shots/{SCENE}.py ({len(SHOTS)})")
else:
    SHOTS = shotlib.default_recipe(ctx)
    log(f"standaardrecept ({len(SHOTS)})")
if ALLEEN:
    SHOTS = [s for s in SHOTS if s['naam'] in ALLEEN]

cam = ctx.cam
cd = cam.data
dof_aan = cd.dof.use_dof
focus_orig = cd.dof.focus_distance


def matrix_van(key):
    from mathutils import Matrix
    return Matrix.Translation(key['loc']) @ key['rot'].to_matrix().to_4x4()


def toets(shot):
    """frame_score op begin en eind; drempels t.o.v. het hero-beeld."""
    uit = []
    ok = True
    for i, k in enumerate(shot['keys']):
        s = ctx.frame_score(matrix_van(k), k['lens'], k.get('shift_x', ctx.shift[0]), k['shift_y'])
        s['blocked'] = bool(ctx.blocked(k['loc'], k['loc'] + (k['rot'].to_quaternion() @ Vector((0, 0, -1))) * k['focus']))
        red = []
        if s['inside'] < 0.90:
            red.append(f"inside {s['inside']}")
        if s['void'] > hs['void'] + 0.01:   # hero heeft soms 1 straal op de horizonrand (0.002); pas melden bij echt gat
            red.append(f"void {s['void']}")
        if s['sky'] > hs['sky'] + 0.10:
            red.append(f"sky {s['sky']} (hero {hs['sky']})")
        if s['ground'] > hs['ground'] + 0.15:
            red.append(f"ground {s['ground']} (hero {hs['ground']})")
        if s['blocked']:
            red.append("blik geblokkeerd")
        s['problemen'] = red
        ok = ok and not red
        uit.append(s)
    return ok, uit


def zet(key):
    cam.location = key['loc']
    cam.rotation_euler = key['rot']
    cd.lens = key['lens']
    cd.shift_x = key.get('shift_x', ctx.shift[0])
    cd.shift_y = key['shift_y']
    if dof_aan:
        cd.dof.focus_distance = key['focus']


def keyframe(frame):
    cam.keyframe_insert('location', frame=frame)
    cam.keyframe_insert('rotation_euler', frame=frame)
    cd.keyframe_insert('lens', frame=frame)
    cd.keyframe_insert('shift_x', frame=frame)
    cd.keyframe_insert('shift_y', frame=frame)
    if dof_aan:
        cd.dof.keyframe_insert('focus_distance', frame=frame)


def reset_cam():
    cam.animation_data_clear()
    cd.animation_data_clear()
    cam.location = ctx.loc
    cam.rotation_euler = ctx.rot
    cd.lens = ctx.lens
    cd.shift_x = ctx.shift[0]
    cd.shift_y = ctx.shift[1]
    cd.dof.focus_distance = focus_orig
    # VERPLICHT: ctx.in_hero() projecteert met world_to_camera_view op de LEVENDE camera, niet op de
    # opgeslagen hero-matrix. Zonder deze update leest matrix_world nog de laatste render-stand van de
    # vorige shot, en dan wordt er tegen een verkeerd 'hero-beeld' getoetst. Dat trof elke C-shot: die
    # volgt op B_push, die eindigt op hero + 10 %, waardoor het echte hero-beeld zelf 0,804 scoorde
    # (camelia_wijnterras C_zoom key0, terwijl hero_score.inside = 1,0 met identieke beeldinhoud).
    bpy.context.view_layer.update()


# ------------------------------------------------------------------ render-instellingen
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'
    prefs.get_devices()
    for dv in prefs.devices:
        dv.use = dv.type in ('OPTIX', 'CPU')
    scn.cycles.device = 'GPU'
except Exception as e:
    log(f"gpu: {e}")
scn.render.engine = 'CYCLES'
scn.render.resolution_percentage = 100
scn.render.use_border = False
scn.cycles.use_adaptive_sampling = True
scn.cycles.use_denoising = True
# Geen persistent data, ook niet in full. Het scheelt per frame een BVH-herbouw, maar het houdt de hele
# scene tussen frames in VRAM en dat past niet: met de GUI-Blender en het bureaublad erbij stond de 3070 op
# 7,26 van 8 GB, 100 % bezet bij 80 W (= SM's die op geheugen staan te wachten) en ~60 s per frame.
# Gemeten 4 sep, zie _probe/_persist_test.md; back-up van de oude versie: _probe/render_clip_voor_persistfix.py.bak
scn.render.use_persistent_data = False
scn.use_nodes = False
scn.render.image_settings.file_format = 'PNG'
scn.render.image_settings.color_depth = '8'
scn.render.fps = FPS
if MODE in ("probe", "toets"):
    scn.cycles.samples = 24
    scn.cycles.adaptive_threshold = 0.05
    scn.cycles.texture_limit_render = '1024'
else:
    scn.cycles.samples = 48
    scn.cycles.adaptive_threshold = 0.02
    scn.cycles.texture_limit_render = '2048'

fstop_orig = cd.dof.aperture_fstop
overzicht = []
for sh in SHOTS:
    naam = sh['naam']
    reset_cam()
    ok, scores = toets(sh)
    with open(os.path.join(UITMAP, f"{naam}_score.json"), 'w', encoding='utf-8') as fh:
        json.dump(dict(shot=naam, frames=sh['frames'], ok=ok, hero=hs, keys=scores,
                       cam=[dict(loc=geo.r3(k['loc']), yaw_deg=round(math.degrees(k['rot'].z), 1), lens=round(k['lens'], 1),
                                 shift_y=round(k['shift_y'], 3), shift_x=round(k.get('shift_x', 0.0), 3),
                                 focus=round(k['focus'], 2)) for k in sh['keys']]), fh, indent=1)
    status = "OK " if ok else "LET OP"
    log(f"{naam}: {status} inside {[s['inside'] for s in scores]} ground {[s['ground'] for s in scores]} "
        f"sky {[s['sky'] for s in scores]} problemen {[s['problemen'] for s in scores]}")
    overzicht.append((naam, ok))
    if MODE == "toets":   # alleen de toets: geen render, geen VRAM, kost alleen het laden van de blend
        continue
    if not ok and MODE == "full" and not FORCE:
        log(f"{naam}: OVERGESLAGEN (faalt de hero-toets; --force om toch te renderen)")
        continue

    cd.dof.aperture_fstop = fstop_orig
    if sh.get('fstop_max') and dof_aan and cd.dof.aperture_fstop > sh['fstop_max']:
        cd.dof.aperture_fstop = sh['fstop_max']
    if MODE == "probe":
        for kant, k in zip(("begin", "eind"), sh['keys']):
            pad = os.path.join(UITMAP, f"{naam}_{kant}.png")
            if os.path.exists(pad) and not FORCE:
                continue
            zet(k)
            bpy.context.view_layer.update()
            scn.render.filepath = pad
            bpy.ops.render.render(write_still=True)
            log(f"{naam} {kant} -> {os.path.basename(pad)}")
    else:
        laatste = os.path.join(UITMAP, f"{naam}_{sh['frames']:04d}.png")
        if os.path.exists(laatste) and not FORCE:
            log(f"{naam}: al compleet, overslaan")
            continue
        # Hervatten per frame i.p.v. per shot (4 sep). Blender slaat met use_overwrite=False
        # frames over die er al staan; zonder dit begon een watchdog-herstart de shot weer bij
        # frame 1 en gooide tot 120 gerenderde frames weg (~2 uur). Het nieuwste frame kan half
        # weggeschreven zijn als het proces midden in een write stierf - dat gooien we dus weg,
        # zodat er hoogstens een frame opnieuw moet i.p.v. de hele shot.
        scn.render.use_overwrite = bool(FORCE)
        scn.render.use_placeholder = False
        if not FORCE:
            al = sorted(glob.glob(os.path.join(UITMAP, f"{naam}_[0-9][0-9][0-9][0-9].png")))
            if al:
                os.remove(al[-1])
                log(f"{naam}: hervat, {len(al) - 1} frames blijven staan (nieuwste weggegooid)")
        zet(sh['keys'][0])
        keyframe(1)
        zet(sh['keys'][1])
        keyframe(sh['frames'])
        scn.frame_start, scn.frame_end = 1, sh['frames']
        scn.render.filepath = os.path.join(UITMAP, f"{naam}_")
        log(f"{naam}: {sh['frames']} frames...")
        bpy.ops.render.render(animation=True)
        log(f"{naam}: KLAAR")

# toets-mode schrijft bewust NIET _shots.json: run_stills_all.sh slaat scenes met dat bestand over
with open(os.path.join(UITMAP, "_toets.json" if MODE == "toets" else "_shots.json"), 'w', encoding='utf-8') as fh:
    json.dump(dict(scene=SCENE, mode=MODE, shots=[dict(naam=n, ok=o, frames=next(s['frames'] for s in SHOTS if s['naam'] == n))
                                                   for n, o in overzicht]), fh, indent=1)
log(f"SCENE KLAAR ({MODE}; blend niet opgeslagen)")
