from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5 import uic

from imageproc import image
from util import resource_path

class OpenFileWindow(QDialog):
    def __init__(self, parent):
        super(OpenFileWindow, self).__init__(parent)
        self.parent = parent
        self.load_ui()
        self.pushButton.clicked.connect(self.browse)
        self.buttonBox.button(self.buttonBox.Ok).clicked.connect(self.ok)
        self.buttonBox.button(self.buttonBox.Cancel).clicked.connect(self.cancel)

    def load_ui(self):
        uic.loadUi(resource_path('openfile.ui'), self)

    def open(self):
        self.show()

    def browse(self):
        fileName = QFileDialog.getOpenFileName(self)
        self.lineEdit.setText(fileName[0])

    def ok(self):
        self.hide()
        img = image(self.lineEdit.text())
        self.parent.set_image(img)
        self.parent.show_image()
    
    def cancel(self):
        self.hide()
