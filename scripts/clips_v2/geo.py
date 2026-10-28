r"""Gedeelde scene-geometrie voor clips-v2 (probe én render-engine gebruiken dit).

Context = wat het hero-beeld is en wat erin staat:
  cam/loc/rot/kijk/doel   hero-camera (bewezen-goede compositie)
  cabin                   wereld-bbox van de blokhut
  ground_names            grote vlakke meshes (gras/grond)
  vignetten               prop-clusters die IN het hero-beeld staan (kandidaat-detailshots)
  frame_score(matrix, lens, shift_x, shift_y)
                          raycast-raster door een kandidaat-camera: welk deel van wat die ziet
                          ligt ook in het hero-beeld ('inside'), plus grond/lucht/void-aandelen.
Draait in Blender (bpy). Niets wordt gewijzigd of opgeslagen.
"""
import math
import re

import bpy
from bpy_extras.object_utils import world_to_camera_view as w2cv
from mathutils import Vector

CABIN_RE = re.compile(r"^(wall|roof|pole|floor|parentBoard|shed|blokhut|door|window|canopy|beam|gording|"
                      r"Deur|DEUR|raam|glas|kozijn|\.DEUR|\.door|\.raam|\.window)", re.I)
VEG_RE = re.compile(r"(tree|boom|shrub|struik|hedge|heg|haag|grass|gras|plant|bloem|flower|leaf|blad|lavend|fern|"
                    r"frond|ivy|klimop|bamboe|bamboo|cluster|scatter|GN_|bos|forest|berk|birch|spruce|pine|den_|"
                    r"maple|cherry|hydrangea|rozen|rose|palm|fir|oak|eik|heide|bush|border_|ring|moss|mos)", re.I)
# geen vignet-kandidaten: vlakken/randen/plantjes met generieke namen
SKIP_RE = re.compile(r"^(F_?\d|F\d|Trunk|Twig|Tak|Branch|Border|Edge_|Pad$|Pad_|Terras|Band_|Stoep|Rand|Voeg|Grind|Klinker|Tegel|Vloer|Deck|Plank|"
                     r"Zand|Schutting|Fence|Hek|Muur|Wall_|Plane|Cube$|Ground|Grond|Stap|Step|Stone|Steen|Boulder|Rots|Rock|Klinker)", re.I)
# 'leven' in beeld: meubels, lampen, spullen -> dit zijn de dingen waar een detailshot op mag landen
LIFE_RE = re.compile(r"(stoel|chair|tafel|table|bank|bench|sofa|lounge|fauteuil|kussen|cushion|coussin|lamp|lantern|"
                     r"lantaarn|kaars|candle|bed|tub|bad|barbecue|bbq|grill|fire|vuur|pit|pizza|glas|glass|fles|bottle|"
                     r"boek|book|schaak|chess|plaid|deken|mand|basket|picnic|picknick|bike|fiets|kruiwagen|wheelbarrow|"
                     r"gieter|watering|pot|vaas|vase|tv|scherm|screen|projector|bar|wijn|wine|koffie|coffee|kop|"
                     r"cup|mok|mug|krant|radio|vinyl|platenspeler|record|gitaar|guitar|hangmat|hammock|schommel|swing|"
                     r"ezel|easel|canvas|palet|verf|paint|hark|schep|spade|emmer|bucket|parasol|umbrella|kleed|rug|"
                     r"ligbed|sunlounger|lounger|hocker|kist|crate|bloembak|planter|kruk|stool|dienblad|tray|bord|plate)", re.I)


def r3(v):
    return [round(float(x), 3) for x in v]


# woorddelen: 'DlTerras_base' en 'LaDeck_p10' zijn net zulke vloeren als 'Terras' en 'Deck'.
# Geen re.I hier: de camelCase-grens moet echt op een kleine->hoofdletter-overgang matchen.
_DEEL_RE = re.compile(r"[_.\-\s\d]+|(?<=[a-z])(?=[A-Z])")


