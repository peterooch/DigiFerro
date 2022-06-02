from createAccount import users
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QDialog, QHeaderView, QAbstractItemView
from PyQt5 import uic
from util import resource_path


FIRSTNAME_COL = 0
LASTNAME_COL = 1
USERNAME_COL = 2
PASSWORD_COL = 3


class UserManagement(QDialog):
    def __init__(self, parent) -> None:
        super(UserManagement, self).__init__(parent)
        self.parent = parent
        self.load_ui()
        table: QTableWidget = self.tableWidget
        table.setRowCount(0)
        for i, user in enumerate(users):
            table.insertRow(i)
            table.setItem(i, FIRSTNAME_COL, QTableWidgetItem(str(user.firstName)))
            table.setItem(i, LASTNAME_COL, QTableWidgetItem(str(user.lastName)))
            table.setItem(i, USERNAME_COL, QTableWidgetItem(str(user.userName)))
            table.setItem(i, PASSWORD_COL, QTableWidgetItem(str(user.passWord)))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.close.clicked.connect(self.close_usermanagement)

    def load_ui(self):
        uic.loadUi(resource_path('Usermanagement.ui'), self)

    def close_usermanagement(self):
        self.hide()

