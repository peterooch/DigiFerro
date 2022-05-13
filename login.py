from os import path

from PyQt5.QtWidgets import QDialog, QFileDialog, QCalendarWidget, QListWidget, QMessageBox
from PyQt5 import uic, QtCore
from util import resource_path

class LoginWindow(QDialog):
    def __init__(self, parent) -> None:
        super(LoginWindow, self).__init__(parent)
        self.parent = parent
        self.load_ui()

    def load_ui(self):
        uic.loadUi(resource_path('Login.ui'), self)

    def open(self):
        self.show()