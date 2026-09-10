"""Overkapping keuken: A opent op vignet 0, B hero-push, C uitsnede op het keukenblok.

Het standaardrecept faalde op C met 0,880/0,878 (post-fix meting, dus tegen het juiste hero-beeld). Buiten
beeld: `IB-Hedge Grass Block.002` 28 stralen, `Terras` 8, GrassTuft_B/A 8, Ground_Grass 2 - samen ~8 %.
Het grondaandeel was hier juist laag (0,007 tegen hero 0,026); het was de heg naast de beeldrand.

Het doel is uit de gerenderde camerasleutel teruggerekend in plaats van uit de probe-JSON (die had 3
verouderde vignetten): de detailcamera stond op (-1,636 / -6,735 / 1,6) met yaw -20,7 en focus 10,64, wat
uitkomt op (2,118 / 3,201 / 0,973) - u = 0,270, v = 0,495. Gecentreerd vanaf 72 mm; hier 72 -> 80 mm.
"""


def shots(ctx, sl):
    return [
        sl.reveal(ctx, ctx.vignet(0), frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.crop_in(ctx, (2.118, 3.201, 0.973), lens0=72, lens1=80, frames=96, naam="C_crop"),
    ]
