# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

from openfile import OpenFileWindow
from history import HistoryWindow
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
        self.actionUpload_file_2.triggered.connect(self.openfile.open)
        self.actionShow_Graph.triggered.connect(self.graph.open)
        self.analyzeButton.clicked.connect(self.openfile.open)
        self.setMinimumWidth(900)
        self.setMinimumHeight(700)

    def load_ui(self):
        uic.loadUi('mainwindow.ui', self)

if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
