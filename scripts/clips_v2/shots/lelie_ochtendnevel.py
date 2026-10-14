"""Ochtendnevel: A reveal, B hero-push, C uitsnede op het tweede vignet.

C_detail gaf 0,868/0,874 en verdubbelde het grondaandeel (0,352 tegen hero 0,196): de detailstand liep
naar het subject toe en kadreerde omlaag, precies de valkuil van goudenborrel en uitslaapochtend.
Nu een crop_in vanuit de hero-stand, zodat de nevel-compositie (het punt van deze scene) intact blijft.
A en B scoorden 1,0 en blijven ongewijzigd.
"""


def shots(ctx, sl):
    return [
        sl.reveal(ctx, ctx.vignet(0), frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.crop_in(ctx, ctx.vignet(1), lens0=52, lens1=60, frames=96, naam="C_crop"),
    ]
