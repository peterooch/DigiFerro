from os import path

from PyQt5.QtWidgets import QDialog, QFileDialog, QCalendarWidget, QListWidget, QMessageBox
from PyQt5 import uic, QtCore
from util import resource_path
from joblib import load, dump

class CreateAccount(QDialog):
    def __init__(self, parent) -> None:
        super(CreateAccount, self).__init__(parent)
        self.parent = parent
        self.load_ui()

    def load_ui(self):
        uic.loadUi(resource_path('createacount.ui'), self)

class User():
    def __init__(self, firstName, lastName, userName, passWord, role) -> None:
        self.firstName = firstName
        self.lastName = lastName
        self.userName = userName
        self.passWord = passWord
        self.role = role



