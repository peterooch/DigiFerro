# This Python file uses the following encoding: utf-8
import os
import sys
import json
from typing import List

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QListWidget
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap, QImage
import cv2
import numpy as np

from imageproc import image
from openfile import OpenFileWindow
from history import HistoryWindow, History
from util import extract_dir, gen_graph, get_distribution, resource_path
#from graph import GraphWindow

SETTINGS_PATH = 'settings.json'

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.load_ui()
        self.openfile = OpenFileWindow(self)
        self.history = HistoryWindow(self)
        #self.graph = GraphWindow(self)
        self.images: List[image] = []
        self.image_id = -1
        self.totals_on = False
        self.graph_img = None

        try:
            with open(SETTINGS_PATH, 'r') as settings:
                self.settings = json.load(settings)
        except:
            self.settings = dict()
            with open(SETTINGS_PATH, 'w') as settings:
                json.dump(self.settings, settings)

        # Menu Items
        self.actionUpload_file.triggered.connect(self.openfile.open)
        self.actionShow_History.triggered.connect(self.history.open)
        self.actionUpload_file_2.triggered.connect(self.load_history)
        #self.actionShow_Graph.triggered.connect(self.graph.open)
        if sys.platform == "win32":
            self.actionHelp.triggered.connect(lambda *args: os.startfile(resource_path('DigiFerro_Guide.pdf')))

        # Window Buttons
        self.analyzeButton.clicked.connect(self.openfile.open)
        self.fragmentButton.clicked.connect(lambda *args: self.show_image('fragments'))
        self.originalButton.clicked.connect(lambda *args: self.show_image('original'))
        self.graphButton.clicked.connect(lambda *args: self.show_image('graph'))
        self.saveButton.clicked.connect(lambda *args: self.save_image())
        self.overallGraphButton.clicked.connect(lambda *args: self.show_totals())

        self.imageList.selectionChanged = self.list_selection

    def load_ui(self):
        uic.loadUi(resource_path('mainwindow.ui'), self)

    def list_selection(self, selected: QtCore.QItemSelection, deselected):
        self.image_id = selected.indexes()[0].row()
        self.show_image('refresh')

    def add_images(self, images: List[image]):
        self.images = images

        for image in images:
            item = QListWidgetItem(str(image))
            item.attached_image = image
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)
            self.imageList.addItem(item)

    def show_image(self, param, image_id=-1):
        if param == 'refresh' and self.totals_on:
            return
        if param == 'refresh':
            param = self.prev_param
        else:
            self.prev_param = param
        self.totals_on = False
        if image_id == -1:
            image_id = self.image_id
        else:
            self.image_id = image_id
        if image_id == -1 or len(self.images) <= image_id:
            return
        self.images[image_id].show(self.label, param)

    def show_totals(self):
        self.totals_on = True
        lw: QListWidget = self.imageList
        items = [lw.item(i) for i in range(lw.count())]
        dims = []
        for item in items:
            if item.checkState() == QtCore.Qt.Unchecked:
                continue
            dims.append(item.attached_image.get_dims())
        if len(dims) == 0:
            return
        dims = np.concatenate(dims)
        dist, bins = get_distribution(dims)
        img = gen_graph(dist, bins)
        self.graph_img = img
        self.label.resize(img.shape[1], img.shape[0])
        img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888).rgbSwapped()
        self.label.setPixmap(QPixmap.fromImage(img))

    def get_setting(self, key, default):
        try:
            return self.settings[key]
        except:
            return default

    def set_setting(self, key, value):
        self.settings[key] = value
        with open(SETTINGS_PATH, 'w') as settings:
            json.dump(self.settings, settings)

    def load_history(self):
        history_dir = self.get_setting('history_file_dir', '')
        fileName, _ = QFileDialog.getOpenFileName(self, directory=history_dir)
        
        if fileName == '':
            return

        self.set_setting('history_file_dir', extract_dir(fileName))
        self.history.set_history(History(fileName))
        self.history.open()

    def save_image(self):
        if self.image_id == -1:
            return
        save_dir = self.get_setting('save_dir', '.')

        if self.totals_on:
            filename = "totals"
        else:
            self.images[self.image_id].show_mode

        file_path, _ = QFileDialog.getSaveFileName(self,
             directory=f'{save_dir}/{filename}.png',
             filter='PNG Image (*.png)')

        if file_path == '':
            return

        self.set_setting('save_dir', extract_dir(file_path))

        if self.totals_on is False:
            self.images[self.image_id].save_image(file_path)
        else:
            cv2.imwrite(file_path, self.graph_img)

if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon(resource_path('icon.png')))
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
