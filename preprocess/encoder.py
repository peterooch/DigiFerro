import json
import cv2
import numpy as np
from collections import namedtuple

DataEntry = namedtuple('DataEntry', ['source', 'target'])

def json_to_img(json_path):
    with open(json_path, "r") as file:
        obj = json.load(file)
    img = np.zeros((obj["imageHeight"], obj["imageWidth"]), dtype='uint8')
    colors = { "rubbing": [1], "spalling": [2] }
    for shape in obj["shapes"]:
        points = np.array(shape["points"], dtype='int')
        cv2.fillPoly(img, [points], colors[shape["label"]])
    orig_img = cv2.imread(obj["imagePath"])
    return DataEntry(orig_img, img)
