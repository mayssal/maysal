from typing import Any


def enhance_image(image_bgr: Any):
    """Apply simple enhancement (CLAHE on L channel) to improve contrast on low-light images.

    Lazy imports OpenCV to avoid heavy dependencies on import time.
    """
    import cv2
    import numpy as np

    if image_bgr is None:
        return image_bgr
    lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # mild denoise
    enhanced = cv2.fastNlMeansDenoisingColored(enhanced, None, 5, 5, 7, 21)
    return enhanced