import bpy, sys, os

def configure_metal_compute():
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'METAL'
    bpy.context.scene.cycles.device = 'GPU'
    for d in bpy.context.preferences.addons['cycles'].preferences.devices:
        if d.type == 'METAL': d.use = True
    print("[BLENDER] Metal Compute + TDA Shading Configured.")

def import_and_shade_mesh(filepath: str, tda_data: dict = None):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if filepath.endswith('.ply'): bpy.ops.import_mesh.ply(filepath=filepath)
    elif filepath.endswith('.glb'): bpy.ops.import_scene.gltf(filepath=filepath)
        
    obj = bpy.context.active_object
    mat = bpy.data.materials.new(name="Topology_SVD_TDA")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (0.83, 0.68, 0.21, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.9
    bsdf.inputs['Roughness'].default_value = 0.1
    obj.data.materials.append(mat)
    
    if tda_data and "beta1" in tda_data:
        print(f"[BLENDER] Applying TDA topology overlay — beta1 = {tda_data['beta1']}")
        vcol = obj.data.vertex_colors.new()
        for i, loop in enumerate(obj.data.loops):
            intensity = min(1.0, tda_data.get("beta1", 0) / 10.0)
            vcol.data[i].color = (intensity, 0.2, 1.0 - intensity, 1.0)
    
    export_path = filepath.replace(os.path.splitext(filepath)[1], "_tda_rendered.glb")
    bpy.ops.export_scene.gltf(filepath=export_path, export_format='GLB')
    return export_path
