"""B11 uitslaapochtend: A opent op ligbed+lantaarn onder de kap, B hero-push, C uitsnede laag op de
plantenbakken voor de veranda.

Twee eerdere pogingen faalden de toets: recht op de deur gaf 0,69 (linkerrand buiten het hero-beeld) en de
detail() op de plantenbakken met dz=-0.25 + hoogte_ndc=0.45 gaf 0,818/0,811 - de camera zakte naar z=1,17
en kadreerde omlaag, waardoor GrassTuft_A/B/C, HedgeSprig, Ground_Grass en het Mist_Rig buiten het
hero-beeld in beeld kwamen.

Met crop_in blijft de camera op hero-hoogte staan en komt "laag" uit het mikpunt: er wordt op 70 cm gemikt,
20 cm boven de plantenbakken, waardoor die in de uitsnede op v = 0,41 (62 mm) tot v = 0,39 (70 mm) vallen.
De bakken staan op u = 0,318; 60 mm is het minimum om dat punt te kunnen centreren.
"""


def shots(ctx, sl):
    return [
        sl.reveal(ctx, (-2.53, -0.08, 0.60), frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.crop_in(ctx, (-1.40, 2.90, 0.70), lens0=62, lens1=70, frames=96, naam="C_crop"),
    ]
