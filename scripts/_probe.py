import bpy, sys
print("PROBE START", flush=True)
argv = sys.argv[sys.argv.index("--")+1:]
print("ARGV", argv, flush=True)
try:
    bpy.ops.wm.open_mainfile(filepath=argv[0])
    print("OPEN OK objects=", len(bpy.data.objects), flush=True)
except Exception as e:
    print("OPEN FAIL", repr(e), flush=True)
print("PROBE END", flush=True)
