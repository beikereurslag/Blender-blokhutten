"""S8 goudenuur: A opent op sofa+tafel onder de kap (lichtsnoer), B hero-push, C detail op de lantaarn aan de veranda-rand
(recht op het bistrotafeltje rechts gaf 0,84: rechterrand buiten het hero-beeld)."""
def shots(ctx, sl):
    return [
        sl.reveal(ctx, (-2.10, -0.04, 0.70), frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.detail(ctx, (-2.60, 1.60, 0.60), lens=50, frames=96, naam="C_detail"),
    ]
