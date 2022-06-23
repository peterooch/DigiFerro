from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic, QtCore

from util import resource_path
from createAccount import CreateAccount
from usermanagement import User, users

# DigiFerro
# Programmers:
# Baruch Rutman
# Roi Amzallag

class LoginWindow(QDialog):
    def __init__(self, parent) -> None:
        super(LoginWindow, self).__init__(parent)
        self.parent = parent
        self.load_ui()
        self.buttonBox.button(self.buttonBox.Ok).clicked.connect(self.ok)
        self.buttonBox.button(self.buttonBox.Cancel).clicked.connect(self.cancel)
        self.setResult(1)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint)

    def load_ui(self):
        uic.loadUi(resource_path('login.ui'), self)

    def open(self):
        self.show()

    def ok(self):
        msgBox: QMessageBox = QMessageBox(self)
        userName = self.Username.text()  
        passWord = self.Password.text()
        selected_user = None
        for user in users:
            if userName == user.userName and passWord == user.passWord:
                selected_user = user
                break
        if selected_user is not None:
            self.parent.set_current_user(selected_user)
            self.close()
        else:
            msgBox.setWindowTitle('Error')
            msgBox.setText('Invalid credentials')
            msgBox.exec()

    def cancel(self):
        self.setResult(0)
        self.close()

    def create_new_account(self):
        self.createaccount = CreateAccount(self)
        self.createaccount.show()
