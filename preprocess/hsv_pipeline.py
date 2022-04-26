from typing import List

import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.exposure import match_histograms

# Spalling fragment hsv range
SPALLING_LOWER = np.uint8([0, 0, 200])
SPALLING_UPPER = np.uint8([255, 255, 255])

# Histogram baseline image
BASELINE = cv2.imread('preprocess/baseline.jpg')

def create_mask(img):
    img = np.uint8(match_histograms(img, BASELINE))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, SPALLING_LOWER, SPALLING_UPPER)

    return mask

def contour_dims(mask) -> List[float]:
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    dims = []
    for contour in contours:
        box = cv2.minAreaRect(contour)
        pts = np.int0(cv2.boxPoints(box))
        cv2.drawContours(img, [pts], -1, (0, 255, 0), 1)
        dims.append(np.linalg.norm(pts[0] - pts[2]))

    #plt.imshow(img)
    #plt.show()
    return sorted(dims, reverse=True)

if __name__ == "__main__":
    with open('preprocess/baseline.jpg', 'rb') as file:
        image_bytes = file.read()

    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    mask = create_mask(img)
    print(contour_dims(mask))