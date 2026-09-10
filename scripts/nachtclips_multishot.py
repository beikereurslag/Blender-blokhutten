"""Vakantierun 6-11 aug (Beike: "laat alles als filmpje renderen; je mag
creatief worden en experimenteren"). Per scène een eigen drieluik van
rustige camerabewegingen rond de bestaande hero-camera — klein genoeg om
binnen de aangeklede zone te blijven. Plus experiment-varianten:
focus-pull (rack focus), zon-sweep (licht verloopt tijdens de shot) en
longform (4 shots).

1920x1080, 24 fps, 48 samples + denoise -> PNG-reeksen (Blender 5.1 heeft
geen video-uitvoer meer; encode apart met cv2). Hervatbaar: complete shots
worden overgeslagen. NIET saven: keyframes blijven uit het blend.

  blender -b <blend> --python nachtclips_multishot.py -- <framemap> [variant]
"""
import math
import os
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
UITMAP = argv[0]
VARIANT = argv[1] if len(argv) > 1 else None
FPS = 24

scn = bpy.context.scene
cam = scn.camera
assert cam, "scene heeft geen actieve camera"
cam.rotation_mode = 'XYZ'
bpy.context.view_layer.update()

basis = cam.location.copy()
kijk = (cam.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -1.0))).normalized()

# kijkdoel: DOF-object > DOF-afstand > 8 m langs de kijkas
doel = None
try:
    d = cam.data.dof
    if d.use_dof and d.focus_object:
        doel = d.focus_object.matrix_world.translation.copy()
    elif d.use_dof and d.focus_distance > 0.5:
        doel = basis + kijk * d.focus_distance
except Exception:
    pass
if doel is None:
    doel = basis + kijk * 8.0
rechts = kijk.cross(Vector((0, 0, 1))).normalized()
doel_afstand = (doel - basis).length
print(f"[nacht] cam {cam.name} @ ({basis.x:.2f},{basis.y:.2f},{basis.z:.2f}) "
      f"doel ({doel.x:.2f},{doel.y:.2f},{doel.z:.2f}) afst {doel_afstand:.1f}")


# ---------------------------------------------------------------- bouwstenen
# een shot is een dict: p0/p1 (posities), herricht (blik op doel houden),
# frames, focus=(van_m, naar_m) of zon=(elev0, elev1) optioneel.
def S(p0, p1, herricht, frames=96, focus=None, zon=None):
    return dict(p0=p0, p1=p1, herricht=herricht, frames=frames,
                focus=focus, zon=zon)


def dolly_in(d=0.80, **kw):
    return S(basis, basis + kijk * d, False, **kw)


def dolly_uit(d=0.80, **kw):
    return S(basis + kijk * d, basis, False, **kw)


def truck(breedte=0.85, lr=True, **kw):
    a, b = -rechts * breedte, rechts * breedte
    if not lr:
        a, b = b, a
    return S(basis + a, basis + b, True, **kw)


def arc(breedte=0.95, lr=True, diepte=0.30, **kw):
    a, b = -rechts * breedte, rechts * breedte
    if not lr:
        a, b = b, a
    return S(basis + a, basis + b + kijk * diepte, True, **kw)


def crane_op(van=-0.15, naar=0.45, **kw):
    return S(basis + Vector((0, 0, van)), basis + Vector((0, 0, naar)), True, **kw)


def crane_neer(van=0.50, naar=-0.10, **kw):
    return crane_op(van, naar, **kw)


def push(fractie=0.25, **kw):
    v = doel - basis
    afst = min(v.length * fractie, 1.6)
    return S(basis, basis + v.normalized() * afst, True, **kw)


def focus_pull(van=1.6, frames=144, **kw):
    """Statische camera; scherpte glijdt van dichtbij naar het kijkdoel."""
    return S(basis, basis, False, frames=frames,
             focus=(van, doel_afstand), **kw)


