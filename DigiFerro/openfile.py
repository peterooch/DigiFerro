from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5 import uic

from imageproc import image


class OpenFileWindow(QDialog):
    def __init__(self, parent):
        super(OpenFileWindow, self).__init__(parent)
        self.parent = parent
        self.load_ui()
        self.pushButton.clicked.connect(self.browse)
        self.buttonBox.button(self.buttonBox.Ok).clicked.connect(self.ok)

    def load_ui(self):
        uic.loadUi('openfile.ui', self)

    def open(self):
        self.show()

    def browse(self):
        fileName = QFileDialog.getOpenFileName(self)
        self.lineEdit.setText(fileName[0])

    def ok(self):
        self.hide()
        image(self.lineEdit.text()).show(self.parent.label)
