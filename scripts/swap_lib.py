"""Gedeelde realism-swap helpers (bewezen in Zonnebloem Ochtendhoek + Magnolia Wintertuin).
Gebruik:
    import sys; sys.path.insert(0, ROOT+r"\\scripts")
    import cabin_lib as cl, swap_lib as sl
    scn = sl.open_scene(SCENE)
    HS, RZ = sl.collections(scn)
    sl.cleanup(RZ, prefixes=("XxDeck","XxPath","RZ_xx"), originals=[...])
    ... bouw ...
    sl.finalize(scn, SCENE, PNG)
"""
import bpy, math, os, random
from mathutils import Vector
import cabin_lib as cl

ROOT = r"C:\Users\beike\Documents\Blender-blokhutten"
TEX_DIRS = [ROOT + r"\assets\polyhaven\models\textures", ROOT + r"\assets\polyhaven\textures"]

def open_scene(path):
    bpy.ops.wm.open_mainfile(filepath=path)
    return bpy.context.scene

def collections(scn):
    def gc(name):
        c = bpy.data.collections.get(name)
        if not c:
            c = bpy.data.collections.new(name); scn.collection.children.link(c)
        return c
    return gc("RealismHardscape"), gc("RealismSwap")

def set_active(coll):
    def find(lc):
        if lc.collection == coll: return lc
        for ch in lc.children:
            r = find(ch)
            if r: return r
    lc = find(bpy.context.view_layer.layer_collection)
    if lc: bpy.context.view_layer.active_layer_collection = lc

