import mlx.core as mx
import numpy as np

class MPSSpatialSVD:
    def __init__(self):
        mx.set_default_device(mx.gpu)

    def decompose_mesh(self, points: np.ndarray):
        tensor = mx.array(points)
        centered = tensor - mx.mean(tensor, axis=0)
        U, S, Vt = mx.linalg.svd(centered, stream=mx.gpu)
        curvature = S[2] / mx.sum(S)
        normal = Vt[2, :]
        mx.eval(normal, curvature)
        return {
            "normal": np.array(normal), "curvature": float(np.array(curvature)),
            "svd_stability": 1.0 - float(np.array(curvature))
        }
