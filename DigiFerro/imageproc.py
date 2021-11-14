import cv2
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
#from matplotlib import pyplot as plt
import shutil

class image():
    def __init__(self, image_path):
        if 'image.jpg' not in image_path:
            shutil.copyfile(image_path, 'image.jpg')
        self.img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)
        #cv2.imshow('image', cv2.resize(self.img, (400, 400)))
    def mask(self):
        pass
    def show(self, label):
        img = cv2.resize(self.img, (self.img.shape[0] >> 2, self.img.shape[1] >> 2))
        label.setGeometry(0, 0, img.shape[1], img.shape[0])
        img = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        label.setPixmap(QPixmap.fromImage(img))