def skip_naam(naam):
    """True als het SKIP-patroon aan het begin van de naam of van een woorddeel staat.

    SKIP_RE is geankerd, dus een scene-prefix liet een vloer ontsnappen ('DlTerras_base',
    'CwTerrasMain', 'LaDeck_p10', 'OnDeck_base'). Zoeken zonder anker kan niet: 'Veranda'
    bevat 'rand'. Daarom per woorddeel toetsen.
    """
    if SKIP_RE.match(naam):
        return True
    return any(deel and SKIP_RE.match(deel) for deel in _DEEL_RE.split(naam))


def onzichtbaar_voor_camera(o):
    """True als de camera dit mesh niet als oppervlak ziet: fog-volume, holdout of ray-invisible.

    Zonder dit stopt de toets-straal op de mistdoos, terwijl in het gerenderde beeld op diezelfde
    pixel de tuin erachter staat. Dat kostte lelie_avondkubus A 52 van 576 stralen (0,861) en
    lelie_ochtendnevel C er 52 (0,814) - vals alarm dus.
    """
    if not o.visible_camera or o.is_holdout:
        return True
    mats = [m for m in o.data.materials if m]
    if not mats:
        return False                      # geen materiaal = gewoon een grijs oppervlak
    for m in mats:
        if not m.use_nodes:
            return False                  # klassiek materiaal = oppervlak
        uit = next((n for n in m.node_tree.nodes if n.type == 'OUTPUT_MATERIAL'), None)
        if uit is None or not uit.inputs['Surface'].is_linked:
            continue                      # alleen volume (of niets) op de output
        bron = uit.inputs['Surface'].links[0].from_node
        if bron.type != 'BSDF_TRANSPARENT':
            return False                  # een echt oppervlak
    return True                           # alle materialen: volume, transparant of leeg


