"""S5 tuinwerkzaterdag: A opent op de fauteuils onder de kap, B hero-push, C detail op lantaarn + veranda-rand
(niet op de staptegels: die trokken kaal gras onder het hero-beeld in beeld, toets 0,58)."""
def shots(ctx, sl):
    return [
        sl.reveal(ctx, (-0.74, 0.175, 0.90), frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.detail(ctx, (-2.0, 1.2, 0.70), lens=50, frames=96, naam="C_detail"),
    ]
