import os
from PIL import Image
ROOT = r"C:\Users\beike\Documents\Blender-blokhutten\assets"
MAXD = 2048; THRESH = 15*1024*1024
cands=[]
for dp,_,fns in os.walk(ROOT):
    for fn in fns:
        if fn.lower().endswith((".png",".jpg",".jpeg")):
            p=os.path.join(dp,fn)
            try: sz=os.path.getsize(p)
            except OSError: continue
            if sz>THRESH: cands.append((sz,p))
cands.sort()
print("DS_START",len(cands))
freed=0
for sz,p in cands:
    tmp=None
    try:
        im=Image.open(p); w,h=im.size
        if max(w,h)<=MAXD: im.close(); continue
        im2=im.copy(); im.close(); im2.thumbnail((MAXD,MAXD),Image.LANCZOS)
        ext=os.path.splitext(p)[1].lower(); tmp=p+".dstmp"+ext
        if ext in (".jpg",".jpeg"):
            if im2.mode not in ("RGB","L"): im2=im2.convert("RGB")
            im2.save(tmp,quality=90,optimize=True)
        else:
            im2.save(tmp,optimize=True)
        new=os.path.getsize(tmp); os.replace(tmp,p); freed+=sz-new
        print("  %6.1f->%5.1fMB %s"%(sz/1e6,new/1e6,os.path.relpath(p,ROOT)))
    except Exception as e:
        print("  SKIP",os.path.relpath(p,ROOT),e)
        try:
            if tmp and os.path.exists(tmp): os.remove(tmp)
        except Exception: pass
print("DS_DONE freed_MB",round(freed/1e6))
