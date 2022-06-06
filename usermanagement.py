import os
from typing import List

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QDialog, QHeaderView, QAbstractItemView, QMessageBox
from PyQt5 import uic
from util import resource_path
from joblib import load, dump

class User:
    # user flags
    ROLE_PERFORM     = (1 << 0)
    ROLE_COMPTROLLER = (1 << 1)
    ROLE_CONFIRM     = (1 << 2)
    def __init__(self, firstName, lastName, userName, passWord, role) -> None:
        self.firstName = firstName
        self.lastName = lastName
        self.userName = userName
        self.passWord = passWord
        self.role = role
        
USER_FILE = 'data/users.pkl'
try:
    users: List[User] = load(USER_FILE)
except:
    users = [User('Dima', 'Fishman', 'Dima', '123456', User.ROLE_CONFIRM), 
             User('Elizabeth', 'Riska', 'Eliz', '123456', User.ROLE_PERFORM),
             User('Chen', 'chef', 'Chen', '123456', User.ROLE_COMPTROLLER)]
    os.makedirs('data', exist_ok=True)
    dump(users, USER_FILE)

def add_user(user: User):
    users.append(user)
    dump(users, USER_FILE)


FIRSTNAME_COL = 0
LASTNAME_COL = 1
USERNAME_COL = 2
PASSWORD_COL = 3

class UserManagement(QDialog):
    def __init__(self, parent) -> None:
        super(UserManagement, self).__init__(parent)
        self.parent = parent
        self.load_ui()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.set_table()
        self.closeButton.clicked.connect(self.close_usermanagement)
        self.removeButton.clicked.connect(self.remove)

    def load_ui(self):
        uic.loadUi(resource_path('Usermanagement.ui'), self)

    def close_usermanagement(self):
        self.hide()

    def _get_selection(self):
        table: QTableWidget = self.tableWidget

        items = table.selectedIndexes()
        if len(items) < 1:
            return
        item = items[0]
        return item.row()

    def set_table(self):
        table: QTableWidget = self.tableWidget
        table.setRowCount(0)
        for i, user in enumerate(users):
            table.insertRow(i)
            table.setItem(i, FIRSTNAME_COL, QTableWidgetItem(str(user.firstName)))
            table.setItem(i, LASTNAME_COL, QTableWidgetItem(str(user.lastName)))
            table.setItem(i, USERNAME_COL, QTableWidgetItem(str(user.userName)))
            table.setItem(i, PASSWORD_COL, QTableWidgetItem(str(user.passWord)))

    def remove(self):
        curr_line = self._get_selection()
        users.pop(curr_line)
        self.set_table()
        dump(users, USER_FILE)

    def show(self):
        self.set_table()        
        super().show()


class ChangePassword(QDialog):
    def __init__(self, parent, user) -> None:
        super().__init__(parent)
        uic.loadUi(resource_path('changepassword.ui'), self)
        self.user = user
        self.ok_Button.clicked.connect(self.ok)

    def ok(self):
        msgBox: QMessageBox = QMessageBox(self)
        oldPassword = self.old_Password.text()
        newPassword = self.new_Password.text()
        if oldPassword != self.user.passWord:
            msgBox.setWindowTitle('Error')
            msgBox.setText('old password doesn\'t match current password')
            msgBox.exec()
        elif newPassword == '':
            msgBox.setWindowTitle('Error')
            msgBox.setText('New password can\'t be Empty')
            msgBox.exec()
        else:
            self.user.passWord = newPassword
            dump(users, USER_FILE)  
