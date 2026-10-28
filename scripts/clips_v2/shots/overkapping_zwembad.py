"""Overkapping zwembad: A opent op de zithoek (vignet 0), B hero-push, C uitsnede op de ligbedden.

Het standaardrecept faalde op C met 0,748/0,752 (post-fix meting) - de op een haar na exacte waarde die de
audit voorspelde (0,747). Buiten beeld: `Deck_links` 45 stralen, `IB-Hedge Grass Block.002` 35,
`Deck_voor` 28, GrassTuft_B/A 26. Het grondaandeel was verwaarloosbaar (0,010 tegen hero 0,003); het waren
de randen van het zwembaddek en de heg naast het beeld.

C-doel is vignet 1: `Sun lounger for pool` (x2) met BadRand_l/BadWand_l, op u = 0,192 / v = 0,280. Dat is
niet te centreren onder de 95 mm (37 % van de hero-breedte), dus een geklemde uitsnede: 75 -> 85 mm, waarbij
de ligbedden op u = 0,40 -> 0,46 landen en verticaal wel gecentreerd zijn.
"""


def shots(ctx, sl):
    return [
        sl.reveal(ctx, ctx.vignet(0), frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.crop_in(ctx, (0.633, -3.842, 0.368), lens0=75, lens1=85, frames=96, naam="C_crop"),
    ]