def cleanup(RZ, prefixes=(), originals=()):
    for o in list(bpy.data.objects):
        if prefixes and o.name.startswith(tuple(prefixes)):
            bpy.data.objects.remove(o, do_unlink=True)
    for o in list(RZ.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    removed = []
    for nm in originals:
        o = bpy.data.objects.get(nm)
        if o: bpy.data.objects.remove(o, do_unlink=True); removed.append(nm)
    bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    return removed

def names_with(prefixes):
    """Alle objectnamen die met een van de prefixes beginnen (voor delete-lijsten)."""
    return [o.name for o in bpy.data.objects if o.name.startswith(tuple(prefixes))]

# ---- materialen -------------------------------------------------------------
def img_mat(name, img, scale=0.7, rough=0.6, bump=0.16, metallic=0.0):
    """Principled uit één image, Object-BOX-mapping (naadloos over add_box-stukken)."""
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metallic
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (scale, scale, scale)
    tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = img; tx.projection = 'BOX'; tx.projection_blend = 0.3
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], tx.inputs['Vector'])
    nt.links.new(tx.outputs['Color'], b.inputs['Base Color'])
    bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = bump
    nt.links.new(tx.outputs['Color'], bm.inputs['Height']); nt.links.new(bm.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return m

def rust_mat(name="MAT_Corten", base=(0.30, 0.14, 0.07), rough=0.72):
    """Cortenstaal/rust: oranje-bruin met noise-patina + lichte bump. Recreate-safe."""
    m = bpy.data.materials.get(name)
    if m: bpy.data.materials.remove(m)
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = 0.35
    tc = nt.nodes.new('ShaderNodeTexCoord'); noi = nt.nodes.new('ShaderNodeTexNoise')
    noi.inputs['Scale'].default_value = 8.0; noi.inputs['Detail'].default_value = 9.0
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (base[0]*0.6, base[1]*0.55, base[2]*0.5, 1)
    ramp.color_ramp.elements[1].color = (min(base[0]*1.5, 1), base[1]*1.3, base[2]*1.2, 1)
    nt.links.new(tc.outputs['Object'], noi.inputs['Vector'])
    nt.links.new(noi.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    noi2 = nt.nodes.new('ShaderNodeTexNoise'); noi2.inputs['Scale'].default_value = 60.0
    bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.2
    nt.links.new(tc.outputs['Object'], noi2.inputs['Vector'])
    nt.links.new(noi2.outputs['Fac'], bm.inputs['Height']); nt.links.new(bm.outputs['Normal'], b.inputs['Normal'])
    return m

# ---- assets -----------------------------------------------------------------
def fix_image_paths(objs):
    seen = set()
    for o in objs:
        for slot in getattr(o, "material_slots", []):
            mm = slot.material
            if not mm or not mm.use_nodes: continue
            for n in mm.node_tree.nodes:
                if n.type == 'TEX_IMAGE' and n.image and n.image not in seen:
                    seen.add(n.image); im = n.image
                    if im.packed_file: continue
                    if os.path.exists(bpy.path.abspath(im.filepath)): continue
                    base = os.path.basename(im.filepath.replace("\\", "/"))
                    for d in TEX_DIRS:
                        cand = os.path.join(d, base)
                        if os.path.exists(cand):
                            im.filepath = cand
                            try: im.reload()
                            except Exception: pass
                            break

def append_blend(path, coll):
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = list(src.objects)
    new = [o for o in dst.objects if o is not None]
    for o in new: coll.objects.link(o)
    fix_image_paths(new)
    bpy.context.view_layer.update()
    return new

def _wbb(objs):
    cs = []
    for o in objs:
        if o.type == 'MESH' and len(o.data.vertices):
            cs += [o.matrix_world @ Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs]; ys=[c.y for c in cs]; zs=[c.z for c in cs]
    return xs, ys, zs

def place(coll, new, tx, ty, base_z, target_longest=None, rot_z=0.0, label="", prefix="RZ_"):
    bpy.context.view_layer.update()
    xs, ys, zs = _wbb(new)
    cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2; cz=(min(zs)+max(zs))/2
    anchor = bpy.data.objects.new(prefix + (label or "a"), None)
    coll.objects.link(anchor); anchor.location = (cx, cy, cz)
    bpy.context.view_layer.update()
    for o in new:
        if o.parent is None or o.parent not in new:
            o.parent = anchor
            o.matrix_parent_inverse = anchor.matrix_world.inverted()
    bpy.context.view_layer.update()
    if rot_z:
        anchor.rotation_euler[2] += rot_z; bpy.context.view_layer.update()
    if target_longest:
        xs, ys, zs = _wbb(new)
        longest = max(max(xs)-min(xs), max(ys)-min(ys))
        if longest > 1e-6:
            anchor.scale *= target_longest/longest; bpy.context.view_layer.update()
    xs, ys, zs = _wbb(new)
    cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2; mnz=min(zs)
    anchor.location.x += tx-cx; anchor.location.y += ty-cy; anchor.location.z += base_z-mnz
    bpy.context.view_layer.update()
    fx, fy, fz = _wbb(new)
    print(f"[swap_lib] place {label}: x[{min(fx):.2f},{max(fx):.2f}] y[{min(fy):.2f},{max(fy):.2f}] z[{min(fz):.2f},{max(fz):.2f}]")
    return anchor

# ---- hardscape --------------------------------------------------------------
def flat_flagstones(name, pts, mat, stride=0.54, target=0.60, sink=0.05, zfac=0.5, rnd=None, bed=True):
    """Verzonken natuursteen-stapstenen op een DONKERE aarde-bedding (breekt de 'geplakt-op-gras'-look).
    Stenen blijven chunky (geen platte tegel), licht proud; de aarde-ribbon eronder meet het gras
    i.p.v. een mes-scherpe bleke steenrand."""
    rnd = rnd or random
    objs = []
    if bed and len(pts) >= 4:
        soilmat = cl.simple_mat("MAT_PadBed", (0.05, 0.04, 0.028), rough=1.0)
        try:
            ob, _ = cl.ribbon_path(name + "_bed", pts, width=target + 0.24, z=0.004, mat=soilmat)
            cl.bevel_all(ob, 0.01); objs.append(ob)
        except Exception as e:
            print("flagstone bed", e)
    flags = cl.flagstone_path(name, pts, stride=stride, target=target, sink=sink, mat=mat, rnd=rnd)
    for o in flags:
        o.scale.z *= zfac
        o.scale.x *= rnd.uniform(0.90, 1.14); o.scale.y *= rnd.uniform(0.90, 1.14)
        bpy.context.view_layer.update()
        bb = cl.wbbox_meshes([o])
        if bb: o.location.z += 0.020 - bb[5]   # steen ~2cm proud van de aarde-bedding
        objs.append(o)
    return objs

def paver_line(name, pts, mat, size=0.60, thick=0.07, sink=0.03, rnd=None):
    """Vierkante platte pavers (modern) langs polyline, verzonken+bevel+lichte rot-jitter."""
    rnd = rnd or random
    P = [Vector((p[0], p[1])) for p in pts]
    seg = [(P[k+1]-P[k]).length for k in range(len(P)-1)]
    total = sum(seg); step = size * 1.15
    samples = [P[0]]; pos = 0.0
    while pos + step < total:
        pos += step; run = pos; k = 0
        while k < len(seg) and run > seg[k]:
            run -= seg[k]; k += 1
        if k >= len(seg): break
        samples.append(P[k].lerp(P[k+1], run/seg[k]))
    objs = []
    for j, s in enumerate(samples):
        o = cl.add_box(f"{name}_{j}", s.x-size/2, s.x+size/2, s.y-size/2, s.y+size/2, 0.012-sink+thick, 0.012-sink, mat)
        o.rotation_euler.z = rnd.uniform(-0.05, 0.05)
        cl.bevel_all(o, 0.006); objs.append(o)
    return objs

def corten_open_box(name, x0, x1, y0, y1, h, mat, thick=0.03, soil_mat=None):
    """Open cortenstaal-bak: 4 dunne wanden (open top) + aarde-plane. Verzonken 1cm."""
    objs = []
    z0 = -0.01
    objs.append(cl.add_box(f"{name}_N", x0, x1, y1-thick, y1, h, z0, mat))
    objs.append(cl.add_box(f"{name}_S", x0, x1, y0, y0+thick, h, z0, mat))
    objs.append(cl.add_box(f"{name}_W", x0, x0+thick, y0, y1, h, z0, mat))
    objs.append(cl.add_box(f"{name}_E", x1-thick, x1, y0, y1, h, z0, mat))
    for o in objs: cl.bevel_all(o, 0.004)
    soil = soil_mat or cl.simple_mat(f"{name}_soilmat", (0.05, 0.035, 0.025), rough=1.0)
    objs.append(cl.add_box(f"{name}_soil", x0+thick, x1-thick, y0+thick, y1-thick, h-0.05, h-0.12, soil))
    return objs

def bollard_lamp(name, x, y, h=0.62, post=0.075, glow=(1.0, 0.62, 0.28), power=14.0, ground_z=0.0):
    """Modern bollard-lampje: donker antraciet paal + warme emissive lens-band + point light.
    (garden_lamp-asset heeft kapotte textures -> procedureel, bewezen in Dahlia Tuinkantoor)."""
    dark = cl.simple_mat("MAT_BollardDark", (0.03, 0.03, 0.035), rough=0.5, metallic=0.6)
    em = cl.simple_mat(f"{name}_em", (1, 1, 1), emission=glow, emission_strength=24.0)
    objs = []
    objs.append(cl.add_box(f"{name}_post", x-post/2, x+post/2, y-post/2, y+post/2, ground_z+h-0.10, ground_z, dark))
    objs.append(cl.add_box(f"{name}_band", x-post/2-0.004, x+post/2+0.004, y-post/2-0.004, y+post/2+0.004,
                           ground_z+h-0.02, ground_z+h-0.10, em))
    objs.append(cl.add_box(f"{name}_cap", x-post/2, x+post/2, y-post/2, y+post/2, ground_z+h+0.01, ground_z+h-0.02, dark))
    for o in objs: cl.bevel_all(o, 0.004)
    li = bpy.data.lights.new(f"{name}_L", 'POINT'); li.energy = power; li.color = glow; li.shadow_soft_size = 0.08
    lo = bpy.data.objects.new(f"{name}_L", li); bpy.context.scene.collection.objects.link(lo)
    lo.location = (x, y, ground_z + h - 0.06)
    objs.append(lo)
    return objs

def add_edging(name, x0, x1, y0, y1, top_z, mat, w=0.06, over=0.02, sink=0.12):
    """Doorlopende kantopsluiting (band) rond terras/pad — breekt de mes-snijrand + grondt."""
    zt = top_z + over; zb = top_z - sink
    objs = [
        cl.add_box(f"{name}_N", x0-w, x1+w, y1, y1+w, zt, zb, mat),
        cl.add_box(f"{name}_S", x0-w, x1+w, y0-w, y0, zt, zb, mat),
        cl.add_box(f"{name}_W", x0-w, x0, y0, y1, zt, zb, mat),
        cl.add_box(f"{name}_E", x1, x1+w, y0, y1, zt, zb, mat),
    ]
    for o in objs: cl.bevel_all(o, 0.005)
    return objs

def retint_moss(objnames, color=(0.09, 0.19, 0.05), flatten=0.5):
    """Gladde groene jelly-blob -> klonterige mos-pol: platdrukken + subsurf + noise-DISPLACE
    (onregelmatig oppervlak) + groen-met-variatie + sterke bump. Verzonken in de grond."""
    n = 0
    for nm in objnames:
        o = bpy.data.objects.get(nm)
        if not o or o.type != 'MESH': continue
        o.scale.z *= flatten
        sub = o.modifiers.new("MossSub", 'SUBSURF'); sub.levels = 2; sub.render_levels = 3
        tex = bpy.data.textures.get(nm + "_moss") or bpy.data.textures.new(nm + "_moss", 'CLOUDS')
        tex.noise_scale = 0.28; tex.noise_depth = 4
        dsp = o.modifiers.new("MossDisp", 'DISPLACE'); dsp.texture = tex
        dsp.strength = 0.06; dsp.mid_level = 0.4; dsp.texture_coords = 'LOCAL'
        try:
            bpy.ops.object.select_all(action='DESELECT'); o.select_set(True)
            bpy.context.view_layer.objects.active = o; bpy.ops.object.shade_smooth()
        except Exception:
            pass
        for s in o.material_slots:
            m = s.material
            if not m or not m.use_nodes: continue
            b = next((x for x in m.node_tree.nodes if x.type == 'BSDF_PRINCIPLED'), None)
            if not b: continue
            nt = m.node_tree
            for l in list(b.inputs['Base Color'].links): nt.links.remove(l)
            noi = nt.nodes.new('ShaderNodeTexNoise'); noi.inputs['Scale'].default_value = 32.0
            noi.inputs['Detail'].default_value = 10.0
            rmp = nt.nodes.new('ShaderNodeValToRGB')
            rmp.color_ramp.elements[0].color = (color[0]*0.5, color[1]*0.5, color[2]*0.5, 1)
            rmp.color_ramp.elements[1].color = (color[0]*1.5, color[1]*1.45, color[2]*1.5, 1)
            nt.links.new(noi.outputs['Fac'], rmp.inputs['Fac'])
            nt.links.new(rmp.outputs['Color'], b.inputs['Base Color'])
            b.inputs['Roughness'].default_value = 1.0
            noi2 = nt.nodes.new('ShaderNodeTexNoise'); noi2.inputs['Scale'].default_value = 85.0
            bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.7
            nt.links.new(noi2.outputs['Fac'], bm.inputs['Height']); nt.links.new(bm.outputs['Normal'], b.inputs['Normal'])
            n += 1
        bpy.context.view_layer.update()
        bb = cl.wbbox_meshes([o])
        if bb: o.location.z += (-0.012) - bb[4]   # iets in de grond verzonken
    return n

def read_centerline(obj_name):
    """Centerline-pts uit een ribbon-mesh (verts in l/r-paren)."""
    o = bpy.data.objects.get(obj_name)
    if not o or o.type != 'MESH': return []
    vs = [o.matrix_world @ v.co for v in o.data.vertices]
    out = []
    for i in range(0, len(vs)-1, 2):
        c = (vs[i] + vs[i+1]) / 2; out.append((c.x, c.y))
    return out

def bevel_existing(names, w=0.005):
    for nm in names:
        o = bpy.data.objects.get(nm)
        if o: cl.bevel_all(o, w)

def jitter_clusters(prefix, rnd, rot=True, scale=(0.88, 1.16)):
    """Rot/scale-jitter op cluster-root-empties met gegeven prefix (breekt klonen)."""
    n = 0
    for o in bpy.data.objects:
        if o.name.startswith(prefix) and o.type == 'EMPTY' and "_m" not in o.name:
            if rot: o.rotation_euler.z += rnd.uniform(0, 6.283)
            f = rnd.uniform(*scale); o.scale = [v*f for v in o.scale]; n += 1
    return n

# ---- finalize ---------------------------------------------------------------
def finalize(scn, SCENE, PNG, samples=130, res=(1600, 900),
             cabin_x=(-1.6, 1.6), cabin_y=(-1.1, 1.1), extra_safe=()):
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        _gpu = 'CUDA'
        for _t in ('OPTIX', 'CUDA'):
            prefs.compute_device_type = _t; prefs.get_devices()
            if any(d.type == _t for d in prefs.devices): _gpu = _t; break
        for dv in prefs.devices: dv.use = (dv.type == _gpu)
        print("[gpu]", _gpu)
        scn.cycles.device = 'GPU'
    except Exception as e:
        print("dev", e)
    scn.cycles.texture_limit_render = '2048'
    scn.render.use_persistent_data = False
    scn.cycles.use_denoising = True
    try: cl.fix_broken_image_materials()
    except Exception as e: print("fixbroken", e)
    try: bpy.ops.file.pack_all()
    except Exception as e: print("pack (non-fatal)", e)
    bpy.context.preferences.filepaths.save_version = 0
    cl.audit(cabin_x=cabin_x, cabin_y=cabin_y, extra_safe=extra_safe)
    cl.save_and_diag(SCENE, PNG, res=res, samples=samples)
    print("[swap_lib] saved + rendered -> " + PNG)
