"""B14 buitenbioscoop: A opent op de zitplek (plaid/poufs/popcorn), B hero-push, C uitsnede op het
projectiedoek.

Deze scene had geen eigen shotlijst en viel voor C terug op settle; die faalde de toets (inside
0,865/0,837), want een pedestal duwt het beeld aan de boven/onderrand open. Het doek is hier het
onderwerp van de scene maar staat niet in de vignet-ranking (LIFE_RE weegt meubels/lampen/spullen, geen
doek+frame). De wereldcoordinaat komt uit de v1-probe (DoekFrame+Doek, ndc 0,662 - ruim binnen het beeld);
hij wordt bij naam opgezocht zodat een verschoven doek meeloopt. Op 58 mm valt het doek in het midden van
de uitsnede (60 % van de hero-breedte), op 66 mm nog steeds (53 %).
"""
import bpy
from mathutils import Vector

DOEK_TERUGVAL = Vector((-2.1, -1.505, 1.37))


def _doek(ctx):
    for naam in ("Doek", "DoekFrame"):
        o = bpy.data.objects.get(naam)
        if o and o.type == 'MESH':
            hoeken = [o.matrix_world @ Vector(b) for b in o.bound_box]
            return sum(hoeken, Vector()) / len(hoeken)
    return DOEK_TERUGVAL


def shots(ctx, sl):
    return [
        sl.reveal(ctx, ctx.vignet(0), frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.crop_in(ctx, _doek(ctx), lens0=58, lens1=66, frames=96, naam="C_crop"),
    ]
