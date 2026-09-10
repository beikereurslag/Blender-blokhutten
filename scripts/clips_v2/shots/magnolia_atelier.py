"""S3 atelier: A opent op ezel+doek+bijzettafel, B hero-push, C detail op de deur met terracotta potten."""
def shots(ctx, sl):
    return [
        sl.reveal(ctx, (-1.17, 1.99, 1.05), frames=120, naam="A_reveal"),
        sl.push(ctx, 0.10, frames=96, naam="B_push"),
        sl.detail(ctx, (0.35, 1.30, 0.85), lens=50, frames=96, naam="C_detail"),
    ]
