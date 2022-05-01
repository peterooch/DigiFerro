import io

import cv2
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel
import numpy as np
import matplotlib.pyplot as plt

from preprocess.hsv_pipeline import contour_dims, create_mask

class image():
    def __init__(self, image_path):
        with open(image_path, 'rb') as file:
            image_bytes = file.read()

        self.img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        self.mask = create_mask(self.img)
        self.show_mode = 'original'
        self.drawed_image = None

    def draw_image(self, label: QLabel, img):
        self.drawed_image = img

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
        elif option == 'fragments':
            img = cv2.cvtColor(cv2.resize(self.mask, (800, 600)), cv2.COLOR_GRAY2BGR)
        else:
            img = cv2.resize(self.img, (800, 600))

        # img should be in BGR format
        self.draw_image(label, img)

    def create_graph(self):
        # NUMBER CRUNCH
        dims = contour_dims(self.mask)
        dist, bins = np.histogram(dims)
        # NUMBER CRUNCH ENDS
        plt.yscale('log')
        plt.bar(np.arange(len(dist)), dist)   
        plt.xticks(np.arange(len(bins[1:])), [f'{dim:.1f}<' for dim in bins[1:]])
        plt.xlabel('Fragment size')
        plt.ylabel('Fragment count')
        plt.title('Fragment count by size in pixels')
        io_buf = io.BytesIO()
        io_buf.seek(0)
        plt.savefig(io_buf, format='raw', transparent=False)
        fig = plt.gcf()
        dim = (fig.get_size_inches() * fig.dpi).astype(int)
        plt.clf()
        img = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8), newshape=(dim[1], dim[0], -1))
        # Convert to BGR to avoid special handling later on
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        return img
