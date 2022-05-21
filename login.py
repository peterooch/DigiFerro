from os import path
from xmlrpc.client import Boolean

from PyQt5.QtWidgets import QDialog, QFileDialog, QCalendarWidget, QListWidget, QMessageBox
from PyQt5 import uic, QtCore
from util import resource_path
from joblib import load, dump
from createAccount import CreateAccount, User, users

class LoginWindow(QDialog):
    def __init__(self, parent) -> None:
        super(LoginWindow, self).__init__(parent)
        self.parent = parent
        self.load_ui()
        self.buttonBox.button(self.buttonBox.Ok).clicked.connect(self.ok)
        self.buttonBox.button(self.buttonBox.Cancel).clicked.connect(self.cancel)

        #self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint)

    def load_ui(self):
        uic.loadUi(resource_path('login.ui'), self)

    def open(self):
        self.show()

    def ok(self):
        msgBox: QMessageBox = QMessageBox(self)
        userName = self.Username.text()  
        passWord = self.Password.text()
        checkUser: Boolean = False
        for user in users:
            if userName == user.userName and passWord == user.passWord:
                checkUser = True
                self.parent.current_user(userName)
        if checkUser:
            self.close()
        else:
            msgBox.setText('Invalid credentials')
            msgBox.show()
            return
        x = self.Confirm.isChecked()

    def cancel(self):
        msgBox: QMessageBox = QMessageBox(self)
        msgBox.setWindowTitle('Error')
        msgBox.setText('You must be logged in')
        msgBox.exec()
        return

    def create_new_acount(self):
        self.createaccount = CreateAccount(self)
        self.createaccount.show()
