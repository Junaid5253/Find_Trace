from pathlib import Path
import numpy as np
import cv2

class FaceEngine:
    def __init__(self):
        self.app = None
        self.error = None
        try:
            from insightface.app import FaceAnalysis
            self.app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
            self.app.prepare(ctx_id=0, det_size=(640, 640))
        except Exception as e:
            self.error = str(e)

    def embedding_from_path(self, path):
        if self.app is None:
            raise RuntimeError(f"InsightFace could not load: {self.error}")
        image = cv2.imread(str(path))
        if image is None:
            return None
        faces = self.app.get(image)
        if not faces:
            return None
        face = max(faces, key=lambda x: float((x.bbox[2]-x.bbox[0]) * (x.bbox[3]-x.bbox[1])))
        emb = np.asarray(face.embedding, dtype=np.float32)
        norm = np.linalg.norm(emb)
        return emb / norm if norm else None

    @staticmethod
    def similarity(a, b):
        a, b = np.asarray(a), np.asarray(b)
        denom = np.linalg.norm(a) * np.linalg.norm(b)
        if denom == 0:
            return 0.0
        cosine = float(np.dot(a, b) / denom)
        return max(0.0, min(1.0, (cosine + 1) / 2))
