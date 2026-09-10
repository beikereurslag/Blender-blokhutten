r"""Shot-woordenschat voor clips-v2. Alle shots blijven binnen het hero-beeld:

  push     dolly langs de kijkas naar het doel (zelfde blik, beeld krimpt naar binnen)
  settle   zachte pedestal (omhoog/omlaag) met shift_y-compensatie: camera blijft waterpas,
           verticalen blijven loodrecht (geen tilt - regel uit het compendium §3)
  truck    kleine zijwaartse beweging, blik vast (parallax)
  zoom     statisch hero-standpunt, alleen de lens kruipt naar binnen (strikt binnen het hero-beeld)
  crop_in  zelfde als zoom, maar pant met shift naar een subject: een uitsnede van het hero-beeld
  detail   langere lens (50-60 mm) op een vignet IN het hero-beeld, met kleine drift
  reveal   begint als detail en opent naar exact het hero-beeld (lens+yaw+shift lopen mee)
  focus    statisch hero-beeld, scherpte glijdt van dichtbij naar het doel

Een shot is een dict met 'naam', 'frames' en twee 'keys' (begin/eind), elke key een
camera-toestand: loc, rot (euler XYZ), lens, shift_y, focus (afstand). De engine zet daar
keyframes op (Bezier = zachte ease in/uit).

Camera's blijven waterpas: rot.x = 90 graden, rot.y = 0, alleen yaw (rot.z) verandert;
verticale framing gaat via shift_y. Dat is precies hoe de hero-camera's zijn opgezet.
"""
import math

from mathutils import Euler, Vector


def _yaw_naar(van, naar):
    """rot.z zodat een waterpas camera (rot.x=90) horizontaal naar 'naar' kijkt."""
    # rot=(90°,0,0) kijkt langs +Y (atan2=90°) -> yaw = atan2 - 90°; klopt met B13: kijk (0.545,-0.838) -> rot.z -146.98°
    d = Vector(naar) - Vector(van)
    return math.atan2(d.y, d.x) - math.pi / 2


def _shift_voor(ctx, van, naar, lens, hoogte_ndc=0.5):
    """shift_y zodat punt 'naar' op relatieve beeldhoogte hoogte_ndc komt (0.5 = midden)."""
    d = Vector(naar) - Vector(van)
    dist_h = math.hypot(d.x, d.y)
    if dist_h < 0.05:
        return ctx.shift[1]
    # verticale hoek -> sensor-eenheden: dz/dist * lens/sensor, gecorrigeerd voor gewenste beeldhoogte
    s = (d.z / dist_h) * lens / ctx.sensor
    s -= (hoogte_ndc - 0.5) * ctx.aspect
    return max(-0.35, min(0.45, s))


def _key(loc, rot, lens, shift_y, focus, shift_x=0.0):
    return dict(loc=Vector(loc), rot=Euler(rot, 'XYZ'), lens=float(lens), shift_y=float(shift_y),
                shift_x=float(shift_x), focus=float(focus))


def _hero_key(ctx, loc=None, focus=None):
    loc = Vector(loc) if loc is not None else ctx.loc.copy()
    f = focus if focus is not None else (ctx.doel - loc).length
    return _key(loc, ctx.rot, ctx.lens, ctx.shift[1], f, ctx.shift[0])


def _level_key(ctx, loc, doel, lens, hoogte_ndc=0.5):
    loc = Vector(loc)
    rot = (math.pi / 2, 0.0, _yaw_naar(loc, doel))
    return _key(loc, rot, lens, _shift_voor(ctx, loc, doel, lens, hoogte_ndc), (Vector(doel) - loc).length,
                ctx.shift[0])


def S(naam, k0, k1, frames=120, **extra):
    d = dict(naam=naam, frames=frames, keys=[k0, k1])
    d.update(extra)
    return d


# ----------------------------------------------------------------------------- hero-shots
def push(ctx, fractie=0.10, frames=120, naam="push"):
    v = ctx.doel - ctx.loc
    p1 = ctx.loc + v * fractie
    return S(naam, _hero_key(ctx), _hero_key(ctx, p1), frames)


def pull(ctx, fractie=0.10, frames=120, naam="pull"):
    sh = push(ctx, fractie, frames, naam)
    sh['keys'].reverse()
    return sh


def settle(ctx, dz0=0.18, dz1=-0.12, push_fractie=0.04, frames=120, naam="settle"):
    """Zachte pedestal omlaag; shift_y compenseert zodat het doel op dezelfde beeldhoogte blijft."""
    v = ctx.doel - ctx.loc
    dist_h = math.hypot(v.x, v.y)
    k = []
    for dz, pf in ((dz0, 0.0), (dz1, push_fractie)):
        loc = ctx.loc + v * pf + Vector((0, 0, dz))
        comp = dz / dist_h * ctx.lens / ctx.sensor
        kk = _hero_key(ctx, loc)
        kk['shift_y'] = ctx.shift[1] + comp
        k.append(kk)
    return S(naam, k[0], k[1], frames)


