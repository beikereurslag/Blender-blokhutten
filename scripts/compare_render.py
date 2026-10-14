"""Create side-by-side composite of render + reference image for self-audit.

Uses Pillow (PIL). Install via: pip install pillow

Run:
    python scripts/compare_render.py training/renders/lavendel_modern_v1.png references/lugarde_modern.jpg

Output: training/comparisons/lavendel_modern_v1_vs_ref.png
"""
import sys
import os


def make_side_by_side(render_path, reference_path, output_path, target_height=720):
    """Create horizontal side-by-side composite scaled to same height."""
    try:
        from PIL import Image
    except ImportError:
        print("PIL not available — install with: pip install pillow")
        return False

    if not os.path.exists(render_path):
        print(f"Render not found: {render_path}")
        return False

    render = Image.open(render_path).convert("RGB")

    if reference_path and os.path.exists(reference_path):
        ref = Image.open(reference_path).convert("RGB")
    else:
        # Make placeholder
        ref = Image.new("RGB", (1280, 720), color=(200, 200, 200))

    # Scale both to target height
    def scale_to_height(img, h):
        w, ih = img.size
        new_w = int(w * h / ih)
        return img.resize((new_w, h), Image.LANCZOS)

    render_scaled = scale_to_height(render, target_height)
    ref_scaled = scale_to_height(ref, target_height)

    # Composite
    gap = 20
    total_w = render_scaled.width + gap + ref_scaled.width
    composite = Image.new("RGB", (total_w, target_height + 60), color=(40, 40, 40))
    composite.paste(render_scaled, (0, 30))
    composite.paste(ref_scaled, (render_scaled.width + gap, 30))

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    composite.save(output_path)
    print(f"Saved comparison: {output_path}")
    print(f"  Render: {render_scaled.size} (left)")
    print(f"  Ref: {ref_scaled.size} (right)")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python compare_render.py <render.png> [reference.jpg]")
        return

    render = sys.argv[1]
    ref = sys.argv[2] if len(sys.argv) > 2 else None

    out_dir = "training/comparisons"
    base = os.path.splitext(os.path.basename(render))[0]
    out = os.path.join(out_dir, f"{base}_vs_ref.png")

    make_side_by_side(render, ref, out)


if __name__ == "__main__":
    main()
