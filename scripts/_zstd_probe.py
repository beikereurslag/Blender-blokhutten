import sys
src = r"C:\Users\beike\Documents\Blender-blokhutten\pilots\Zonnebloem-300x300-300-zijwand\style-boerderij\zonnebloem_zomeravond.blend"
out = r"C:\Users\beike\Documents\Blender-blokhutten\zstd_probe_result.txt"
res = []
mod = None
for name in ("zstandard", "zstd"):
    try:
        mod = __import__(name)
        res.append("module=%s ver=%s" % (name, getattr(mod, "__version__", "?")))
        break
    except Exception as e:
        res.append("import %s failed: %r" % (name, e))
if mod is not None and mod.__name__ == "zstandard":
    try:
        d = mod.ZstdDecompressor()
        with open(src, "rb") as f:
            head = f.read(2_000_000)  # 2MB compressed chunk
        # stream-decompress just the head to peek magic
        dctx = d.decompressobj()
        chunk = dctx.decompress(head)
        magic = chunk[:12]
        res.append("decompressed_head_len=%d" % len(chunk))
        res.append("magic_hex=" + " ".join("%02X" % b for b in magic))
        res.append("magic_ascii=" + "".join(chr(b) if 32 <= b < 127 else "." for b in magic))
    except Exception as e:
        res.append("decompress failed: %r" % e)
with open(out, "w") as f:
    f.write("\n".join(res) + "\n")
print("\n".join(res))
