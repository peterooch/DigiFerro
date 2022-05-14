from os import path

from PyQt5.QtWidgets import QDialog, QFileDialog, QCalendarWidget, QListWidget, QMessageBox
from PyQt5 import uic, QtCore
from util import resource_path
from joblib import load, dump

class LoginWindow(QDialog):
    def __init__(self, parent) -> None:
        super(LoginWindow, self).__init__(parent)
        self.parent = parent
        self.load_ui()
        self.buttonBox.button(self.buttonBox.Ok).clicked.connect(self.ok)
        self.buttonBox.button(self.buttonBox.Cancel).clicked.connect(self.cancel)

    def load_ui(self):
        uic.loadUi(resource_path('login.ui'), self)

    def open(self):
        self.show()

    def ok(self):
        msgBox: QMessageBox = QMessageBox(self)
        userName = self.Username.text()   
        passWord = self.Password.text()
        x = self.Confirm.isChecked()


    def cancel(self):
        pass