class Ctx:
    def __init__(self, scn=None, grid=(32, 18)):
        self.scn = scn or bpy.context.scene
        scn = self.scn
        self.cam = scn.camera
        assert self.cam, "scene heeft geen actieve camera"
        self.cam.rotation_mode = 'XYZ'
        bpy.context.view_layer.update()
        self.dg = bpy.context.evaluated_depsgraph_get()
        self.grid = grid
        cd = self.cam.data
        self.cd = cd
        self.res = (scn.render.resolution_x, scn.render.resolution_y)
        self.aspect = self.res[1] / self.res[0]
        self.lens = float(cd.lens)
        self.sensor = float(cd.sensor_width)
        self.shift = (float(cd.shift_x), float(cd.shift_y))
        self.matrix = self.cam.matrix_world.copy()
        self.loc = self.matrix.translation.copy()
        self.rot = self.matrix.to_euler('XYZ')
        self.kijk = (self.matrix.to_quaternion() @ Vector((0, 0, -1))).normalized()
        self.rechts = self.kijk.cross(Vector((0, 0, 1))).normalized()

        self.meshes = [o for o in scn.objects if o.type == 'MESH' and not o.hide_render]
        # De toets mag alleen zien wat de render ziet: hide_render-meshes zitten wél in de
        # depsgraph waar scn.ray_cast tegenaan kijkt, en mist/holdout heeft geen oppervlak.
        self.doorzichtig = {o.name for o in scn.objects if o.type == 'MESH'
                            and (o.hide_render or onzichtbaar_voor_camera(o))}
        self.cabin_objs = [o for o in self.meshes if self.is_cabin(o)]
        mn, mx = [1e9] * 3, [-1e9] * 3
        for o in self.cabin_objs:
            a, b = wbbox(o)
            mn = [min(mn[i], a[i]) for i in range(3)]
            mx = [max(mx[i], b[i]) for i in range(3)]
        self.cabin_min, self.cabin_max = Vector(mn), Vector(mx)
        self.cabin_c = (self.cabin_min + self.cabin_max) / 2

        self.ground_names = set()
        for o in self.meshes:
            a, b = wbbox(o)
            if (b[0] - a[0]) > 12 and (b[1] - a[1]) > 12 and (b[2] - a[2]) < 1.5:
                self.ground_names.add(o.name)

        # kijkdoel: DOF-object > DOF-afstand > raycast langs de kijkas > 9 m
        doel = None
        if cd.dof.use_dof and cd.dof.focus_object:
            doel = cd.dof.focus_object.matrix_world.translation.copy()
        elif cd.dof.use_dof and cd.dof.focus_distance > 0.5:
            doel = self.loc + self.kijk * cd.dof.focus_distance
        if doel is None:
            hit, hloc, _ob, _fog = self.cast(self.loc, self.kijk, 60)
            doel = Vector(hloc) if hit else self.loc + self.kijk * 9.0
        self.doel = doel
        self.vignetten = self._vignetten()
        self.deuren = self._deuren()
        self.hero_score = self.frame_score(self.matrix, self.lens, *self.shift)

    # ------------------------------------------------------------------ classificatie
    def is_cabin(self, o):
        if CABIN_RE.match(o.name):
            return True
        if o.type == 'MESH':
            for m in o.data.materials:
                if m and ('firstlayer' in m.name.lower() or m.name.startswith('DG_')):
                    return True
        p = o.parent
        while p:
            if p.name.lower().startswith(('shed', 'blokhut')):
                return True
            p = p.parent
        return False

    def classify(self, name):
        if name in self.ground_names:
            return 'ground'
        o = bpy.data.objects.get(name)
        if o is None:
            return 'other'
        if self.is_cabin(o):
            return 'cabin'
        if VEG_RE.search(name) or (o.type == 'MESH' and any(m and VEG_RE.search(m.name) for m in o.data.materials)):
            return 'veg'
        return 'prop'

    # ------------------------------------------------------------------ hero-beeld
    def ndc(self, p):
        return w2cv(self.scn, self.cam, Vector(p))

    def in_hero(self, p, marge=0.0):
        n = self.ndc(p)
        return -marge <= n.x <= 1 + marge and -marge <= n.y <= 1 + marge and n.z > 0

    def cast(self, oorsprong, richting, distance):
        """ray_cast die door onzichtbare meshes (mist, holdout, hide_render) heen kijkt.

        Geeft (hit, punt, object, door_mist): het eerste mesh dat de camera écht als oppervlak
        ziet, plus of de straal onderweg door een mistvolume is gegaan.
        """
        o = Vector(oorsprong)
        d = Vector(richting).normalized()
        rest = float(distance)
        door_mist = False
        for _ in range(8):                      # 8 lagen mist is meer dan genoeg
            hit, hloc, _n, _i, ob, _m = self.scn.ray_cast(self.dg, o, d, distance=rest)
            if not hit:
                return False, None, None, door_mist
            if ob.name not in self.doorzichtig:
                return True, Vector(hloc), ob, door_mist
            door_mist = True
            stap = (Vector(hloc) - o).length + 1e-3
            rest -= stap
            if rest <= 0:
                return False, None, None, door_mist
            o = Vector(hloc) + d * 1e-3
        return False, None, None, door_mist

    def rays(self, m_world, lens, shift_x, shift_y):
        rot3 = m_world.to_3x3()
        o = m_world.translation.copy()
        nx, ny = self.grid
        out = []
        for j in range(ny):
            v = (j + 0.5) / ny
            for i in range(nx):
                u = (i + 0.5) / nx
                lx = (u - 0.5 + shift_x) * self.sensor / lens
                ly = ((v - 0.5) * self.aspect + shift_y) * self.sensor / lens
                out.append((o, (rot3 @ Vector((lx, ly, -1.0))).normalized()))
        return out

    def frame_score(self, m_world, lens, shift_x=0.0, shift_y=0.0):
        """Aandeel van het kandidaat-beeld dat in het hero-beeld ligt + wat het beeld toont."""
        tel = dict(cabin=0, ground=0, veg=0, prop=0, sky=0, void=0, fog=0, other=0)
        inside = 0
        buiten = {}
        rays = self.rays(m_world, lens, shift_x, shift_y)
        for o, d in rays:
            hit, hloc, ob, door_mist = self.cast(o, d, 400)
            if hit:
                k = self.classify(ob.name)
                p = Vector(hloc)
            elif door_mist:
                # Niets achter de mist: op die pixel staat in de render gewoon nevel. Mist verbergt
                # onafgewerkte tuin, hij kan hem niet onthullen -> deze straal zegt niets over 'inside'
                # en telt dus niet mee. (Zonder deze regel las de toets nevel als een gat in de wereld:
                # lelie_ochtendnevel C ging van 0,814 naar 0,781 toen de mist doorlaatbaar werd.)
                tel['fog'] += 1
                continue
            else:
                k = 'sky' if d.z >= -0.02 else 'void'   # omlaag kijken en niets raken = rand van de wereld
                p = o + d * 150
            tel[k] += 1
            if self.in_hero(p):
                inside += 1
            elif hit:
                buiten[ob.name] = buiten.get(ob.name, 0) + 1
        n = len(rays)
        n_beeld = n - tel['fog']
        d = {k: round(v / n, 3) for k, v in tel.items()}
        # alles nevel = er is niets dat buiten het hero-beeld kan vallen
        d['inside'] = round(inside / n_beeld, 3) if n_beeld else 1.0
        d['outside_top'] = sorted(buiten.items(), key=lambda kv: -kv[1])[:6]
        return d

    def blocked(self, p, doel, frac=0.45):
        """True als de blik van p naar doel vlak voor de lens iets raakt (heg/wand/boom)."""
        d = Vector(doel) - Vector(p)
        hit, hloc, _ob, _fog = self.cast(p, d.normalized(), d.length)
        return hit and (Vector(hloc) - Vector(p)).length < frac * d.length

    # ------------------------------------------------------------------ inhoud
    def _vignetten(self):
        props = []
        for o in self.meshes:
            if self.is_cabin(o) or o.name in self.ground_names or VEG_RE.search(o.name) or skip_naam(o.name):
                continue
            a, b = wbbox(o)
            dims = [b[i] - a[i] for i in range(3)]
            vol = dims[0] * dims[1] * dims[2]
            if vol < 0.004 or vol > 12 or max(dims) > 6:
                continue
            c = Vector([(a[i] + b[i]) / 2 for i in range(3)])
            if (c - self.loc).length > 16:
                continue
            n = self.ndc(c)
            if not (0.04 <= n.x <= 0.96 and 0.04 <= n.y <= 0.96 and n.z > 0):
                continue
            props.append(dict(name=o.name, c=c, dims=dims, top=b[2], w=3 if LIFE_RE.search(o.name) else 1))
        clusters = []
        for p in sorted(props, key=lambda q: -q['dims'][0] * q['dims'][1]):
            for cl in clusters:
                if (cl['c'] - p['c']).length < 1.4 and abs(cl['c'].z - p['c'].z) < 1.2:
                    cl['leden'].append(p)
                    k = len(cl['leden'])
                    cl['c'] = (cl['c'] * (k - 1) + p['c']) / k
                    cl['top'] = max(cl['top'], p['top'])
                    cl['w'] += p['w']
                    break
            else:
                clusters.append(dict(c=p['c'].copy(), leden=[p], top=p['top'], w=p['w']))
        uit = []
        for cl in clusters:
            if cl['w'] < 3:          # geen 'leven' in het cluster -> geen vignet
                continue
            # Een stapel gewone objecten haalt de drempel ook (17 terrastegels x w1 = 17) en versloeg
            # zo bijna de zithoek. Dus apart wegen wat er echt LEEFT, en daarop eerst sorteren.
            levend = [q for q in cl['leden'] if q['w'] >= 3]
            w_life = sum(q['w'] for q in levend)
            if levend:               # mikpunt op het leven zelf, niet op het midden van de stapel eronder
                cl['c'] = sum((q['c'] for q in levend), Vector()) / len(levend)
                cl['top'] = max(q['top'] for q in levend)
            n = self.ndc(cl['c'])
            leden = sorted(cl['leden'], key=lambda q: -q['w'])
            uit.append(dict(center=cl['c'], top=cl['top'], n=len(cl['leden']), w=cl['w'], w_life=w_life,
                            ndc=(n.x, n.y), afstand=(cl['c'] - self.loc).length,
                            leden=[q['name'] for q in leden[:8]]))
        # LIFE-clusters eerst, daarbinnen op massa. Geen harde eis: de R4-scenes hebben generieke
        # propnamen (Object_8, SM_vgztealha) en zouden anders helemaal zonder vignet komen te staan.
        uit.sort(key=lambda v: (-v['w_life'], -v['w']))
        return uit

    def _deuren(self):
        uit = []
        for o in self.meshes:
            if re.search(r"deur|door", o.name, re.I) and self.is_cabin(o) and 'handle' not in o.name.lower():
                a, b = wbbox(o)
                c = Vector([(a[i] + b[i]) / 2 for i in range(3)])
                n = self.ndc(c)
                if 0 <= n.x <= 1 and 0 <= n.y <= 1 and n.z > 0:
                    uit.append(dict(name=o.name, center=c, ndc=(n.x, n.y), afstand=(c - self.loc).length))
        return uit

    def vignet(self, i=0):
        """i-de vignet (grootste eerst); valt terug op de deur en dan op het kijkdoel."""
        if i < len(self.vignetten):
            v = self.vignetten[i]
            return Vector((v['center'].x, v['center'].y, (v['center'].z + v['top']) / 2))
        if self.deuren:
            return self.deuren[0]['center'].copy()
        return self.doel.copy()

    def to_json(self, scene_naam):
        cd = self.cd
        zonnen = [dict(name=o.name, energy=round(o.data.energy, 2), angle_deg=round(math.degrees(o.data.angle), 1),
                       rot_deg=r3([math.degrees(a) for a in o.rotation_euler])) for o in self.scn.objects
                  if o.type == 'LIGHT' and o.data.type == 'SUN']
        w = self.scn.world
        volume = bool(w and w.use_nodes and any(n.type.startswith('VOLUME') for n in w.node_tree.nodes))
        return dict(
            scene=scene_naam, blend=bpy.data.filepath, res=list(self.res),
            cam=dict(name=self.cam.name, loc=r3(self.loc), rot_deg=r3([math.degrees(a) for a in self.rot]),
                     lens=round(self.lens, 2), sensor=round(self.sensor, 1), shift=r3(self.shift),
                     dof=dict(on=cd.dof.use_dof, fstop=round(cd.dof.aperture_fstop, 2), dist=round(cd.dof.focus_distance, 2),
                              obj=cd.dof.focus_object.name if cd.dof.focus_object else None),
                     kijk=r3(self.kijk), doel=r3(self.doel), doel_afst=round((self.doel - self.loc).length, 2)),
            cabin=dict(min=r3(self.cabin_min), max=r3(self.cabin_max), center=r3(self.cabin_c), n_objs=len(self.cabin_objs),
                       ndc_center=r3(self.ndc(self.cabin_c)[:2])),
            ground=sorted(self.ground_names)[:8],
            hero_score=self.hero_score,
            vignetten=[dict(center=r3(v['center']), top=round(v['top'], 2), n=v['n'], w=v['w'],
                            w_life=v['w_life'], ndc=r3(v['ndc']), afstand=round(v['afstand'], 2),
                            leden=v['leden']) for v in self.vignetten[:8]],
            doorzichtig=sorted(self.doorzichtig)[:12],
            deuren=[dict(name=d['name'], center=r3(d['center']), ndc=r3(d['ndc'])) for d in self.deuren[:4]],
            zonnen=zonnen, world_volume=volume,
            exposure=round(self.scn.view_settings.exposure, 2), view=self.scn.view_settings.view_transform,
            look=self.scn.view_settings.look,
        )


def wbbox(o):
    pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
    xs, ys, zs = [p.x for p in pts], [p.y for p in pts], [p.z for p in pts]
    return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))
