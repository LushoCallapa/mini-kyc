import cv2
import numpy as np


BLUR_THRESHOLD = 80.0


def is_image_blurry(image_bytes: bytes) -> bool:
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("The uploaded file is not a valid image.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()

    return variance < BLUR_THRESHOLD
