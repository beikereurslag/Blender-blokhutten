"""R4 buitenbad: A opent als uitsnede op de zitgroep bij het bad en zoomt uit naar het hero-beeld,
B hero-push, C uitsnede op de bank.

Deze scene faalde als enige op **twee** shots. A (reveal op vignet 0, 6 % naar het subject toe) opende op
0,792: Ground_Grass 46 stralen en HedgeSprig 39 buiten het hero-beeld. C (detail op de bank) gaf
0,859/0,875. Het hero-beeld heeft hier veel grond (0,234) en de vignetten liggen ver naar rechts
(u = 0,794 en 0,699), dus elke camerabeweging haalt gras en heg binnen.

Daarom hier alleen uitsnede-shots: A met crop_reveal (opent op 60 mm, zoomt uit naar de 35 mm hero-stand),
C met crop_in (60 -> 70 mm, bank gecentreerd). De beweging in de scene komt van B_push.

R4-scene: de propnamen zijn generiek (Object_3/5/6/8/11), dus de vignet-ranking op 'leven' is hier zwak -
vandaar de vaste wereldcoordinaten.
"""


def shots(ctx, sl):
    return [
        sl.crop_reveal(ctx, (-1.064, 4.092, 0.84), lens0=60, frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.crop_in(ctx, (-1.606, 2.506, 0.70), lens0=60, lens1=70, frames=96, naam="C_crop"),
    ]
