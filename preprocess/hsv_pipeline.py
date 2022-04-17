import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.exposure import match_histograms

RED_LOWER = np.uint8([0, 0, 200])
RED_UPPER = np.uint8([255, 255, 255])

BASELINE = cv2.imread('preprocess/baseline.jpg')

def create_mask(file_name):
    with open(file_name, 'rb') as file:
        image_bytes = file.read()

    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    img = np.uint8(match_histograms(img, BASELINE))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, RED_LOWER, RED_UPPER)

    return mask

def to_countour(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    dims = []
    for contour in contours:
        box = cv2.minAreaRect(contour)
        pts = np.int0(cv2.boxPoints(box))
        cv2.drawContours(img, [pts], -1, (0, 255, 0), 1)
        dims.append(np.linalg.norm(pts[0] - pts[2]))

    plt.imshow(img)
    plt.show()
    return sorted(dims, reverse=True)

if __name__ == "__main__":
    mask = create_mask('preprocess/baseline.jpg')
    print(to_countour(mask))