"""Start a visible, isolated garden scene and the community MCP listener."""
import bpy
import addon_utils
import sys
scene = bpy.data.scenes.new('Astra — De Regentuinkamer')
bpy.context.window.scene = scene
scene.unit_settings.system = 'METRIC'
scene['phase'] = 'Anchoring — concept approved by Beike'
addon_utils.enable('addon', default_set=False, persistent=True)
bpy.ops.blendermcp.start_server()
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.shading.type = 'SOLID'
            area.spaces.active.overlay.show_floor = False
print('ASTRA live scene and MCP ready', flush=True)
sys.path.insert(0,r'D:\Blender-blokhutten\scripts')
bpy.ops.import_scene.gltf(filepath=r'D:\Blender-blokhutten\source-glbs\Jasmijn 300x250 + 250.glb')
import astra_anchor
astra_anchor.stage1()
