from os import path
from typing import List

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic
from util import resource_path
from joblib import load, dump
from usermanagement import add_user, User

# DigiFerro
# Programmers:
# Baruch Rutman
# Roi Amzallag

class CreateAccount(QDialog):
    def __init__(self, parent) -> None:
        super(CreateAccount, self).__init__(parent)
        self.parent = parent
        self.load_ui()
        self.buttonBox.button(self.buttonBox.Ok).clicked.connect(self.ok)
        self.buttonBox.button(self.buttonBox.Cancel).clicked.connect(self.cancel)

    def load_ui(self):
        uic.loadUi(resource_path('createaccount.ui'), self)
    
    def open(self):
        self.show()

    def ok(self):
        msgBox: QMessageBox = QMessageBox(self)
        firstname = self.firstName.text()
        lastname = self.lastName.text()
        username = self.userName.text()
        password = self.password.text()
        role = 0
        if self.performs.isChecked():
            role |= User.ROLE_PERFORM
        if self.comptroller.isChecked():
            role |= User.ROLE_COMPTROLLER
        if self.confirm.isChecked():
            role |= User.ROLE_CONFIRM
        if firstname == '' or lastname == '' or username == '' or password == '' or role == 0:
            msgBox.setText('All fields must be filled in as required')
            msgBox.exec()
        else: #User created successfully, user object must be created with all relevant variables.
            user = User(firstname, lastname, username, password, role)
            add_user(user)
            msgBox.setText('User created successfully')
            msgBox.show()
            return


    def cancel(self):
        self.hide()





