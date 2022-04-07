from collections import namedtuple
import json

import cv2
import numpy as np
from skimage.exposure import match_histograms

def load_image(filename):
    return cv2.imread(filename)

DataEntry = namedtuple('DataEntry', ['source', 'target'])

baseline = load_image('preprocess/baseline.jpg')

def json_to_img(json_path):
    with open(json_path, "r") as file:
        obj = json.load(file)
    img = np.zeros((obj["imageHeight"], obj["imageWidth"]), dtype='uint8')
    colors = { "rubbing": [2], "spalling": [1] }
    for shape in obj["shapes"]:
        points = np.array(shape["points"], dtype='int')
        cv2.fillPoly(img, [points], colors[shape["label"]])
    orig_img = load_image(obj["imagePath"])

    matched = np.uint8(match_histograms(orig_img, baseline))

    return DataEntry(matched, img)
