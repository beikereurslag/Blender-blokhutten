"""S7 leesplek: A opent op de leesstoel met boek onder de kap, B hero-push, C detail tussen leesstoel en wijnton
(recht op de ton gaf 0,81: rechterrand liep buiten het hero-beeld)."""
def shots(ctx, sl):
    return [
        sl.reveal(ctx, (-1.30, 0.11, 0.75), frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.detail(ctx, (-2.30, 1.10, 0.65), lens=50, frames=96, naam="C_detail"),
    ]
