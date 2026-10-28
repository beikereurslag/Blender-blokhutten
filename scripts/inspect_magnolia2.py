import bpy, math
from mathutils import Vector
OUT=r'C:/Users/beike/Documents/Blender-blokhutten/scripts/inspect_magnolia_out2.txt'
_f=open(OUT,'w',encoding='utf-8')
def P(*a): _f.write(" ".join(str(x) for x in a)+"\n"); _f.flush()

def rm(o):
    out=[];st=[o]
    while st:
        x=st.pop()
        if x.type=='MESH': out.append(x)
        st.extend(x.children)
    return out
def wbb(ms):
    pts=[(m.matrix_world @ Vector(c)) for m in ms for c in m.bound_box]
    if not pts: return None
    return (min(p.x for p in pts),max(p.x for p in pts),min(p.y for p in pts),max(p.y for p in pts),min(p.z for p in pts),max(p.z for p in pts))

# 1) FULL list of every root object (mesh/empty) with bb, regardless of name
P("=== EVERY VISIBLE ROOT OBJECT (not light/cam, not hide_render) ===")
for o in sorted(bpy.data.objects,key=lambda x:x.name):
    if o.parent is not None: continue
    if o.type in ('LIGHT','CAMERA'): continue
    if o.hide_render: continue
    ms=rm(o); bb=wbb(ms) if ms else None
    if bb:
        P("%-26s %-6s x[%.2f,%.2f] y[%.2f,%.2f] z[%.2f,%.2f]"%((o.name,o.type)+bb))
    else:
        P("%-26s %-6s (no mesh)"%(o.name,o.type))

# 2) Terrace mesh: check for holes / ngons / face count + material
P("\n=== TERRAS detail ===")
t=bpy.data.objects.get('Terras')
if t:
    me=t.data
    P("verts",len(me.vertices),"polys",len(me.polygons),"edges",len(me.edges))
    P("materials:",[m.name if m else None for m in me.materials])
    # check for interior boundary loops (holes): edges with 1 face
    from collections import Counter
    ec=Counter()
    for p in me.polygons:
        for ek in p.edge_keys: ec[ek]+=1
    boundary=sum(1 for k,v in ec.items() if v==1)
    P("boundary_edges(1-face):",boundary)

# 3) Bench (Bank) orientation: find seat-facing direction
P("\n=== Bank orientation ===")
b=bpy.data.objects.get('Bank')
if b:
    P("Bank loc",tuple(round(v,3) for v in b.location),"rot_deg",tuple(round(math.degrees(v),1) for v in b.rotation_euler),"scale",tuple(round(v,3) for v in b.scale))
    # local +Y axis in world (which way bench 'forward' points)
    mw=b.matrix_world
    fwd=(mw.to_3x3() @ Vector((0,1,0))).normalized()
    P("local+Y world dir",tuple(round(v,2) for v in fwd))

# 4) Vacht detail
P("\n=== Vacht ===")
v=bpy.data.objects.get('Vacht')
if v:
    P("Vacht loc",tuple(round(x,3) for x in v.location),"matrixZmin/max via bb")
    bb=wbb([v]); P("Vacht world bb x[%.2f,%.2f] y[%.2f,%.2f] z[%.2f,%.2f]"%bb)

# 5) any black/dark/hole material on terras or nearby
P("\n=== materials with very dark base color ===")
for mat in bpy.data.materials:
    if not mat.use_nodes: continue
    for n in mat.node_tree.nodes:
        if n.type=='BSDF_PRINCIPLED':
            bc=n.inputs.get('Base Color')
            if bc and not bc.is_linked:
                c=bc.default_value
                if c[0]<0.05 and c[1]<0.05 and c[2]<0.05:
                    P("DARK mat:",mat.name,"rgb",tuple(round(x,3) for x in c[:3]))

P("=== END ===")
_f.close()
