
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

class HistoryWindow(QDialog):
    def __init__(self, parent):
        super(HistoryWindow, self).__init__(parent)
        self.load_ui()

    def load_ui(self):
        uic.loadUi('history.ui', self)

    def open(self):
        self.show()