"""Dahlia leeshoek: A opent op de leesplek (vignet 0), B hero-push, C uitsnede op tafel+fauteuil met het
open boek.

Het standaardrecept mikte C op vignet 1, en dat vignet is de **terrasvloer**: `DlTerras_base/_1_1/_1_2/...`.
Resultaat 0,502/0,503 - de slechtste van de hele pass, met 178 stralen op Ground_Grass en een grondaandeel
van 0,363 tegen hero 0,085. Een detailshot op een vloer kan niet anders dan grond in beeld halen.

Twee oorzaken, beide in geo.py (niet aangepast, want dat verandert ook de A-doelen van andere scenes):

1. `SKIP_RE` is geankerd met `^`, dus een naam met scene-prefix ontsnapt aan het filter: `DlTerras_base`
   matcht niet op `^Terras`. Zelfde patroon: `CwTerrasMain` (wijnterras), `LaDeck_p10` (avondkubus),
   `OnDeck_base` (ochtendnevel), `Betonvloer` (bergkap).
2. De 'leven'-drempel `cl['w'] < 3` is bedoeld als "er moet minstens iets van leven in zitten" (LIFE_RE
   geeft w=3), maar een stapel gewone objecten haalt die drempel net zo goed: 17 terrastegels x w=1 = 17.
   En omdat er op `-w` gesorteerd wordt, verslaat die stapel bijna de zithoek (v0 w=18, v1 w=17).

Hier daarom C met een vaste coordinaat op de leesplek zelf: tafel, fauteuil en het open boek, gecentreerd
op 75 -> 85 mm. A blijft het standaardrecept (haalde 0,924/1,00).
"""


def shots(ctx, sl):
    return [
        sl.reveal(ctx, ctx.vignet(0), frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.crop_in(ctx, (-1.598, 2.718, 0.67), lens0=75, lens1=85, frames=96, naam="C_crop"),
    ]
