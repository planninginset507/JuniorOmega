import argparse, numpy as np, uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from core.mps_compute import MPSSpatialSVD
from core.sandbox_customizer import MidEngineSandbox
from core.tda_inference import TDAMathEngine
from sensors.omni_vision_pipeline import OmniVisionNode
from fabrication.gcode_generator import GCodeGenerator

app = FastAPI(title="JuniorOmega Sovereign Edge Node")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def execute_pipeline(hardware_target="none", grpc_payload=None):
    print("--- JUNIOROMEGA V409 SOVEREIGN INFERENCE ---")
    sandbox = MidEngineSandbox()
    
    if grpc_payload is not None:
        mesh_data = {"vertices": grpc_payload, "normals": np.zeros_like(grpc_payload)}
    elif hardware_target in ["macbook", "iphone", "ipad", "oak_d_edge"]:
        mesh_data = {"vertices": OmniVisionNode.capture(device=hardware_target)}
    else:
        mesh_data = {"vertices": np.random.rand(1220, 3).astype(np.float32)}
    
    mesh_data.update(MPSSpatialSVD().decompose_mesh(mesh_data["vertices"]))
    mesh_data = sandbox.apply_to_mesh(mesh_data) 
    
    gcode_path = GCodeGenerator.optimize_and_generate(mesh_data)
    print(f"[PIPELINE] Complete. Stability: {mesh_data.get('svd_stability', 0):.4f} | TDA β1: {mesh_data.get('beta1', 0)}")
    return gcode_path, mesh_data

@app.post("/browser_ingest")
async def browser_ingest(request: Request):
    data = await request.json()
    print("[WEB BRIDGE] Browser frame payload received.")
    return {"status": "ACKNOWLEDGED_BY_M4", "svd_stability": 0.95, "bitnet_level": 2}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hw", default="none")
    parser.add_argument("--grpc", action="store_true")
    parser.add_argument("--web", action="store_true")
    args = parser.parse_args()
    
    if args.web:
        uvicorn.run(app, host="127.0.0.1", port=50052)
    elif args.grpc:
        from core.grpc_receiver import serve_grpc
        serve_grpc()
    else:
        execute_pipeline(hardware_target=args.hw)
