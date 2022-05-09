from os import path
from typing import List

import cv2
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel
import numpy as np
from joblib import Parallel, delayed

from preprocess.hsv_pipeline import contour_dims, create_mask
from util import gen_graph, get_distribution

class image():
    def __init__(self, image_path, scale=2):
        with open(image_path, 'rb') as file:
            image_bytes = file.read()
        
        self.scale = scale
        _, self.filename = path.split(image_path)
        self.img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        self.mask = create_mask(self.img)
        self.show_mode = 'original'
        self.drawed_image = None

        self.dims = contour_dims(self.mask)
        self.dist, self.bins = get_distribution(self.dims, self.scale)

    @property
    def graph_data(self):
        return self.dist, self.bins[1:]

    def __str__(self):
        return self.filename

    def draw_image(self, label: QLabel, img):
        label.resize(img.shape[1], img.shape[0])
        img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888).rgbSwapped()
        label.setPixmap(QPixmap.fromImage(img))

    def save_image(self, filename):
        if self.drawed_image is None:
            return

        cv2.imwrite(filename, self.drawed_image)
        
    def show(self, label: QLabel, option='original'):
        self.show_mode = option

        if option == 'graph':
            img = self.create_graph()
            self.drawed_image = img
        elif option == 'fragments':
            self.drawed_image = cv2.cvtColor(self.mask, cv2.COLOR_GRAY2BGR)
            img = cv2.resize(self.drawed_image, (800, 600))
        else:
            self.drawed_image = self.img
            img = cv2.resize(self.img, (800, 600))

        # img should be in BGR format
        self.draw_image(label, img)

    def get_dims(self):
        return self.dims

    def create_graph(self):
        return gen_graph(self.dist, self.bins)

def paths_to_imgs(paths) -> List[image]:
    # Use all cores for image processing
    return Parallel(n_jobs=-1, verbose=0)(delayed(image)(path) for path in paths)
