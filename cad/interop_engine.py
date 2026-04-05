# cad/interop_engine.py
import trimesh
import rhino3dm
import numpy as np

class CADInteropPipeline:
    """
    Ingests and translates SolidWorks (STEP/STL), FreeCAD, and Grasshopper (3DM) 
    architectures into MLX-ready Nx3 tensor arrays.
    """
    @staticmethod
    def ingest_geometry(filepath: str):
        print(f"[CAD] Ingesting architectural payload: {filepath}")
        ext = filepath.lower().split('.')[-1]
        
        if ext in ['stl', 'obj', 'ply', 'step', 'stp']:
            # Trimesh handles standard CAD exports (STEP requires FreeCAD/Gmsh backend or pre-converted STL)
            mesh = trimesh.load(filepath, force='mesh')
            vertices = np.array(mesh.vertices, dtype=np.float32)
            normals = np.array(mesh.vertex_normals, dtype=np.float32)
            return {"vertices": vertices, "normals": normals, "faces": mesh.faces}
            
        elif ext == '3dm':
            # Grasshopper / Rhino native ingest
            model = rhino3dm.File3dm.Read(filepath)
            vertices = []
            for obj in model.Objects:
                geom = obj.Geometry
                if geom.ObjectType == rhino3dm.ObjectType.Mesh:
                    for pt in geom.Vertices:
                        vertices.append([pt.X, pt.Y, pt.Z])
            return {"vertices": np.array(vertices, dtype=np.float32), "normals": []}
            
        else:
            raise ValueError(f"Unsupported CAD format: {ext}. Export as STL/OBJ/3DM.")

    @staticmethod
    def export_geometry(mesh_data: dict, output_path: str):
        """Re-compiles the MLX-optimized tensor back into a CAD-readable mesh."""
        mesh = trimesh.Trimesh(vertices=mesh_data['vertices'], faces=mesh_data.get('faces', []))
        mesh.export(output_path)
        print(f"[CAD] Exported optimized spatial artifact to: {output_path}")
        return output_path
