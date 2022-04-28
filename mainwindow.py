# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import uic

from imageproc import image
from openfile import OpenFileWindow
from history import HistoryWindow, History
from util import resource_path
#from graph import GraphWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.load_ui()
        self.openfile = OpenFileWindow(self)
        self.history = HistoryWindow(self)
        #self.graph = GraphWindow(self)
        self.img = None

        self.actionUpload_file.triggered.connect(self.openfile.open)
        self.actionShow_History.triggered.connect(self.history.open)
        self.actionUpload_file_2.triggered.connect(self.load_history)
        #self.actionShow_Graph.triggered.connect(self.graph.open)
        self.analyzeButton.clicked.connect(self.openfile.open)
        self.fragmentButton.clicked.connect(lambda *args: self.show_image('fragments'))
        self.originalButton.clicked.connect(lambda *args: self.show_image())
        self.graphButton.clicked.connect(lambda *args: self.show_image('graph'))
        self.setMinimumWidth(900)
        self.setMinimumHeight(700)

    def set_image(self, img: image):
        self.img = img

    def show_image(self, param=None):
        if self.img is None:
            return
        self.img.show(self.label, param)

    def load_ui(self):
        uic.loadUi(resource_path('mainwindow.ui'), self)

    def load_history(self):
        fileName = QFileDialog.getOpenFileName(self)
        # TODO add caching to directory
        self.history.history = History(fileName[0])
        self.history.open()

if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
