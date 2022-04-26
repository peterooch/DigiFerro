import cv2
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import numpy as np
from preprocess.hsv_pipeline import create_mask

class image():
    def __init__(self, image_path):
        with open(image_path, 'rb') as file:
            image_bytes = file.read()

        self.img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        self.mask = create_mask(self.img)

    def show(self, label, option=None):
        if option == 'fragments':
            img = cv2.cvtColor(cv2.resize(self.mask, (800, 600)), cv2.COLOR_GRAY2BGR)
        else:
            img = cv2.resize(self.img, (800, 600))
   
        label.setGeometry(20, 20, img.shape[1], img.shape[0])
        img = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        label.setPixmap(QPixmap.fromImage(img))
