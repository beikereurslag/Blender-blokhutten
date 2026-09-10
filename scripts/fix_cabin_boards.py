"""Repair the wall-board layout that comes out of the tekentool GLB export.

Three defects, measured on all 33 source GLBs (14 aug 2026):

1. ADJACENT WALLS SIT ON DIFFERENT COURSE GRIDS. Every cabin has two kinds of
   wall: one whose starter course is 7.5 cm high (boards then start at z=6.0)
   and one whose starter is 14.25 cm (boards start at z=12.75). Half a course
   of the 13.5 cm pitch. Result: at every corner the horizontal seams of the
   two walls meet at different heights.
2. SLIVER TOP COURSE. Because of (1) some walls close with a 0.75 cm board --
   a 7.5 mm hairline strip under the roof.
3. NO BOARD RELIEF. The courses butt flush, so the seam is a hairline and the
   wall reads as one smooth plane once a wood texture is on it.

`fix_cabin()` re-lays every wall on one shared grid (lowest starter wins),
closes the top course properly, and optionally chamfers the board edges so each
plank casts its own shadow line.

Units are the GLB's native ones: 1 unit == 1 cm. Run this BEFORE any 0.01x
scale-to-metres step.
"""
import math
import re
from collections import defaultdict

import bpy
from mathutils import Vector

BOARD_RE = re.compile(r"^(wall-(?:openEnded-)?\d+)-board-(\d+)")
# starter slab / top closer belonging to a wall
PARENT_RE = re.compile(r"^parentBoard-(?:openEnd[AB]-)?(\d+)-scaled$")
CLOSER_RE = re.compile(r"^parentBoard-(?:openEnd[AB]-)?(\d+)-scaled-roofWallBoard-\d+$")

# Everything below is derived from the measured geometry, so the module works
# both on a freshly imported GLB (1 unit == 1 cm) and inside a finished scene
# blend (1 unit == 1 m). Never hard-code a length here.
SLIVER_FRAC = 0.15     # a top course thinner than this fraction of a full
                       # course is a hairline strip, not a plank
CHAMFER_FRAC = 0.023   # plank edge break, as a fraction of the course height


# --------------------------------------------------------------------------
# geometry helpers -- everything is expressed in world cm

def _up_axis(obj):
    """Which local axis of `obj` points along world +Z, and cm per local unit."""
    lin = obj.matrix_world.to_3x3()
    best, best_dot = 1, 0.0
    for i in range(3):
        e = Vector((0, 0, 0))
        e[i] = 1.0
        dot = (lin @ e).z
        if abs(dot) > abs(best_dot):
            best, best_dot = i, dot
    return best, best_dot


def _world_z(obj):
    zs = [(obj.matrix_world @ Vector(c)).z for c in obj.bound_box]
    return min(zs), max(zs)


def _single_user_mesh(obj):
    if obj.data.users > 1:
        obj.data = obj.data.copy()
    return obj.data


def _shift(obj, dz):
    """Move `obj` dz along world Z by translating its mesh.

    Deliberately not via obj.location: these objects carry a rotation from the
    glTF import, so a location delta lives in the parent's space, not the
    object's. Moving the mesh keeps us in one space -- the same one `_set_top`
    edits -- and every board owns its mesh, so nothing else moves with it.
    """
    if abs(dz) < 1e-9:
        return
    axis, per_unit = _up_axis(obj)
    me = _single_user_mesh(obj)
    d_local = dz / per_unit
    for v in me.vertices:
        v.co[axis] += d_local
    me.update()


def _set_top(obj, target_z, current_top=None):
    """Move only the upper half of obj's mesh so its top lands on target_z.

    Keeps the bottom tongue-and-groove profile intact -- we are lengthening or
    trimming a plank, not scaling it.

    `current_top` lets the caller supply the plank's present top instead of
    reading bound_box, which goes stale the moment we touch a transform.
    """
    z1 = current_top if current_top is not None else _world_z(obj)[1]
    dz = target_z - z1
    if abs(dz) < 1e-6:
        return
    axis, per_unit = _up_axis(obj)
    me = _single_user_mesh(obj)
    vals = [v.co[axis] for v in me.vertices]
    mid = (min(vals) + max(vals)) / 2.0
    d_local = dz / per_unit
    for v in me.vertices:
        if v.co[axis] > mid:
            v.co[axis] += d_local
    me.update()


