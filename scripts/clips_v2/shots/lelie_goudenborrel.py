"""S2 goudenborrel: A opent op sofa+salontafel onder de kap, B hero-push, C uitsnede op de vuurkorf met
krukjes (stone_fire_pit op 3,6 / 5,2 met VuurKruk_0/1 ernaast).

De vorige C was een detail() met dz=-0.35 en hoogte_ndc=0.40: de camera zakte 35 cm, liep 10 % naar de
vuurkorf toe en kantelde de kadrering naar beneden. Dat haalde de voorgrond binnen en faalde de toets hard
(inside 0,597/0,582 - 200 van 576 stralen op GrassTuft_A/B/C, IB-Hedge Grass Block en Ground_Grass).

Met crop_in blijft de camera exact op de hero-positie en -hoogte staan. De gewenste kadrering (vuur in het
onderste derde) komt nu uit het mikpunt in plaats van uit een lagere camera: er wordt op 80 cm boven de
grond gemikt, 45 cm boven de vuurkorf zelf, waardoor de korf in de uitsnede op v = 0,27 (65 mm) tot
v = 0,24 (74 mm) valt. Horizontaal is 65 mm het minimum om dat punt te kunnen centreren (u = 0,285).
"""


def shots(ctx, sl):
    return [
        sl.reveal(ctx, (-2.33, -0.33, 0.70), frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.crop_in(ctx, (3.55, 4.9, 0.80), lens0=65, lens1=74, frames=96, naam="C_crop"),
    ]
