import cv2
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import shutil

class image():
    def __init__(self, image_path):
        try:
            shutil.copyfile(image_path, 'image.jpg')
        except shutil.SameFileError:
            pass

        self.img = cv2.imread('image.jpg', cv2.IMREAD_COLOR)
    def show(self, label):
        self.img = cv2.resize(self.img, (800, 600))
        label.setGeometry(20, 20, self.img.shape[1], self.img.shape[0])
        img = QtGui.QImage(self.img.data, self.img.shape[1], self.img.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        label.setPixmap(QPixmap.fromImage(img))