def truck(ctx, breedte=0.5, lr=True, push_fractie=0.03, frames=120, naam="truck"):
    a = ctx.rechts * (-breedte / 2)
    b = ctx.rechts * (breedte / 2)
    if not lr:
        a, b = b, a
    v = ctx.doel - ctx.loc
    return S(naam, _hero_key(ctx, ctx.loc + a), _hero_key(ctx, ctx.loc + b + v * push_fractie), frames)


def zoom(ctx, factor=1.30, lens_eind=None, frames=120, naam="zoom"):
    """Zelfde standpunt, blik en shift als de hero; alleen de lens loopt naar binnen. Daarmee is het
    beeld een smaller frustum van het hero-beeld en dus per definitie frame-veilig - anders dan settle,
    die als pedestal het beeld aan de boven/onderrand openduwt (C_settle 0,865 op buitenbioscoop)."""
    k1 = _hero_key(ctx)
    k1['lens'] = float(lens_eind) if lens_eind else ctx.lens * factor
    return S(naam, _hero_key(ctx), k1, frames)


def _beeldcoord(ctx, doel):
    """Doel -> beeldcoordinaten (lx, ly) zoals geo.rays ze rekent: lx = X/diepte, ly = Z/diepte,
    met X langs ctx.rechts (camera-rechts) en de camera waterpas (camera-omhoog = wereld +Z)."""
    d = Vector(doel) - ctx.loc
    diepte = d.dot(ctx.kijk)
    if diepte < 0.5:
        return None
    return d.dot(ctx.rechts) / diepte, d.z / diepte


_CROP_MARGE = 0.01   # in shift-eenheden (fractie sensorbreedte)


def _crop_shift(ctx, lx, ly, lens):
    """shift zodat (lx, ly) in het midden komt, geklemd zodat het beeld een echte uitsnede van het
    hero-beeld blijft. geo.rays: lx = (u - 0.5 + sx) * S / L, ly = ((v - 0.5) * a + sy) * S / L, dus het
    beeld beslaat lx in [(-0.5 + sx)S/L, (0.5 + sx)S/L] en ly in [(-a/2 + sy)S/L, (a/2 + sy)S/L].
    Bevatting t.o.v. de hero (L0, sx0, sy0) met k = L/L0 geeft sx in [k(sx0 - 0.5) + 0.5, k(sx0 + 0.5) - 0.5]
    (idem verticaal met a/2). Voor k > 1 is dat een niet-leeg interval -> altijd een veilige uitsnede."""
    k = lens / ctx.lens
    h = ctx.aspect / 2.0
    sx0, sy0 = ctx.shift

    def klem(lo, hi, wens):
        # marge: een geklemde uitsnede mag niet exact op de hero-rand liggen, dan vallen er door
        # afrondingen randstralen buiten (buitenbioscoop verloor ongeklemd al 2 van 576 stralen)
        if hi - lo <= 2 * _CROP_MARGE:
            return (lo + hi) / 2.0
        return max(lo + _CROP_MARGE, min(hi - _CROP_MARGE, wens))

    sx = klem(k * (sx0 - 0.5) + 0.5, k * (sx0 + 0.5) - 0.5, lx * lens / ctx.sensor)
    sy = klem(k * (sy0 - h) + h, k * (sy0 + h) - h, ly * lens / ctx.sensor)
    return sx, sy


def crop_in(ctx, doel, lens0=None, lens1=None, frames=120, naam="crop"):
    """Uitsnede van het hero-beeld die naar 'doel' pant: standpunt en blikrichting blijven exact die van
    de hero, alleen de lens kruipt naar binnen en de shift pant mee. Omdat het frustum daarmee binnen het
    hero-frustum blijft (zie _crop_shift) is de shot frame-veilig voor elk subject, ook aan de beeldrand -
    een subject dat te ver naar buiten zit wordt geklemd en komt dan uit het midden te liggen i.p.v. de
    toets te laten falen. Dit is de manier om een prop uit te lichten zonder de camera te verplaatsen;
    detail() loopt richting het subject en onthult daarmee ongeklede randen (C 0,851 op familiemiddag)."""
    lens0 = float(lens0 or ctx.lens * 1.5)
    lens1 = float(lens1 or lens0 * 1.15)
    bc = _beeldcoord(ctx, doel)
    assert bc, f"{naam}: doel {tuple(round(c, 2) for c in doel)} ligt niet voor de camera"
    lx, ly = bc
    k = []
    for lens in (lens0, lens1):
        sx, sy = _crop_shift(ctx, lx, ly, lens)
        kk = _hero_key(ctx, focus=(Vector(doel) - ctx.loc).length)
        kk['lens'], kk['shift_x'], kk['shift_y'] = lens, sx, sy
        k.append(kk)
    return S(naam, k[0], k[1], frames)


