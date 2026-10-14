import bpy
from mathutils import Vector
F = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Zonnebloem-300x300-300-zijwand\style-scandi\zonnebloem_ochtendhoek.blend"
bpy.ops.wm.open_mainfile(filepath=F)
def bb(o):
    cs=[o.matrix_world@Vector(c) for c in o.bound_box]
    xs=[c.x for c in cs];ys=[c.y for c in cs];zs=[c.z for c in cs]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
print("PROBE_START")
print("CAMERA:", bpy.context.scene.camera.name if bpy.context.scene.camera else None)
# props of interest: mug/kan/coffee, firewood/hout/blok, table/tafel, plus cameras + lights
keys=('mok','mug','kan','koffie','coffee','press','hout','brand','blok','log','vuur','fire',
      'tafel','table','stoel','chair','bank','bench','terras','deck','vlonder','cam','lamp','licht','light')
rows=[]
for o in bpy.data.objects:
    n=o.name.lower()
    if any(k in n for k in keys):
        if o.type=='MESH':
            b=bb(o); rows.append((o.name,o.type,f"x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}]"))
        else:
            rows.append((o.name,o.type,f"loc{tuple(round(v,2) for v in o.location)}"))
for nm,t,info in sorted(rows):
    print(f"  {nm:28s} {t:8s} {info}")
print("--- ALL top-level (parentless) mesh objects, name only:")
print("  ", [o.name for o in bpy.data.objects if o.type=='MESH' and not o.parent][:80])
print("--- collections:", [c.name for c in bpy.data.collections])
print("PROBE_END")