def _clone_board(src, name):
    new = src.copy()
    new.data = src.data.copy()
    new.name = name
    for coll in src.users_collection:
        coll.objects.link(new)
    new.parent = src.parent
    new.matrix_parent_inverse = src.matrix_parent_inverse.copy()
    return new


# --------------------------------------------------------------------------

def survey():
    """Group board objects per wall and read their current course layout."""
    walls = defaultdict(list)
    for o in bpy.data.objects:
        if o.type != 'MESH':
            continue
        m = BOARD_RE.match(o.name)
        if m:
            walls[m.group(1)].append(o)

    info = {}
    for name, objs in walls.items():
        objs.sort(key=lambda o: _world_z(o)[0])
        z0s = [_world_z(o)[0] for o in objs]
        steps = [round(z0s[i + 1] - z0s[i], 3) for i in range(len(z0s) - 1)]
        pitch = min(steps) if steps else 13.5
        heights = [_world_z(o)[1] - _world_z(o)[0] for o in objs]
        info[name] = dict(objs=objs, z_start=z0s[0],
                          z_end=max(_world_z(o)[1] for o in objs),
                          pitch=pitch, full_h=max(heights))
    return info


def _wall_index(wall_name):
    m = re.search(r"(\d+)$", wall_name)
    return m.group(1) if m else None


def align_courses(verbose=True):
    """Re-lay every wall on the lowest course grid found in the cabin."""
    info = survey()
    if not info:
        print("[boards] no wall boards found")
        return 0

    z_ref = min(w["z_start"] for w in info.values())
    pitch = min(w["pitch"] for w in info.values())
    full_h = max(w["full_h"] for w in info.values())
    overlap = max(full_h - pitch, 0.0)     # the tongue hidden by the course above
    min_course = full_h * SLIVER_FRAC
    if verbose:
        print(f"[boards] reference grid: start={z_ref:.4g} pitch={pitch:.4g} "
              f"course={full_h:.4g} overlap={overlap:.4g}")

    # starter slabs, keyed by wall index (closers blijven waar ze staan)
    starters = {}
    for o in bpy.data.objects:
        if o.type != 'MESH':
            continue
        m = PARENT_RE.match(o.name)
        if m:
            starters.setdefault(m.group(1), []).append(o)

    moved = 0
    for name, w in sorted(info.items()):
        idx = _wall_index(name)
        z_end = w["z_end"]

        # Track each plank's world span ourselves. bound_box only refreshes on a
        # depsgraph evaluation, so re-reading it mid-edit double-applies shifts.
        objs = sorted(w["objs"], key=lambda o: _world_z(o)[0])
        span = {o: list(_world_z(o)) for o in objs}

        def move(o, dz):
            _shift(o, dz)
            span[o][0] += dz
            span[o][1] += dz

        def top_to(o, target):
            _set_top(o, target, current_top=span[o][1])
            span[o][1] = target

        delta = w["z_start"] - z_ref
        if abs(delta) > 1e-6:
            for o in objs:
                move(o, -delta)
            # De closers (roofWallBoard) NIET meeschuiven: de wandtop (z_end)
            # verandert niet, dus een closer die van wandtop tot dak loopt
            # hoort exact te blijven staan. Meeschuiven opende een gap van
            # `delta` onder het dak (gezien op jasmijn_familiemiddag, 20 aug).
            moved += 1
            if verbose:
                print(f"[boards] {name}: lowered {delta:.2f} cm onto the grid")

        # starter slab closes the gap under the first course
        for o in starters.get(idx, []):
            _set_top(o, z_ref + overlap)

        # rebuild the course rhythm bottom-up, then close the top
        n_slots = int(math.floor((z_end - z_ref) / pitch)) + 1

        while len(objs) < n_slots:
            src = objs[-1]
            new = _clone_board(src, f"{name}-board-{len(objs) + 1}-fill")
            span[new] = list(span[src])
            move(new, pitch)
            objs.append(new)
            if verbose:
                print(f"[boards] {name}: added course {len(objs)}")
        while len(objs) > n_slots:
            extra = objs.pop()
            span.pop(extra, None)
            bpy.data.objects.remove(extra, do_unlink=True)
            if verbose:
                print(f"[boards] {name}: removed course above the wall top")

        for i, o in enumerate(objs):
            slot_z = z_ref + i * pitch
            move(o, slot_z - span[o][0])
            top_to(o, min(slot_z + full_h, z_end))

        # a hairline top course is worse than none: fold it into the plank below
        if len(objs) >= 2:
            top_h = span[objs[-1]][1] - span[objs[-1]][0]
            if top_h < min_course:
                gone = objs.pop()
                span.pop(gone, None)
                bpy.data.objects.remove(gone, do_unlink=True)
                top_to(objs[-1], z_end)
                if verbose:
                    print(f"[boards] {name}: folded {top_h:.2f} cm sliver away")

    bpy.context.view_layer.update()
    print(f"[boards] aligned {len(info)} walls ({moved} were off-grid)")
    return moved


