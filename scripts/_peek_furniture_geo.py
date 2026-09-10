"""Append meubel-assets in een leeg bestand, rapporteer afmetingen + rugleuning-richting
(welke horizontale kant de hoge geometrie zit = achterkant), dan info printen.
Bepaalt 'forward' = weg van de rugleuning."""
import bpy, os
from mathutils import Vector
ROOT = r"C:\Users\beike\Documents\Blender-blokhutten\assets\polyhaven\models"
ITEMS = [("modern_arm_chair_01_2k.blend", "modern_arm_chair_01"),
         ("coffee_table_round_01_2k.blend", "coffee_table_round_01"),
         ("painted_wooden_bench_2k.blend", "painted_wooden_bench"),
         ("potted_plant_02_2k.blend", "potted_plant_02")]

for fn, coll in ITEMS:
    full = os.path.join(ROOT, fn)
    with bpy.data.libraries.load(full, link=False) as (src, dst):
        dst.objects = list(src.objects)
    new = [o for o in dst.objects if o is not None]
    for o in new:
        if o.name not in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.update()
    ms = [o for o in new if o.type == 'MESH' and len(o.data.vertices)]
    cs = []
    for m in ms: cs += [m.matrix_world @ Vector(c) for c in m.bound_box]
    if not cs:
        print(f"\n### {coll}: GEEN mesh"); continue
    x0=min(c.x for c in cs); x1=max(c.x for c in cs); y0=min(c.y for c in cs); y1=max(c.y for c in cs); z0=min(c.z for c in cs); z1=max(c.z for c in cs)
    h = z1-z0
    # rugleuning: verts in bovenste 35% van hoogte -> hun horizontale zwaartepunt
    thr = z0 + 0.65*h
    hx=hy=n=0
    for m in ms:
        for v in m.data.vertices:
            w = m.matrix_world @ v.co
            if w.z >= thr:
                hx += w.x; hy += w.y; n += 1
    cx=(x0+x1)/2; cy=(y0+y1)/2
    back = ""
    if n:
        hx/=n; hy/=n
        dx=hx-cx; dy=hy-cy
        back = f"rugleuning naar ({'+X' if dx>0.05 else '-X' if dx<-0.05 else '·'},{'+Y' if dy>0.05 else '-Y' if dy<-0.05 else '·'})  [dx={dx:.2f} dy={dy:.2f}]"
    print(f"\n### {coll}: dims {x1-x0:.2f} x {y1-y0:.2f} x {h:.2f} m  (z0={z0:.2f})  {back}")
    for o in new: bpy.data.objects.remove(o, do_unlink=True)
