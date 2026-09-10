"""S-scene lavendelveld: A reveal op het grootste vignet, B hero-push, C uitsnede op het tweede vignet.

Alleen C week af van het standaardrecept: detail() op vignet 1 gaf 0,762/0,772 - de camera liep 10 %
richting het subject en haalde daarmee de lavendelrand buiten het hero-beeld binnen. Vervangen door
crop_in (uitsnede vanuit de hero-stand), dat per definitie een deelverzameling van het hero-beeld is.
A (1,0) en B (1,0) haalden de toets ruim en blijven ongewijzigd.
"""


def shots(ctx, sl):
    return [
        sl.reveal(ctx, ctx.vignet(0), frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.crop_in(ctx, ctx.vignet(1), lens0=52, lens1=60, frames=96, naam="C_crop"),
    ]
