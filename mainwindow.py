# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

from PyQt5 import uic
from imageproc import image

from openfile import OpenFileWindow
from history import HistoryWindow, History
from graph import GraphWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.load_ui()
        self.openfile = OpenFileWindow(self)
        self.history = HistoryWindow(self)
        self.graph = GraphWindow(self)
        self.actionUpload_file.triggered.connect(self.openfile.open)
        self.actionShow_History.triggered.connect(self.history.open)
        self.actionUpload_file_2.triggered.connect(self.load_history)
        self.actionShow_Graph.triggered.connect(self.graph.open)
        self.analyzeButton.clicked.connect(self.openfile.open)
        self.fragmentButton.clicked.connect(self.show_fragments)
        self.setMinimumWidth(900)
        self.setMinimumHeight(700)

    def set_image(self, img: image):
        self.img = img

    def show_fragments(self):
        if self.img is None:
            return
        self.img.show(self.label, 'fragments')

    def show_image(self):
        self.img.show(self.label)

    def load_ui(self):
        uic.loadUi('mainwindow.ui', self)

    def load_history(self):
        fileName = QFileDialog.getOpenFileName(self)
        self.history.history = History(fileName[0])
        self.history.open()

if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
