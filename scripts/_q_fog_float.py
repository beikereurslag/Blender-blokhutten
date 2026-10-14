import bpy, sys, re
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
F=sys.argv[sys.argv.index("--")+1]
bpy.ops.wm.open_mainfile(filepath=F)
scn=bpy.context.scene; cam=scn.camera
def wbb(o):
    cs=[o.matrix_world @ Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs]; ys=[c.y for c in cs]; zs=[c.z for c in cs]
    return (min(xs),max(xs),min(ys),max(ys),min(zs),max(zs))
def ndc(co):
    c=world_to_camera_view(scn,cam,Vector(co)); return (round(c.x,2),round(c.y,2),round(c.z,1))
print("QF_START", F)
# fog
for o in bpy.data.objects:
    if o.type!='MESH': continue
    for s in o.material_slots:
        m=s.material
        if m and ('fog' in m.name.lower() or 'mist' in m.name.lower()):
            b=wbb(o); print(f"FOG obj={o.name} mat={m.name} bbox x[{b[0]:.1f},{b[1]:.1f}] y[{b[2]:.1f},{b[3]:.1f}] z[{b[4]:.1f},{b[5]:.1f}]")
            if m.use_nodes:
                for n in m.node_tree.nodes:
                    if n.type=='VOLUME_PRINCIPLED':
                        print("   VOL color=", tuple(round(c,2) for c in n.inputs['Color'].default_value), "aniso=", round(n.inputs['Anisotropy'].default_value,2), "density(socket)=", round(n.inputs['Density'].default_value,4))
                    if n.type=='MAP_RANGE':
                        print("   MAPRANGE ToMin=", round(n.inputs['To Min'].default_value,4), "ToMax=", round(n.inputs['To Max'].default_value,4))
# floating plant parts (zmin>0.25) in frame
print("--- FLOATING plant parts (zmin>0.25), in-frame ---")
rows=[]
for o in bpy.data.objects:
    if o.type!='MESH' or not len(o.data.vertices): continue
    if not re.search(r'(BakGras_|Drift_|weed_plant)', o.name): continue
    b=wbb(o)
    if b[4] > 0.25:
        cx=(b[0]+b[1])/2; cy=(b[2]+b[3])/2; cz=(b[4]+b[5])/2
        n=ndc((cx,cy,cz)); inf=(0<=n[0]<=1 and 0<=n[1]<=1 and n[2]>0)
        rows.append((n[0], o.name, b[4], (cx,cy), n, inf, o.parent.name if o.parent else None))
rows.sort(reverse=True)  # high ndc.x = right of frame first
for x,nm,zmin,c,n,inf,par in rows[:24]:
    fl="  <<RIGHT-INFRAME" if (inf and n[0]>0.6) else ""
    print(f"  {nm:16s} zmin={zmin:.2f} c=({c[0]:.1f},{c[1]:.1f}) ndc{n} inframe={inf} par={par}{fl}")
print("QF_END")
