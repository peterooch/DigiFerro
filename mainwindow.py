# This Python file uses the following encoding: utf-8
import os
import sys
import json

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import uic
from PyQt5.QtGui import QIcon

from imageproc import image
from openfile import OpenFileWindow
from history import HistoryWindow, History
from util import extract_dir, resource_path
#from graph import GraphWindow

SETTINGS_PATH = 'settings.json'

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.load_ui()
        self.openfile = OpenFileWindow(self)
        self.history = HistoryWindow(self)
        #self.graph = GraphWindow(self)
        self.img = None

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

    def set_image(self, img: image):
        self.img = img

    def show_image(self, param):
        if self.img is None:
            return
        self.img.show(self.label, param)

    def load_ui(self):
        uic.loadUi(resource_path('mainwindow.ui'), self)

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
        if self.img is None:
            return
        save_dir = self.get_setting('save_dir', '.')
        file_path, _ = QFileDialog.getSaveFileName(self, directory=f'{save_dir}/{self.img.show_mode}.png', filter='PNG Image (*.png)')

        if file_path == '':
            return
        self.set_setting('save_dir', extract_dir(file_path))

        self.img.save_image(file_path)

if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon(resource_path('icon.png')))
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