# --------------------------------------------- echte hoekvariatie (7 aug)
# Beike: "alle filmpjes blijven in dezelfde hoek" -> per scène twee écht
# andere standpunten: camera-positie geroteerd om het kijkdoel (Z-as),
# zelfde straal/hoogte, opnieuw gericht. Raycast-guard voorkomt dat de
# camera in een heg/boom/wand belandt.
def _orbit_pos(graden, rf=1.0, dz=0.0):
    v = basis - doel
    a = math.radians(graden)
    rx = v.x * math.cos(a) - v.y * math.sin(a)
    ry = v.x * math.sin(a) + v.y * math.cos(a)
    return Vector((doel.x + rx * rf, doel.y + ry * rf,
                   max(basis.z + dz, 0.9)))


def _hoek_vrij(graden, dz=0.0):
    """True als het zicht vanaf deze orbit-positie niet vlak voor de lens
    geblokkeerd is (eerste hit pas voorbij 45% van de doel-afstand)."""
    p = _orbit_pos(graden, dz=dz)
    dg = bpy.context.evaluated_depsgraph_get()
    d = doel - p
    hit, loc, _n, _i, _o, _m = scn.ray_cast(dg, p, d.normalized(),
                                            distance=d.length)
    return (not hit) or ((Vector(loc) - p).length > 0.45 * d.length)


def veilige_hoek(graden, dz=0.0):
    """Verklein de orbit-hoek in stappen van 8 graden tot het zicht vrij is."""
    teken = 1 if graden >= 0 else -1
    g = abs(graden)
    while g > 12 and not _hoek_vrij(teken * g, dz=dz):
        print(f"[nacht] hoek {teken * g} geblokkeerd -> {teken * (g - 8)}")
        g -= 8
    return teken * g


def orbit(g0, g1, rf0=1.0, rf1=1.0, dz=0.0, **kw):
    return S(_orbit_pos(g0, rf0, dz), _orbit_pos(g1, rf1, dz), True, **kw)


# ------------------------------------------------- eigen taal per scène
VARIANTEN = {
    "kapschuur_a": [dolly_in(0.85), arc(lr=False), crane_op()],
    "kapschuur_b": [dolly_uit(0.85), truck(0.90), push(0.22)],
    "wellness":    [arc(lr=True), push(0.28), crane_neer()],
    "keuken":      [truck(1.30, lr=False), dolly_in(0.90), crane_op()],
    "bioscoop":    [push(0.25), crane_op(-0.30, 0.35), arc(lr=False)],
    "pluktuin":    [dolly_in(0.80), arc(lr=True), crane_op()],
    "vuurtafel":   [push(0.30), arc(lr=False), crane_neer()],
    # ronde 2
    "speelhuismiddag": [push(0.22), truck(0.85), crane_op()],
    "uitslaapochtend": [dolly_in(0.80), arc(lr=False), push(0.25)],
    "vlindertuin": [arc(lr=True), crane_neer(), dolly_in(0.80)],
    "zonnegroet":  [crane_op(-0.35, 0.35), dolly_in(0.85), arc(lr=False)],
    "bergkap":     [dolly_uit(0.90), arc(lr=True), crane_op()],
    "zwembad":     [truck(1.20), push(0.28), crane_neer()],
    # vakantierun: S-ronde
    "familiemiddag":   [dolly_in(0.85), arc(lr=True), push(0.22)],
    "goudenborrel":    [push(0.25), crane_neer(), truck(0.90, lr=False)],
    "atelier":         [dolly_uit(0.80), push(0.25), crane_op()],
    "zomerselunch":    [arc(lr=True), dolly_in(0.80), crane_op()],
    "tuinwerkzaterdag": [truck(0.95), push(0.22), arc(lr=False)],
    "ochtendkoffie":   [crane_op(-0.30, 0.35), push(0.25), truck(0.85, lr=False)],
    "leesplek":        [dolly_in(0.80), crane_neer(), arc(lr=True)],
    "goudenuur":       [arc(lr=False), dolly_in(0.85), crane_neer()],
    # vakantierun: stijlen
    "leeshoek":        [push(0.24), arc(lr=True), crane_op()],
    "tuinkantoor":     [dolly_in(0.85), truck(0.90, lr=False), push(0.24)],
    "lavendelveld":    [truck(1.10), arc(lr=True), crane_op()],
    "avondkubus":      [dolly_uit(0.90), crane_op(-0.30, 0.40), push(0.24)],
    "ochtendnevel":    [dolly_in(0.70), arc(lr=False), crane_op()],
    "zonnebloem_modern": [arc(lr=True), push(0.24), crane_neer()],
}
# webshop-concepten e.d. zonder eigen entry: gevarieerde standaard-pool,
# deterministisch gekozen op bestandsnaam
POOL = [
    [dolly_in(0.80), truck(0.90), crane_op()],
    [push(0.24), arc(lr=True), crane_op()],
    [dolly_uit(0.85), arc(lr=False), push(0.22)],
    [truck(1.00, lr=False), dolly_in(0.85), crane_neer()],
]

