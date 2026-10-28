"""B15 modern: A opent op het houtblok-hoekje met schep (vignet 0), B hero-push, C uitsnede op de
designfauteuil.

Het standaardrecept mikte C op vignet 1 = modern_arm_chair_01, en dat faalde de toets op 0,625/0,627: de
fauteuil staat op u = 0,135, dus vlak tegen de linkerrand, en detail() liep er 10 % naartoe. Daarmee kwamen
Ground_Grass (60 stralen), Deck_Wood (45) en drie berken (62) buiten het hero-beeld in beeld, en verdubbelde
het grondaandeel (0,132 tegen hero 0,049).

De fauteuil is met geen enkele redelijke brandpuntsafstand te centreren (dat lukt pas vanaf 118 mm, en dan
is de uitsnede 27 % van de hero-breedte). Daarom hier bewust een geklemde uitsnede: op 70 -> 80 mm loopt de
uitsnede tegen de linkerrand van het hero-beeld aan en staat de fauteuil op u = 0,29 -> 0,33, dus in het
linkerderde, verticaal gecentreerd. Let op: deze scene heeft een hero-lens van 32 mm, niet 35.
Nagekomen (4 sep, hertoets na de geo-fix): ook A faalde, op 0,694 met grondaandeel 0,12 tegen hero 0,049.
reveal() opent op de vignet-stand en die ligt hier laag-links op het gazon. Omgezet naar crop_reveal:
opent als uitsnede op 58 mm bij het houtblok-hoekje en zoomt uit naar exact het 32 mm hero-beeld.
"""


def shots(ctx, sl):
    return [
        sl.crop_reveal(ctx, ctx.vignet(0), lens0=58, frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.crop_in(ctx, (3.184, 2.194, 0.66), lens0=70, lens1=80, frames=96, naam="C_crop"),
    ]
