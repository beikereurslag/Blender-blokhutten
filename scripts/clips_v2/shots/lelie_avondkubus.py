"""Avondkubus: de enige scene naast buitenbad die op twee shots faalde, dus volledig op uitsnede-shots.

A_reveal opende op 0,614 met een grondaandeel van 0,443 tegen hero 0,161 - de openingsstand stond laag en
dicht bij het vignet, waardoor het beeld voor bijna de helft uit gras bestond dat in het hero-beeld niet
te zien is. C_detail gaf 0,828/0,817. Het hero-beeld heeft hier geen lucht (sky 0,0), dus elke camera die
zakt of naar voren loopt ruilt kubus in voor grond.

A gaat daarom via crop_reveal (opent op 60 mm bij het vignet, zoomt uit naar de 35 mm hero-stand) en C via
crop_in. De beweging in de clip komt van B_push.
"""


def shots(ctx, sl):
    return [
        sl.crop_reveal(ctx, ctx.vignet(0), lens0=60, frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.crop_in(ctx, ctx.vignet(1), lens0=55, lens1=65, frames=96, naam="C_crop"),
    ]
