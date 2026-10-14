"""B10 vinylmiddag: A opent op fauteuil+platenspeler onder de kap, B hero-push, C detail laag op de plantenbakken
voor de veranda-rand (recht op de deur gaf 0,87: linkerrand buiten het hero-beeld)."""
def shots(ctx, sl):
    return [
        sl.reveal(ctx, (-2.03, -0.49, 0.55), frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.detail(ctx, (-1.20, 2.60, 0.55), lens=50, dz=-0.25, hoogte_ndc=0.45, frames=96, naam="C_detail"),
    ]
