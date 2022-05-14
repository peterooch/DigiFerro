from os import path
from typing import List

import cv2
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel
import numpy as np
from joblib import Parallel, delayed

from preprocess.hsv_pipeline import contour_dims, create_mask, get_rects
from util import gen_graph, get_distribution

class image:
    SHOW_ORIGINAL  = (1 << 0)
    SHOW_MASK      = (1 << 1)
    SHOW_GRAPH     = (1 << 2)
    SHOW_BOX_PLOTS = (1 << 3)

    __slots__ = ("scale", "filename", "img", "mask", "show_mode",
                 "drawed_image", "dims", "dist", "bins", "box_plots")

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
        self.box_plots = get_rects(self.mask)

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

    def show(self, label: QLabel, option=None):
        if option is None:
            option = image.SHOW_ORIGINAL
        self.show_mode = option

        if option & image.SHOW_GRAPH:
            img = self.create_graph()
            self.drawed_image = img
            return self.draw_image(label, img)

        if option & image.SHOW_MASK:
            img = cv2.cvtColor(self.mask, cv2.COLOR_GRAY2BGR)
        else:
            img = self.img

        if option & image.SHOW_BOX_PLOTS:
            img = self.apply_box_plots(img)

        self.drawed_image = img
        img = cv2.resize(img, (960, 720))

        # img should be in BGR format
        self.draw_image(label, img)

    def apply_box_plots(self, image):
        b, g, r = cv2.split(image)
        _, g2, _ = cv2.split(self.box_plots)
        img = cv2.merge((b, (g | g2), r))
        return img

    def get_dims(self):
        return self.dims

    def create_graph(self):
        return gen_graph(self.dist, self.bins)

def paths_to_imgs(paths) -> List[image]:
    # Use all cores for image processing
    return Parallel(n_jobs=-1, verbose=0)(delayed(image)(path) for path in paths)
