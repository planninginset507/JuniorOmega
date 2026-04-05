import argparse, numpy as np
from core.mps_compute import MPSSpatialSVD
from core.sandbox_customizer import MidEngineSandbox
from sensors.omni_vision_pipeline import OmniVisionNode

def execute_pipeline(hardware_target="none", grpc_payload=None):
    print("--- JUNIOROMEGA V408 SOVEREIGN INFERENCE ---")
    sandbox = MidEngineSandbox()
    
    if grpc_payload is not None:
        print(f"[EDGE] Processing {len(grpc_payload)} vertices via gRPC.")
        mesh_data = {"vertices": grpc_payload, "normals": np.zeros_like(grpc_payload)}
    elif hardware_target in ["macbook", "iphone", "ipad", "oak_d_edge"]:
        mesh_data = {"vertices": OmniVisionNode.capture(device=hardware_target)}
    else:
        mesh_data = {"vertices": np.random.rand(1220, 3).astype(np.float32)}
    
    mesh_data.update(MPSSpatialSVD().decompose_mesh(mesh_data["vertices"]))
    mesh_data = sandbox.apply_to_mesh(mesh_data)
    
    print(f"[PIPELINE] Execution Complete. Stability: {mesh_data['svd_stability']:.4f}")
    return mesh_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hw", default="none")
    parser.add_argument("--grpc", action="store_true")
    args = parser.parse_args()
    
    if args.grpc:
        from core.grpc_receiver import serve_grpc
        serve_grpc()
    else:
        execute_pipeline(hardware_target=args.hw)
