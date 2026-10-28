"""Rommel-detector vanuit de hero-camera. Rapporteert per scene:
  - ZWEVERS: meshes met onderkant > 0.12 boven grond die IN BEELD vallen
  - LOW-POLY foliage/tree-meshes in beeld (verts < 2500, plant/tree/leaf/branch-mat)
  - TRANSPARENT/alpha materialen + meshes met meerdere mat-slots waarvan er leeg zijn
Run: blender --background scene.blend --python scripts/_probe_junk.py
"""
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

scn = bpy.context.scene
cam = scn.camera
def in_frame(co):
    if not cam: return True
    c = world_to_camera_view(scn, cam, co)
    return -0.05 < c.x < 1.05 and -0.05 < c.y < 1.05 and c.z > 0

def wbb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]
    return (min(c.x for c in cs),max(c.x for c in cs),min(c.y for c in cs),max(c.y for c in cs),min(c.z for c in cs),max(c.z for c in cs))

SKIP=("wall-","roof","fascia","trim-","parentboard","flatroof",".scharnier",".doorhandle",
      ".deurbasic","hedge_","ground","mist","slinger","bulb","sun","cam","festoon","lantaarn")
PLANTKW=("tree","boom","pine","birch","berk","maple","leaf","blad","branch","tak","foliage",
         "shrub","plant","flower","bloem","weed","twig","needle")

floaters=[]; lowpoly=[]; alpha=[]; emptyslot=[]
for o in bpy.data.objects:
    if o.type!='MESH' or not len(o.data.vertices) or o.hide_render: continue
    nl=o.name.lower()
    if any(k in nl for k in SKIP): continue
    b=wbb(o); cx=(b[0]+b[1])/2; cy=(b[2]+b[3])/2; cz=(b[4]+b[5])/2
    framed = in_frame(Vector((cx,cy,cz)))
    if not framed: continue
    nv=len(o.data.vertices)
    # floaters (klein-ish, onderkant duidelijk boven grond)
    if b[4] > 0.12 and (b[5]-b[4]) < 4.0 and max(b[1]-b[0],b[3]-b[2]) < 4.0:
        floaters.append((round(b[4],2),o.name,round(cx,1),round(cy,1),nv))
    # low-poly foliage
    mats=" ".join(s.material.name.lower() for s in o.material_slots if s.material)
    if any(k in (nl+" "+mats) for k in PLANTKW) and nv < 2500 and (b[5]-b[4])>0.3:
        lowpoly.append((nv,o.name,round(b[5]-b[4],1),round(cx,1),round(cy,1)))
    # transparency + lege slots
    for s in o.material_slots:
        m=s.material
        if not m: emptyslot.append(o.name); continue
        if hasattr(m,'use_nodes') and m.use_nodes:
            bd=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
            if bd:
                a=bd.inputs['Alpha'].default_value
                if a<0.99 or bd.inputs['Alpha'].is_linked:
                    alpha.append((o.name,m.name,round(a,2),bd.inputs['Alpha'].is_linked))
            if getattr(m,'blend_method','OPAQUE')!='OPAQUE':
                alpha.append((o.name,m.name,'blend='+m.blend_method,''))

print("\n==== JUNK in-frame:", bpy.data.filepath.split('\\')[-1])
print(f"-- ZWEVERS ({len(floaters)}):")
for z,nm,cx,cy,nv in sorted(floaters)[-30:]:
    print(f"   min_z={z:5.2f} {nm:<30} c=({cx:5.1f},{cy:4.1f}) v={nv}")
print(f"-- LOW-POLY foliage in beeld ({len(lowpoly)}):")
for nv,nm,h,cx,cy in sorted(lowpoly)[:25]:
    print(f"   v={nv:<5} {nm:<30} h={h} c=({cx:5.1f},{cy:4.1f})")
print(f"-- TRANSPARENT/alpha mats ({len(alpha)}):")
seen=set()
for row in alpha:
    if row[0] in seen: continue
    seen.add(row[0]); print("   ", row)
print(f"-- LEGE mat-slots: {sorted(set(emptyslot))[:20]}")
print("==== end\n")
