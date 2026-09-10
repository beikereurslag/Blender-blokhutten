"""Lavendel pluktuin: A opent op de plantvakken (vignet 0), B hero-push, C uitsnede op de bank.

Het standaardrecept mikte C op vignet 1 (`Object_7/9/5`, u = 0,761) en faalde op 0,807/0,844 - dit is een
post-fix meting, dus tegen het juiste hero-beeld. Buiten beeld: Object_9.007 (29 stralen), HedgeSprig (24),
Ground_Grass (19). Het grondaandeel was niet het probleem (0,271 tegen hero 0,257); het was de heg en de
plantvakken naast de beeldrand.

C ligt nu op `bench_bench_0` (vignet 3, u = 0,704 / v = 0,453): het enige herkenbare 'leven' in deze scene
tussen de generieke R4-namen, en het geeft variatie omdat A al op de plantvakken opent. Gecentreerd vanaf
62 mm; hier 62 -> 72 mm.
"""


def shots(ctx, sl):
    return [
        sl.reveal(ctx, ctx.vignet(0), frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.crop_in(ctx, (-1.848, 2.70, 0.6775), lens0=62, lens1=72, frames=96, naam="C_crop"),
    ]