def chamfer_boards(width=None, segments=2, angle_deg=35):
    """Bevel the plank edges so every course reads as its own board.

    With no width, the edge break is scaled off the measured course height, so
    the same call is right in cm-space and in metre-space.
    """
    if width is None:
        info = survey()
        if not info:
            return 0
        width = max(w["full_h"] for w in info.values()) * CHAMFER_FRAC
    n = 0
    for o in bpy.data.objects:
        if o.type != 'MESH' or not BOARD_RE.match(o.name):
            continue
        if any(m.type == 'BEVEL' and m.name == "PlankChamfer" for m in o.modifiers):
            continue
        md = o.modifiers.new("PlankChamfer", 'BEVEL')
        # Bevel width is in the object's LOCAL units. These boards hang under a
        # non-uniform parent scale, so a world-space width has to be converted
        # or the modifier clamps itself into nothing.
        _, per_unit = _up_axis(o)
        md.width = width / abs(per_unit)
        md.segments = segments
        md.limit_method = 'ANGLE'
        md.angle_limit = math.radians(angle_deg)
        n += 1
    print(f"[boards] chamfered {n} planks @ {width:.4g} (world units)")
    return n


WALL_MATS = ("basetexture-firstLayer-wall", "basetexture-firstLayer-canopyWall")


def board_materials():
    """The materials actually used by the wall boards.

    Safer than matching on name: scenes rename these (the B-series calls its
    wall material `DG_wand`), and a name-based match silently grooves nothing.
    """
    found = []
    for o in bpy.data.objects:
        if o.type != 'MESH' or not BOARD_RE.match(o.name):
            continue
        for m in o.data.materials:
            if m and m not in found:
                found.append(m)
    return found


