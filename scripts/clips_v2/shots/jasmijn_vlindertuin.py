"""B12 vlindertuin: A opent op bank+tafel met vaas onder de kap, B hero-push, C detail laag op het vogelbad met de bloemen
(deur-fallback gaf 0,89 en toonde vooral wand)."""
def shots(ctx, sl):
    return [
        sl.reveal(ctx, (-1.67, -0.28, 0.45), frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.detail(ctx, (-2.66, 3.20, 0.65), lens=50, dz=-0.30, hoogte_ndc=0.45, frames=96, naam="C_detail"),
    ]
