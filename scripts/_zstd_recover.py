import zstandard, os
src = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Zonnebloem-300x300-300-zijwand\style-boerderij\zonnebloem_zomeravond.blend"
dst = r"C:\Users\beike\Documents\Blender-blokhutten\zonnebloem_zomeravond_RECOVERED.blend"
d = zstandard.ZstdDecompressor()
with open(src, "rb") as fin, open(dst, "wb") as fout:
    d.copy_stream(fin, fout)
sz = os.path.getsize(dst)
with open(dst, "rb") as f:
    head = f.read(12)
print("RECOVERED size=%d magic=%s" % (sz, head[:7].decode("latin1")))