def plank_groove(depth=0.004, half_width=0.06, strength=1.0, mats=None,
                 verbose=True):
    """Carve a shadow line into the wall material at every course line.

    The planks cannot be given real relief: consecutive courses interpenetrate
    by the tongue depth and their outer faces are coplanar, so a chamfer just
    ends up buried inside the neighbouring board. Instead we drive a bump off
    world Z, folded onto the measured course pitch, which puts a groove exactly
    where each seam is.

    `half_width` is the groove half-width as a fraction of the course pitch.
    """
    info = survey()
    if not info:
        print("[groove] no walls found")
        return 0
    z_ref = min(w["z_start"] for w in info.values())
    pitch = min(w["pitch"] for w in info.values())

    if mats is None:
        targets = board_materials()
    else:
        # explicit names, matched by prefix so duplicated slots (".001") count
        targets = [m for m in bpy.data.materials
                   if any(m.name.startswith(p) for p in mats)]
    if not targets:
        print("[groove] no wall materials found on the boards")
        return 0
    done = 0
    for mat in targets:
        if not mat.use_nodes:
            continue
        name = mat.name
        nt = mat.node_tree
        bsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if not bsdf:
            print(f"[groove] {name}: SKIPPED, no Principled BSDF")
            continue

        # Where does the groove plug in? Straight into the BSDF if nothing drives
        # the normal yet, otherwise chain it into the existing bump/normal node so
        # we add the seam without throwing away the wood shading already there.
        target = bsdf.inputs['Normal']
        chained = False
        if target.is_linked:
            upstream = target.links[0].from_node
            slot = upstream.inputs.get('Normal')
            if slot is None or slot.is_linked:
                print(f"[groove] {name}: SKIPPED, normal chain is full "
                      f"({upstream.type})")
                continue
            target = slot
            chained = True

        def new(kind, x, y):
            n = nt.nodes.new(kind)
            n.location = (x, y)
            return n

        geo = new('ShaderNodeNewGeometry', -1600, -700)
        sep = new('ShaderNodeSeparateXYZ', -1420, -700)
        nt.links.new(geo.outputs['Position'], sep.inputs['Vector'])

        off = new('ShaderNodeMath', -1250, -700); off.operation = 'SUBTRACT'
        off.inputs[1].default_value = z_ref
        nt.links.new(sep.outputs['Z'], off.inputs[0])

        div = new('ShaderNodeMath', -1080, -700); div.operation = 'DIVIDE'
        div.inputs[1].default_value = pitch
        nt.links.new(off.outputs[0], div.inputs[0])

        fra = new('ShaderNodeMath', -910, -700); fra.operation = 'FRACT'
        nt.links.new(div.outputs[0], fra.inputs[0])

        inv = new('ShaderNodeMath', -910, -880); inv.operation = 'SUBTRACT'
        inv.inputs[0].default_value = 1.0
        nt.links.new(fra.outputs[0], inv.inputs[1])

        # distance to the nearest seam, so the groove is symmetric
        mn = new('ShaderNodeMath', -740, -780); mn.operation = 'MINIMUM'
        nt.links.new(fra.outputs[0], mn.inputs[0])
        nt.links.new(inv.outputs[0], mn.inputs[1])

        ramp = new('ShaderNodeValToRGB', -560, -780)
        ramp.color_ramp.elements[0].position = 0.0
        ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
        ramp.color_ramp.elements[1].position = max(half_width, 1e-4)
        ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
        nt.links.new(mn.outputs[0], ramp.inputs['Fac'])

        bump = new('ShaderNodeBump', -330, -780)
        bump.inputs['Strength'].default_value = strength
        bump.inputs['Distance'].default_value = depth
        nt.links.new(ramp.outputs['Color'], bump.inputs['Height'])
        nt.links.new(bump.outputs['Normal'], target)
        done += 1
        if verbose:
            how = "chained into existing bump" if chained else "into BSDF normal"
            print(f"[groove] {name}: seam every {pitch:.4g} from z={z_ref:.4g} "
                  f"({how})")

    print(f"[groove] grooved {done} wall materials")
    return done


def fix_cabin(chamfer=True, verbose=True):
    """Full repair: align the courses, then give the planks an edge.

    `chamfer` may be True (auto width), False, or an explicit width in the
    units of the open file.
    """
    moved = align_courses(verbose=verbose)
    if chamfer:
        chamfer_boards(width=None if chamfer is True else chamfer)
    return moved


def report():
    """Print the per-wall course layout -- use to verify before/after."""
    bpy.context.view_layer.update()
    for name, w in sorted(survey().items()):
        print(f"  {name:20s} n={len(w['objs']):3d} start={w['z_start']:7.2f} "
              f"end={w['z_end']:7.2f} pitch={w['pitch']:6.2f}")


# ---------------------------------------------------------------------------
# Coplanaire overlappende wanden (2 sep 2026)
# ---------------------------------------------------------------------------