def crop_reveal(ctx, doel, lens0=None, frames=144, naam="reveal"):
    """Opent als uitsnede op 'doel' en zoomt uit naar exact het hero-beeld. Standpunt, blik en hoogte
    blijven die van de hero; alleen lens en shift lopen. Elke tussenstand is dus ook een uitsnede: het
    bevattingsgebied is per as begrensd door twee lineaire ongelijkheden in (k, shift) en dus convex, en de
    baan tussen begin- en eindsleutel is recht - dus frame-veilig over de hele shot, niet alleen op de
    sleutels. Alternatief voor reveal() als die op de openingsstand faalt (buitenbad A: 0,792)."""
    lens0 = float(lens0 or ctx.lens * 1.7)
    bc = _beeldcoord(ctx, doel)
    assert bc, f"{naam}: doel {tuple(round(c, 2) for c in doel)} ligt niet voor de camera"
    sx, sy = _crop_shift(ctx, bc[0], bc[1], lens0)
    k0 = _hero_key(ctx, focus=(Vector(doel) - ctx.loc).length)
    k0['lens'], k0['shift_x'], k0['shift_y'] = lens0, sx, sy
    return S(naam, k0, _hero_key(ctx), frames)


# ----------------------------------------------------------------------------- vignet-shots
def _detail_pos(ctx, doel, nader=0.30, min_afst=3.0, dz=0.0, zij=0.0):
    """Camerapositie voor een detailshot: vanaf de hero-positie een stuk richting het vignet,
    nooit dichter dan min_afst, hoogte hero (+dz), optioneel zijwaarts (langs hero-rechts)."""
    doel = Vector(doel)
    v = Vector((doel.x - ctx.loc.x, doel.y - ctx.loc.y, 0.0))
    afst = v.length
    stap = min(afst * nader, max(afst - min_afst, 0.0))
    p = ctx.loc + v.normalized() * stap + ctx.rechts * zij
    return Vector((p.x, p.y, ctx.loc.z + dz))


def detail(ctx, doel, lens=55.0, nader=0.10, drift=0.25, dz=0.0, hoogte_ndc=0.5, frames=120, naam="detail",
           min_afst=3.0):
    p0 = _detail_pos(ctx, doel, nader, min_afst, dz, zij=-drift / 2)
    p1 = _detail_pos(ctx, doel, nader + 0.03, min_afst, dz, zij=drift / 2)
    return S(naam, _level_key(ctx, p0, doel, lens, hoogte_ndc), _level_key(ctx, p1, doel, lens, hoogte_ndc), frames)


def reveal(ctx, doel, lens0=55.0, nader=0.06, dz=0.0, hoogte_ndc=0.5, frames=144, naam="reveal", min_afst=3.0):
    """Opent op het vignet en landt op exact het hero-beeld."""
    p0 = _detail_pos(ctx, doel, nader, min_afst, dz)
    return S(naam, _level_key(ctx, p0, doel, lens0, hoogte_ndc), _hero_key(ctx), frames)


def focus_pull(ctx, van=1.6, frames=120, naam="focus"):
    k0 = _hero_key(ctx, focus=van)
    k1 = _hero_key(ctx)
    return S(naam, k0, k1, frames, fstop_max=2.8)


# ----------------------------------------------------------------------------- standaardrecept
def default_recipe(ctx):
    """A reveal op het grootste vignet -> B hero-push -> C detail op het tweede vignet/deur."""
    v0 = ctx.vignet(0)
    # 120+96+96 frames = 13 s bruto, ~12 s met crossfades; ~40 s/frame op 1080p/48 -> ~3,5 u per scene
    shots = [reveal(ctx, v0, frames=120, naam="A_reveal"), push(ctx, 0.10, frames=96, naam="B_push")]
    if len(ctx.vignetten) > 1:
        shots.append(detail(ctx, ctx.vignet(1), lens=50.0, frames=96, naam="C_detail"))
    else:
        # geen tweede vignet: de deur zit in de B-reeks aan de linkerrand (toets 0,69-0,87) en een
        # pedestal is niet frame-veilig (C_settle 0,865/0,837 op buitenbioscoop) -> lens-inzoom
        shots.append(zoom(ctx, factor=1.30, frames=96, naam="C_zoom"))
    return shots
