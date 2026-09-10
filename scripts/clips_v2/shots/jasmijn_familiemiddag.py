"""S1 familiemiddag: A opent op de picknicktafel+mand onder de kap, B hero-push, C uitsnede op de deur
met de plantenborder.

De vorige C was een detail() op de deur en faalde de toets (inside 0,851/0,847): detail() loopt 10 % naar
het subject toe plus een zijwaartse drift, en dat kleine stapje zwaaide heg en grasranden buiten het
hero-beeld in beeld (149 van 576 stralen op IB-Hedge Grass Block, GrassTuft_A/B/C, Ground_Grass, een
pine-trunk). Met crop_in blijft de camera exact op de hero-positie en -blik staan en snijdt alleen de lens
naar binnen, dus er kan per definitie geen nieuwe rand in beeld komen.

Het doel ligt tussen de deur (1,485 / 1,251) en BorderR1 (0,553 / 1,759) zodat beide in de uitsnede vallen;
op 55 mm valt dat punt precies in het midden (64 % van de hero-breedte), op 64 mm nog steeds (55 %).
"""


def shots(ctx, sl):
    return [
        sl.reveal(ctx, (-1.675, 0.05, 0.80), frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.crop_in(ctx, (1.02, 1.505, 0.69), lens0=55, lens1=64, frames=96, naam="C_crop"),
    ]
