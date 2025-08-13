from typing import List, Optional


class FaceRecognizer:
    def __init__(self, detection_threshold: float = 0.95, device: str = None):
        import torch
        from facenet_pytorch import MTCNN, InceptionResnetV1

        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.mtcnn = MTCNN(keep_all=False, thresholds=[detection_threshold, detection_threshold, detection_threshold], device=self.device)
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)

    def _to_pil(self, bgr_image):
        from PIL import Image
        import cv2
        rgb = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb)

    def embed_bgr_image(self, bgr_image) -> Optional[List[float]]:
        import torch
        from torchvision import transforms

        pil = self._to_pil(bgr_image)
        face = self.mtcnn(pil)
        if face is None:
            return None
        face = face.to(self.device)
        with torch.no_grad():
            emb = self.resnet(face.unsqueeze(0)).detach().cpu().numpy().flatten().astype(float)
        return emb.tolist()

    def embed_bgr_frames(self, frames_bgr: List, enhance: bool = True) -> Optional[List[float]]:
        import numpy as np
        from app.recognition.preprocessing import enhance_image

        embeddings = []
        for frame in frames_bgr:
            img = enhance_image(frame) if enhance else frame
            emb = self.embed_bgr_image(img)
            if emb:
                embeddings.append(emb)
        if not embeddings:
            return None
        mean_emb = np.mean(np.array(embeddings, dtype=float), axis=0)
        return mean_emb.astype(float).tolist()