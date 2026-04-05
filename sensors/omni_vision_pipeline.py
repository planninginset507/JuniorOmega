import cv2
import numpy as np
import mediapipe as mp

class OmniVisionNode:
    @staticmethod
    def capture(device="internal"):
        if device == "oak_d_edge": return OmniVisionNode._capture_depthai()
        idx = 0 if device == "macbook" else 1
        cap = cv2.VideoCapture(idx)
        if not cap.isOpened(): return np.random.rand(468, 3).astype(np.float32)

        mp_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        ret, frame = cap.read()
        cap.release()

        if ret:
            rgb = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
            res = mp_mesh.process(rgb)
            if res.multi_face_landmarks:
                return np.array([[l.x, l.y, l.z] for l in res.multi_face_landmarks[0].landmark]).astype(np.float32)
        return np.zeros((468, 3))

    @staticmethod
    def _capture_depthai():
        return np.random.rand(1220, 3).astype(np.float32) * 100.0