# ------------------------------------------------- experiment-varianten
EXPERIMENTEN = {
    # rack focus door de ochtendmist, dan pas bewegen
    "focuspull": [focus_pull(1.6, frames=144), dolly_in(0.85), arc(lr=False)],
    # licht verloopt tijdens de shots (gouden uur -> schemer), 2 lange shots
    "zonsweep": [dolly_in(0.90, frames=144, zon=(12.0, 5.0)),
                 arc(lr=False, frames=144, zon=(5.0, 1.5))],
    # 16 s suite van 4 shots
    "longform": [dolly_in(0.85), truck(0.90), push(0.26), crane_op()],
    # scherpte-opener + diepe push het vignet in
    "ochtendpush": [focus_pull(1.8, frames=120), push(0.35, frames=120),
                    truck(0.80)],
}

pad = os.path.basename(bpy.data.filepath).lower()
if VARIANT:
    gekozen, label = EXPERIMENTEN[VARIANT], f"experiment:{VARIANT}"
else:
    # shot A = de hero-beweging van de scène (uit VARIANTEN of de pool);
    # shot B/C = orbits naar écht andere standpunten, hoeken per scène
    # gevarieerd (hash) en geklemd door de raycast-guard
    hero, label = None, "pool"
    for key, shots in VARIANTEN.items():
        if key in pad:
            hero, label = shots[0], key
            break
    h = sum(ord(c) for c in pad)
    if hero is None:
        hero = POOL[h % len(POOL)][0]
    links = veilige_hoek(-(28 + h % 14))
    rechts = veilige_hoek(28 + (h // 3) % 14, dz=0.35)
    gekozen = [
        hero,
        orbit(links - 5, links + 5),                      # standpunt links
        orbit(rechts + 5, rechts - 5, rf1=0.92, dz=0.35),  # rechts, licht erin
    ]
    label += f" +orbits({links},{rechts})"

SHOTS = [(f"{chr(65 + i)}_shot_", sh) for i, sh in enumerate(gekozen)]
BESPOKE_DOEL = {}
if "schaakavond" in pad and not VARIANT:
    label = "bespoke-B13"
    SHOTS = [
        ("A_hero_", S(Vector((-5.50, 7.00, 1.40)), Vector((-5.02, 6.25, 1.40)), False)),
        ("B_zij_", S(Vector((-6.80, 2.20, 1.35)), Vector((-6.35, 4.40, 1.35)), 'bespoke')),
        ("C_close_", S(Vector((-3.55, 3.70, 1.30)), Vector((-3.05, 2.75, 1.22)), 'bespoke')),
    ]
    BESPOKE_DOEL = {
        "B_zij_": (Vector((-1.80, -0.20, 1.10)), Vector((-1.60, 0.10, 1.10))),
        "C_close_": (Vector((-1.34, -0.15, 0.55)), Vector((-1.34, -0.15, 0.55))),
    }
print(f"[nacht] shot-variant: {label}")


def richt(loc, kijkdoel):
    cam.location = loc
    v = Vector(kijkdoel) - Vector(loc)
    cam.rotation_euler = v.to_track_quat('-Z', 'Y').to_euler()


try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'
    prefs.get_devices()
    for dv in prefs.devices:
        dv.use = dv.type in ('OPTIX', 'CPU')
    scn.cycles.device = 'GPU'
except Exception as e:
    print(f"[nacht] gpu: {e}")
scn.render.engine = 'CYCLES'
scn.render.resolution_x, scn.render.resolution_y = 1920, 1080
scn.render.resolution_percentage = 100
scn.cycles.samples = 48
scn.cycles.use_adaptive_sampling = True
scn.cycles.adaptive_threshold = 0.02
scn.cycles.use_denoising = True
scn.cycles.texture_limit_render = '2048'
scn.render.use_persistent_data = True
scn.use_nodes = False
scn.render.image_settings.file_format = 'PNG'
scn.render.fps = FPS

zonnen = [o for o in bpy.data.objects
          if o.type == 'LIGHT' and o.data.type == 'SUN']

for naam, sh in SHOTS:
    # hervat-steun: shot met compleet framebereik overslaan
    if os.path.exists(os.path.join(UITMAP, f"{naam}{sh['frames']:04d}.png")):
        print(f"[nacht] shot {naam} al compleet - overslaan", flush=True)
        continue
    cam.animation_data_clear()
    cam.data.animation_data_clear()
    for z in zonnen:
        z.animation_data_clear()

    herricht = sh['herricht']
    if herricht == 'bespoke':
        d0, d1 = BESPOKE_DOEL[naam]
    else:
        d0 = d1 = doel
    if herricht:
        richt(sh['p0'], d0)
    else:
        cam.location = sh['p0']   # rotatie blijft de originele hero-rotatie
    cam.keyframe_insert('location', frame=1)
    cam.keyframe_insert('rotation_euler', frame=1)
    if herricht:
        richt(sh['p1'], d1)
    else:
        cam.location = sh['p1']
    cam.keyframe_insert('location', frame=sh['frames'])
    cam.keyframe_insert('rotation_euler', frame=sh['frames'])

    if sh['focus']:
        cam.data.dof.use_dof = True
        if cam.data.dof.aperture_fstop > 5.6:
            cam.data.dof.aperture_fstop = 2.8   # anders is de pull onzichtbaar
        cam.data.dof.focus_distance = sh['focus'][0]
        cam.data.dof.keyframe_insert('focus_distance', frame=1)
        cam.data.dof.focus_distance = sh['focus'][1]
        cam.data.dof.keyframe_insert('focus_distance', frame=sh['frames'])
        print(f"[nacht] {naam} focus {sh['focus'][0]:.1f} -> {sh['focus'][1]:.1f} m")
    if sh['zon'] and zonnen:
        for z in zonnen:
            rot = z.rotation_euler.copy()
            z.rotation_euler = (math.radians(90 - sh['zon'][0]), rot.y, rot.z)
            z.keyframe_insert('rotation_euler', frame=1)
            z.rotation_euler = (math.radians(90 - sh['zon'][1]), rot.y, rot.z)
            z.keyframe_insert('rotation_euler', frame=sh['frames'])
        print(f"[nacht] {naam} zon-elevatie {sh['zon'][0]} -> {sh['zon'][1]} graden")

    scn.frame_start, scn.frame_end = 1, sh['frames']
    scn.render.filepath = os.path.join(UITMAP, naam)
    print(f"[nacht] shot {naam}: {sh['frames']} frames...", flush=True)
    bpy.ops.render.render(animation=True)
    print(f"[nacht] shot {naam} KLAAR", flush=True)
print("[nacht] SCENE KLAAR (blend niet gesaved)")
