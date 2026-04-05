import grpc
from concurrent import futures
import numpy as np
from proto import facial_pb2, facial_pb2_grpc

class FacialPayloadServicer(facial_pb2_grpc.FacialServiceServicer):
    def SendFacialMesh(self, request, context):
        vertices = np.array(request.vertices).reshape(-1, 3).astype(np.float32)
        print(f"[gRPC EDGE] Acknowledged {len(vertices)} coordinates from Swift TrueDepth.")
        
        from omega_orchestrator import execute_pipeline
        gcode_path, _ = execute_pipeline(input_path=None, grpc_payload=vertices)
        return facial_pb2.MeshResponse(status="OK", gcode_path=gcode_path)

def serve_grpc(port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    facial_pb2_grpc.add_FacialServiceServicer_to_server(FacialPayloadServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"[gRPC] Sovereign Receiver Active on Port {port}.")
    server.wait_for_termination()
