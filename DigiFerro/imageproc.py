import cv2
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.uic.properties import QtWidgets
from matplotlib import pyplot as plt


class image():
    def __init__(self, image):
        self.Image = image
        self.image_frame = QtWidgets.QLabel()
    def mask(self):
        self.img = cv2.imread(self.Image, cv2.IMREAD_GRAYSCALE)
    def show(self, label):
        self.img = QtGui.QImage(self.img.data, self.img.shape[1], self.img.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        label.setPixmap(QPixmap.fromImage(self.img))
