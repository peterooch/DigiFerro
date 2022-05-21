from os import path

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic
from util import resource_path
from joblib import load, dump

class CreateAccount(QDialog):
    def __init__(self, parent) -> None:
        super(CreateAccount, self).__init__(parent)
        self.parent = parent
        self.load_ui()
        self.buttonBox.button(self.buttonBox.Ok).clicked.connect(self.ok)
        self.buttonBox.button(self.buttonBox.Cancel).clicked.connect(self.cancel)

    def load_ui(self):
        uic.loadUi(resource_path('createacount.ui'), self)
    
    def open(self):
        self.show()

    def ok(self):
        msgBox: QMessageBox = QMessageBox(self)
        firstname = self.firstName.text()
        lastname = self.lastName.text()
        username = self.userName.text()
        password = self.password.text()
        if self.performs.isChecked():
            role = 'performs'
        elif self.comptroller.isChecked():
            role = 'comptroller'
        elif self.confirm.isChecked():
            role = 'confirm'
        if firstname == '' or lastname == '' or username == '' or password == '' or role == '':
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

class User:
    def __init__(self, firstName, lastName, userName, passWord, role) -> None:
        self.firstName = firstName
        self.lastName = lastName
        self.userName = userName
        self.passWord = passWord
        self.role = role

# FIXME implement somesort of encryption
USER_FILE = 'data/users.pkl'
try:
    users = load(USER_FILE)
except:
    users = [User('Dima', 'Fishman', 'Dima', '123456', 'Confirm'), 
             User('Elizabeth', 'Riska', 'Eliz', '123456', 'Opertaor'),
             User('Chen', 'chef', 'Chen', '123456', 'Comptroller')]
    dump(users, USER_FILE)

def add_user(user: User):
    users.append(user)
    dump(users, USER_FILE)
