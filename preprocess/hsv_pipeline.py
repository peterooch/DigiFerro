from typing import List

import cv2
import numpy as np
from skimage.exposure import match_histograms
from joblib import Memory

from util import resource_path

# Spalling fragment hsv range
SPALLING_LOWER = np.uint8([0, 0, 200])
SPALLING_UPPER = np.uint8([255, 255, 255])

# Histogram baseline image
BASELINE = cv2.imread(resource_path('preprocess/baseline.jpg'))

memory = Memory('data')

def create_mask(img):
    img = np.uint8(match_histograms(img, BASELINE))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, SPALLING_LOWER, SPALLING_UPPER)

    return mask

@memory.cache(verbose=0)
def find_contours(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def contour_dims(mask) -> List[float]:
    contours = find_contours(mask)
    dims = []
    for contour in contours:
        box = cv2.minAreaRect(contour)
        pts = np.int0(cv2.boxPoints(box))
        dims.append(np.linalg.norm(pts[0] - pts[2]))
    return sorted(dims, reverse=True)

def get_rects(mask):
    contours = find_contours(mask)
    img = np.zeros((*mask.shape, 3), np.uint8)
    points = [np.int0(cv2.boxPoints(cv2.minAreaRect(contour))) for contour in contours]
    cv2.drawContours(img, points, -1, (0, 255, 0), 3)
    return img

if __name__ == "__main__":
    with open('preprocess/baseline.jpg', 'rb') as file:
        image_bytes = file.read()

    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    mask = create_mask(img)
    print(contour_dims(mask))