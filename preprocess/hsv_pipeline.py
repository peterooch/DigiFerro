from typing import List

import cv2
import numpy as np
from skimage.exposure import match_histograms
#from joblib import Memory

from util import resource_path

# Spalling fragment hsv range
SPALLING_LOWER = np.uint8([[0, 230, 210]])
SPALLING_UPPER = np.uint8([[255, 255, 255]])
# Rubbing V Layer range
RUBBING_LOWER = np.uint8([[0, 0, 0]])
RUBBING_UPPER = np.uint8([[255, 255, 100]])

# Histogram baseline image
BASELINE = cv2.imread(resource_path('preprocess/baseline.jpg'))

#memory = Memory('data')

def equalize_img(img):
    return np.uint8(match_histograms(img, BASELINE))

def apply_clahe(hsv):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    h, s, v = cv2.split(hsv)
    v = clahe.apply(v)
    hsv = cv2.merge((h, s, v))
    return hsv

def create_masks(img):
    img = equalize_img(img)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = apply_clahe(hsv)
    # FIXME this should a bit more clever than just hardcoded ranges
    spalling = cv2.inRange(hsv, SPALLING_LOWER, SPALLING_UPPER)
    rubbing = cv2.inRange(hsv, RUBBING_LOWER, RUBBING_UPPER)
    return spalling, rubbing

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

# def get_rects(mask):
#     contours = find_contours(mask)
#     img = np.zeros((*mask.shape, 3), np.uint8)
#     points = [np.int0(cv2.boxPoints(cv2.minAreaRect(contour))) for contour in contours]
#     cv2.drawContours(img, points, -1, (0, 255, 0), 3)
#     return img

# box plots with text
CONTOUR_COLOR = (0, 255, 0)
TEXT_COLOR    = (0, 0, 255)

def get_rects(mask, scale):
    contours = find_contours(mask)
    img = np.zeros((*mask.shape, 3), np.uint8)
    points = [np.int0(cv2.boxPoints(cv2.minAreaRect(contour))) for contour in contours]
    cv2.drawContours(img, points, -1, CONTOUR_COLOR, 2)
    for pts in points:
        dim = np.linalg.norm(pts[0] - pts[2]) / scale
        if dim < 40: # FIXME hardcoded value
            continue
        text_pt = (0, 0)
        for pt in pts:
            pt = tuple(pt)
            if pt >= text_pt:
                text_pt = pt
        cv2.putText(img, f'{dim:.2f}', text_pt, cv2.FONT_HERSHEY_SIMPLEX, 0.75, TEXT_COLOR, 2)
    return img

if __name__ == "__main__":
    with open('preprocess/baseline.jpg', 'rb') as file:
        image_bytes = file.read()

    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    mask, _ = create_masks(img)
    print(contour_dims(mask))
