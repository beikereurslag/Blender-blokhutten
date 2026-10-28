import bpy, re
from collections import Counter
c = Counter()
for o in bpy.data.objects:
    if o.type == 'MESH':
        b = re.sub(r'_(LOD\d|Atlas|bark)_?\d*$', '', o.name)
        b = re.sub(r'[_\.\- ]?\d+$', '', b)
        c[b] += 1
print("TAX_START")
for name, n in sorted(c.items()):
    print(f"{n:4d}  {name}")
print("TAX_END")