def _axis_for_world(obj, world_axis):
    """Which local axis of `obj` points along the given world axis (0=x, 1=y, 2=z), and world units per local unit."""
    lin = obj.matrix_world.to_3x3()
    best, best_dot = 0, 0.0
    for i in range(3):
        e = Vector((0, 0, 0))
        e[i] = 1.0
        dot = (lin @ e)[world_axis]
        if abs(dot) > abs(best_dot):
            best, best_dot = i, dot
    return best, best_dot


def _world_bounds(objs):
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    return [(min(p[i] for p in pts), max(p[i] for p in pts)) for i in range(3)]


def _translate_world(obj, world_axis, d):
    """Move `obj` by d along a world axis by translating its mesh (same reasoning as `_shift`)."""
    if abs(d) < 1e-9:
        return
    axis, per_unit = _axis_for_world(obj, world_axis)
    me = _single_user_mesh(obj)
    dl = d / per_unit
    for v in me.vertices:
        v.co[axis] += dl
    me.update()


def separate_overlapping_walls(offset=0.006, verbose=True):
    """Push coplanar, overlapping walls apart so they stop z-fighting.

    The tekentool lets the canopy back wall (wall-7) run 20 cm into the span of
    the cabin wall (wall-0) in exactly the same plane. Before the course
    alignment the two board sets masked each other's gaps; after it the gaps
    line up and the corner shows dark holes. Per overlap the canopy wall (else
    the higher wall index) moves `offset` scene units along the thickness axis,
    towards the scene camera (so the canopy wall stays in front), closers of that wall included. Opt-in: not part
    of fix_cabin(). Returns the list of moves.
    """
    info = survey()
    names = sorted(info)
    bounds = {n: _world_bounds(info[n]["objs"]) for n in names}
    cam = bpy.context.scene.camera

    def is_canopy(n):
        return any('canopy' in (m.name.lower() if m else '')
                   for o in info[n]["objs"] for m in o.data.materials)

    moves = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            ba, bb = bounds[a], bounds[b]
            for thick, along in ((1, 0), (0, 1)):
                same_plane = (abs(ba[thick][0] - bb[thick][0]) < 0.002
                              and abs(ba[thick][1] - bb[thick][1]) < 0.002)
                ov = min(ba[along][1], bb[along][1]) - max(ba[along][0], bb[along][0])
                if not (same_plane and ov > 0.05):
                    continue
                if is_canopy(a) and not is_canopy(b):
                    mover = a
                elif is_canopy(b) and not is_canopy(a):
                    mover = b
                else:
                    mover = max(a, b, key=lambda n: int(_wall_index(n) or 0))
                center = (bounds[mover][thick][0] + bounds[mover][thick][1]) / 2
                # naar de camera toe: dan blijft de canopy-wand (blank hout) vóór de cabinewand en zie je
                # geen strook van de andere wand in de hoek (Beike, 3 sep: 'blanke planken zijn grijs' bij naar binnen)
                sign = 1.0
                if cam is not None:
                    sign = 1.0 if cam.matrix_world.translation[thick] > center else -1.0
                d = sign * offset
                idx = _wall_index(mover)
                objs = list(info[mover]["objs"])
                objs += [o for o in bpy.data.objects if CLOSER_RE.match(o.name)
                         and re.match(r"^parentBoard-(?:openEnd[AB]-)?%s-scaled" % idx, o.name)]
                for o in objs:
                    _translate_world(o, thick, d)
                moves.append(dict(walls=(a, b), mover=mover, axis='xyz'[thick], d=d, overlap=ov, n=len(objs)))
                if verbose:
                    print(f"[overlap] {a} ~ {b}: overlap {ov:.3f} langs {'xyz'[along]}; "
                          f"{mover} {d * 1000:+.1f} mm langs {'xyz'[thick]} ({len(objs)} objecten)")
    if verbose and not moves:
        print("[overlap] geen coplanaire overlappende wanden")
    return moves

