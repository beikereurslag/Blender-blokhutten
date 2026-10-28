import bpy
from mathutils import Vector

F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Dahlia-250x250-300-zijwand\style-scandi\dahlia_leeshoek.blend"
bpy.ops.wm.open_mainfile(filepath=F)

def bb(o):
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs]; ys=[c.y for c in cs]; zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)

print("PROBE_START")
v = bpy.data.objects.get("Vlonder")
if v:
    mats = [s.material.name if s.material else None for s in v.material_slots]
    print(f"Vlonder mats={mats} bbox={bb(v)}")
    # report base color of each mat
    for s in v.material_slots:
        m = s.material
        if m and m.use_nodes:
            b = next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'), None)
            if b:
                print(f"   mat {m.name}: BaseColor={tuple(round(x,3) for x in b.inputs['Base Color'].default_value)} Rough={b.inputs['Roughness'].default_value:.2f}")

# any mesh with center inside cabin footprint x[-2.75,2.75] y[-1.3,1.45] and low z (<0.25) = potential floor
print("--- low meshes inside cabin footprint:")
for o in bpy.data.objects:
    if o.type!='MESH' or not len(o.data.vertices): continue
    x0,x1,y0,y1,z0,z1 = bb(o)
    cx=(x0+x1)/2; cy=(y0+y1)/2
    if -2.75<cx<2.75 and -1.35<cy<1.5 and z1<0.30 and (x1-x0)*(y1-y0)>0.5:
        print(f"   {o.name:38s} x[{x0:.2f},{x1:.2f}] y[{y0:.2f},{y1:.2f}] z[{z0:.2f},{z1:.2f}]")

# front-wall boards near y~1.2-1.45 to find the open-bay opening x-range
print("--- objs touching front facade (y in [1.0,1.5]) z>0.3 (walls/posts):")
for o in bpy.data.objects:
    if o.type!='MESH' or not len(o.data.vertices): continue
    x0,x1,y0,y1,z0,z1 = bb(o)
    if y0>0.9 and y1<1.6 and z1>0.4 and (y1-y0)<0.6:
        print(f"   {o.name:38s} x[{x0:.2f},{x1:.2f}] y[{y0:.2f},{y1:.2f}] z[{z0:.2f},{z1:.2f}]")
print("PROBE_END")
