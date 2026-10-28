"""Camelia wijnterras: A opent als uitsnede op de eettafel en zoomt uit naar het hero-beeld, B hero-push,
C lens-inzoom (zoals het standaardrecept).

A faalde op **0,688**, de slechtste A van de hele pass. Het vignet (bord, plateau, rieten stoelen; w = 54)
staat op u = 0,855, dus vlak tegen de rechterrand, en reveal() loopt 6 % ernaartoe - dat haalde Ground_Grass
(76 stralen), HedgeSprig (50), FestoenPaal (13) en CwTerrasMain (5) binnen, en tilde het grondaandeel van
0,125 naar 0,201. A-verdicts zijn betrouwbaar ook van voor de reset_cam-fix (de A-toets loopt als eerste,
voordat een render de camera heeft verplaatst), dus dit is een echte fout.

Nu crop_reveal: opent geklemd op 65 mm tegen de rechterrand (62 % van de hero-breedte, eettafel rechts in
beeld) en zoomt uit naar exact de 40 mm hero-stand.

C blijft de lens-inzoom van het standaardrecept. Die scoorde 0,804 in de pass, maar dat was volledig het
reset_cam-artefact: de eerste sleutel van een zoom *is* het hero-beeld, dus die is in werkelijkheid 1,000.
Deze scene heeft een hero-lens van 40 mm en maar een vignet.
"""


def shots(ctx, sl):
    return [
        sl.crop_reveal(ctx, (-1.601, 3.555, 0.7245), lens0=65, frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.zoom(ctx, factor=1.30, frames=96, naam="C_zoom"),
    ]
