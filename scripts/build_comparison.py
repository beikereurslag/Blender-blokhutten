"""Build side-by-side comparison composite of multiple renders.

Usage:
    python scripts/build_comparison.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

RENDER_DIR = "C:/Users/beike/Documents/Blender-blokhutten/training/renders"

# TUIN INRICHTING comparison — procedural placement vs designed garden
COMPARISONS = [
    [
        ("lavendel_real_v6.png", "OLD: mirror potten, tree row, no zones"),
        ("lavendel_garden_v7.png", "NEW: asymmetric, 4 zones, real design ★"),
    ],
]


def main():
    # Load images
    grid = []
    target_w = 850  # per-tile width (2-wide before/after)
    for row in COMPARISONS:
        row_imgs = []
        for fname, label in row:
            path = os.path.join(RENDER_DIR, fname)
            if not os.path.exists(path):
                print(f"WARN: skip {fname}")
                continue
            img = Image.open(path)
            ratio = target_w / img.width
            new_h = int(img.height * ratio)
            img = img.resize((target_w, new_h), Image.LANCZOS)

            # Add label bar at bottom
            label_bar_h = 36
            new_img = Image.new("RGB", (target_w, new_h + label_bar_h), (40, 40, 50))
            new_img.paste(img, (0, 0))
            draw = ImageDraw.Draw(new_img)
            try:
                font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 18)
            except OSError:
                font = ImageFont.load_default()
            draw.text((12, new_h + 8), label, fill=(220, 220, 220), font=font)
            row_imgs.append(new_img)
        if row_imgs:
            grid.append(row_imgs)

    if not grid:
        print("No images found")
        return

    # Composite into grid
    n_cols = max(len(r) for r in grid)
    n_rows = len(grid)
    tile_w = grid[0][0].width
    tile_h = grid[0][0].height
    gap = 8
    total_w = tile_w * n_cols + gap * (n_cols + 1)
    total_h = tile_h * n_rows + gap * (n_rows + 1) + 60  # header room

    out = Image.new("RGB", (total_w, total_h), (24, 24, 30))
    draw = ImageDraw.Draw(out)
    try:
        title_font = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 28)
    except OSError:
        title_font = ImageFont.load_default()
    draw.text((gap, 12), "TUIN INRICHTING: procedural placement vs garden design principles", fill=(245, 245, 250), font=title_font)

    for r, row in enumerate(grid):
        for c, tile in enumerate(row):
            x = gap + c * (tile_w + gap)
            y = 60 + gap + r * (tile_h + gap)
            out.paste(tile, (x, y))

    out_path = os.path.join(RENDER_DIR, "TUIN_before_after.png")
    out.save(out_path, "PNG")
    print(f"Saved: {out_path}")
    print(f"Size: {total_w}x{total_h}")


if __name__ == "__main__":
    main()
