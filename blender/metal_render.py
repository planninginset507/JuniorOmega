# blender/metal_render.py
import bpy
import sys
import os

def configure_metal_compute():
    """Forces Blender headless to utilize Apple Silicon GPU/Metal."""
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'METAL'
    bpy.context.scene.cycles.device = 'GPU'
    
    # Initialize Metal devices
    bpy.context.preferences.addons['cycles'].preferences.get_devices()
    for d in bpy.context.preferences.addons['cycles'].preferences.devices:
        if d.type == 'METAL':
            d.use = True
    print("[BLENDER] Metal Compute Architecture Configured.")

def import_and_shade_mesh(filepath: str):
    """Imports .ply/.las derived mesh and applies Sovereign logic shading."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # Import topology
    if filepath.endswith('.ply'):
        bpy.ops.import_mesh.ply(filepath=filepath)
    elif filepath.endswith('.glb'):
        bpy.ops.import_scene.gltf(filepath=filepath)
        
    obj = bpy.context.active_object
    
    # Apply high-contrast topology material (CLI-optimized)
    mat = bpy.data.materials.new(name="Topology_SVD")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (0.83, 0.68, 0.21, 1.0) # Sovereign Gold
    bsdf.inputs['Metallic'].default_value = 0.8
    obj.data.materials.append(mat)
    
    export_path = filepath.replace(os.path.splitext(filepath)[1], "_rendered.glb")
    bpy.ops.export_scene.gltf(filepath=export_path, export_format='GLB')
    print(f"[BLENDER] Encoded artifact to: {export_path}")

if __name__ == "__main__":
    # Slice sys.argv to get CLI arguments passed after '--'
    try:
        argv = sys.argv[sys.argv.index("--") + 1:]
        target_file = argv[0]
        configure_metal_compute()
        import_and_shade_mesh(target_file)
    except Exception as e:
        print(f"[ERR] Metal Render Failure: {e}")
